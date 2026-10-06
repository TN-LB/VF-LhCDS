"""Build the exact pinned, patched IPPV tree; no implicit fetch or source edits."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--cmake', type=Path, required=True)
    parser.add_argument('--boost', type=Path, required=True)
    parser.add_argument('--sanitizers', action='store_true')
    args = parser.parse_args()
    source, build, output = args.source.resolve(), args.build.resolve(), args.evidence.resolve()
    lock = json.loads((Path(__file__).parent / 'source-lock.json').read_text())
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != lock['commit']:
        raise ValueError('upstream commit does not match pin')
    for name, expected in lock['patched_source_sha256'].items():
        if digest(source / name) != expected:
            raise ValueError('unexpected baseline source bytes: ' + name)
    for patch in lock['patches']:
        if digest(ROOT / patch['path']) != patch['sha256']:
            raise ValueError('patch checksum mismatch')
    if '#define BOOST_VERSION 108600' not in (args.boost / 'boost/version.hpp').read_text():
        raise ValueError('requires the recorded Boost 1.86.0 headers')
    output.mkdir(parents=True, exist_ok=False)
    flags = '-I' + str(args.boost.resolve())
    if args.sanitizers:
        flags += ' -g -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer'
        if platform.system() == 'Darwin':
            flags += ' -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG'
    env = os.environ.copy()
    env['CXXFLAGS'] = flags
    commands = [
        # CXXFLAGS only initializes a fresh CMake cache. Set the cached value too,
        # so changing profiles in an existing build cannot silently retain it.
        [str(args.cmake.resolve()), '-S', str(source), '-B', str(build),
         '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON', '-DCMAKE_CXX_FLAGS=' + flags],
        [str(args.cmake.resolve()), '--build', str(build), '-j2'],
    ]
    logs = []
    for i, command in enumerate(commands, 1):
        record = {'command': command, 'cwd': str(ROOT), 'environment_overrides': {'CXXFLAGS': flags},
                  'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'stdout': f'{i:02d}.stdout', 'stderr': f'{i:02d}.stderr'}
        with (output / record['stdout']).open('w') as stdout, (output / record['stderr']).open('w') as stderr:
            completed = subprocess.run(command, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
        record.update(exit_code=completed.returncode, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        for field in ('stdout', 'stderr'):
            record[field + '_sha256'] = digest(output / record[field])
        logs.append(record)
        (output / 'commands.json').write_text(json.dumps(logs, indent=2) + '\n')
        if completed.returncode:
            raise SystemExit(completed.returncode)
    compile_commands = build / 'compile_commands.json'
    (output / 'compile_commands.json').write_bytes(compile_commands.read_bytes())
    provenance = dict(lock, executable_sha256=digest(build / 'IPPV'),
                      sanitizers=args.sanitizers, environment=platform.platform(),
                      commands_manifest=str(output / 'commands.json'), commands_manifest_sha256=digest(output / 'commands.json'),
                      compile_commands_sha256=digest(compile_commands),
                      build_script_sha256=digest(Path(__file__)))
    (output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    (build / 'IPPV.provenance.json').write_bytes((output / 'provenance.json').read_bytes())
    print(json.dumps({'status': 'built', 'binary': str(build / 'IPPV'), 'sanitizers': args.sanitizers}))


if __name__ == '__main__':
    main()
