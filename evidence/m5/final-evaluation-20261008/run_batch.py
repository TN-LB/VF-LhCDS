"""Freeze D040 pins/environment then execute the three fixed serial suites once."""
import datetime
import json
import signal
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.environment import snapshot, power_change, probe
from experiments.run import load_config, schedule
from experiments.support import save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    assert not (HERE / 'launch.json').exists(), 'no automatic retry'
    ready = read(HERE / 'readiness/completion.json')
    assert ready['passed']
    tests = read(HERE / 'readiness/final-tests.json')
    assert tests['passed']
    for name, digest in tests['source_sha256'].items(): assert sha256(ROOT / name) == digest
    configs = {name: load_config(HERE / name / 'config.json') for name in ('main', 'core', 'stop')}
    for name, config in configs.items():
        assert sha256(HERE / name / 'config.json') == ready['config_sha256'][name]
        assert schedule(config) == read(HERE / name / 'schedule.json')
    assert [len(schedule(c)) * 2 for c in configs.values()] == [240, 60, 60]
    paper_pins = read(ROOT / 'review/source_snapshot_sha256.json')['sha256']
    for name, digest in paper_pins.items():
        assert sha256(ROOT / name) == digest
    baseline = snapshot()
    if power_change(baseline, baseline) is not None:
        save(HERE / 'environment-preflight-failure.json', baseline)
        return 1
    save(HERE / 'environment-baseline.json', baseline)
    hardware = {name: probe(['/usr/sbin/sysctl', '-n', name]) for name in
                ('machdep.cpu.brand_string', 'hw.memsize', 'hw.logicalcpu')}
    assert hardware['machdep.cpu.brand_string']['stdout'].strip() == 'Apple M1'
    assert hardware['hw.memsize']['stdout'].strip() == '17179869184'
    assert hardware['hw.logicalcpu']['stdout'].strip() == '8'
    save(HERE / 'hardware.json', hardware)
    scripts = list((ROOT / 'experiments').glob('*.py')) + list((ROOT / 'baselines/ippv').glob('*.py'))
    pins = {'script_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted(scripts)},
            'driver_sha256': sha256(Path(__file__)), 'papers_sha256': paper_pins,
            'decision_log_sha256': sha256(ROOT / 'docs/DECISIONS.md'),
            'baseline_sha256': sha256(HERE / 'environment-baseline.json'),
            'hardware_sha256': sha256(HERE / 'hardware.json'),
            'readiness_sha256': sha256(HERE / 'readiness/completion.json'),
            'final_tests_sha256': sha256(HERE / 'readiness/final-tests.json'),
            'configs_sha256': ready['config_sha256'],
            'schedules_sha256': {name: sha256(HERE / name / 'schedule.json') for name in configs}}
    save(HERE / 'preflight.json', pins)
    commands = {}
    for name in configs:
        commands[name] = [str(ROOT / '.venv/bin/python'), str(ROOT / 'experiments/run.py'),
                          '--config', str(HERE / name / 'config.json'), '--evidence', str(HERE / name / 'campaign'),
                          '--stop-on-failure', '--continue-on-timeout',
                          '--environment-baseline', str(HERE / 'environment-baseline.json')]
        if name == 'core': commands[name].append('--require-strict-agreement')
        if name == 'stop': commands[name].append('--require-prefix-agreement')
    save(HERE / 'launch.json', {'commands': commands, 'suite_order': list(configs),
         'cwd': str(ROOT), 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'preflight_sha256': sha256(HERE / 'preflight.json'),
         'policy': 'continue native timeouts; no retries; stop affected suite on other failures; power change stops batch'})
    completed = []
    active = {'process': None, 'interrupted': False}
    def request_stop(signum, frame):
        active['interrupted'] = True
        if active['process'] is not None and active['process'].poll() is None:
            active['process'].send_signal(signum)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    for name, command in commands.items():
        if active['interrupted']:
            break
        for path, digest in pins['script_sha256'].items(): assert sha256(ROOT / path) == digest
        folder = HERE / name
        print('START', name, flush=True)
        started = time.monotonic()
        with (folder / 'driver.stdout').open('w') as out, (folder / 'driver.stderr').open('w') as err:
            process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err)
            active['process'] = process
            process.wait()
            active['process'] = None
        result = {'exit_code': process.returncode, 'wall_seconds': time.monotonic() - started,
                  'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'stdout_sha256': sha256(folder / 'driver.stdout'), 'stderr_sha256': sha256(folder / 'driver.stderr')}
        save(folder / 'completion.json', result)
        completed.append(name)
        print('FINISH', name, json.dumps(result), flush=True)
        stopped = folder / 'campaign/stopped.json'
        if not (folder / 'campaign/checksums.json').exists() or (stopped.exists() and
                read(stopped)['reason']['kind'] in ('power_condition_changed', 'power_observation_unavailable', 'baseline_not_ac_power', 'external_interruption')):
            break
    save(HERE / 'completion.json', {'completed_suites': completed,
         'unlaunched_suites': [name for name in commands if name not in completed],
         'scope': 'suite completion does not imply every native call succeeded; see per-suite ledgers'})
    return 0 if len(completed) == 3 and all(read(HERE / name / 'completion.json')['exit_code'] == 0 for name in completed) else 1


if __name__ == '__main__':
    raise SystemExit(main())
