"""Run the frozen campaign once, preserving wrapper logs separately."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config
from experiments.support import save, sha256
out = Path(__file__).resolve().parent
assert not (out / 'launch.json').exists(), 'No silent retries'
config = load_config(out / 'config.json')
assert sha256(out / 'config.json') == json.loads((out / 'approval.json').read_text())['config_sha256']
assert (out / 'environment.stderr').read_text() == ''
assert 'matches approved' in (out / 'environment.stdout').read_text()
cmd = [str(ROOT / '.venv/bin/python'), 'experiments/run.py', '--config', str((out / 'config.json').relative_to(ROOT)), '--evidence', str((out / 'campaign').relative_to(ROOT)), '--stop-on-failure']
save(out / 'launch.json', {'command': cmd, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'sha256': {str(p.relative_to(ROOT)): sha256(p) for p in [out/'config.json', out/'approval.json', out/'schedule.json', out/'preflight.json', out/'environment.json', ROOT/'docs/DECISIONS.md', out/'launch.py']}})
start = time.monotonic()
with (out / 'driver.stdout').open('w') as stdout, (out / 'driver.stderr').open('w') as stderr:
    proc = subprocess.run(cmd, cwd=ROOT, stdout=stdout, stderr=stderr)
result = {'command': cmd, 'exit_code': proc.returncode, 'wall_seconds': time.monotonic()-start, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'timing_scope': 'Entire campaign driver, including validation and evidence I/O; not algorithm timing.'}
save(out / 'completion.json', result)
print(json.dumps(result))
raise SystemExit(proc.returncode)
