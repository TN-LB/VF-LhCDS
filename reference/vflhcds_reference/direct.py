"""P01.1/P01.2: direct Definitions 1.1-1.3, independent of parametric oracles."""

from fractions import Fraction
from itertools import combinations

from .graph import Graph, require_integer


DEFAULT_MAX_VERTICES = 12


class SizeLimitError(RuntimeError):
    """Exponential reference work exceeds the explicit local size guard."""


def check_size(graph: Graph, max_vertices: int = DEFAULT_MAX_VERTICES) -> None:
    require_integer(max_vertices, "max_vertices", 1)
    if graph.n > max_vertices:
        raise SizeLimitError(f"reference has {graph.n} vertices; limit is {max_vertices}")


def exact_threshold(value: int | Fraction) -> Fraction:
    if type(value) not in (int, Fraction) or value < 0:
        raise ValueError("threshold must be a nonnegative exact integer or Fraction")
    return Fraction(value)


def submasks(mask: int):
    """All subsets, including empty; callers validate against their universe."""
    require_integer(mask, "mask", 0)
    subset = mask
    while True:
        yield subset
        if subset == 0:
            break
        subset = (subset - 1) & mask


def combination_cliques(graph: Graph, h: int, *, max_vertices: int = DEFAULT_MAX_VERTICES) -> tuple[int, ...]:
    require_integer(h, "h", 2)
    check_size(graph, max_vertices)
    # Avoid passing an arbitrarily large valid h through a machine-sized C API.
    if h > graph.n:
        return ()
    result = []
    for vertices in combinations(range(graph.n), h):
        if all(graph.adjacency[u] & (1 << v) for u, v in combinations(vertices, 2)):
            result.append(sum(1 << v for v in vertices))
    return tuple(result)


class Reference:
    """Reusable counts for one graph/h; no production or parametric dependency.

    The guard runs before clique enumeration or allocating the 2**n count table.
    Counts are cached as specified by the correctness plan; no compactness,
    maximality or oracle condition is replaced with a production shortcut.
    """

    def __init__(self, graph: Graph, h: int, *, max_vertices: int = DEFAULT_MAX_VERTICES):
        require_integer(h, "h", 2)
        check_size(graph, max_vertices)
        self.graph, self.h, self.max_vertices = graph, h, max_vertices
        self.cliques = combination_cliques(graph, h, max_vertices=max_vertices)
        self.counts = tuple(sum(clique & mask == clique for clique in self.cliques)
                            for mask in range(graph.full_mask + 1))

    def mu_h(self, mask: int) -> int:
        return self.counts[self.graph.check_mask(mask)]

    def density(self, mask: int) -> Fraction:
        count = self.mu_h(mask)
        if mask == 0:
            raise ValueError("density is undefined for the empty set")
        return Fraction(count, mask.bit_count())

    def deletion_loss(self, mask: int, deleted: int) -> int:
        self.graph.check_mask(mask)
        self.graph.check_mask(deleted)
        if deleted & mask != deleted:
            raise ValueError("deleted vertices must be a subset of the induced set")
        return self.counts[mask] - self.counts[mask & ~deleted]


def direct_compact(ref: Reference, mask: int, threshold: int | Fraction) -> bool:
    threshold = exact_threshold(threshold)
    ref.graph.check_mask(mask)
    if not ref.graph.connected(mask):
        return False
    a, b = threshold.numerator, threshold.denominator
    for deleted in submasks(mask):
        if b * (ref.counts[mask] - ref.counts[mask & ~deleted]) < a * deleted.bit_count():
            return False
    return True


def compactness(ref: Reference, mask: int) -> Fraction:
    ref.graph.check_mask(mask)
    if mask == 0:
        raise ValueError("compactness is undefined for the empty set")
    if not ref.graph.connected(mask):
        return Fraction(0)
    return min(Fraction(ref.counts[mask] - ref.counts[mask & ~deleted], deleted.bit_count())
               for deleted in submasks(mask) if deleted)


def direct_maximal_compact(ref: Reference, mask: int, threshold: int | Fraction) -> bool:
    threshold = exact_threshold(threshold)
    if not direct_compact(ref, mask, threshold):
        return False
    complement = ref.graph.full_mask ^ mask
    # Enumerate EVERY possible extension, not only one-vertex additions.
    for extra in submasks(complement):
        if extra and direct_compact(ref, mask | extra, threshold):
            return False
    return True


def maximal_compact_sets(ref: Reference, threshold: int | Fraction) -> tuple[int, ...]:
    threshold = exact_threshold(threshold)
    return tuple(mask for mask in range(1, ref.graph.full_mask + 1)
                 if direct_maximal_compact(ref, mask, threshold))


def rank_sets(ref: Reference, masks) -> tuple[int, ...]:
    return tuple(sorted(masks, key=lambda mask: (-ref.density(mask), ref.graph.ids(mask))))


def direct_lhcds(ref: Reference, *, k: int | None = None) -> tuple[int, ...]:
    """All direct truth, sorted by exact density/original IDs, then optional prefix."""
    if k is not None:
        require_integer(k, "k", 1)
    ranked = rank_sets(ref, (mask for mask in range(1, ref.graph.full_mask + 1)
                            if direct_maximal_compact(ref, mask, ref.density(mask))))
    return ranked if k is None else ranked[:k]
