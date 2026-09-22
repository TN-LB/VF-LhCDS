"""T01 wire-level preservation and exact reference serialization."""

from fractions import Fraction
import sys

import pytest

from vflhcds_reference.direct import Reference, SizeLimitError, direct_lhcds
from vflhcds_reference.graph import Graph
from vflhcds_reference.io import (GraphFormatError, canonical_graph, decimal_integer, decimal_text, graph_sha256, json_line,
                                parse_graph, parse_set, solution_records)


def test_canonical_roundtrip_input_order_and_big_original_ids():
    huge = 10**100
    graph = Graph((-7, 2, huge), ((-7, huge),))
    alternate = f"vflhcds-graph 1\r\nn 3 v {huge} v -7 v 2 m 1 e {huge} -7\t\n"
    parsed = parse_graph(alternate)
    assert parsed == graph
    assert parse_graph(canonical_graph(graph)) == graph
    assert graph_sha256(graph) == graph_sha256(parsed)
    assert graph_sha256(graph) != graph_sha256(Graph((-7, huge), ((-7, huge),)))


@pytest.mark.parametrize("text", [
    "", "vflhcds-graph 2 n 1 v 0 m 0", "vflhcds-graph 1 n 0 m 0",
    "vflhcds-graph 1 n 1 v -0 m 0", "vflhcds-graph 1 n 1 v 01 m 0",
    "vflhcds-graph 1 n 1 v +1 m 0", "vflhcds-graph 1 n 1 v 1.0 m 0",
    "vflhcds-graph 1 n 1 v 0 m 1 e 0 0", "vflhcds-graph 1 n 1 v 0 m 1 e 0 1",
    "vflhcds-graph 1 n 2 v 0 v 0 m 0", "vflhcds-graph 1 n 2 v 0 v 1 m 2 e 0 1 e 1 0",
    "vflhcds-graph 1 n 2 v 0 m 0", "vflhcds-graph 1 n 1 v 0 m 1",
    "vflhcds-graph 1 n 1 v 0 m 0 extra", "vflhcds-graph 1 n 1 v ０ m 0",
])
def test_t01_canonical_reader_rejects_malformed_graphs(text):
    with pytest.raises(GraphFormatError):
        parse_graph(text)


def test_set_files_distinguish_empty_and_undeclared_vertices():
    graph = Graph((-7, 2, 100), ())
    assert parse_set("vflhcds-set 1 n 0", graph) == 0
    assert parse_set("vflhcds-set 1 n 2 v 100 v -7", graph) == 5
    for text in ["vflhcds-set 1 n 1 v 3", "vflhcds-set 1 n 2 v 2 v 2", "vflhcds-set 1 n 0 x"]:
        with pytest.raises(ValueError):
            parse_set(text, graph)


def test_exact_ranked_records_match_frozen_fields_and_zero_density():
    graph = Graph((-2, 1, 4, 9), ((1, 4), (1, 9), (4, 9)))
    ref = Reference(graph, 3)
    records = solution_records(ref, direct_lhcds(ref))
    assert records == [
        {"rank": 1, "h": 3, "vertex_count": 3, "clique_count": "1", "density_num": "1", "density_den": "3", "vertices": [1, 4, 9]},
        {"rank": 2, "h": 3, "vertex_count": 1, "clique_count": "0", "density_num": "0", "density_den": "1", "vertices": [-2]},
    ]
    assert json_line(records).endswith("\n")
    assert all(Fraction(r["density_num"] + "/" + r["density_den"]) == Fraction(int(r["clique_count"]), r["vertex_count"]) for r in records)


def test_interpreter_decimal_resource_limit_never_becomes_truncation():
    if not hasattr(sys, "set_int_max_str_digits"):
        return  # Python 3.10 has no such interpreter resource limit.
    previous = sys.get_int_max_str_digits()
    try:
        sys.set_int_max_str_digits(640)
        with pytest.raises(SizeLimitError):
            decimal_integer("1" + "0" * 650)
        with pytest.raises(SizeLimitError):
            decimal_text(10**650)
        with pytest.raises(SizeLimitError):
            json_line({"vertices": [10**650]})
    finally:
        sys.set_int_max_str_digits(previous)
