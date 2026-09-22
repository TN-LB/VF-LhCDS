"""Persistent canonical hand expectations reused by later production comparisons."""

import json
from pathlib import Path

import pytest

from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.graph import Graph
from vflhcds_reference.io import solution_records


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
CASES = json.loads((FIXTURES / "named_truth.json").read_text())["cases"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["name"])
def test_hand_specified_canonical_truth(case):
    graph = Graph(tuple(case["vertices"]), tuple(tuple(edge) for edge in case["edges"]))
    ref = Reference(graph, case["h"])
    assert solution_records(ref, direct_lhcds(ref)) == case["expected_results"]
