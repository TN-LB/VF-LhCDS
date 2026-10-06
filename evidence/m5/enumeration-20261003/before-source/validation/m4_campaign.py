"""M4: unchanged M3 truth corpus through four modes, plus definition-level cores.

Core truth enumerates all induced sets; it never implements production peeling.
Original failures are saved and the run stops, respecting the M4 owner boundary.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations
import json
import shutil
from pathlib import Path
import tempfile
import time

from oracle_campaign import Probe, encoded_set
from solver_campaign import Campaign, fixtures, equal, Reference, Graph, canonical_graph

MODES = [('off', 'sorted'), ('off', 'membership'), ('safe', 'sorted'), ('safe', 'membership')]


class ModesProbe:
    def __init__(self, executable, error, output):
        self.raw = Probe(executable, error)
        self.counts = Counter()
        self.records = gzip.open(output/'mode_results.jsonl.gz', 'wt')
        self.case_number = -1
        self.context = None

    def emit(self, command, mode, actual):
        self.records.write(json.dumps({'case_id': self.case_number, 'command': command,
            'core': mode[0], 'footprints': mode[1], 'actual': actual}, separators=(',', ':'))+'\n')

    def configure(self, mode):
        equal('mode_configuration', {}, self.raw.ask(f'config {mode[0]} {mode[1]}'))

    def core(self, threshold):
        if threshold not in self.cores:
            # Union of ALL qualifying subsets, including empty; no peeling.
            result = 0
            for mask in range(1, self.graph.full_mask+1):
                if self.minimum_degree[mask] >= threshold:
                    result |= mask
            self.cores[threshold] = result
        return self.cores[threshold]

    def begin(self, graph, h):
        self.case_number += 1
        self.graph, self.h, self.ref = graph, h, Reference(graph, h)
        self.cores = {0: graph.full_mask}
        self.minimum_degree = [0] + [min(self.ref.counts[mask]-self.ref.counts[mask ^ (1<<v)]
            for v in range(graph.n) if mask & (1<<v)) for mask in range(1,graph.full_mask+1)]
        self.tokens, self.points = {}, {}
        self.context = {'vertices':list(graph.vertices), 'edges':list(map(list,graph.edges)), 'h':h}
        self.raw.begin(graph, h)
        degree = [self.ref.counts[-1]-self.ref.counts[graph.full_mask ^ (1<<v)] for v in range(graph.n)]
        thresholds = list(range(max(degree)+2)) + [2**200]
        for threshold in thresholds:
            command = f'core {threshold}'; self.context.update(command=command)
            actual = self.raw.ask(command); mask = self.core(threshold)
            invalidated = self.ref.counts[-1]-self.ref.counts[mask]
            expected = {'vertices':list(graph.ids(mask)), 'vertices_removed':graph.n-mask.bit_count(),
                'cliques_invalidated':invalidated, 'degree_decrements':(h-1)*invalidated,
                'incidence_visits':sum(degree[v] for v in range(graph.n) if not mask & (1<<v))}
            equal('all_subset_core_definition_and_updates', expected, actual)
            self.emit(command, ('peeling','none'), actual); self.counts['core_definition_requests'] += 1
        full = graph.full_mask
        if graph.n <= 4:
            pairs = [(x,y) for y in range(full+1) for x in range(y+1) if x&y==x]
        else:
            pairs = [(0,full),(full,full),(full>>1,full),(0,full>>1),(0,0)]
        for x,y in pairs:
            weights = Counter(clique & ~x for clique in self.ref.cliques if clique&y==clique and clique&~x)
            expected = {'scanned':len(self.ref.cliques), 'total_weight':sum(weights.values()),
                'footprints':sorted([{'vertices':list(graph.ids(mask)), 'weight':weight}
                    for mask,weight in weights.items()],key=lambda item:item['vertices'])}
            for scan in ('sorted','membership'):
                mode = ('off',scan); self.configure(mode); command=f'footprints {x} {y}'
                self.context.update(command=command, core=mode[0], footprints=scan)
                actual=self.raw.ask(command); equal('exact_footprint_records',expected,actual)
                self.emit(command,mode,actual);self.counts['footprint_executions']+=1
            self.counts['footprint_bound_pairs']+=1

    def check_query(self, stats, mode, x, y, lam):
        reduced = y
        if mode[0]=='safe' and lam>0:
            threshold = (lam.numerator+lam.denominator-1)//lam.denominator
            core = self.core(threshold); reduced &= core
            equal('core_threshold',threshold,stats['core_threshold'])
            equal('core_vertices_removed',self.graph.n-core.bit_count(),stats['core']['vertices_removed'])
            invalidated=self.ref.counts[-1]-self.ref.counts[core]
            equal('core_cliques_invalidated',invalidated,stats['core']['cliques_invalidated'])
            equal('core_degree_updates',(self.h-1)*invalidated,stats['core']['degree_decrements'])
            equal('core_time_available',True,stats['core_reduction_seconds'] is not None and stats['core_reduction_seconds']>=0)
            self.counts['core_executions']+=1
            self.counts['oracle_vertices_removed']+=(y^reduced).bit_count()
        else:
            equal('core_bypass_nulls',(None,None,None),(stats['core_threshold'],stats['core'],stats['core_reduction_seconds']))
        equal('lower_endpoint_retained',x,x&reduced)
        n=(reduced^x).bit_count()
        equal('original_interval_size',(y^x).bit_count(),stats['original_interval_size'])
        equal('reduced_interval_size',n,stats['oracle_interval_size'])
        bypass=lam==0 or n==0
        equal('actual_reduced_cut_count',int(not bypass),stats['mincut_calls'])
        if bypass:
            equal('bypass_network_nulls',True,all(stats[key] is None for key in ['cliques_scanned','unique_footprints','forward_nodes','forward_arcs','residual_arcs','capacity_bit_length','capacity_backend']))
        else:
            weights=Counter(c&~x for c in self.ref.cliques if c&reduced==c and c&~x)
            p=len(weights);arcs=n+p+sum(mask.bit_count() for mask in weights)
            infinity=1+(n+1)*lam.denominator*sum(weights.values())+n*((n+1)*lam.numerator-1)
            equal('reduced_network_sizes',(n+p+2,arcs,2*arcs),(stats['forward_nodes'],stats['forward_arcs'],stats['residual_arcs']))
            equal('reduced_footprints',(len(self.ref.cliques),p),(stats['cliques_scanned'],stats['unique_footprints']))
            equal('reduced_capacity_bits',(infinity if p else (n+1)*lam.numerator-1).bit_length(),stats['capacity_bit_length'])
            if stats['capacity_backend']=='arbitrary_precision':self.counts['big_flows']+=1

    def ask(self, command):
        parts=command.split();kind=parts[0];answers=[];mode_tokens={}
        for mode in MODES:
            self.configure(mode);actual_command=command
            if kind=='separator':
                actual_command=' '.join(parts[:2]+[str(self.tokens[int(t)][mode]) for t in parts[2:]])
            self.context.update(command=command,actual_command=actual_command,core=mode[0],footprints=mode[1])
            actual=self.raw.ask(actual_command)
            if kind=='point':
                mode_tokens[mode]=actual['token']
                self.check_query(actual['stats'],mode,0,self.graph.full_mask,Fraction(parts[2]))
                semantic={k:v for k,v in actual.items() if k not in ('stats','token')}
            elif kind=='separator':
                x,y=(self.points[int(t)] for t in parts[2:])
                self.check_query(actual['stats'],mode,x,y,Fraction(actual['lambda']))
                semantic={k:v for k,v in actual.items() if k!='stats'}
            else:
                for event,query in zip(actual['trace'],actual['stats']['queries']):
                    x,y=(self.graph.mask(event[k]) for k in ('x','y'))
                    self.check_query(query,mode,x,y,Fraction(event['lambda']))
                equal('mode_logical_count',len(actual['trace']),actual['stats']['logical_interval_queries'])
                equal('mode_cut_sum',sum(q['mincut_calls'] for q in actual['stats']['queries']),actual['stats']['mincut_calls'])
                semantic={k:v for k,v in actual.items() if k!='stats'}
            if answers:equal('mode_exact_output_trace_equality',answers[0][1],semantic)
            answers.append((actual,semantic));self.emit(command,mode,actual)
            self.counts[f'{kind}_executions']+=1
        baseline=answers[0][0]
        if kind=='point':
            self.tokens[baseline['token']]=mode_tokens
            self.points[baseline['token']]=self.graph.mask(baseline['vertices'])
        return baseline

    def end(self):self.raw.end()
    def close(self):self.raw.close()
    def abort(self):self.raw.abort()


def run(args,output):
    start=time.monotonic()
    with (output/'probe.stderr').open('w') as error:
        probe=ModesProbe(args.probe.resolve(),error,output);campaign=Campaign(probe,output)
        try:
            for graph,h,metadata in fixtures(args.tier):campaign.case(graph,h,metadata,args.tier)
            if args.tier=='smoke':
                graph=Graph(tuple(range(8)),tuple(sorted((*combinations(range(4),2),(4,5),(4,6),(5,6),(4,7)))))
                campaign.case(graph,2,{'family':'named','name':'core-non-chain-pendant'},args.tier)
            probe.close()
        except Exception as failure:
            probe.abort()
            context=dict(probe.context or {},error=str(failure),check=getattr(failure,'check',None),
                         expected=getattr(failure,'expected',None),actual=getattr(failure,'actual',None))
            (output/'failure-original.json').write_text(json.dumps(context,indent=2,default=str)+'\n')
            if probe.context:
                (output/'failure.graph').write_text(canonical_graph(probe.graph))
            raise
        finally:
            campaign.close();probe.records.close()
    summary=dict(campaign.counts,distinct_base_graphs=len(campaign.graphs),mode_checks=dict(probe.counts),
        tier=args.tier,status='passed',seed=20260929 if args.tier!='exhaustive-small' else None,
        modes=MODES,wall_seconds=time.monotonic()-start,
        probe_sha256=hashlib.sha256(args.probe.read_bytes()).hexdigest(),
        evidence_scope='Independent finite definition checks plus mode equality; not theorem or performance proof')
    summary['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True),flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--probe',type=Path,required=True)
    parser.add_argument('--tier',choices=['smoke','exhaustive-small','seeded','higher-h'],required=True)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    if args.output:args.output.mkdir(parents=True,exist_ok=False);run(args,args.output)
    else:
        with tempfile.TemporaryDirectory() as directory:
            try:run(args,Path(directory))
            except Exception:
                saved=Path(__file__).resolve().parents[1]/'evidence/m4/failures'/str(time.time_ns())
                shutil.copytree(directory,saved)
                print(f'Original failing evidence retained at {saved}',flush=True)
                raise


if __name__=='__main__':main()
