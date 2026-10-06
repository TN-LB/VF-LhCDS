"""M2 differential harness. Expected truth imports only the independent M1 package.

The persistent C++ probe avoids process-startup cost; it is a BUILD_TESTING-only
adapter. All declared graphs and exact requests/results are retained in evidence.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference"))
from vflhcds_reference.direct import Reference, submasks
from vflhcds_reference.graph import Graph
from vflhcds_reference.generators import all_labelled_graphs, seeded_cases
from vflhcds_reference.io import canonical_graph, graph_sha256, oracle_record
from vflhcds_reference.parametric import cardinality_line_chain, exhaustive_F, exhaustive_restricted

HUGE = Fraction(2**130 + 1, 2**131 + 3)


def encoded_set(graph, mask):
    ids = graph.ids(mask)
    return " ".join(map(str, (len(ids), *ids)))


class Probe:
    def __init__(self, executable, stderr):
        self.process = subprocess.Popen([str(executable)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=stderr, text=True, bufsize=1)
    def begin(self, graph, h):
        self.process.stdin.write(f"case {graph.n} {len(graph.edges)} {h}\n")
        self.process.stdin.write(" ".join(map(str, graph.vertices)) + "\n")
        for u, v in graph.edges:
            self.process.stdin.write(f"{u} {v}\n")
    def ask(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise AssertionError("probe exited before a response; see probe.stderr")
        return json.loads(line)
    def end(self):
        self.process.stdin.write("end\n")
    def close(self):
        self.process.stdin.close()
        self.process.stdout.close()
        code = self.process.wait()
        assert code == 0, f"probe exit {code}"
    def abort(self):
        if self.process.poll() is None:
            self.process.terminate()
        self.process.wait()


def fixtures(tier):
    if tier == "exhaustive-small":
        for n in range(1, 6):
            for ordinal, graph in enumerate(all_labelled_graphs(n)):
                for h in (2, 3):
                    yield graph, h, {"family": "all-labelled", "n": n, "ordinal": ordinal}
    elif tier == "seeded":
        yield from seeded_cases(20260922, 1000)
    else:
        named = json.loads((ROOT / "reference/fixtures/named_truth.json").read_text())["cases"]
        named.append(json.loads((ROOT / "reference/fixtures/outer_breakpoint.json").read_text()))
        for case in named:
            if tier == "higher-h" and case["h"] < 4:
                continue
            yield Graph(tuple(case["vertices"]), tuple(map(tuple, case["edges"]))), case["h"], {"family": "named", "name": case["name"]}
        for h in (4, 5):
            n = h + 1
            yield Graph(tuple(range(n)), tuple(combinations(range(n), 2))), h, {"family": "complete-boundary", "name": f"K{n}-h{h}"}
            yield Graph(tuple(range(h)), tuple(combinations(range(h), 2))), h, {"family": "complete", "name": f"K{h}"}
            yield Graph(tuple(range(h-1)), tuple(combinations(range(h-1), 2))), h, {"family": "h>n", "name": f"K{h-1}-h{h}"}
        if tier == "smoke":
            yield from seeded_cases(20260922, 10)
        else:
            # The full 1000-case seeded tier also includes h=4,5 and h>n.
            for graph, h, metadata in seeded_cases(20260922, 100):
                if h >= 4:
                    yield graph, h, metadata


def queries(ref, metadata, tier):
    graph = ref.graph
    result = {("global", Fraction(0), 0, graph.full_mask),
              ("global", Fraction(ref.counts[-1]+1), 0, graph.full_mask),
              ("global", Fraction(1, 2), 0, graph.full_mask),
              ("global", HUGE, 0, graph.full_mask)}
    chain_pairs = 0
    if tier != "seeded":
        chain = cardinality_line_chain(ref)
        for sample in chain.samples:
            result.add(("global", sample.parameter, 0, graph.full_mask))
        for x, y in combinations(chain.sets, 2):
            threshold = Fraction(ref.counts[y]-ref.counts[x], y.bit_count()-x.bit_count())
            result.add(("restricted", threshold, x, y))
            chain_pairs += 1
    # Every case includes explicit X=Y, smaller zero upper bounds and arbitrary
    # restricted requests. No arbitrary bound is promoted to a global certificate.
    result.add(("restricted", Fraction(0), 0, graph.full_mask >> 1))
    result.add(("restricted", Fraction(3, 2), graph.full_mask, graph.full_mask))
    rng = random.Random(20260922 + metadata.get("case_index", metadata.get("ordinal", 0)))
    while len(result) < 12:
        y = rng.randrange(1 << graph.n)
        x = rng.randrange(1 << graph.n) & y
        result.add(("restricted", Fraction(rng.randrange(20), rng.randrange(1, 11)), x, y))
    return sorted(result), chain_pairs


class Campaign:
    def __init__(self, probe, output):
        self.probe, self.output = probe, output
        self.counts = Counter()
        self.graphs = set()
        self.context = None
        self.cases = (output / "cases.jsonl").open("w")
        self.records = gzip.open(output / "results.jsonl.gz", "wt")
    def emit(self, record):
        self.records.write(json.dumps(record, separators=(",", ":")) + "\n")
    def check(self, condition, message):
        if not condition:
            raise AssertionError(message)
    def case(self, graph, h, metadata, tier):
        ref = Reference(graph, h)
        case_id = self.counts["graph_h_cases"]
        self.context = {"kind": "infrastructure", "case_id": case_id, "vertices": graph.vertices,
                        "edges": graph.edges, "h": h, "metadata": metadata}
        self.cases.write(json.dumps(self.context) + "\n")
        self.cases.flush()
        self.probe.begin(graph, h)
        inspection = self.probe.ask("inspect")
        expected_cliques = [list(graph.ids(mask)) for mask in ref.cliques]
        self.check(inspection["cliques"] == expected_cliques, "T04 clique tuples")
        self.check(inspection["counts"] == list(ref.counts), "T04 all induced subset counts")
        incidences = [[i for i, mask in enumerate(ref.cliques) if mask & (1 << v)] for v in range(graph.n)]
        self.check(inspection["incidences"] == incidences, "T04 incidence IDs")
        self.check(inspection["degrees"] == list(map(len, incidences)), "T04 degrees")
        self.check(sum(inspection["degrees"]) == h * len(ref.cliques), "T04 degree sum")
        self.check(inspection["graph_sha256"] == graph_sha256(graph), "T01 canonical checksum")
        self.emit({"case_id": case_id, "inspection": inspection})
        self.counts["subset_count_comparisons"] += 1 << graph.n
        checked_bounds = {}
        def footprints(x, y):
            if (x, y) in checked_bounds:
                return checked_bounds[x, y]
            observed = self.probe.ask(f"footprints {encoded_set(graph,x)} {encoded_set(graph,y)}")
            self.check(observed["scanned"] == len(ref.cliques), "T06 scanned includes rejected cliques")
            self.check(observed["total_weight"] == ref.counts[y] - ref.counts[x], "T06 total weight")
            keys = [tuple(f["vertices"]) for f in observed["footprints"]]
            self.check(keys == sorted(set(keys)), "T06 deterministic unique footprints")
            masks = []
            for f in observed["footprints"]:
                mask = graph.mask(f["vertices"])
                self.check(mask != 0 and mask & (y ^ x) == mask and f["weight"] > 0, "T06 footprint domain")
                masks.append((mask, f["weight"]))
            for s in submasks(y ^ x):
                rhs = sum(weight for mask, weight in masks if mask & s == mask)
                self.check(rhs == ref.counts[x | s] - ref.counts[x], "T06 every-subset identity")
                self.counts["footprint_subset_identities"] += 1
            self.counts["footprint_bound_pairs"] += 1
            checked_bounds[x, y] = observed
            self.emit({"case_id": case_id, "footprints": observed, "x": graph.ids(x), "y": graph.ids(y)})
            return observed
        if graph.n <= 4 and tier == "exhaustive-small":
            for y in range(1 << graph.n):
                for x in submasks(y):
                    footprints(x, y)
                    self.counts["exhaustive_nested_pairs"] += 1
        requested, chain_pairs = queries(ref, metadata, tier)
        self.counts["chain_pairs"] += chain_pairs
        for scope, parameter, x, y in requested:
            self.context = {"kind": "oracle", "case_id": case_id, "vertices": graph.vertices, "edges": graph.edges,
                            "h": h, "metadata": metadata, "scope": scope, "lambda": str(parameter),
                            "x": graph.ids(x), "y": graph.ids(y)}
            expected = oracle_record(ref, exhaustive_F(ref, parameter) if scope == "global"
                                     else exhaustive_restricted(ref, parameter, x, y))
            f = footprints(x, y)
            n, p = (y ^ x).bit_count(), len(f["footprints"])
            a, b = parameter.numerator, parameter.denominator
            infinity = 1 + (n+1)*b*f["total_weight"] + n*((n+1)*a-1)
            bypass = n == 0 or a == 0
            safe = infinity <= 2**128-1
            policies = ["auto", "big"] + (["uint128"] if safe or bypass else [])
            outputs = []
            for policy in policies:
                command = f"{scope} {policy} {a}/{b}"
                if scope == "restricted":
                    command += f" {encoded_set(graph,x)} {encoded_set(graph,y)}"
                actual = self.probe.ask(command)
                stats = actual.pop("stats")
                self.context.update(policy=policy, expected=expected, actual=actual)
                self.check(actual == expected, "T08/T09 largest exact set/record")
                self.check(stats["logical_interval_queries"] == 0 and stats["mincut_calls"] == (0 if bypass else 1), "P03.5 event counters")
                self.check(stats["original_interval_size"] == n and stats["oracle_interval_size"] == n, "P03.5 interval sizes")
                if bypass:
                    self.check(all(stats[key] is None for key in ["capacity_backend", "cliques_scanned", "unique_footprints", "forward_nodes", "forward_arcs", "residual_arcs", "capacity_bit_length"]), "P03.5 bypass nulls")
                else:
                    backend = "arbitrary_precision" if policy == "big" or not safe else "uint128"
                    arcs = n + p + sum(len(record["vertices"]) for record in f["footprints"])
                    self.check(stats["capacity_backend"] == backend and stats["cliques_scanned"] == len(ref.cliques)
                               and stats["unique_footprints"] == p and stats["forward_nodes"] == n+p+2
                               and stats["forward_arcs"] == arcs and stats["residual_arcs"] == 2*arcs
                               and stats["capacity_bit_length"] == (infinity if p else (n+1)*a-1).bit_length(), "P03.5 exact network telemetry")
                    self.counts[f"flow_{backend}"] += 1
                    if policy == "auto" and backend == "arbitrary_precision":
                        self.counts["automatic_big_flows"] += 1
                self.counts["backend_executions"] += 1
                outputs.append({"policy": policy, "actual": actual, "stats": stats})
            self.emit({"case_id": case_id, "scope": scope, "lambda": f"{a}/{b}", "x": graph.ids(x), "y": graph.ids(y),
                       "expected": expected, "outputs": outputs})
            self.counts["oracle_requests"] += 1
            self.counts[f"{scope}_requests"] += 1
        self.probe.end()
        self.counts["graph_h_cases"] += 1
        self.counts[f"h_{h}_cases"] += 1
        self.counts[f"family_{metadata['family']}"] += 1
        self.graphs.add(graph_sha256(graph))
    def close(self):
        self.cases.close(); self.records.close()


def minimize_failure(executable, failure, output):
    """Semantic oracle mismatches only; retain request scope and valid bounds.

    Save original first. Other failures retain the original as the minimal known
    reproducer with an explicit reason; they are never silently reclassified.
    """
    (output / "failure-original.json").write_text(json.dumps(failure, indent=2) + "\n")
    current = dict(failure)
    if failure.get("kind") == "oracle" and failure.get("expected") != failure.get("actual"):
        def still_fails(candidate):
            graph = Graph(tuple(candidate["vertices"]), tuple(map(tuple, candidate["edges"])))
            ref = Reference(graph, candidate["h"])
            parameter = Fraction(candidate["lambda"])
            x, y = graph.mask(candidate["x"]), graph.mask(candidate["y"])
            expected = oracle_record(ref, exhaustive_F(ref, parameter) if candidate["scope"] == "global"
                                     else exhaustive_restricted(ref, parameter, x, y))
            with (output / "minimizer.stderr").open("a") as error:
                probe = Probe(executable, error)
                try:
                    probe.begin(graph, ref.h)
                    command = f"{candidate['scope']} {candidate['policy']} {parameter.numerator}/{parameter.denominator}"
                    if candidate["scope"] == "restricted":
                        command += f" {encoded_set(graph,x)} {encoded_set(graph,y)}"
                    actual = probe.ask(command); actual.pop("stats")
                    probe.end(); probe.close()
                except Exception:
                    probe.abort(); return False  # Preserve semantic mismatch, not a crash.
            return expected != actual
        changed = True
        while changed:
            changed = False
            for edge in list(current["edges"]):
                trial = dict(current, edges=[e for e in current["edges"] if e != edge])
                if still_fails(trial): current, changed = trial, True
            for vertex in list(current["vertices"]):
                if len(current["vertices"]) == 1: break
                trial = dict(current, vertices=[v for v in current["vertices"] if v != vertex],
                             edges=[e for e in current["edges"] if vertex not in e],
                             x=[v for v in current["x"] if v != vertex], y=[v for v in current["y"] if v != vertex])
                if still_fails(trial): current, changed = trial, True
        for h in range(2, current["h"]):
            trial = dict(current, h=h)
            if still_fails(trial): current = trial; break
        for value in ["0", "1/2", "1", "2"]:
            trial = dict(current, **{"lambda": value})
            if still_fails(trial): current = trial; break
        if current["scope"] == "restricted":
            trial = dict(current, x=[])
            if still_fails(trial): current = trial
        current["reduction"] = "deterministic edges/vertices/h/lambda/lower-bound; scope retained"
    else:
        current["reduction"] = "not reduced: nonsemantic failure; original retained as minimal known reproducer"
    (output / "failure-minimized.json").write_text(json.dumps(current, indent=2) + "\n")
    graph = Graph(tuple(current["vertices"]), tuple(map(tuple, current["edges"])))
    (output / "failure.graph").write_text(canonical_graph(graph))
    for bound in ("x", "y"):
        ids = current.get(bound, [])
        (output / f"failure.{bound}.set").write_text("vflhcds-set 1\nn " + str(len(ids)) + "\n" + "".join(f"v {v}\n" for v in ids))


def run(args, output):
    started = time.monotonic()
    with (output / "probe.stderr").open("w") as error:
        probe = Probe(args.probe.resolve(), error)
        campaign = Campaign(probe, output)
        try:
            for graph, h, metadata in fixtures(args.tier):
                campaign.case(graph, h, metadata, args.tier)
            probe.close()
        except Exception as failure:
            probe.abort()
            if campaign.context:
                minimize_failure(args.probe.resolve(), dict(campaign.context, error=str(failure)), output)
            raise
        finally:
            campaign.close()
    summary = dict(campaign.counts, distinct_graphs=len(campaign.graphs), tier=args.tier,
                   seed=20260922 if args.tier != "exhaustive-small" else None,
                   status="passed", wall_seconds=time.monotonic()-started,
                   probe=str(args.probe.resolve()), probe_sha256=hashlib.sha256(args.probe.read_bytes()).hexdigest(),
                   scope="M2 exact primitives only; finite implementation evidence, not a theorem proof")
    summary["evidence_sha256"] = {name: hashlib.sha256((output/name).read_bytes()).hexdigest()
                                  for name in ["cases.jsonl", "results.jsonl.gz", "probe.stderr"]}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--tier", choices=["smoke", "exhaustive-small", "seeded", "higher-h"], required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=False)
        run(args, args.output)
    else:
        with tempfile.TemporaryDirectory() as directory:
            run(args, Path(directory))


if __name__ == "__main__":
    main()
