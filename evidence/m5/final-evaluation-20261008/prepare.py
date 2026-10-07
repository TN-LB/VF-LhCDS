"""Create accepted configs and run harness/tiny readiness checks, never benchmarks."""
import copy
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule, validate_comparison
from experiments.support import capture, save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    draft = ROOT / 'evidence/m5/final-scope-20261008'
    assert not (HERE / 'readiness').exists(), 'readiness records must be fresh'
    specs = {}
    for name in ('main', 'core'):
        config = read(draft / f'{name}.draft.json')
        config.update(scope='approved_campaign', name=f'final-local-{name}-20261008')
        specs[name] = config
    stop = read(draft / 'stop.draft.json')
    full = copy.deepcopy(stop['algorithm'])
    full['name'] = 'vf-count-membership-all'
    full['options']['output'] = 'all'
    config = copy.deepcopy(specs['core'])
    config.update(name='final-local-stop-20261008', cases=stop['cases'],
                  algorithms=[stop['algorithm'], full])
    specs['stop'] = config
    old_schedules = read(draft / 'schedules.json')
    for name, config in specs.items():
        folder = HERE / name
        folder.mkdir()
        save(folder / 'config.json', config)
        assert load_config(folder / 'config.json') == config
        validate_comparison(config, name == 'core', name == 'stop')
        assert schedule(config) == old_schedules[name]
        save(folder / 'schedule.json', schedule(config))
    ready = HERE / 'readiness'
    ready.mkdir()
    test_dir = ready / 'pytest'
    test_dir.mkdir()
    python = str(ROOT / '.venv/bin/python')
    test = capture([python, '-m', 'pytest', str(ROOT / 'experiments/test_harness.py'),
                    str(ROOT / 'reference/tests'), str(ROOT / 'baselines/ippv/test_adapter.py'), '-q'], test_dir, 180)
    if test['status'] != 'completed':
        return 1
    tiny = copy.deepcopy(config)
    tiny.update(scope='diagnostic', name='full-prefix-readiness', repeats=1)
    tiny['cases'] = []
    for name, h, k in [('triangle_and_isolate', 3, 1), ('bridged_triangles', 3, 5),
                        ('triangle_and_isolate', 5, 5)]:
        graph = f'reference/fixtures/{name}.graph'
        tiny['cases'].append({'name': f'{name}-h{h}-k{k}', 'graph': graph,
                              'sha256': sha256(ROOT / graph), 'h': h, 'k': k, 'definition': True})
    save(ready / 'config.json', tiny)
    tiny_dir = ready / 'driver'
    tiny_dir.mkdir()
    result = capture([python, str(ROOT / 'experiments/run.py'), '--config', str(ready / 'config.json'),
                      '--evidence', str(ready / 'campaign'), '--stop-on-failure',
                      '--require-prefix-agreement'], tiny_dir, 180)
    if result['status'] != 'completed':
        return 1
    summary = read(ready / 'campaign/summary.json')
    assert len(summary['runs']) == 6 and all(r['status'] == 'completed' for r in summary['runs'])
    assert len(summary['comparisons']) == 3 and all(p['prefix_match'] for p in summary['comparisons'])
    for row in summary['runs']:
        manifest = read(ready / 'campaign' / row['directory'] / 'manifest.json')
        assert manifest['validation']['level'] == 'definition_checked' and manifest['validation']['completeness_certified']
    save(ready / 'completion.json', {'passed': True, 'pytest': (test_dir / 'stdout.txt').read_text().strip(),
         'tiny_native_calls': 6, 'definition_checks_passed': 6, 'strict_prefix_pairs': 3,
         'fixture_manifest': tiny['cases'], 'benchmark_native_calls': 0,
         'config_sha256': {name: sha256(HERE / name / 'config.json') for name in specs}})
    print(json.dumps(read(ready / 'completion.json'), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
