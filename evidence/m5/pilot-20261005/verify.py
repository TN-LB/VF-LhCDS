"""Verify saved pilot evidence without running either algorithm or changing raw logs."""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes(base, values):
    for name, expected in values.items():
        assert sha(base / name) == expected, name
    return len(values)


def verify():
    before = read(HERE / 'preflight.json')
    checks = {}
    for key in ('paper_sha256', 'reference_sha256', 'production_source_sha256',
                'pinned_harness_sha256', 'binary_sha256', 'provenance_sha256',
                'draft_artifacts_sha256', 'graph_sha256'):
        checks[key + '_matched'] = hashes(ROOT, before[key])
    checks['ippv_source_files_matched'] = hashes(ROOT / '.deps/baselines/ippv', before['ippv_source_sha256'])
    assert sha(ROOT / 'baselines/ippv/source-lock.json') == before['baseline_lock_sha256']
    campaign = HERE / 'campaign'
    inventory = read(campaign / 'checksums.json')
    checks['raw_inventory_entries_matched'] = hashes(campaign, inventory)
    actual = {str(p.relative_to(campaign)) for p in campaign.rglob('*') if p.is_file() and p.name != 'checksums.json'}
    assert actual == set(inventory)
    config = read(HERE / 'config.json')
    approval, launch, completion = [read(HERE / name) for name in ('approval.json', 'launch.json', 'completion.json')]
    assert approval['status'] == 'accepted' and approval['owner_reply'] == '可以'
    assert approval['recorded_utc'] <= launch['started_utc'] <= completion['finished_utc']
    assert launch['approval_sha256'] == sha(HERE / 'approval.json')
    assert launch['environment_sha256'] == sha(HERE / 'environment.json')
    assert launch['decision_log_sha256'] == sha(ROOT / 'docs/DECISIONS.md')
    assert approval['approved_config_sha256'] == sha(HERE / 'config.json')
    assert config == read(campaign / 'config.json')
    draft = read(ROOT / 'evidence/m5/campaign-proposal-20261005/draft-config.json')
    assert {k for k in config if config[k] != draft[k]} == {'name', 'scope'}
    assert config['scope'] == 'approved_campaign'
    assert read(HERE / 'schedule.json') == read(campaign / 'schedule.json') == read(ROOT / 'evidence/m5/campaign-proposal-20261005/draft-schedule.json')
    assert '--stop-on-failure' in launch['command'] == completion['command']
    assert completion['exit_code'] == 1
    policy, summary, stopped = [read(campaign / name) for name in ('execution-policy.json', 'summary.json', 'stopped.json')]
    assert policy['stop_on_failure'] is True and len(policy['planned_runs']) == 48
    assert len(summary['runs']) == 20 and len(summary['comparisons']) == 10
    assert all(r['status'] == 'completed' for r in summary['runs'])
    assert sum(c['strict_match'] for c in summary['comparisons']) == 6
    assert sum(c['tie_aware_match'] for c in summary['comparisons']) == 9
    directories = {r['directory'] for r in summary['runs']}
    assert [r for r in policy['planned_runs'] if r['directory'] not in directories] == stopped['unrun']
    assert len(stopped['unrun']) == 28
    assert all(not (campaign / r['directory']).exists() for r in stopped['unrun'])
    native_count = validator_count = 0
    for row in summary['runs']:
        manifest = read(campaign / row['directory'] / 'manifest.json')
        assert manifest['native']['native_exit_code'] == 0
        assert manifest['external_validation']['native_exit_code'] == 0
        assert manifest['validation']['passed'] and manifest['validation']['level'] == 'structural_checked'
        assert manifest['validation']['completeness_certified'] is False
        assert manifest['native']['finished_utc'] <= manifest['external_validation']['started_utc']
        native_count += 1
        validator_count += 1
    aggregate = HERE / 'aggregate'
    cells = read(aggregate / 'cells.json')
    assert len(cells) == 16 and sum(c['unrun_repeats'] for c in cells) == 28
    for cell in cells:
        source = [r for r in summary['runs'] if r['case'] == cell['case'] and r['algorithm'] == cell['algorithm']]
        raw = [read(campaign / r['directory'] / 'manifest.json')['native'] for r in source]
        assert cell['raw_wall_seconds'] == [m['wall_seconds'] for m in raw]
        assert cell['raw_peak_rss_bytes'] == [m['peak_rss_bytes'] for m in raw]
        assert len(cell['semantic_hashes']) == (1 if source else 0)
        if cell['three_repeat_agreement_available']:
            assert len(raw) == 3
            assert cell['wall_median_seconds'] == sorted(m['wall_seconds'] for m in raw)[1]
            assert cell['rss_median_bytes'] == sorted(m['peak_rss_bytes'] for m in raw)[1]
        else:
            assert cell['wall_median_seconds'] is None and cell['rss_median_bytes'] is None
    failure = read(aggregate / 'failure/reproducer.json')
    assert sha(aggregate / 'failure/original.graph') == failure['case']['sha256']
    details = failure['details']
    assert all(Fraction(v['cutoff']) == Fraction(10, 3) for v in details.values())
    extra = details['vf-adjacency-basic']['above_cutoff_sets_absent_from_other_output']
    assert len(extra) == 1 and extra[0]['rank'] == 18 and extra[0]['vertex_count'] == 13
    assert int(extra[0]['clique_count']) == 56 and Fraction(extra[0]['density_num'] + '/' + extra[0]['density_den']) == Fraction(56, 13)
    assert details['ippv-five-patches']['above_cutoff_sets_absent_from_other_output'] == []
    assert read(HERE / 'aggregate-command.json')['exit_code'] == 0
    checks.update(native_successes=native_count, external_validator_successes=validator_count,
                  strict_matches=6, tie_aware_matches=9, tie_aware_disagreements=1,
                  unrun_native_calls=28, stable_hashes_within_each_observed_algorithm_case=True,
                  campaign_exit_code=1, raw_graph_and_disagreement_preserved=True,
                  post_stop_native_calls=0, aggregate_cells_verified=16,
                  theoretical_fault_attribution='unresolved', build_or_test_suite_rerun=False)
    (HERE / 'verification.json').write_text(json.dumps(checks, indent=2) + '\n')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    verify()
