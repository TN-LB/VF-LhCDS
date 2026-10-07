"""Freeze pins, then run the predeclared twelve calls through the existing harness."""
import copy
import datetime
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    assert read(HERE / 'correctness.json')['status'] == 'passed'
    assert not (HERE / 'launch.json').exists(), 'No automatic retry'
    config = read(ROOT / 'evidence/m5/core-ablation-20261006/config.json')
    config.update(name='two-graphs-clique-count-h3-k5-20261007', scope='diagnostic')
    config['cases'] = [case for case in config['cases'] if case['k'] == 5]
    binary = ROOT / 'build-m5-counting-release/vflhcds'
    base = config['algorithms'][0]
    base.update(executable=str(binary.relative_to(ROOT)), sha256=sha256(binary))
    config['algorithms'] = []
    for mode in ('sorted', 'membership'):
        algorithm = copy.deepcopy(base)
        algorithm['name'] = 'vf-count-' + mode
        algorithm['options']['counting'] = mode
        config['algorithms'].append(algorithm)
    plan = read(HERE / 'plan.json')['performance']
    assert len(config['cases']) == 2 and len(schedule(config)) * 2 == plan['native_calls']
    assert all(case['h'] == plan['h'] and case['k'] == plan['k'] for case in config['cases'])
    for name in ('seed', 'repeats', 'timeout_seconds', 'threads', 'memory_limit_bytes', 'cache_policy'):
        assert config[name] == plan[name]
    save(HERE / 'config.json', config)
    assert load_config(HERE / 'config.json') == config
    save(HERE / 'schedule.json', schedule(config))
    for name, digest in read(HERE / 'checks/source-sha256.json').items():
        assert sha256(ROOT / name) == digest
    pins = {'config_sha256': sha256(HERE / 'config.json'), 'plan_sha256': sha256(HERE / 'plan.json'),
            'binary_sha256': sha256(binary), 'provenance_sha256': sha256(binary.with_suffix('.provenance.json')),
            'decision_log_sha256': sha256(ROOT / 'docs/DECISIONS.md'),
            'environment_sha256': sha256(HERE / 'environment.json'),
            'correctness_sha256': sha256(HERE / 'correctness.json'),
            'runner_sha256': sha256(ROOT / 'experiments/run.py'), 'driver_sha256': sha256(Path(__file__))}
    save(HERE / 'preflight.json', pins)
    command = [str(ROOT / '.venv/bin/python'), str(ROOT / 'experiments/run.py'),
               '--config', str(HERE / 'config.json'), '--evidence', str(HERE / 'campaign'),
               '--stop-on-failure', '--continue-on-timeout', '--require-strict-agreement']
    save(HERE / 'launch.json', {'command': command, 'cwd': str(ROOT),
         'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'preflight_sha256': sha256(HERE / 'preflight.json')})
    started = time.monotonic()
    with (HERE / 'performance.stdout').open('w') as out, (HERE / 'performance.stderr').open('w') as err:
        process = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err)
    save(HERE / 'completion.json', {'exit_code': process.returncode, 'wall_seconds': time.monotonic() - started,
         'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'stdout_sha256': sha256(HERE / 'performance.stdout'), 'stderr_sha256': sha256(HERE / 'performance.stderr')})
    print(json.dumps(read(HERE / 'completion.json'), indent=2))
    return process.returncode


if __name__ == '__main__':
    raise SystemExit(main())
