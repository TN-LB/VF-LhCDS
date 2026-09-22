"""P01.3/P01.4: exhaustive subset maximization and independent line envelope.

No recursive separator, closure network, direct LhCDS selection or flow is used.
"""

from dataclasses import dataclass
from fractions import Fraction

from .direct import Reference, exact_threshold, submasks


@dataclass(frozen=True)
class OracleResult:
    scope: str
    parameter: Fraction
    x: int
    y: int
    largest: int
    objective_scaled: int
    maximizers: tuple[int, ...]


def _maximize(ref: Reference, parameter: int | Fraction, x: int, y: int, scope: str) -> OracleResult:
    parameter = exact_threshold(parameter)
    ref.graph.check_mask(x)
    ref.graph.check_mask(y)
    if x & y != x:
        raise ValueError("restricted bounds require X subseteq Y")
    a, b = parameter.numerator, parameter.denominator
    best = None
    maximizers = []
    for extra in submasks(y ^ x):
        mask = x | extra
        value = b * ref.counts[mask] - a * mask.bit_count()
        if best is None or value > best:
            best, maximizers = value, [mask]
        elif value == best:
            maximizers.append(mask)
    union = 0
    for mask in maximizers:
        union |= mask
    if b * ref.counts[union] - a * union.bit_count() != best:
        raise AssertionError("union of exhaustive maximizers is not optimal")
    return OracleResult(scope, parameter, x, y, union, best, tuple(sorted(maximizers)))


def exhaustive_F(ref: Reference, parameter: int | Fraction) -> OracleResult:
    """Full-graph global F, including empty maximizers; no strict progress promise."""
    return _maximize(ref, parameter, 0, ref.graph.full_mask, "global")


def exhaustive_restricted(ref: Reference, parameter: int | Fraction, x: int, y: int) -> OracleResult:
    """Largest restricted optimum. Even full bounds retain the restricted label."""
    return _maximize(ref, parameter, x, y, "restricted")


@dataclass(frozen=True)
class Chain:
    sets: tuple[int, ...]
    breakpoints: tuple[Fraction, ...]
    cardinality_maxima: tuple[int, ...]
    intersections: tuple[Fraction, ...]
    sentinel: Fraction
    samples: tuple[OracleResult, ...]


def cardinality_line_chain(ref: Reference) -> Chain:
    maxima = [0] * (ref.graph.n + 1)
    for mask, count in enumerate(ref.counts):
        cardinality = mask.bit_count()
        maxima[cardinality] = max(maxima[cardinality], count)
    intersections = {Fraction(maxima[j] - maxima[i], j - i)
                     for i in range(ref.graph.n + 1) for j in range(i + 1, ref.graph.n + 1)
                     if maxima[j] >= maxima[i]}
    sentinel = Fraction(ref.counts[ref.graph.full_mask] + 1)
    points = sorted(intersections | {Fraction(0), sentinel})
    parameters = set(points) | {(a + b) / 2 for a, b in zip(points, points[1:])}
    samples = tuple(exhaustive_F(ref, value) for value in sorted(parameters))
    sets = tuple(sorted({sample.largest for sample in samples}, key=int.bit_count))
    if sets[0] != 0 or sets[-1] != ref.graph.full_mask:
        raise AssertionError("line envelope does not span empty through V")
    if any(x == y or x & y != x for x, y in zip(sets, sets[1:])):
        raise AssertionError("line-envelope results are not a strict nested chain")
    # Only AFTER constructing the sets independently, report their outer densities.
    breakpoints = tuple(Fraction(ref.counts[y] - ref.counts[x], y.bit_count() - x.bit_count())
                        for x, y in zip(sets, sets[1:]))
    if any(a <= b for a, b in zip(breakpoints, breakpoints[1:])):
        raise AssertionError("principal breakpoints are not strictly decreasing")
    return Chain(sets, breakpoints, tuple(maxima), tuple(sorted(intersections)), sentinel, samples)
