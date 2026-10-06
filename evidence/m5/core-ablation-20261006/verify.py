"""Recheck frozen inputs, saved outputs and aggregates; launch no native solver."""
from collections import Counter
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import file_hashes, parse_graph, save, semantic_hash, sha256
from experiments.validate import compare, parse_records

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def main():
    pins = read(HERE / 'preflight.json')
    checks = {}
    for key in ('paper_sha256', 'reference_sha256', 'production_source_sha256',
                'binary_sha256', 'provenance_sha256', 'pinned_harness_sha256',
                'library_sha256', 'old_probe_sha256'):
        for name, digest in pins[key].items():
            assert sha256(ROOT / name) == digest, name
        checks[key] = len(pins[key])
    for name, digest in pins['ippv_source_sha256'].items():
        assert sha256(ROOT / '.deps/baselines/ippv' / name) == digest, name
    for patch in pins['ippv_patches']:
        assert sha256(ROOT / patch['path']) == patch['sha256']
    assert len(pins['ippv_patches']) == 7
    assert sha256(ROOT / 'baselines/ippv/source-lock.json') == pins['baseline_lock_sha256']
    assert sha256(ROOT / 'docs/DECISIONS.md') == pins['decision_log_sha256']
    assert sha256(HERE / 'run_campaign.py') == pins['runner_sha256']
    assert sha256(HERE / 'pytest-command.json') == pins['pytest_command_sha256']
    assert read(HERE / 'pytest-command.json')['exit_code'] == 0
    before = read(HERE / 'files-before.json')
    assert sha256(HERE / 'run.py.before') == before['experiments/run.py']
    for name, change in pins['harness_changes'].items():
        assert change['before_sha256'] == before[name]
        assert change['after_sha256'] == sha256(ROOT / name)
    checks['historical_evidence_files'] = {}
    for directory, inventory in pins['historical_evidence_sha256'].items():
        assert file_hashes(ROOT / directory) == inventory, directory
        checks['historical_evidence_files'][directory] = len(inventory)

    prior = ROOT / 'evidence/m5/pilot-membership-20261006'
    assert sha256(prior / 'config.json') == pins['previous_config_sha256']
    previous_config, config = read(prior / 'config.json'), load_config(HERE / 'config.json')
    assert {key for key in config if config[key] != previous_config[key]} == {'name', 'algorithms'}
    off, on = config['algorithms']
    assert off['options']['core'] == 'off' and on['options']['core'] == 'safe'
    assert {k for k in off if off[k] != on[k]} == {'name', 'options'}
    assert {k for k in off['options'] if off['options'][k] != on['options'][k]} == {'core'}
    assert all(off[k] == previous_config['algorithms'][0][k] for k in off if k != 'name')
    assert config['scope'] == 'approved_campaign' and config['repeats'] == 3
    assert config['timeout_seconds'] == 60 and config['threads'] == 1
    campaign = HERE / 'campaign'
    assert config == read(campaign / 'config.json')
    assert schedule(config) == read(HERE / 'schedule.json') == read(campaign / 'schedule.json')
    inventory = read(campaign / 'checksums.json')
    for name, digest in inventory.items():
        assert sha256(campaign / name) == digest, name
    assert set(file_hashes(campaign)) == set(inventory) | {'checksums.json'}
    checks['raw_inventory_entries'] = len(inventory)
    launch, completion = [read(HERE / f'{name}.json') for name in ('launch', 'completion')]
    assert launch['command'] == completion['command']
    assert launch['configuration_sha256'] == sha256(HERE / 'config.json') == pins['configuration_sha256']
    assert launch['preflight_sha256'] == sha256(HERE / 'preflight.json')
    assert launch['environment_sha256'] == sha256(HERE / 'environment.json')
    env, old_env = read(HERE / 'environment.json'), read(prior / 'environment.json')
    for key in ('hardware', 'platform', 'environment'):
        assert env[key] == old_env[key], key
    assert all(h['exit_code'] == 0 for h in env['hardware'].values())
    assert (HERE / 'driver.stderr').read_bytes() == b''
    summary, policy = read(campaign / 'summary.json'), read(campaign / 'execution-policy.json')
    assert len(policy['planned_runs']) == 48
    assert policy['stop_on_failure'] and policy['continue_on_timeout'] and policy['require_strict_agreement']
    assert len(summary['runs']) <= 48
    assert [r['directory'] for r in summary['runs']] == [r['directory'] for r in policy['planned_runs'][:len(summary['runs'])]]
    unrun = policy['planned_runs'][len(summary['runs']):]
    if unrun:
        assert read(campaign / 'stopped.json')['unrun'] == unrun
    else:
        assert not (campaign / 'stopped.json').exists()
    assert all(not (campaign / r['directory']).exists() for r in unrun)

    cases = {c['name']: c for c in config['cases']}
    algorithms = {a['name']: a for a in config['algorithms']}
    records, hashes, manifests = {}, {}, {}
    last_finish, native_statuses, validators = launch['started_utc'], Counter(), 0
    for row in summary['runs']:
        run = campaign / row['directory']
        manifest = read(run / 'manifest.json')
        manifests[(row['case'], row['repeat'], row['algorithm'])] = manifest
        case, algorithm = cases[row['case']], algorithms[row['algorithm']]
        native = manifest['native']
        assert native == read(run / 'process.json')
        assert row['status'] == manifest['status']
        native_statuses[row['status']] += 1
        assert last_finish <= native['started_utc'] <= native['finished_utc']
        last_finish = native['finished_utc']
        assert native['timeout_seconds'] == 60 and native['executable_sha256'] == algorithm['sha256']
        assert manifest['build_provenance'] == read((ROOT / algorithm['executable']).with_suffix('.provenance.json'))
        graph = parse_graph((run / 'graph.txt').read_text())
        assert sha256(run / 'graph.txt') == case['sha256'] == row['graph_sha256']
        for name, digest in manifest['sha256'].items():
            assert sha256(run / name) == digest, name
        if row['status'] == 'completed':
            external = manifest['external_validation']
            assert external == read(run / 'validation/process.json')
            assert native['native_exit_code'] == external['native_exit_code'] == 0
            assert last_finish <= external['started_utc'] <= external['finished_utc']
            last_finish = external['finished_utc']
            assert external['timeout_seconds'] == 60
            check = manifest['validation']
            assert check['passed'] and check['level'] == 'structural_checked'
            assert not check['completeness_certified'] and all(check['checks'].values())
            values = parse_records((run / 'canonical_output.jsonl').read_text(), graph, case['h'])
            assert len(values) == check['output_count'] <= case['k']
            assert semantic_hash(graph, case['h'], values) == row['semantic_sha256']
            queries = manifest['native_status']['counters']['queries']
            for query in queries:
                assert query['oracle_interval_size'] <= query['original_interval_size']
                if algorithm['options']['core'] == 'off':
                    assert query['oracle_interval_size'] == query['original_interval_size']
                    assert query['core'] is None and query['core_reduction_seconds'] is None
                elif query['core'] is not None:
                    assert query['core_threshold'] >= 1 and query['core_reduction_seconds'] >= 0
                    assert all(value >= 0 for value in query['core'].values())
            reduction_seconds = sum(q['core_reduction_seconds'] or 0 for q in queries)
            assert reduction_seconds <= manifest['phase_wall_seconds']['postindex'] + 1e-6
            records[(row['case'], row['repeat'], row['algorithm'])] = values
            hashes.setdefault((row['case'], row['algorithm']), set()).add(row['semantic_sha256'])
            validators += 1
        elif row['status'] == 'timeout':
            assert native['status'] == 'timeout' and native['native_exit_code'] == -9
            assert native['wall_seconds'] >= 60
            assert manifest['validation']['level'] == 'not_run' and 'external_validation' not in manifest
            assert row['semantic_sha256'] is None and not (run / 'canonical_output.jsonl').exists()
        else:
            raise AssertionError(f"Substantive failure requires diagnosis: {row['directory']}: {row['status']}")
    assert last_finish <= completion['finished_utc']
    comparisons = summary['comparisons']
    core_pairs = []
    for pair in comparisons:
        keys = [(pair['case'], pair['repeat'], name) for name in pair['algorithms']]
        if all(key in records for key in keys):
            expected = compare(*(records[key] for key in keys), k=cases[pair['case']]['k'])
            assert all(pair[key] == value for key, value in expected.items())
            assert expected['strict_match'], 'Core switch changed canonical output'
            off_key, on_key = [(pair['case'], pair['repeat'], a) for a in ('vf-core-off', 'vf-core-safe')]
            off_m, on_m = manifests[off_key], manifests[on_key]
            off_c, on_c = [m['native_status']['counters'] for m in (off_m, on_m)]
            off_q, on_q = off_c['queries'], on_c['queries']
            assert off_c['logical_interval_queries'] == on_c['logical_interval_queries']
            assert off_c['cliques_scanned'] == on_c['cliques_scanned']
            assert len(off_q) == len(on_q)
            for a, b in zip(off_q, on_q):
                assert a['original_interval_size'] == b['original_interval_size']
                assert b['oracle_interval_size'] <= a['oracle_interval_size']
                assert (b['forward_nodes'] or 0) <= (a['forward_nodes'] or 0)
                assert (b['forward_arcs'] or 0) <= (a['forward_arcs'] or 0)
            core_pairs.append({
                'case': pair['case'], 'repeat': pair['repeat'], 'strict_match': True,
                'logical_queries': off_c['logical_interval_queries'],
                'same_footprint_scan_visits': off_c['cliques_scanned'],
                'off_wall_seconds': off_m['native']['wall_seconds'],
                'safe_wall_seconds': on_m['native']['wall_seconds'],
                'safe_core_seconds': sum(q['core_reduction_seconds'] or 0 for q in on_q),
                'off_sum_oracle_interval_sizes': sum(q['oracle_interval_size'] for q in off_q),
                'safe_sum_oracle_interval_sizes': sum(q['oracle_interval_size'] for q in on_q),
                'off_sum_forward_nodes': sum(q['forward_nodes'] or 0 for q in off_q),
                'safe_sum_forward_nodes': sum(q['forward_nodes'] or 0 for q in on_q),
                'off_sum_forward_arcs': sum(q['forward_arcs'] or 0 for q in off_q),
                'safe_sum_forward_arcs': sum(q['forward_arcs'] or 0 for q in on_q),
            })
        else:
            assert pair['level'] == 'not_compared' and 'tie_aware_match' not in pair
    save(HERE / 'core-pair-details.json', core_pairs)
    expected_exit = 0 if len(summary['runs']) == 48 and all(r['status'] == 'completed' for r in summary['runs']) and all(p.get('strict_match') for p in comparisons) else 1
    assert completion['exit_code'] == expected_exit
    assert all(len(values) == 1 for values in hashes.values()), 'Unstable repeated outputs'

    # Compare semantic outputs only; historical timings stay in their own campaign.
    previous_campaign = prior / 'campaign'
    previous = read(previous_campaign / 'summary.json')
    historical_matches = []
    for row in summary['runs']:
        if row['status'] != 'completed' or not row['case'].startswith('ca-grqc-'):
            continue
        old_name = 'vf-adjacency-membership'
        old_row = next(r for r in previous['runs'] if r['case'] == row['case'] and r['repeat'] == row['repeat'] and r['algorithm'] == old_name)
        assert row['semantic_sha256'] == old_row['semantic_sha256']
        assert (campaign / row['directory'] / 'canonical_output.jsonl').read_bytes() == (previous_campaign / old_row['directory'] / 'canonical_output.jsonl').read_bytes()
        historical_matches.append({'new_directory': row['directory'], 'old_directory': old_row['directory'],
                                   'case': row['case'], 'repeat': row['repeat'], 'algorithm': row['algorithm'],
                                   'semantic_sha256': row['semantic_sha256']})
    old_condmat = ROOT / 'evidence/m5/condmat-pair-20261006/campaign'
    old_condmat_row = next(r for r in read(old_condmat / 'summary.json')['runs'] if r['algorithm'] == 'vf-adjacency-membership')
    old_condmat_output = (old_condmat / old_condmat_row['directory'] / 'canonical_output.jsonl').read_bytes()
    condmat_matches = []
    for row in summary['runs']:
        if row['case'] != 'ca-condmat-h3-k5' or row['status'] != 'completed':
            continue
        assert row['semantic_sha256'] == old_condmat_row['semantic_sha256']
        assert (campaign / row['directory'] / 'canonical_output.jsonl').read_bytes() == old_condmat_output
        condmat_matches.append(row['directory'])
    save(HERE / 'historical-output-comparison.json', {
        'previous_campaign': str(previous_campaign.relative_to(ROOT)),
        'exact_matches': historical_matches, 'historical_timings_combined': False,
        'condmat_previous_campaign': str(old_condmat.relative_to(ROOT)),
        'condmat_k5_exact_matches': condmat_matches})

    aggregate = HERE / 'aggregate'
    cells = read(aggregate / 'cells.json')
    rows = read(aggregate / 'runs.json')
    assert len(cells) == 16 and len(rows) == len(summary['runs'])
    for cell in cells:
        selected = [r for r in rows if r['case'] == cell['case'] and r['algorithm'] == cell['algorithm']]
        available = len(selected) == 3 and all(r['status'] == 'completed' for r in selected)
        assert cell['three_repeat_measurements_available'] == available
        for label, function in [('median', statistics.median), ('min', min), ('max', max)]:
            for key, unit in [('wall', 'seconds'), ('rss', 'bytes')]:
                values = cell[f'raw_{"wall_seconds" if key == "wall" else "peak_rss_bytes"}']
                assert cell[f'{key}_{label}_{unit}'] == (function(values) if available else None)
        assert cell['statuses'] == dict(Counter(r['status'] for r in selected))
    assert read(aggregate / 'unrun.json') == unrun
    totals = read(aggregate / 'totals.json')
    assert totals['native_statuses'] == dict(native_statuses)
    assert totals['external_validators_completed'] == totals['structural_passes'] == validators
    assert totals['recorded_native_runs'] == len(rows)
    assert totals['unrun_native_runs'] == len(unrun)
    checks.update(native_statuses=dict(native_statuses), external_validator_successes=validators,
                  paired_blocks=len(comparisons),
                  tie_aware_matches=sum(p.get('tie_aware_match', False) for p in comparisons),
                  strict_matches=sum(p.get('strict_match', False) for p in comparisons),
                  strict_disagreements=sum(p.get('strict_match') is False for p in comparisons),
                  pairs_not_compared=sum(p.get('level') == 'not_compared' for p in comparisons),
                  stable_completed_cells=len(hashes), planned_native_runs=48, unrun=len(unrun),
                  historical_grqc_exact_output_matches=len(historical_matches),
                  historical_condmat_k5_exact_output_matches=len(condmat_matches),
                  all_16_aggregate_cells_verified=True, native_and_validator_times_separate=True,
                  completed_core_pair_counter_checks=len(core_pairs), core_cost_included_in_solve=True,
                  completeness_certified=False, builds_ctest_sanitizers_rerun=False)
    save(HERE / 'verification.json', checks)
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
