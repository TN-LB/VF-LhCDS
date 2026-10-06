"""Build a Release VF binary and retain source/compiler/binary provenance."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.support import ROOT, save, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--cmake', type=Path, required=True)
    args = parser.parse_args()
    build, output = args.build.resolve(), args.evidence.resolve()
    output.mkdir(parents=True, exist_ok=False)
    sources = [ROOT / 'CMakeLists.txt']
    sources += [p for d in ('include', 'src', 'cmake') for p in sorted((ROOT / d).rglob('*')) if p.is_file()]
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    commands = [[str(args.cmake.resolve()), '-S', str(ROOT), '-B', str(build),
                 '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_TESTING=OFF', '-DVFLHCDS_ENABLE_SANITIZERS=OFF', '-DCMAKE_CXX_FLAGS='],
                [str(args.cmake.resolve()), '--build', str(build), '-j2']]
    records = []
    for i, command in enumerate(commands):
        record = {'command': command, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'stdout': f'{i}.stdout', 'stderr': f'{i}.stderr'}
        with (output / record['stdout']).open('w') as so, (output / record['stderr']).open('w') as se:
            result = subprocess.run(command, cwd=ROOT, stdout=so, stderr=se)
        record['exit_code'] = result.returncode
        for stream in ('stdout', 'stderr'):
            record[stream + '_sha256'] = sha256(output / record[stream])
        records.append(record)
        save(output / 'commands.json', records)
        if result.returncode:
            return result.returncode
    if hashes != {str(p.relative_to(ROOT)): sha256(p) for p in sources}:
        raise RuntimeError('source changed during build')
    binary = build / 'vflhcds'
    info = subprocess.run([str(binary), 'print-build-info'], capture_output=True, text=True, check=True)
    (output / 'build-info.stdout').write_text(info.stdout)
    (output / 'compile_commands.json').write_bytes((build / 'compile_commands.json').read_bytes())
    save(output / 'provenance.json', {
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'dirty_tree': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'source_sha256': hashes, 'executable_sha256': sha256(binary),
        'build_info_text': info.stdout, 'build_script_sha256': sha256(Path(__file__)),
        'commands_manifest': str(output / 'commands.json'), 'commands_manifest_sha256': sha256(output / 'commands.json'),
        'compile_commands_sha256': sha256(output / 'compile_commands.json')})
    binary.with_suffix('.provenance.json').write_bytes((output / 'provenance.json').read_bytes())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
