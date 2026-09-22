"""T01/T02: independent definition-level behavior, not production validation."""

from fractions import Fraction
from itertools import combinations

import pytest

from vflhcds_reference.graph import Graph, normalize_graph
from vflhcds_reference.direct import (
    Reference, SizeLimitError, compactness, direct_compact, direct_lhcds,
    direct_maximal_compact,
)


def test_t01_normalization_preserves_declared_vertices():
    normalized = normalize_graph([9, -10, 100, 2], [(9, 2), (2, 9), (9, 2), (-10, -10)])
    assert normalized.graph.vertices == (-10, 2, 9, 100)
    assert normalized.graph.edges == ((2, 9),)
    assert (normalized.removed_self_loops, normalized.removed_duplicate_edges) == (1, 2)
    graph = normalized.graph
    assert graph.ids(graph.mask([100, -10])) == (-10, 100)
    assert graph.components(graph.full_mask) == (1, 6, 8)
    assert not graph.connected(0)
    assert graph.connected(graph.mask([-10]))


@pytest.mark.parametrize("vertices,edges", [([], []), ([1, 1], []), ([1], [(1, 2)]),
                                         ([1], [(2, 2)]), ([True], []), ([1], [(1.0, 1)])])
def test_t01_reject_invalid_declared_graph(vertices, edges):
    with pytest.raises(ValueError):
        normalize_graph(vertices, edges)


@pytest.mark.parametrize("h", [2, 3, 5])
def test_t01_singleton(h):
    ref = Reference(Graph((42,), ()), h)
    assert ref.cliques == ()
    assert ref.mu_h(0) == 0
    assert ref.density(1) == 0
    assert compactness(ref, 1) == 0
    assert direct_lhcds(ref) == (1,)
    assert direct_lhcds(ref, k=5) == (1,)


@pytest.mark.parametrize("h", [3, 6, 10**100])
def test_t01_no_cliques_returns_ordinary_components(h):
    graph = Graph((-20, 1, 2, 3, 10**100), ((1, 2), (2, 3)))
    ref = Reference(graph, h)
    assert tuple(graph.ids(s) for s in direct_lhcds(ref)) == ((-20,), (1, 2, 3), (10**100,))
    assert compactness(ref, graph.full_mask) == 0  # disconnected convention
    assert not direct_compact(ref, graph.full_mask, Fraction(0))


def test_t02_multi_vertex_extension_cannot_be_replaced_by_single_addition():
    edges = tuple(sorted([*combinations(range(3), 2), *combinations(range(3, 6), 2), (2, 3)]))
    ref = Reference(Graph(tuple(range(6)), edges), 3)
    first = ref.graph.mask([0, 1, 2])
    assert direct_compact(ref, first, Fraction(1, 3))
    assert all(not direct_compact(ref, first | (1 << v), Fraction(1, 3)) for v in range(3, 6))
    assert direct_compact(ref, ref.graph.full_mask, Fraction(1, 3))
    assert not direct_maximal_compact(ref, first, Fraction(1, 3))
    assert direct_lhcds(ref) == (ref.graph.full_mask,)


def test_deletion_loss_counts_a_clique_once_even_if_multiple_vertices_deleted():
    ref = Reference(Graph(tuple(range(4)), tuple(combinations(range(4), 2))), 3)
    assert ref.cliques == (7, 11, 13, 14)
    assert ref.deletion_loss(15, 3) == 4
    assert ref.deletion_loss(15, 1) == 3
    assert ref.deletion_loss(15, 0) == 0
    assert compactness(ref, 15) == 1
    assert direct_compact(ref, 15, Fraction(1))
    assert not direct_compact(ref, 15, Fraction(1001, 1000))


def test_compactness_checks_multi_vertex_deletions():
    # In K3, single deletions have loss/size=2, but deleting all has ratio=1.
    ref = Reference(Graph((0, 1, 2), ((0, 1), (0, 2), (1, 2))), 2)
    assert all(ref.deletion_loss(7, 1 << v) == 2 for v in range(3))
    assert not direct_compact(ref, 7, Fraction(3, 2))
    assert compactness(ref, 7) == 1


def test_exact_domains_and_default_exponential_guard():
    graph = Graph(tuple(range(13)), ())
    with pytest.raises(SizeLimitError, match="12"):
        Reference(graph, 2)
    # Explicit override on a tiny input tests configuration without costly work.
    assert Reference(Graph((0,), ()), 2, max_vertices=13).max_vertices == 13
    ref = Reference(Graph((0, 1), ((0, 1),)), 2)
    for h in [0, 1, True, 2.0]:
        with pytest.raises(ValueError):
            Reference(ref.graph, h)
    for mask in [-1, 4, True, 1.0]:
        with pytest.raises(ValueError):
            ref.mu_h(mask)
    for threshold in [-1, Fraction(-1, 2), 0.5, True]:
        with pytest.raises(ValueError):
            direct_compact(ref, 3, threshold)
    for k in [0, -1, True, 1.0]:
        with pytest.raises(ValueError):
            direct_lhcds(ref, k=k)
    with pytest.raises(ValueError):
        ref.density(0)
    with pytest.raises(ValueError):
        compactness(ref, 0)
    with pytest.raises(ValueError):
        ref.deletion_loss(1, 2)
    assert not direct_compact(ref, 0, Fraction(0))
