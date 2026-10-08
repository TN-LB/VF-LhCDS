"""Bootstrap new Linux dependencies, reuse recorded smoke, regenerate saved tables."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--reproduction-driver', type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.repo.resolve(), args.evidence.resolve()
    assert platform.system() == 'Linux'
    assert digest(args.bundle) == args.sha256
    assert not repo.exists() and not output.exists() and not args.build.exists()
    repo.mkdir()
    output.mkdir()
    logs = output / 'commands'
    logs.mkdir()
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': str(Path.home()), 'LANG': 'C.UTF-8'}
    save(output / 'environment.json', {'scope': 'fresh Ubuntu userspace/dependencies under shared-kernel OrbStack',
         'independent_kernel_or_hardware': False, 'new_benchmark_calls': 0,
         'os_release': Path('/etc/os-release').read_text(), 'uname': list(platform.uname()),
         'bootstrap_python': sys.version, 'script_sha256': digest(Path(__file__)),
         'reproduction_driver_sha256': digest(args.reproduction_driver),
         'base_commit': args.commit, 'bundle_sha256': args.sha256,
         'environment_passed_to_children': env, 'source_workdir': str(repo),
         'host_venv_boost_or_binaries_copied': False})
    records = []

    def run(name, command, timeout=900):
        directory = logs / name
        directory.mkdir()
        record = {'name': name, 'command': command, 'cwd': str(repo),
                  'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'timeout_seconds': timeout}
        started = time.monotonic()
        print('Running', name, flush=True)
        with (directory / 'stdout.txt').open('w') as stdout, (directory / 'stderr.txt').open('w') as stderr:
            try:
                completed = subprocess.run(command, cwd=repo, env=env, stdout=stdout, stderr=stderr, timeout=timeout)
                record['exit_code'] = completed.returncode
                record['status'] = 'completed' if completed.returncode == 0 else 'error'
            except subprocess.TimeoutExpired:
                record.update(exit_code=None, status='timeout')
        record.update(wall_seconds=time.monotonic()-started,
                      finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      stdout_sha256=digest(directory / 'stdout.txt'), stderr_sha256=digest(directory / 'stderr.txt'))
        save(directory / 'process.json', record)
        records.append(record)
        save(output / 'commands.json', records)
        if record['status'] != 'completed':
            save(output / 'completion.json', {'passed': False, 'failed_step': name, 'new_benchmark_calls': 0})
            print((directory / 'stdout.txt').read_text()[-3000:])
            print((directory / 'stderr.txt').read_text()[-3000:])
            raise SystemExit(1)

    run('source-init', ['/usr/bin/git', 'init', str(repo)])
    run('source-fetch', ['/usr/bin/git', 'fetch', str(args.bundle.resolve()), 'HEAD'])
    run('source-checkout', ['/usr/bin/git', 'checkout', '--detach', args.commit])
    shutil.copyfile(args.reproduction_driver, repo / 'scripts/reproduce_release.py')
    assert subprocess.check_output(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=repo, env=env, text=True).strip() == args.commit
    assert not (repo / '.venv').exists() and not (repo / '.deps').exists()
    run('system-packages', ['/usr/bin/dpkg-query', '-W'])
    run('venv-create', ['/usr/bin/python3', '-m', 'venv', str(repo / '.venv')])
    python = str(repo / '.venv/bin/python')
    run('python-install', [python, '-m', 'pip', 'install', 'pytest==8.4.2', 'cmake==4.4.3'])
    run('python-freeze', [python, '-m', 'pip', 'freeze', '--all'])
    run('boost-fetch', [python, str(repo / 'scripts/fetch_boost.py')])
    source = repo / '.deps/baselines/ippv'
    source.parent.mkdir()
    lock = json.loads((repo / 'baselines/ippv/source-lock.json').read_text())
    run('ippv-acquire', ['/usr/bin/git', 'clone', '--no-checkout', lock['repository'], str(source)])
    run('ippv-pin', ['/usr/bin/git', '-C', str(source), 'checkout', '--detach', lock['commit']])
    run('fresh-smoke', [python, str(repo / 'scripts/reproduce_release.py'),
                       '--build', str(args.build.resolve()), '--evidence', str(output / 'smoke')], timeout=1800)
    derived = {}
    for suite in ('main', 'core', 'stop'):
        original = repo / 'evidence/m5' / ('final-main-repaired-20261008' if suite == 'main' else 'final-evaluation-20261008')
        target = output / 'aggregate' / suite
        command = ([python, str(original / 'postprocess.py'), '--aggregate', str(target)] if suite == 'main' else
                   [python, str(original / 'summarize.py'), '--suite', suite, '--output', str(target)])
        run('aggregate-' + suite, command)
        expected = {p.name: digest(p) for p in (original / 'aggregate' / suite).iterdir() if p.is_file()}
        actual = {p.name: digest(p) for p in target.iterdir() if p.is_file()}
        assert actual == expected, suite
        derived[suite] = actual
    original = repo / 'evidence/m5/final-main-repaired-20261008'
    run('descriptive-review', [python, str(original / 'review.py'), '--output', str(output / 'review')])
    expected = {p.name: digest(p) for p in (original / 'review').iterdir() if p.is_file()}
    actual = {p.name: digest(p) for p in (output / 'review').iterdir() if p.is_file()}
    assert actual == expected
    derived['review'] = actual
    save(output / 'regeneration.json', {'passed': True, 'identical_artifacts': derived,
         'total_artifacts': sum(map(len, derived.values())), 'native_benchmark_reruns': 0})
    save(output / 'completion.json', {'passed': True, 'steps_completed': len(records),
         'clean_userspace_installation': True, 'independent_kernel_or_hardware': False,
         'fresh_smoke_manifest': 'smoke/completion.json',
         'regenerated_artifacts': sum(map(len, derived.values())), 'new_benchmark_calls': 0})
    print('Clean userspace checks and saved table regeneration complete.', flush=True)


if __name__ == '__main__':
    main()
