"""D041: fresh paired main suite after the independently validated B09 repair."""
import datetime
import json
from pathlib import Path
import signal
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
    assert not (HERE / 'launch.json').exists(), 'no automatic retries'
    previous = ROOT / 'evidence/m5/final-evaluation-20261008'
    repair = ROOT / 'evidence/m5/ippv/equality-20261008'
    assert read(repair / 'completion.json')['passed']
    for path, digest in read(previous / 'readiness/final-tests.json')['source_sha256'].items():
        assert sha256(ROOT / path) == digest
    config = read(previous / 'main/config.json')
    config['name'] = 'final-local-main-eight-patches-20261008'
    baseline = config['algorithms'][1]
    assert baseline['kind'] == 'ippv'
    baseline.update(name='ippv-eight-patches', executable='build-ippv-equality-release/IPPV',
                    sha256=sha256(ROOT / 'build-ippv-equality-release/IPPV'))
    folder = HERE / 'main'
    folder.mkdir()
    save(folder / 'config.json', config)
    assert load_config(folder / 'config.json') == config
    assert schedule(config) == read(previous / 'main/schedule.json')
    assert len(schedule(config))*2 == 240 and config['repeats'] == 5
    save(folder / 'schedule.json', schedule(config))
    environment = snapshot()
    assert power_change(read(previous / 'environment-baseline.json'), environment) is None
    save(HERE / 'environment-baseline.json', environment)
    hardware = {name: probe(['/usr/sbin/sysctl', '-n', name]) for name in
                ('machdep.cpu.brand_string', 'hw.memsize', 'hw.logicalcpu')}
    assert [hardware[n]['stdout'].strip() for n in hardware] == ['Apple M1', '17179869184', '8']
    save(HERE / 'hardware.json', hardware)
    scripts = list((ROOT / 'experiments').glob('*.py')) + list((ROOT / 'baselines/ippv').glob('*.py'))
    save(HERE / 'preflight.json', {'script_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted(scripts)},
         'driver_sha256': sha256(Path(__file__)), 'config_sha256': sha256(folder / 'config.json'),
         'schedule_sha256': sha256(folder / 'schedule.json'), 'repair_checks_sha256': sha256(repair / 'completion.json'),
         'decision_log_sha256': sha256(ROOT / 'docs/DECISIONS.md'),
         'environment_sha256': sha256(HERE / 'environment-baseline.json'), 'hardware_sha256': sha256(HERE / 'hardware.json'),
         'older_measurements_used': False, 'retained_vf_ablations': str(previous.relative_to(ROOT))})
    command = [str(ROOT / '.venv/bin/python'), str(ROOT / 'experiments/run.py'),
               '--config', str(folder / 'config.json'), '--evidence', str(folder / 'campaign'),
               '--stop-on-failure', '--continue-on-timeout', '--environment-baseline', str(HERE / 'environment-baseline.json')]
    save(HERE / 'launch.json', {'command': command, 'cwd': str(ROOT),
         'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'preflight_sha256': sha256(HERE / 'preflight.json'), 'planned_native_calls': 240})
    start = time.monotonic()
    active = {'process': None, 'interrupted': False}
    def interrupt(signum, frame):
        active['interrupted'] = True
        if active['process'] is not None and active['process'].poll() is None:
            active['process'].send_signal(signum)
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    with (folder / 'driver.stdout').open('w') as out, (folder / 'driver.stderr').open('w') as err:
        process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err)
        active['process'] = process
        if active['interrupted']: process.send_signal(signal.SIGINT)
        process.wait()
    result = {'exit_code': process.returncode, 'wall_seconds': time.monotonic()-start,
              'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'stdout_sha256': sha256(folder / 'driver.stdout'), 'stderr_sha256': sha256(folder / 'driver.stderr')}
    save(folder / 'completion.json', result)
    print(json.dumps(result, indent=2))
    return process.returncode


if __name__ == '__main__':
    raise SystemExit(main())
