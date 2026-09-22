"""T03 plus reference-only oracle boundary/tie checks."""

from fractions import Fraction
import json
from pathlib import Path

import pytest

from vflhcds_reference.graph import Graph
from vflhcds_reference.direct import Reference
from vflhcds_reference.parametric import exhaustive_F, exhaustive_restricted, cardinality_line_chain


def test_largest_union_of_incomparable_ties_and_empty_tie():
    ref = Reference(Graph((0, 1, 2, 3), ((0, 1), (2, 3))), 2)
    result = exhaustive_F(ref, Fraction(1, 2))
    assert set(result.maximizers) == {0, 3, 12, 15}
    assert result.largest == 15 and result.objective_scaled == 0
    assert result.scope == "global"
    assert exhaustive_F(ref, Fraction(0)).largest == 15
    assert exhaustive_F(ref, Fraction(2)).largest == 0


def test_restricted_results_do_not_claim_global_and_allow_equal_bounds():
    ref = Reference(Graph((0, 1, 2), ((0, 1),)), 2)
    result = exhaustive_restricted(ref, Fraction(0), 0, 3)
    assert result.largest == 3 and result.scope == "restricted"
    assert exhaustive_F(ref, Fraction(0)).largest == 7
    forced = exhaustive_restricted(ref, Fraction(2**200, 3), 1, 1)
    assert forced.largest == 1 and forced.objective_scaled == -(2**200)
    assert exhaustive_restricted(ref, Fraction(1), 3, 7).largest == 3
    for x, y in [(1, 2), (0, 8), (-1, 7), (True, 7)]:
        with pytest.raises(ValueError):
            exhaustive_restricted(ref, Fraction(1), x, y)
    for value in [Fraction(-1), 0.1, True]:
        with pytest.raises(ValueError):
            exhaustive_F(ref, value)


def test_t03_envelope_has_exact_intersections_midpoints_zero_and_sentinel():
    ref = Reference(Graph((0, 1, 2), ((0, 1),)), 2)
    chain = cardinality_line_chain(ref)
    assert chain.sets == (0, 3, 7)
    assert chain.breakpoints == (Fraction(1, 2), Fraction(0))
    assert chain.cardinality_maxima == (0, 0, 1, 1)
    assert chain.sentinel == 2
    params = {s.parameter for s in chain.samples}
    assert {Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(1), Fraction(2)} <= params
    points = sorted({*chain.intersections, Fraction(0), chain.sentinel})
    assert {(a + b) / 2 for a, b in zip(points, points[1:])} <= params
    assert all(isinstance(s.parameter, Fraction) for s in chain.samples)


def test_t03_zero_chain_keeps_all_isolates_at_zero():
    ref = Reference(Graph((-2, 10), ()), 5)
    chain = cardinality_line_chain(ref)
    assert chain.sets == (0, 3)
    assert chain.breakpoints == (0,)
    assert exhaustive_F(ref, Fraction(0)).largest == 3
    assert exhaustive_F(ref, Fraction(1, 10**100)).largest == 0


def test_t03_outer_breakpoint_is_not_any_induced_subgraph_density():
    fixture = json.loads((Path(__file__).resolve().parents[1] / "fixtures/outer_breakpoint.json").read_text())
    graph = Graph(tuple(fixture["vertices"]), tuple(tuple(e) for e in fixture["edges"]))
    ref = Reference(graph, fixture["h"])
    chain = cardinality_line_chain(ref)
    assert tuple(graph.ids(s) for s in chain.sets) == ((), (0, 1, 2, 3, 5, 6), tuple(range(7)))
    assert chain.breakpoints == (Fraction(13, 6), Fraction(2))
    assert Fraction(2) not in {ref.density(s) for s in range(1, 1 << 7)}
    assert exhaustive_F(ref, Fraction(2)).largest == graph.full_mask
    assert exhaustive_F(ref, Fraction(25, 12)).largest == graph.mask([0, 1, 2, 3, 5, 6])
    assert [list(graph.ids(s)) for s in chain.sets] == fixture["expected_chain"]
