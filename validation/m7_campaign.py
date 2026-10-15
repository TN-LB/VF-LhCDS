"""T23/T24/T25: original independent M3/M4 truth tiers across all M7 modes.

Standalone certificates remain on their original path. Solver modes share no truth
with production; local work counts use independent Python clique masks.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

from m4_campaign import ModesProbe as CoreProbe
from solver_campaign import Campaign, fixtures, equal, Graph, canonical_graph

WORK = ['global', 'interval-scan', 'interval-reuse']
MODES = [(core, scan, work) for core in ('off', 'safe')
         for scan in ('sorted', 'membership') for work in WORK]


class ModesProbe(CoreProbe):
    def ask(self, command):
        if not command.startswith('solve '):
            return super().ask(command)
        answers = []
        for core, scan, work in MODES:
            self.configure((core, scan))
            equal('work_configuration', {}, self.raw.ask('work '+work))
            self.context.update(command=command, core=core, footprints=scan, work=work)
            actual = self.raw.ask(command)
            pending = [(0, self.graph.full_mask, 0)]
            visited_local = 0
            for event, query in zip(actual['trace'], actual['stats']['queries']):
                x, y, depth = pending.pop()
                equal('local_depth', depth, query['depth'])
                equal('original_intervals', (list(self.graph.ids(x)), list(self.graph.ids(y))),
                      (event['x'], event['y']))
                z = self.graph.mask(event['z'])
                local = [c for c in self.ref.cliques if c & y == c and c & x != c]
                left = [c for c in local if c & z == c]
                split = z != y
                # Reuse the independently enumerated M4 core/network checks.
                checked = dict(query)
                if query['cliques_scanned'] is not None:
                    equal('local_aggregation_visits', len(self.ref.cliques) if work == 'global' else len(local),
                          query['cliques_scanned'])
                    checked['cliques_scanned'] = len(self.ref.cliques)
                self.check_query(checked, (core, scan), x, y, Fraction(event['lambda']))
                fields = ['interval_cliques', 'partition_clique_visits', 'partition_left_cliques',
                          'partition_right_cliques', 'reused_endpoint_counts']
                expected = [None]*5 if work == 'global' else [len(local), len(local) if split else 0,
                    len(left) if split else None, len(local)-len(left) if split else None,
                    int(split and work == 'interval-reuse')]
                equal('partition_reuse_counters', expected, [query[f] for f in fields])
                if split:
                    equal('partition_exact_count', self.ref.counts[z], self.ref.counts[x]+len(left))
                    pending.extend([(z, y, depth+1), (x, z, depth+1)])
                visited_local += len(local)
            stats = actual['stats']
            equal('mode_record', work, stats['clique_work'])
            equal('single_id_permutation', 0 if work == 'global' else len(self.ref.cliques), stats['clique_id_size'])
            equal('id_capacity_sufficient', True, stats['clique_id_capacity'] >= stats['clique_id_size'])
            equal('mode_logical_count', len(actual['trace']), stats['logical_interval_queries'])
            equal('mode_cut_sum', sum(q['mincut_calls'] for q in stats['queries']), stats['mincut_calls'])
            equal('mode_scan_sum', sum(q['cliques_scanned'] or 0 for q in stats['queries']), stats['cliques_scanned'])
            depth = max(q['depth'] for q in stats['queries'])
            equal('depth_visit_bound', True, visited_local <= len(self.ref.cliques)*(depth+1))
            equal('frontier_depth_bound', True, stats['frontier_peak_size'] <= depth+2)
            semantic = {k: v for k, v in actual.items() if k != 'stats'}
            if answers:
                equal('work_mode_exact_output_trace_equality', answers[0][1], semantic)
            answers.append((actual, semantic))
            self.records.write(json.dumps({'case_id':self.case_number, 'command':command,
                'core':core, 'footprints':scan, 'work':work, 'actual':actual}, separators=(',',':'))+'\n')
            self.counts['solve_executions'] += 1
            self.counts['local_partition_id_visits'] += sum(q['partition_clique_visits'] or 0 for q in stats['queries'])
            self.counts['reused_counts'] += sum(q['reused_endpoint_counts'] or 0 for q in stats['queries'])
            self.counts['max_depth'] = max(self.counts['max_depth'], depth)
        return answers[0][0]


def run(args):
    output=args.output; output.mkdir(parents=True, exist_ok=False)
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
            (output/'failure-minimized.json').write_text(json.dumps(dict(context,
                reduction='Original retained; stop this path before any mode-specific reduction.'),indent=2,default=str)+'\n')
            if probe.context:(output/'failure.graph').write_text(canonical_graph(probe.graph))
            raise
        finally:campaign.close();probe.records.close()
    summary=dict(campaign.counts,distinct_base_graphs=len(campaign.graphs),mode_checks=dict(probe.counts),
        tier=args.tier,status='passed',seed=20260929 if args.tier!='exhaustive-small' else None,
        modes=MODES,wall_seconds=time.monotonic()-start,
        probe_sha256=hashlib.sha256(args.probe.read_bytes()).hexdigest(),
        evidence_scope='Independent finite definition checks and work accounting; not theorem or performance proof')
    summary['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--probe',type=Path,required=True)
    parser.add_argument('--tier',choices=['smoke','exhaustive-small','seeded','higher-h'],required=True)
    parser.add_argument('--output',type=Path,required=True);run(parser.parse_args())
