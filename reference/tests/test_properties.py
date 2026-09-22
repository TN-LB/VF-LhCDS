"""Reference-only metamorphic and higher-h cases (no M2/M3 gate claims)."""

from fractions import Fraction
from itertools import combinations

import pytest

from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.graph import Graph, normalize_graph
from vflhcds_reference.generators import all_labelled_graphs, seeded_cases


@pytest.mark.parametrize("h", [4, 5])
def test_higher_h_complete_graph_and_overlapping_cliques(h):
    ref = Reference(Graph(tuple(range(h)), tuple(combinations(range(h), 2))), h)
    assert direct_lhcds(ref) == (ref.graph.full_mask,)
    assert ref.density(ref.graph.full_mask) == Fraction(1, h)
    # Two K_h sharing h-1 vertices, with no edge between the two outer vertices.
    n = h + 1
    graph = Graph(tuple(range(n)), tuple(e for e in combinations(range(n), 2) if e != (h - 1, h)))
    ref = Reference(graph, h)
    assert len(ref.cliques) == 2
    assert direct_lhcds(ref) == (graph.full_mask,)
    assert ref.density(graph.full_mask) == Fraction(2, n)


def test_relabel_complete_truth_then_resort_before_fixed_k():
    graph = Graph((0, 1, 2, 3), ((0, 1), (2, 3)))
    ref = Reference(graph, 2)
    original = direct_lhcds(ref)
    mapping = {0: 20, 1: 30, 2: -5, 3: -4}
    renamed = normalize_graph(mapping.values(), ((mapping[u], mapping[v]) for u, v in graph.edges)).graph
    transformed = sorted(tuple(sorted(mapping[v] for v in graph.ids(s))) for s in original)
    new_ref = Reference(renamed, 2)
    assert tuple(renamed.ids(s) for s in direct_lhcds(new_ref)) == tuple(transformed)
    assert tuple(sorted(mapping[v] for v in graph.ids(original[0]))) != transformed[0]
    for k in range(1, len(original) + 3):
        assert tuple(renamed.ids(s) for s in direct_lhcds(new_ref, k=k)) == tuple(transformed[:k])


def test_disjoint_union_and_added_isolates_keep_exact_family():
    edges = tuple([*combinations(range(4), 2), (10, 11)])
    graph = Graph(tuple([*range(4), 10, 11, 100]), edges)
    ref = Reference(graph, 2)
    assert tuple(graph.ids(s) for s in direct_lhcds(ref)) == ((0, 1, 2, 3), (10, 11), (100,))
    assert tuple(ref.density(s) for s in direct_lhcds(ref)) == (Fraction(3, 2), Fraction(1, 2), Fraction(0))


def test_generators_are_deterministic_unique_and_preserve_declared_n():
    assert sum(1 for n in range(1, 6) for _ in all_labelled_graphs(n)) == 1099
    first = list(seeded_cases(20260917))
    assert first == list(seeded_cases(20260917))
    assert len({(graph, h) for graph, h, _ in first}) == 100
    assert all(6 <= graph.n <= 8 and h >= 2 for graph, h, _ in first)
    for family in ["random", "planted", "bridge", "tied", "disconnected"]:
        assert sum(metadata["family"] == family for _, _, metadata in first) == 20
