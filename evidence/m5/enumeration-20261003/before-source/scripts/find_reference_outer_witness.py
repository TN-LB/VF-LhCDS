"""Reconstruct a T03 fixture; the historical review witness was not supplied.

Run: PYTHONPATH=reference python scripts/find_reference_outer_witness.py
Writes the first witness and its provenance, without editing theory documents.
"""

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random

from vflhcds_reference.direct import Reference
from vflhcds_reference.graph import Graph
from vflhcds_reference.parametric import cardinality_line_chain


def main():
    seed = 20260917
    rng = random.Random(seed)
    pairs = tuple(combinations(range(7), 2))
    for index in range(10000):
        edges = tuple(pair for pair in pairs if rng.randrange(2))
        graph = Graph(tuple(range(7)), edges)
        for h in (2, 3):
            ref = Reference(graph, h)
            chain = cardinality_line_chain(ref)
            densities = {ref.density(s) for s in range(1, graph.full_mask + 1)}
            missing = [b for b in chain.breakpoints if b not in densities]
            if missing:
                record = {
                    "name": "outer_breakpoint_not_induced_density", "h": h,
                    "vertices": list(graph.vertices), "edges": list(graph.edges),
                    "seed": seed, "sample_index_zero_based": index,
                    "provenance": "New M1 reconstruction; unavailable historical review fixture not reproduced",
                    "expected_chain": [list(graph.ids(s)) for s in chain.sets],
                    "expected_breakpoints": [str(b) for b in chain.breakpoints],
                    "absent_from_all_induced_densities": [str(b) for b in missing],
                    "tested_graph_h_cases_before_including_witness": 2 * index + h - 1,
                }
                target = Path(__file__).resolve().parents[1] / "reference/fixtures/outer_breakpoint.json"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(record, indent=2) + "\n")
                print(json.dumps(record, indent=2))
                return
    raise SystemExit("No witness found in the declared search; T03 remains incomplete")


if __name__ == "__main__":
    main()
