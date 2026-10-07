"""Five-repeat aggregation/censoring checks using synthetic manifests, no solver."""
import importlib.util
import json
from pathlib import Path

import pytest

SOURCE = Path(__file__).with_name('summarize.py')
spec = importlib.util.spec_from_file_location('final_summary', SOURCE)
summary_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summary_module)
from experiments.support import file_hashes, save


@pytest.mark.parametrize('suite,recorded,timeout,mismatch', [
    ('stop', 5, False, False), ('stop', 4, False, False),
    ('stop', 5, True, False), ('stop', 5, False, True),
    ('main', 5, False, False), ('core', 5, False, False)])
def test_all_repetitions_and_correct_comparator(tmp_path, monkeypatch, suite, recorded, timeout, mismatch):
    monkeypatch.setattr(summary_module, 'HERE', tmp_path)
    monkeypatch.setattr(summary_module, 'ROOT', tmp_path)
    folder = tmp_path / suite
    campaign = folder / 'campaign'
    campaign.mkdir(parents=True)
    config = {'cases': [{'name': 'case'}], 'algorithms': [{'name': 'a'}, {'name': 'b'}], 'repeats': 5, 'seed': 20261003}
    save(campaign / 'config.json', config)
    plan, rows, pairs = [], [], []
    key = {'stop': 'prefix_match', 'core': 'strict_match', 'main': 'tie_aware_match'}[suite]
    for repeat in range(5):
        for i, algorithm in enumerate(('a', 'b')):
            entry = {'case': 'case', 'repeat': repeat, 'algorithm': algorithm, 'directory': f'runs/{repeat}-{i}'}
            plan.append(entry)
            if repeat >= recorded: continue
            failed = timeout and repeat == 4 and algorithm == 'a'
            row = {**entry, 'status': 'timeout' if failed else 'completed', 'semantic_sha256': None if failed else 'hash'}
            rows.append(row)
            run = campaign / entry['directory']
            run.mkdir(parents=True)
            native = {'native_exit_code': -9 if failed else 0, 'wall_seconds': 60 if failed else (repeat + 1) * (i + 1),
                      'peak_rss_bytes': 100, 'user_seconds': 1, 'system_seconds': .1, 'finished_utc': '0'}
            manifest = {'status': row['status'], 'native': native, 'phase_wall_seconds': {},
                        'validation': {'level': 'not_run' if failed else 'structural_checked', 'passed': not failed}}
            if not failed:
                manifest['external_validation'] = {'native_exit_code': 0, 'started_utc': '1'}
            save(run / 'manifest.json', manifest)
        if repeat < recorded:
            pairs.append({'case': 'case', 'repeat': repeat, 'level': 'not_compared'} if timeout and repeat == 4 else
                         {'case': 'case', 'repeat': repeat, key: not (mismatch and repeat == 0),
                          **({'strict_match': False} if suite == 'main' else {})})
    policy = {'planned_runs': plan, 'require_strict_agreement': suite == 'core', 'require_prefix_agreement': suite == 'stop'}
    save(campaign / 'execution-policy.json', policy)
    save(campaign / 'summary.json', {'runs': rows, 'comparisons': pairs})
    if recorded != 5:
        save(campaign / 'stopped.json', {'reason': {'kind': 'external_interruption'}, 'unrun': plan[2*recorded:]})
    save(folder / 'completion.json', {'exit_code': 1 if timeout or mismatch or recorded < 5 else 0, 'wall_seconds': 1})
    save(campaign / 'checksums.json', file_hashes(campaign))
    totals = summary_module.summarize(suite)
    cells = json.loads((tmp_path / 'aggregate' / suite / 'cells.json').read_text())
    a, b = cells
    assert totals['required_agreement'] == key
    assert totals['recorded_native_runs'] == recorded * 2 and totals['unrun_native_runs'] == 10 - recorded * 2
    assert a['wall_median_seconds'] == (3 if recorded == 5 and not timeout else None)
    assert b['wall_median_seconds'] == (6 if recorded == 5 else None)
    assert a['complete_repetitions_agree'] == (recorded == 5 and not timeout and not mismatch)
    if timeout:
        assert a['raw_wall_seconds'][-1] == 60 and a['wall_median_seconds'] is None
    if suite == 'main':
        assert a['complete_repetitions_agree'] and a['strict_matches'] == 0
