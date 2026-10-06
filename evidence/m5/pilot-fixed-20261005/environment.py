"""Read current hardware and execution environment; launch no benchmark."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
out = Path(__file__).resolve().parent
hardware = {}
for key in ('machdep.cpu.brand_string', 'hw.memsize', 'hw.physicalcpu', 'hw.logicalcpu'):
    cmd = ['sysctl', '-n', key]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    hardware[key] = {'command': cmd, 'exit_code': proc.returncode, 'stdout': proc.stdout.strip(), 'stderr': proc.stderr.strip()}
env = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'platform': platform.platform(), 'python': sys.version, 'host_id_sha256': hashlib.sha256(platform.node().encode()).hexdigest(), 'hardware': hardware, 'environment': {k: os.environ.get(k) for k in ('CC', 'CXX', 'CXXFLAGS', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'ASAN_OPTIONS', 'UBSAN_OPTIONS')}}
(out / 'environment.json').write_text(json.dumps(env, indent=2) + '\n')
prior = json.loads((out.parent / 'pilot-20261005/environment.json').read_text())
assert env['platform'] == prior['platform']
assert env['host_id_sha256'] == prior['host_id_sha256']
assert env['environment'] == prior['environment']
assert hardware == prior['hardware'], hardware
print('Current hardware/environment matches approved D030 profile.')
