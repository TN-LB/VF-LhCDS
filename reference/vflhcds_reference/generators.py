"""Deterministic tiny fixtures; seeds select test graphs, not solver behavior."""

from itertools import combinations
import random

from .graph import Graph, require_integer


def all_labelled_graphs(n: int):
    require_integer(n, "n", 1)
    # This generator is more expensive than subset truth; explicit small domain.
    if n > 5:
        raise ValueError("all-labelled generator is restricted to n<=5")
    edges = tuple(combinations(range(n), 2))
    for bits in range(1 << len(edges)):
        yield Graph(tuple(range(n)), tuple(edge for i, edge in enumerate(edges) if bits & (1 << i)))


def seeded_cases(seed: int, count: int = 100):
    """Unique (labelled graph,h) cases, five families, n=6..8; integer-only RNG.

    The seed, accepted case index and sampling attempt are retained in metadata.
    Family cycling applies to accepted cases, so count=100 yields 20 of each.
    """
    require_integer(seed, "seed", 0)
    require_integer(count, "count", 1)
    rng, seen = random.Random(seed), set()
    families = ("random", "planted", "bridge", "tied", "disconnected")
    attempt = 0
    while len(seen) < count:
        index = len(seen)
        family = families[index % len(families)]
        attempt += 1
        # Explicit finite generator safeguard, unrelated to benchmark timeouts.
        if attempt > count * 1000:
            raise RuntimeError("unique fixture generation exhausted its attempt guard")
        n = rng.randrange(6, 9)
        vertices = list(range(n))
        rng.shuffle(vertices)
        left, right = vertices[:n // 2], vertices[n // 2:]
        pairs = tuple(combinations(range(n), 2))
        if family == "random":
            edges = {pair for pair in pairs if rng.randrange(2)}
        elif family == "planted":
            edges = {pair for pair in pairs if rng.randrange(4) == 0}
            edges.update(tuple(sorted(pair)) for pair in combinations(left, 2))
        elif family in ("bridge", "tied"):
            if family == "tied":
                right = right[:len(left)]
            edges = {tuple(sorted(pair)) for block in [left, right] for pair in combinations(block, 2)}
            if family == "bridge":
                edges.add(tuple(sorted((left[0], right[0]))))
        else:
            edges = {tuple(sorted(pair)) for block in [left, right]
                     for pair in combinations(block, 2) if rng.randrange(2)}
        h = rng.choice([2, 3, 4, 5, n + 1])
        graph = Graph(tuple(range(n)), tuple(sorted(edges)))
        key = (graph, h)
        if key in seen:
            continue
        seen.add(key)
        yield graph, h, {"seed": seed, "case_index": index, "sampling_attempt": attempt, "family": family}
