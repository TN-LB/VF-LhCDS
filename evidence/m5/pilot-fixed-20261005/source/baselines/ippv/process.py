"""Capture one native child, including its own wait4 resource usage.

Timeout is explicit. No wrapper exit is substituted for the native exit, and no
signal is guessed to be OOM. The caller owns fresh run directories and validation.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import time


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def capture(command, directory, timeout_seconds, *, environment=None):
    if timeout_seconds <= 0:
        raise ValueError('timeout_seconds must be positive')
    directory = Path(directory).resolve()
    for name in ('stdout.txt', 'stderr.txt', 'process.json'):
        if (directory / name).exists():
            raise FileExistsError(directory / name)
    manifest = {
        'command': command, 'cwd': str(directory), 'platform': platform.platform(),
        'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'timeout_seconds': timeout_seconds, 'memory_limit_bytes': None,
        'environment_overrides': environment or {},
        'executable_sha256': sha256(command[0]),
        'timing_scope': 'native process launch through wait4 completion; validation excluded',
        'rss_scope': 'native child peak RSS; no external validator or compiler included',
    }
    env = os.environ.copy()
    env.update(environment or {})
    with (directory / 'stdout.txt').open('w') as stdout, (directory / 'stderr.txt').open('w') as stderr:
        start = time.monotonic()
        proc = subprocess.Popen(command, cwd=directory, stdin=subprocess.DEVNULL,
                                stdout=stdout, stderr=stderr, env=env, start_new_session=True)
        timed_out = False
        while True:
            pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
            if pid:
                break
            if time.monotonic() - start >= timeout_seconds:
                timed_out = True
                os.killpg(proc.pid, signal.SIGKILL)
                _, status, usage = os.wait4(proc.pid, 0)
                break
            time.sleep(0.005)
        proc.returncode = os.waitstatus_to_exitcode(status)
        manifest.update(native_exit_code=proc.returncode,
                        status='timeout' if timed_out else ('completed' if proc.returncode == 0 else 'error'),
                        wall_seconds=time.monotonic() - start,
                        user_seconds=usage.ru_utime, system_seconds=usage.ru_stime,
                        peak_rss_bytes=usage.ru_maxrss if platform.system() == 'Darwin' else usage.ru_maxrss * 1024)
        if proc.returncode < 0:
            manifest['signal'] = -proc.returncode
    manifest['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest['sha256'] = {name: sha256(directory / name) for name in ('stdout.txt', 'stderr.txt')}
    (directory / 'process.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest
