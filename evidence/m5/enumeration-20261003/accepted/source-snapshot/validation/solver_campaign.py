"""M3 definition-level solver validation. Reference remains a separate package.

All expected families use ALL proper supersets. Chain points come from the
independent cardinality-line envelope, never from production separation.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference"))
from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.graph import Graph, normalize_graph
from vflhcds_reference.generators import all_labelled_graphs, seeded_cases
from vflhcds_reference.io import canonical_graph, graph_sha256, solution_records, json_line
from vflhcds_reference.parametric import cardinality_line_chain, exhaustive_F
from oracle_campaign import Probe, fixtures as old_fixtures, HUGE


class Failure(AssertionError):
    def __init__(self, check, expected, actual):
        self.check, self.expected, self.actual = check, expected, actual
        super().__init__(check)


def equal(check, expected, actual):
    if expected != actual:
        raise Failure(check, expected, actual)


def semantic_hash(graph, h, records):
    header = {"schema_version": 1, "graph_sha256": graph_sha256(graph), "h": h}
    return hashlib.sha256((json_line(header) + "".join(map(json_line, records))).encode()).hexdigest()


def fixtures(tier):
    if tier == "seeded":
        yield from seeded_cases(20260929, 1000)
    elif tier == "higher-h":
        for graph, h, metadata in old_fixtures("higher-h"):
            if "seed" not in metadata:
                yield graph, h, metadata
        for graph, h, metadata in seeded_cases(20260929, 100):
            if h >= 4: yield graph, h, metadata
    elif tier == "exhaustive-small":
        yield from old_fixtures(tier)
    else:
        for graph, h, metadata in old_fixtures("smoke"):
            if "seed" not in metadata: yield graph, h, metadata
        graph = Graph(tuple(range(5)), tuple(combinations(range(4), 2)) + ((3,4),))
        yield graph, 2, {"family":"named", "name":"k4-pendant-non-emitting"}
        yield Graph((-90,-2,5,11,100), ((-90,-2),(5,11))), 2, {"family":"named", "name":"two-ties-isolate"}
        yield from seeded_cases(20260929, 10)


def minimize_case(case, predicate):
    """Predicate preserves the exact failed check and request kind; no solver truth here."""
    current = dict(case)
    changed = True
    while changed:
        changed = False
        for edge in list(current["edges"]):
            candidate = dict(current, edges=[e for e in current["edges"] if e != edge])
            if predicate(candidate): current, changed = candidate, True
        for vertex in list(current["vertices"]):
            if len(current["vertices"]) <= 1: break
            candidate = dict(current, vertices=[v for v in current["vertices"] if v != vertex],
                             edges=[e for e in current["edges"] if vertex not in e])
            if predicate(candidate): current, changed = candidate, True
    for h in range(2, current["h"]):
        candidate = dict(current, h=h)
        if predicate(candidate): current = candidate; break
    if isinstance(current.get("k"), int):
        for k in range(1, current["k"]):
            candidate = dict(current, k=k)
            if predicate(candidate): current = candidate; break
    return current


class Campaign:
    def __init__(self, probe, output):
        self.probe, self.output = probe, output
        self.counts = Counter(); self.graphs = set(); self.context = None
        self.cases = (output/"cases.jsonl").open("w")
        self.results = gzip.open(output/"results.jsonl.gz", "wt")
        self.traces = []
    def emit(self, record):
        self.results.write(json.dumps(record, separators=(",",":")) + "\n")
    def inspect_trace(self, ref, chain, actual):
        trace, stats = actual["trace"], actual["stats"]
        equal("logical_counter", len(trace), stats["logical_interval_queries"])
        equal("query_trace_lengths", len(trace), len(stats["queries"]))
        equal("actual_cut_sum", sum(q["mincut_calls"] for q in stats["queries"]), stats["mincut_calls"])
        equal("scan_sum", sum(q["cliques_scanned"] or 0 for q in stats["queries"]), stats["cliques_scanned"])
        equal("initial_clique_count",ref.counts[-1],stats["cliques_enumerated"])
        pending = [(0,ref.graph.full_mask)]
        indices = {point:i for i,point in enumerate(chain.sets)}
        terminals = []
        for event, query in zip(trace,stats["queries"]):
            x,y,z = (ref.graph.mask(event[key]) for key in ("x","y","z"))
            equal("left_first_original_endpoints", pending.pop(), (x,y))
            equal("stored_original_counts", (str(ref.counts[x]),str(ref.counts[y])), (event["mu_x"],event["mu_y"]))
            lam = Fraction(ref.counts[y]-ref.counts[x],y.bit_count()-x.bit_count())
            equal("exact_outer_lambda", lam, Fraction(event["lambda"]))
            equal("separator_global_set", exhaustive_F(ref,lam).largest, z)
            equal("strict_separator_progress", True, x != z and x&z == x and z&y == z)
            equal("consecutive_terminal", indices[y] == indices[x]+1, z == y)
            equal("interval_event_counter", 1, query["logical_interval_queries"])
            equal("actual_cut_event", int(lam != 0), query["mincut_calls"])
            n=(y^x).bit_count()
            equal("original_bound_size", n, query["original_interval_size"])
            equal("oracle_bound_size", n, query["oracle_interval_size"])
            if z != y:
                pending.append((z,y)); pending.append((x,z))
            else:
                accepted=[]; rejected=[]
                for mask in ref.graph.components(y^x):
                    touches=any(ref.graph.adjacency[v] & x for v in range(ref.graph.n) if mask & (1<<v))
                    (rejected if touches else accepted).append(mask)
                for mask in accepted: equal("accepted_layer_density", lam,ref.density(mask))
                terminals.append({"x":event["x"],"y":event["y"],"lambda":event["lambda"],
                                  "accepted":[list(ref.graph.ids(s)) for s in accepted],
                                  "rejected":[list(ref.graph.ids(s)) for s in rejected]})
        if actual["termination"]=="exhausted":
            equal("exhausted_pending_stack", [],pending)
            equal("full_query_bound",2*(len(chain.sets)-1)-1,len(trace))
        return terminals
    def variant(self, graph, h, metadata, variant, expected_transformed=None, *, parameters=True):
        ref=Reference(graph,h); truth=direct_lhcds(ref); records=solution_records(ref,truth)
        if expected_transformed is not None:
            equal("metamorphic_complete_truth",expected_transformed,records)
        chain=cardinality_line_chain(ref)
        case_id=self.counts["checked_variants"]
        self.context={"kind":"case","vertices":list(graph.vertices),"edges":list(map(list,graph.edges)),
                      "h":h,"metadata":metadata,"variant":variant}
        self.cases.write(json.dumps(dict(self.context,case_id=case_id,graph_sha256=graph_sha256(graph),truth=records,
                                         chain=[list(graph.ids(s)) for s in chain.sets]))+"\n"); self.cases.flush()
        self.probe.begin(graph,h)
        if parameters:
            params={Fraction(i,7) for i in range(11)}|{HUGE}
            representative={}
            for sample in chain.samples:
                representative.setdefault(sample.largest,sample.parameter)
            params.update(representative.values())
            tokens={}
            for parameter in sorted(params):
                observed=self.probe.ask(f"point auto {parameter.numerator}/{parameter.denominator}")
                expected=exhaustive_F(ref,parameter).largest
                equal("certified_chain_point",list(graph.ids(expected)),observed["vertices"])
                equal("chain_point_count",str(ref.counts[expected]),observed["clique_count"])
                tokens[expected]=observed["token"]
                self.counts["standalone_global_requests"]+=1
                if observed["stats"]["capacity_backend"]=="arbitrary_precision":self.counts["automatic_big_flows"]+=1
                self.emit({"case_id":case_id,"kind":"global_point","lambda":str(parameter),"actual":observed})
            equal("independent_chain_tokens",set(chain.sets),set(tokens))
            for x,y in combinations(chain.sets,2):
                lam=Fraction(ref.counts[y]-ref.counts[x],y.bit_count()-x.bit_count())
                expected=exhaustive_F(ref,lam).largest
                for policy in ("auto","big"):
                    observed=self.probe.ask(f"separator {policy} {tokens[x]} {tokens[y]}")
                    equal("all_chain_pair_separator",list(graph.ids(expected)),observed["vertices"])
                    equal("all_chain_pair_lambda",lam,Fraction(observed["lambda"]))
                    equal("separator_api_standalone_counter",0,observed["stats"]["logical_interval_queries"])
                    self.counts["certified_separator_requests"]+=1
                    self.emit({"case_id":case_id,"kind":"separator","policy":policy,"x":list(graph.ids(x)),"y":list(graph.ids(y)),"actual":observed})
                self.counts["chain_pairs"]+=1
        full_trace=None
        for k in [None,*range(1,len(truth)+3)]:
            by_policy=[]
            for policy in ("auto","big"):
                self.context.update(kind="solve",k=k,policy=policy)
                observed=self.probe.ask(f"solve {policy} {'all' if k is None else k}")
                expected=records if k is None else records[:k]
                equal("ranked_prefix",expected,observed["records"])
                equal("termination", "k_reached" if k is not None and k<=len(truth) else "exhausted",observed["termination"])
                equal("semantic_hash",semantic_hash(graph,h,expected),observed["semantic_sha256"])
                terminals=self.inspect_trace(ref,chain,observed)
                if k is None and policy=="auto":
                    full_trace=observed["trace"]
                    if metadata.get("name") in {"k4-pendant-non-emitting","two-ties-isolate","outer_breakpoint_not_induced_density"} and variant=="original":
                        self.traces.append({"name":metadata["name"],"trace":full_trace,"terminals":terminals,"records":records})
                if full_trace is not None:
                    equal("stop_is_prefix_of_full_traversal",full_trace[:len(observed["trace"])],observed["trace"])
                self.emit({"case_id":case_id,"kind":"solve","k":k,"policy":policy,"expected":expected,"actual":observed})
                self.counts["solver_runs"]+=1
                self.counts["solver_logical_queries"]+=observed["stats"]["logical_interval_queries"]
                self.counts["solver_mincuts"]+=observed["stats"]["mincut_calls"]
                by_policy.append(observed)
            equal("solver_backend_equivalence",by_policy[0]["records"],by_policy[1]["records"])
            self.counts["all_runs" if k is None else "fixed_k_prefixes"]+=1
        self.probe.end()
        self.counts["checked_variants"]+=1
        return ref,truth,records
    def case(self,graph,h,metadata,tier):
        self.context={"kind":"case","vertices":list(graph.vertices),"edges":list(map(list,graph.edges)),"h":h,"metadata":metadata}
        ref,truth,records=self.variant(graph,h,metadata,"original")
        mapping={v:10**60-7*v for v in graph.vertices}
        renamed=normalize_graph(mapping.values(),((mapping[u],mapping[v]) for u,v in graph.edges)).graph
        transformed=[]
        for record in records:
            transformed.append(dict(record,vertices=sorted(mapping[v] for v in record["vertices"])))
        transformed.sort(key=lambda record:(-Fraction(int(record["density_num"]),int(record["density_den"])),record["vertices"]))
        transformed=[dict(record,rank=i) for i,record in enumerate(transformed,1)]
        self.variant(renamed,h,metadata,"relabeled",transformed,parameters=False)
        if tier=="smoke" or (tier=="seeded" and metadata["case_index"]<20):
            fresh=max(graph.vertices)+17
            for edge_added in (False,True):
                extra=(fresh,fresh+1) if edge_added else (fresh,)
                augmented=Graph(tuple(sorted(graph.vertices+extra)),tuple(sorted(graph.edges+(((fresh,fresh+1),) if edge_added else ()))))
                extra_count=int(edge_added and h==2); density=Fraction(extra_count,len(extra))
                expected=records+[dict(rank=0,h=h,vertex_count=len(extra),clique_count=str(extra_count),density_num=str(density.numerator),density_den=str(density.denominator),vertices=list(extra))]
                expected.sort(key=lambda record:(-Fraction(int(record["density_num"]),int(record["density_den"])),record["vertices"]))
                expected=[dict(record,rank=i) for i,record in enumerate(expected,1)]
                self.variant(augmented,h,metadata,"disjoint-edge" if edge_added else "added-isolate",expected,parameters=False)
                self.counts["disjoint_union_cases" if edge_added else "isolate_cases"]+=1
        self.counts["base_graph_h_cases"]+=1
        self.counts[f"family_{metadata['family']}"]+=1
        self.graphs.add(graph_sha256(graph))
    def close(self):
        self.cases.close();self.results.close()
        (self.output/"named_traces.json").write_text(json.dumps(self.traces,indent=2)+"\n")


def retain_failure(executable, context, error, output):
    record=dict(context,error=str(error),check=getattr(error,"check",None),expected=getattr(error,"expected",None),actual=getattr(error,"actual",None))
    (output/"failure-original.json").write_text(json.dumps(record,indent=2,default=lambda v: sorted(v) if isinstance(v,set) else str(v))+"\n")
    if context.get("kind")=="solve" and isinstance(error,Failure) and error.check=="ranked_prefix":
        def still_fails(candidate):
            graph=Graph(tuple(candidate["vertices"]),tuple(map(tuple,candidate["edges"])))
            ref=Reference(graph,candidate["h"]); truth=direct_lhcds(ref)
            expected=solution_records(ref,truth if candidate["k"] is None else truth[:candidate["k"]])
            with (output/"minimizer.stderr").open("a") as stderr:
                probe=Probe(executable,stderr)
                try:
                    probe.begin(graph,candidate["h"])
                    observed=probe.ask(f"solve {candidate['policy']} {'all' if candidate['k'] is None else candidate['k']}")
                    probe.end();probe.close()
                except Exception:
                    probe.abort();return False
            return observed["records"]!=expected
        minimized=minimize_case(context,still_fails)
        minimized["reduction"]="deterministic edges/vertices/h/k, same ranked-prefix failure and fixed-k/all scope"
    else:
        minimized=dict(context,reduction="original retained; this failure kind is not automatically reduced")
    graph=Graph(tuple(minimized["vertices"]),tuple(map(tuple,minimized["edges"])))
    ref=Reference(graph,minimized["h"]); truth=direct_lhcds(ref)
    minimized["expected_full_truth"]=solution_records(ref,truth)
    (output/"failure-minimized.json").write_text(json.dumps(minimized,indent=2)+"\n")
    (output/"failure.graph").write_text(canonical_graph(graph))
    mode=["--all"] if minimized.get("k") is None else ["--k",str(minimized["k"])]
    (output/"reproduce.json").write_text(json.dumps({"cli_arguments":["solve","--graph","failure.graph","--h",str(minimized["h"]),*mode],"capacity_policy_in_test_probe":minimized.get("policy","auto")},indent=2)+"\n")


def run(args,output):
    start=time.monotonic()
    with (output/"probe.stderr").open("w") as error:
        probe=Probe(args.probe.resolve(),error); campaign=Campaign(probe,output)
        try:
            for graph,h,metadata in fixtures(args.tier):campaign.case(graph,h,metadata,args.tier)
            probe.close()
        except Exception as failure:
            probe.abort()
            if campaign.context:retain_failure(args.probe.resolve(),campaign.context,failure,output)
            raise
        finally:campaign.close()
    summary=dict(campaign.counts,distinct_base_graphs=len(campaign.graphs),tier=args.tier,status="passed",
                 wall_seconds=time.monotonic()-start,seed=20260929 if args.tier!="exhaustive-small" else None,
                 probe=str(args.probe.resolve()),probe_sha256=hashlib.sha256(args.probe.read_bytes()).hexdigest(),
                 evidence_level="definition-checked finite implementation evidence; not theorem proof")
    summary["oracle_requests"]=summary["standalone_global_requests"]+summary["certified_separator_requests"]
    summary["sha256"]={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,sort_keys=True),flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--probe",type=Path,required=True)
    parser.add_argument("--tier",choices=["smoke","exhaustive-small","seeded","higher-h"],required=True)
    parser.add_argument("--output",type=Path);args=parser.parse_args()
    if args.output:
        args.output.mkdir(parents=True,exist_ok=False);run(args,args.output)
    else:
        with tempfile.TemporaryDirectory() as directory:run(args,Path(directory))


if __name__=="__main__":main()
