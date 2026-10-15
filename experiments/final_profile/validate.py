"""T19/T20 development evidence: independent expected work and exact output checks."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'reference'))
sys.path.insert(0, str(ROOT / 'baselines/ippv'))
from process import capture, sha256
from vflhcds_reference.graph import Graph
from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.io import canonical_graph, graph_sha256, solution_records
from vflhcds_reference.parametric import cardinality_line_chain, exhaustive_F
from fixtures import fixtures
from reports import read_events, complete, semantic_trace, build as reports, load_bundle


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def check_events(events, ref, records, core, k, work="global"):
    assert complete(events), 'complete observer stream'
    final = events[-1]['work']
    clique_sets = [set(ref.graph.ids(mask)) for mask in ref.cliques]
    m = len(clique_sets)
    chain = cardinality_line_chain(ref)
    chain_position = {mask: i for i, mask in enumerate(chain.sets)}
    index = next(e for e in events if e['event'] == 'index')
    assert index['cliques'] == m
    assert index['tuple_slots'] == index['incidence_slots'] == m * ref.h
    queries = [e for e in events if e['event'] == 'separator']
    oracles = {e['query_id']: e for e in events if e['event'] == 'oracle'}
    histograms = {e['query_id']: e for e in events if e['event'] == 'footprints'}
    pending = [(0, 0, set(), set(ref.graph.vertices))]
    count_sets = []; expected_count_members = 0
    upper_rejected = contributions = visits = core_filtered = member_tests = 0
    accepted_count = rejected_count = nonoutput = 0
    partition_visits = partition_members = partition_left = partition_right = partition_calls = 0
    for q in queries:
        parent, depth, x, y = pending.pop()
        begin = next(e for e in events if e['event'] == 'query_begin' and e['query_id'] == q['query_id'])
        assert begin['parent'] == parent and begin['depth'] == depth
        assert x == set(q['x']) and y == set(q['y'])
        z = set(q['z']); o = oracles[q['query_id']]; stats = o['stats']
        lam = Fraction(q['lambda'])
        assert lam == Fraction(ref.counts[ref.graph.mask(y)] - ref.counts[ref.graph.mask(x)], len(y-x))
        assert z == set(ref.graph.ids(exhaustive_F(ref, lam).largest)), 'independent global optimum'
        assert (z == y) == (chain_position[ref.graph.mask(y)] == chain_position[ref.graph.mask(x)] + 1), 'independent chain terminal'
        eligible = set(ref.graph.vertices)
        if core == 'safe' and lam:
            threshold = (lam.numerator + lam.denominator - 1) // lam.denominator
            while True:
                remove = {v for v in eligible if sum(v in c and c <= eligible for c in clique_sets) < threshold}
                if not remove:
                    break
                eligible -= remove
        bound = y & eligible if core == 'safe' and lam else y
        assert stats['oracle_interval_size'] == len(bound-x)
        local_cliques = [c for c in clique_sets if c <= y and not c <= x]
        scanned_cliques = clique_sets if work == 'global' else local_cliques
        if o['shortcut'] == 'none':
            residuals = Counter(tuple(sorted(c-x)) for c in clique_sets if c <= bound and c-x)
            h = histograms[q['query_id']]
            unique = Counter(len(c) for c in residuals)
            weighted = Counter()
            for c, weight in residuals.items(): weighted[len(c)] += weight
            assert {int(s): n for s, n in h['unique_by_size'].items()} == unique
            assert {int(s): n for s, n in h['weight_by_size'].items()} == weighted
            p = len(residuals); n = len(bound-x)
            assert stats['forward_nodes'] == n+p+2
            assert stats['forward_arcs'] == n+p+sum(len(c) for c in residuals)
            assert stats['residual_arcs'] == 2 * stats['forward_arcs']
            assert stats['cliques_scanned'] == len(scanned_cliques)
            visits += len(scanned_cliques)
            upper_rejected += sum(not c <= bound for c in scanned_cliques)
            core_filtered += sum(c <= y and not c <= bound for c in scanned_cliques)
            contributions += sum(residuals.values())
            for c in scanned_cliques:
                for v in sorted(c):
                    member_tests += 1
                    if v not in bound: break
                if c <= bound: member_tests += len(c)
        else:
            assert q['query_id'] not in histograms and stats['forward_nodes'] is None
        if z != y:
            if work != 'interval-reuse': count_sets.append(z)
            if work != 'global':
                partition_calls += 1
                partition_visits += len(local_cliques)
                partition_left += sum(c <= z for c in local_cliques)
                partition_right += sum(not c <= z for c in local_cliques)
                for c in local_cliques:
                    for v in sorted(c):
                        partition_members += 1
                        if v not in z: break
            pending.extend([(q['query_id'], depth+1, z, y), (q['query_id'], depth+1, x, z)])
        else:
            accepted = 0
            for component in ref.graph.components(ref.graph.mask(y-x)):
                ids = set(ref.graph.ids(component))
                touches = any((u in ids and v in x) or (v in ids and u in x) for u, v in ref.graph.edges)
                rejected_count += touches
                accepted += not touches
            accepted_count += accepted
            nonoutput += accepted == 0
    count_sets.extend(set(r['vertices']) for r in records)
    for target in count_sets:
        for c in clique_sets:
            for v in sorted(c):
                expected_count_members += 1
                if v not in target: break
    assert final.get('count_calls', 0) == len(count_sets)
    assert final.get('count_clique_visits', 0) == m * len(count_sets)
    assert final.get('count_membership_vertex_tests', 0) == expected_count_members
    assert final.get('count_matches', 0) == sum(sum(c <= target for c in clique_sets) for target in count_sets)
    assert final.get('footprint_clique_visits', 0) == visits
    assert final.get('footprint_upper_rejected', 0) == upper_rejected
    assert final.get('footprint_core_filtered_tuples', 0) == core_filtered
    assert final.get('footprint_contributions', 0) == contributions
    assert final.get('footprint_membership_vertex_tests', 0) == member_tests
    assert final.get('accepted_components', 0) == accepted_count
    assert final.get('rejected_components', 0) == rejected_count
    assert final.get('non_output_layers', 0) == nonoutput
    assert final['logical_queries'] == len(queries)
    assert final.get('outputs', 0) == len(records)
    assert final.get('count_separator_calls', 0) == (0 if work == 'interval-reuse' else sum(q['z'] != q['y'] for q in queries))
    assert final['partition_calls'] == partition_calls
    assert final['partition_clique_visits'] == partition_visits
    assert final['partition_membership_vertex_tests'] == partition_members
    assert final['partition_left_cliques'] == final['partition_swap_calls'] == partition_left
    assert final['partition_right_cliques'] == partition_right
    assert final['partition_marker_slots'] == partition_calls * ref.graph.n
    assert final['reused_endpoint_counts'] == (partition_calls if work == 'interval-reuse' else 0)
    assert final['clique_ids_initialized'] == (0 if work == 'global' else m)
    assert final['clique_id_capacity'] >= final['clique_ids_initialized']
    assert final['clique_id_bytes'] == final['clique_id_capacity'] * 8
    assert final.get('count_emitted_calls', 0) == len(records)
    for field in ('incidence_visits', 'cliques_invalidated', 'degree_decrements', 'vertices_removed'):
        assert final.get('core_' + field, 0) == sum(o['stats']['core'][field] for o in oracles.values() if o['stats']['core'])
    if k == 'all':
        assert not pending
        assert len(queries) == 2 * final['terminal_layers'] - 1
        assert len(queries) == 2 * (len(chain.sets) - 1) - 1
    return {'queries': len(queries), 'maximum_depth': final.get('maximum_depth', 0),
            'non_output_layers': nonoutput, 'cliques': m, 'footprint_visits': visits,
            'count_visits': m * len(count_sets), 'partition_visits': partition_visits,
            'reused_counts': final['reused_endpoint_counts'], 'id_capacity': final['clique_id_capacity']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--small', action='store_true')
    parser.add_argument('--work-modes', nargs='+', choices=['global','interval-scan','interval-reuse'], default=['global'])
    args = parser.parse_args()
    args.build = args.build.resolve(); args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    binaries = {'control': args.build / 'production/vflhcds', 'diagnostic': args.build / 'vflhcds_final_profile'}
    source = json.loads((args.build / 'instrumented/manifest.json').read_text())
    source_hash = hashlib.sha256(json.dumps(source['production'], sort_keys=True).encode()).hexdigest()
    observer_hash = hashlib.sha256(json.dumps(source['observer'], sort_keys=True).encode()).hexdigest()
    cases = list(fixtures())
    if args.small: cases = cases[:8]
    schedule = [f'{c["name"]}-{core}-{work}-{k}-{role}' for c in cases for core, work in product(('off', 'safe'), args.work_modes)
                for k in ('all', 1) for role in binaries]
    bundle = {'schema': 1, 'scope': 'development', 'freeze_approved': False,
              'host': platform.platform(), 'schedule': schedule, 'rows': [],
              'pins': {'VF': {'source_sha256': source_hash, 'observer_sha256': observer_hash,
                             **{role: sha256(p) for role, p in binaries.items()}}}}
    save(args.output / 'configuration.json', {'scope': 'development-only', 'fixtures': cases,
         'schedule': schedule, 'native_timeout_seconds': 30, 'workers': 1, 'memory_limit_bytes': None,
         'cache_policy': 'uncontrolled', 'repeats': 1, 'source_manifest': source,
         'resource_rationale': 'small deterministic validation; no real-graph or M8 performance claim'})
    save(args.output / 'bundle.json', bundle)
    validation = []
    try:
        for case in cases:
            graph = Graph(tuple(case['vertices']), tuple(map(tuple, case['edges'])))
            ref = Reference(graph, case['h'])
            truth = solution_records(ref, direct_lhcds(ref))
            graph_path = args.output / (case['name'] + '.graph'); graph_path.write_text(canonical_graph(graph))
            for core, work in product(('off', 'safe'), args.work_modes):
                for k in ('all', 1):
                    by_role = {}
                    for role, binary in binaries.items():
                        run_id = f'{case["name"]}-{core}-{work}-{k}-{role}'
                        directory = args.output / run_id; directory.mkdir()
                        command = [str(binary), 'solve', '--graph', str(graph_path), '--h', str(case['h']),
                                   '--clique-enumeration', 'adjacency', '--clique-count', 'membership',
                                   '--footprint-scan', 'membership', '--core-reduction', core, '--clique-work', work]
                        command += ['--all'] if k == 'all' else ['--k', str(k)]
                        env = {'VF_PROFILE_OUTPUT': str(directory / 'events.jsonl')} if role == 'diagnostic' else {}
                        outcome = capture(command, directory, 30, environment=env)
                        row = dict(run_id=run_id, scope='development', algorithm='VF', role=role,
                                   suite='development:' + case['name'], graph_sha256=graph_sha256(graph), h=case['h'], k=k,
                                   core=core, work_mode=work, host=bundle['host'], repeat=0,
                                   source_sha256=source_hash, binary_sha256=sha256(binary), status=outcome['status'],
                                   observer_sha256=observer_hash if role == 'diagnostic' else None,
                                   wall_seconds=outcome['wall_seconds'], peak_rss_bytes=outcome['peak_rss_bytes'],
                                   output=f'{run_id}/stdout.txt', events=f'{run_id}/events.jsonl'
                                   if role == 'diagnostic' and (directory / 'events.jsonl').exists() else None)
                        row['artifact_sha256'] = {'output': sha256(directory / 'stdout.txt')}
                        if role == 'diagnostic' and (directory / 'events.jsonl').exists():
                            row['artifact_sha256']['events'] = sha256(directory / 'events.jsonl')
                        bundle['rows'].append(row); save(args.output / 'bundle.json', bundle)
                        assert outcome['status'] == 'completed', run_id
                        records = [json.loads(line) for line in (directory / 'stdout.txt').read_text().splitlines()]
                        assert records == (truth if k == 'all' else truth[:k]), (run_id, 'independent definition')
                        by_role[role] = records
                        if role == 'diagnostic':
                            events = read_events(directory / 'events.jsonl')
                            structure = check_events(events, ref, records, core, k, work)
                            # Existing production TraceSink adapter is an independent control observation.
                            request = 'case {} {} {} {} {}\nconfig {} membership\nwork {}\nsolve auto {}\nend\n'.format(
                                graph.n, len(graph.edges), case['h'], ' '.join(map(str, graph.vertices)),
                                ' '.join(f'{u} {v}' for u, v in graph.edges), core, work, k)
                            probe = args.build / 'final_control_solver_probe'
                            trace_run = subprocess.run([str(probe)], input=request, text=True, capture_output=True, timeout=30)
                            (directory / 'control-trace-input.txt').write_text(request)
                            (directory / 'control-trace-stdout.txt').write_text(trace_run.stdout)
                            (directory / 'control-trace-stderr.txt').write_text(trace_run.stderr)
                            assert trace_run.returncode == 0 and not trace_run.stderr
                            expected_trace = json.loads(trace_run.stdout.splitlines()[-1])['trace']
                            assert semantic_trace(events) == expected_trace, 'semantic query trace'
                            validation.append({'run_id': run_id, 'definition_checked': True, 'trace_equal': True,
                                               'independent_counters_checked': True, **structure})
                    assert by_role['control'] == by_role['diagnostic']
        if not args.small:
            assert max(row['maximum_depth'] for row in validation) >= 2, 'nested traversal coverage'
            assert any(row['non_output_layers'] for row in validation), 'non-output layer coverage'
        report = reports(load_bundle(args.output / 'bundle.json'))
        save(args.output / 'reports.json', report)
        assert json.dumps(report, sort_keys=True) == json.dumps(reports(load_bundle(args.output / 'bundle.json')), sort_keys=True)
        save(args.output / 'checks.json', {'passed': True, 'native_calls': len(bundle['rows']),
             'diagnostic_checks': validation, 'seed': 20261014, 'formal_experiment': False})
    except Exception as error:
        save(args.output / 'failure.json', {'error': repr(error), 'completed_checks': validation,
             'preserved_all_executed_rows': True, 'unrun': [r for r in schedule if r not in {x['run_id'] for x in bundle['rows']}]})
        raise


if __name__ == '__main__':
    main()
