"""Read saved outcomes/pins; does not launch either algorithm or the draft grid."""
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import save, sha256


def read(path):
    return json.loads(path.read_text())


def hashes_match(base, hashes):
    for name, digest in hashes.items():
        assert sha256(base / name) == digest, str(base / name)
    return len(hashes)


def main():
    here = Path(__file__).resolve().parent
    campaign = here / 'campaign'
    before = read(here / 'preflight.json')
    checks = {}
    checks['campaign_files_matched'] = hashes_match(campaign, read(campaign / 'checksums.json'))
    checks['papers_matched'] = hashes_match(ROOT, before['paper_sha256'])
    checks['reference_files_matched'] = hashes_match(ROOT, before['reference_sha256'])
    production = read(ROOT / 'build-m5-adjacency-release/vflhcds.provenance.json')
    checks['production_source_files_matched'] = hashes_match(ROOT, production['source_sha256'])
    lock = read(ROOT / 'baselines/ippv/source-lock.json')
    checks['ippv_source_files_matched'] = hashes_match(ROOT / '.deps/baselines/ippv', lock['patched_source_sha256'])
    assert sha256(ROOT / 'baselines/ippv/source-lock.json') == before['baseline_lock_sha256']
    checks['pre_edit_runner_snapshot_files_matched'] = hashes_match(
        here / 'source-before', read(campaign / 'environment.json')['script_sha256'])
    changed = [name for name, digest in before['enumeration_source_sha256'].items()
               if sha256(ROOT / name) != digest]
    assert sorted(changed) == ['experiments/run.py', 'experiments/test_harness.py']
    checks['changed_source_paths_since_preflight'] = changed
    config = load_config(here / 'config.json')  # Pin validation only; no execution.
    assert config['repeats'] == 1 and len(config['cases']) == 1
    assert read(campaign / 'schedule.json') == schedule(config)
    summary = read(campaign / 'summary.json')
    assert len(summary['runs']) == 2 and len(summary['comparisons']) == 1
    native = []
    for row in summary['runs']:
        manifest = read(campaign / row['directory'] / 'manifest.json')
        assert row['status'] == manifest['status'] == 'completed'
        assert manifest['native']['native_exit_code'] == manifest['external_validation']['native_exit_code'] == 0
        assert manifest['validation']['passed'] and manifest['validation']['output_count'] == 5
        assert manifest['validation']['level'] == 'structural_checked'
        assert manifest['validation']['completeness_certified'] is False
        assert manifest['native']['finished_utc'] <= manifest['external_validation']['started_utc']
        native.append({'algorithm': row['algorithm'], 'wall_seconds': manifest['native']['wall_seconds'],
                       'peak_rss_bytes': manifest['native']['peak_rss_bytes'],
                       'external_validation_wall_seconds': manifest['external_validation']['wall_seconds']})
    outputs = [(campaign / row['directory'] / 'canonical_output.jsonl').read_bytes() for row in summary['runs']]
    assert outputs[0] == outputs[1]
    comparison = summary['comparisons'][0]
    assert comparison['strict_match'] and comparison['tie_aware_match'] and not comparison['completeness_certified']
    assert len({row['semantic_sha256'] for row in summary['runs']}) == 1
    checks['paired_runs'] = native
    checks['semantic_sha256'] = summary['runs'][0]['semantic_sha256']
    tests = here / 'stop-control-final-tests'
    checks['tested_python_source_files_matched'] = hashes_match(ROOT, read(tests / 'source_sha256.json'))
    assert read(tests / 'command.json')['exit_code'] == 0
    assert '123 passed' in (tests / 'stdout.txt').read_text()
    assert not (tests / 'stderr.txt').read_text()
    checks['pytest_passed'] = 123
    proposal = ROOT / 'evidence/m5/campaign-proposal-20261005'
    pins = read(proposal / 'pins.json')
    assert pins['owner_approval'] is None and pins['benchmark_runs_executed'] == 0
    assert sha256(proposal / 'draft-config.json') == pins['config_sha256']
    assert sha256(proposal / 'draft-schedule.json') == pins['schedule_sha256']
    for field in ('binary_pins', 'provenance_sha256', 'harness_sha256'):
        checks[field + '_matched'] = hashes_match(ROOT, pins[field])
    draft = read(proposal / 'draft-config.json')
    assert draft['scope'] == 'draft'
    try:
        load_config(proposal / 'draft-config.json')
    except ValueError as error:
        assert 'draft configurations cannot run' in str(error)
    else:
        raise AssertionError('draft accepted for execution')
    # Check every non-scope field through the real loader, without calling execute.
    copy = dict(draft, scope='diagnostic')
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'validation-only.json'
        save(path, copy)
        assert load_config(path) == copy
    assert read(proposal / 'draft-schedule.json') == schedule(draft)
    assert sum(len(b['algorithm_indices']) for b in schedule(draft)) == 48
    for dataset in read(proposal / 'dataset-manifest.json'):
        assert sha256(ROOT / dataset['graph']) == dataset['graph_sha256']
        assert sha256(dataset['source_path']) == dataset['source_sha256']
        assert dataset['declared_vertices'] == dataset['vertices']
    checks['draft_schema_and_pins_valid_without_execution'] = True
    checks['draft_rejected_for_execution'] = True
    checks['draft_planned_native_calls'] = 48
    checks['draft_actual_native_calls'] = 0
    save(here / 'verification.json', checks)
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
