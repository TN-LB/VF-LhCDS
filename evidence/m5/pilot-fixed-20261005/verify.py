"""Check saved results, version pins, aggregation and stop boundary; no native run."""
from collections import Counter
import copy
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import parse_graph, save, sha256, semantic_hash
from experiments.validate import compare, parse_records
HERE = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text())

def hashes(base, pins):
    for name, digest in pins.items():
        assert sha256(base / name) == digest, name
    return len(pins)

def verify():
    pins = read(HERE / 'preflight.json')
    checks = {}
    for key in ('paper_sha256', 'reference_sha256', 'production_source_sha256', 'pinned_harness_sha256', 'binary_sha256', 'provenance_sha256', 'graph_sha256', 'draft_artifacts_sha256', 'repair_evidence_sha256'):
        checks[key] = hashes(ROOT, pins[key])
    hashes(HERE / 'source', pins['pinned_harness_sha256'])
    checks['ippv_sources'] = hashes(ROOT / '.deps/baselines/ippv', pins['ippv_source_sha256'])
    assert sha256(ROOT / 'baselines/ippv/source-lock.json') == pins['baseline_lock_sha256']
    assert len(pins['patches']) == 7
    for patch in pins['patches']:
        assert sha256(ROOT / patch['path']) == patch['sha256']
    old = ROOT / 'evidence/m5/pilot-20261005'
    checks['historical_pilot_files'] = hashes(old, pins['historical_pilot_sha256'])
    assert {str(p.relative_to(old)) for p in old.rglob('*') if p.is_file()} == set(pins['historical_pilot_sha256'])
    campaign = HERE / 'campaign'
    inventory = read(campaign / 'checksums.json')
    checks['raw_inventory_entries'] = hashes(campaign, inventory)
    assert {str(p.relative_to(campaign)) for p in campaign.rglob('*') if p.is_file()} == set(inventory) | {'checksums.json'}
    config = load_config(HERE / 'config.json')
    assert config == read(campaign / 'config.json')
    original = read(old / 'config.json')
    normalized = copy.deepcopy(config)
    normalized['name'] = original['name']
    for key in ('name', 'executable', 'sha256'):
        normalized['algorithms'][1][key] = original['algorithms'][1][key]
    assert normalized == original
    assert schedule(config) == read(HERE / 'schedule.json') == read(campaign / 'schedule.json') == read(old / 'schedule.json')
    approval, launch, completion = [read(HERE / f'{name}.json') for name in ('approval', 'launch', 'completion')]
    assert approval['recorded_utc'] <= launch['started_utc'] <= completion['finished_utc']
    assert approval['status'] == 'accepted' and approval['decision_id'] == 'D031'
    assert sha256(HERE / 'config.json') == approval['config_sha256']
    hashes(ROOT, launch['sha256'])
    assert launch['command'] == completion['command'] and '--stop-on-failure' in launch['command']
    assert completion['exit_code'] == 1
    assert (HERE / 'driver.stderr').read_text() == ''
    summary, policy, stopped = [read(campaign / f'{name}.json') for name in ('summary', 'execution-policy', 'stopped')]
    rows = summary['runs']
    assert len(policy['planned_runs']) == 48 and policy['stop_on_failure']
    assert len(rows) == 25 and Counter(r['status'] for r in rows) == {'completed': 24, 'timeout': 1}
    assert [r['directory'] for r in rows] == [r['directory'] for r in policy['planned_runs'][:25]]
    assert stopped['unrun'] == policy['planned_runs'][25:]
    assert all(not (campaign / r['directory']).exists() for r in stopped['unrun'])
    assert stopped['reason'] == {'kind':'unsuccessful_run', 'directory':'runs/0012-0', 'status':'timeout'}
    graphs = {c['name']: parse_graph((ROOT / c['graph']).read_text()) for c in config['cases']}
    parsed, last_finish, successes, validators = {}, launch['started_utc'], 0, 0
    for row in rows:
        directory = campaign / row['directory']
        manifest = read(directory / 'manifest.json')
        process = read(directory / 'process.json')
        assert manifest['native'] == process
        assert process['started_utc'] >= last_finish
        assert process['timeout_seconds'] == config['timeout_seconds']
        assert process['memory_limit_bytes'] is None
        algorithm = next(a for a in config['algorithms'] if a['name'] == row['algorithm'])
        assert process['executable_sha256'] == algorithm['sha256']
        assert manifest['build_provenance'] == read((ROOT / algorithm['executable']).with_suffix('.provenance.json'))
        last_finish = process['finished_utc']
        if row['status'] == 'completed':
            assert process['native_exit_code'] == 0
            validation = manifest['external_validation']
            assert validation == read(directory / 'validation/process.json')
            assert validation['native_exit_code'] == 0 and validation['started_utc'] >= last_finish
            last_finish = validation['finished_utc']
            assert manifest['validation']['passed'] and manifest['validation']['level'] == 'structural_checked'
            assert not manifest['validation']['completeness_certified']
            records = parse_records((directory / 'canonical_output.jsonl').read_text(), graphs[row['case']], row['h'])
            assert len(records) == row['k']
            assert semantic_hash(graphs[row['case']], row['h'], records) == row['semantic_sha256']
            parsed[(row['case'], row['repeat'], row['algorithm'])] = records
            successes += 1
            validators += 1
        else:
            assert process['status'] == 'timeout' and process['native_exit_code'] == -9 and process['signal'] == 9
            assert process['wall_seconds'] >= 60
            assert manifest['validation']['level'] == 'not_run' and 'external_validation' not in manifest
            assert (directory / 'stdout.txt').read_bytes() == (directory / 'stderr.txt').read_bytes() == b''
    assert last_finish <= completion['finished_utc']
    assert len(summary['comparisons']) == 12
    for pair in summary['comparisons']:
        expected = compare(*(parsed[(pair['case'], pair['repeat'], a)] for a in pair['algorithms']), k=next(c['k'] for c in config['cases'] if c['name'] == pair['case']))
        assert all(pair[k] == v for k, v in expected.items()) and pair['tie_aware_match']
    assert sum(p['strict_match'] for p in summary['comparisons']) == 6
    aggregate = HERE / 'aggregate'
    cells = read(aggregate / 'cells.json')
    assert len(cells) == 16 and sum(c['unrun_repeats'] for c in cells) == 23
    for cell in cells:
        selected = [r for r in rows if r['case'] == cell['case'] and r['algorithm'] == cell['algorithm']]
        native = [read(campaign / r['directory'] / 'process.json') for r in selected]
        assert cell['raw_wall_seconds'] == [p['wall_seconds'] for p in native]
        assert cell['raw_peak_rss_bytes'] == [p['peak_rss_bytes'] for p in native]
        assert len(cell['semantic_hashes']) == (1 if any(r['status']=='completed' for r in selected) else 0)
        if cell['three_repeat_agreement_available']:
            assert len(native) == 3 and all(p['status'] == 'completed' for p in native)
            assert cell['wall_median_seconds'] == sorted(p['wall_seconds'] for p in native)[1]
            assert cell['rss_median_bytes'] == sorted(p['peak_rss_bytes'] for p in native)[1]
        else:
            assert cell['wall_median_seconds'] is None and cell['rss_median_bytes'] is None
    assert sum(c['three_repeat_agreement_available'] for c in cells) == 8
    assert read(HERE / 'aggregate-command.json')['exit_code'] == 0
    assert (HERE / 'aggregate.stderr').read_text() == ''
    checks.update(native_completed=successes, native_timeout=1, validators_passed=validators, pairs_recomputed=12, strict_matches=6, tie_aware_matches=12, unrun=23, stable_hashes_for_all_completed_triples=True, all_planned_cells_verified=16, successful_median_cells=8, post_stop_native_calls=0, benchmark_driver_exit=1, build_or_test_suite_rerun=False, timeout_phase='unknown')
    save(HERE / 'verification.json', checks)
    print(json.dumps(checks, indent=2))

if __name__ == '__main__':
    verify()
