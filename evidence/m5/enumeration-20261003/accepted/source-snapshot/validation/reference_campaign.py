"""M1 finite reference checks; no production code, recursion or flow.

Run from the repository root with PYTHONPATH=reference. Every completed case and
any original/minimized failure is saved. Output directory must be new.
"""

import argparse
import datetime
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import platform
import sys
import traceback

from vflhcds_reference.direct import Reference, compactness, direct_lhcds, maximal_compact_sets
from vflhcds_reference.generators import all_labelled_graphs, seeded_cases
from vflhcds_reference.graph import Graph, normalize_graph
from vflhcds_reference.io import graph_sha256, json_line, solution_records
from vflhcds_reference.parametric import cardinality_line_chain, exhaustive_F, exhaustive_restricted


class CheckFailure(AssertionError):
    def __init__(self, check, expected, actual):
        self.check, self.expected, self.actual = check, expected, actual
        super().__init__(check)


def equal(check, expected, actual):
    if expected != actual:
        raise CheckFailure(check, expected, actual)


def check_case(graph: Graph, h: int) -> dict:
    ref = Reference(graph, h)
    # Independent induced-combination counting using original-ID edge pairs,
    # rather than the reference's materialized clique masks and adjacency bits.
    edges = set(graph.edges)
    counts = []
    for mask in range(graph.full_mask + 1):
        ids = graph.ids(mask)
        count = 0 if h > len(ids) else sum(
            all(edge in edges for edge in combinations(clique, 2))
            for clique in combinations(ids, h))
        counts.append(count)
    equal("induced_combination_counts", tuple(counts), ref.counts)
    truth = direct_lhcds(ref)
    chain = cardinality_line_chain(ref)

    # A second parameter grid comes from direct deletion compactness values,
    # not cardinality maxima or recursive separators. This checks chain coverage.
    levels = {Fraction(0), Fraction(counts[-1] + 1)}
    levels.update(compactness(ref, mask) for mask in range(1, graph.full_mask + 1))
    points = sorted(levels)
    direct_grid = levels | {(a + b) / 2 for a, b in zip(points, points[1:])}
    samples = {sample.parameter: sample for sample in chain.samples}
    for value in sorted(direct_grid - samples.keys()):
        samples[value] = exhaustive_F(ref, value)
    hierarchy = set()
    for value, sample in samples.items():
        expected = tuple(sorted(maximal_compact_sets(ref, value)))
        components = tuple(sorted(graph.components(sample.largest)))
        equal("parametric_components_vs_all_superset_definition", expected, components)
        hierarchy.update(expected)
    equal("independent_chain_coverage", set(chain.sets), {sample.largest for sample in samples.values()})
    leaves = {s for s in hierarchy if not any(t != s and t & s == t for t in hierarchy)}
    equal("hierarchy_leaves_vs_direct_truth", set(truth), leaves)

    pairs = 0
    for i, x in enumerate(chain.sets):
        for j in range(i + 1, len(chain.sets)):
            y = chain.sets[j]
            value = Fraction(counts[y] - counts[x], y.bit_count() - x.bit_count())
            global_result = exhaustive_F(ref, value)
            restricted = exhaustive_restricted(ref, value, x, y)
            z = global_result.largest
            equal("certified_reference_bounds", z, restricted.largest)
            equal("separator_reference_progress", True, x != z and x & z == x and z & y == z)
            equal("separator_reference_consecutive", j == i + 1, z == y)
            pairs += 1

    for k in range(1, len(truth) + 3):
        equal("fixed_k_reference_prefix", truth[:k], direct_lhcds(ref, k=k))

    # A decreasing mapping changes original-ID tie order. Transform full truth
    # and re-sort before any truncation, including zero-density cases.
    mapping = {v: 10**30 - 7 * v for v in graph.vertices}
    renamed = normalize_graph(mapping.values(), ((mapping[u], mapping[v]) for u, v in graph.edges)).graph
    new_ref = Reference(renamed, h)
    transformed = sorted((ref.density(s), tuple(sorted(mapping[v] for v in graph.ids(s)))) for s in truth)
    transformed.sort(key=lambda item: (-item[0], item[1]))
    new_truth = direct_lhcds(new_ref)
    expected_ids = tuple(ids for _, ids in transformed)
    equal("complete_truth_relabeling", expected_ids, tuple(renamed.ids(s) for s in new_truth))
    for k in range(1, len(truth) + 3):
        equal("reranked_relabeling_prefix", expected_ids[:k],
              tuple(renamed.ids(s) for s in direct_lhcds(new_ref, k=k)))
    return {"results": solution_records(ref, truth), "chain": [list(graph.ids(s)) for s in chain.sets],
            "breakpoints": [str(value) for value in chain.breakpoints],
            "sample_parameters": [str(value) for value in sorted(samples)],
            "global_oracle_queries": len(samples) + pairs, "restricted_oracle_queries": pairs,
            "chain_pairs_checked": pairs, "prefixes_checked": 2 * (len(truth) + 2)}


def graph_record(graph, h, metadata):
    return {"graph_sha256": graph_sha256(graph), "vertices": list(graph.vertices),
            "edges": [list(edge) for edge in graph.edges], "h": h, "metadata": metadata}


def minimize_failure(graph, h, failure):
    """Deterministic edge/vertex deletion preserving the exact failed check ID."""
    def same(candidate):
        try:
            check_case(candidate, h)
        except CheckFailure as error:
            return error.check == failure.check
        return False

    while True:
        candidates = [Graph(graph.vertices, graph.edges[:i] + graph.edges[i + 1:])
                      for i in range(len(graph.edges))]
        if graph.n > 1:
            candidates.extend(Graph(tuple(v for v in graph.vertices if v != removed),
                                    tuple(edge for edge in graph.edges if removed not in edge))
                              for removed in graph.vertices)
        reduced = next((candidate for candidate in candidates if same(candidate)), None)
        if reduced is None:
            return graph
        graph = reduced


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=["exhaustive-small", "seeded"], required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=False)
    if args.tier == "exhaustive-small":
        cases = ((graph, h, {"n": n, "labelled_graph_index": index, "seed": None})
                 for n in range(1, 6) for index, graph in enumerate(all_labelled_graphs(n)) for h in (2, 3))
    else:
        cases = seeded_cases(20260917, 100)
    summary = {"tier": args.tier, "scope": "M1 reference only", "status": "running",
               "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "python": sys.version, "platform": platform.platform(), "graph_h_cases": 0,
               "global_oracle_queries": 0, "restricted_oracle_queries": 0,
               "chain_pairs_checked": 0, "prefixes_checked": 0}
    unique_graphs, unique_cases = set(), set()
    current = None
    try:
        with (output / "cases.jsonl").open("w") as stream:
            for graph, h, metadata in cases:
                current = graph_record(graph, h, metadata)
                checked = check_case(graph, h)
                current.update(checked)
                stream.write(json_line(current))
                stream.flush()
                summary["graph_h_cases"] += 1
                unique_graphs.add(current["graph_sha256"])
                unique_cases.add((current["graph_sha256"], h))
                for name in ["global_oracle_queries", "restricted_oracle_queries", "chain_pairs_checked", "prefixes_checked"]:
                    summary[name] += checked[name]
                if summary["graph_h_cases"] % 100 == 0:
                    print(f"{args.tier}: {summary['graph_h_cases']} cases passed", flush=True)
        summary["status"] = "completed"
    except Exception as error:
        summary["status"] = "failed"
        failure_dir = output / "failure"
        failure_dir.mkdir()
        original = {"case": current, "error": str(error), "traceback": traceback.format_exc()}
        if isinstance(error, CheckFailure):
            original.update(check=error.check, expected=repr(error.expected), actual=repr(error.actual))
        (failure_dir / "original.json").write_text(json.dumps(original, indent=2) + "\n")
        if isinstance(error, CheckFailure):
            minimized = minimize_failure(graph, h, error)
            (failure_dir / "minimized.json").write_text(json.dumps(graph_record(minimized, h, metadata), indent=2) + "\n")
        raise
    finally:
        summary.update(unique_graphs=len(unique_graphs), unique_graph_h_cases=len(unique_cases),
                       finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
