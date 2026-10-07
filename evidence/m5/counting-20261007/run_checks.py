"""Reuse the established correctness tiers; save actual commands and failures."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256


def main():
    output = HERE / 'checks'
    output.mkdir(exist_ok=False)
    paths = [ROOT / 'CMakeLists.txt', ROOT / 'pyproject.toml']
    paths += [p for folder in ('src', 'include', 'cmake', 'tests', 'validation', 'experiments')
              for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in ('.cpp', '.hpp', '.py', '.in')]
    sources = {str(p.relative_to(ROOT)): sha256(p) for p in sorted(paths)}
    save(output / 'source-sha256.json', sources)
    cmake, ctest, python = [str(ROOT / '.venv/bin' / name) for name in ('cmake', 'ctest', 'python')]
    commands = []
    for profile in ('debug', 'sanitize', 'release'):
        build = ROOT / ('build-counting-' + profile)
        commands += [[cmake, '-S', str(ROOT), '-B', str(build),
                      '-DCMAKE_BUILD_TYPE=' + ('Release' if profile == 'release' else 'Debug'),
                      '-DCMAKE_CXX_FLAGS=', '-DPython3_EXECUTABLE=' + python,
                      '-DVFLHCDS_ENABLE_SANITIZERS=' + ('ON' if profile == 'sanitize' else 'OFF'),
                      '-DVFLHCDS_TEST_COUNT_MEMBERSHIP=' + ('OFF' if profile == 'release' else 'ON')],
                     [cmake, '--build', str(build), '-j2'],
                     [ctest, '--test-dir', str(build), '--output-on-failure', '-V']]
        if profile != 'release':
            for family, script, probe, tiers in (
                    ('m4', 'm4_campaign.py', 'vflhcds_m3_probe', ('smoke', 'exhaustive-small', 'seeded', 'higher-h')),
                    ('m2', 'oracle_campaign.py', 'vflhcds_m2_probe', ('exhaustive-small', 'seeded', 'higher-h'))):
                for tier in tiers:
                    commands.append([python, str(ROOT / 'validation' / script), '--probe', str(build / probe),
                                     '--tier', tier, '--output', str(output / f'{profile}-{family}-{tier}')])
    commands.append([python, str(ROOT / 'experiments/build_vf.py'), '--build', str(ROOT / 'build-m5-counting-release'),
                     '--evidence', str(output / 'production-build'), '--cmake', cmake])
    commands.append([python, str(ROOT / 'scripts/verify_papers.py')])
    save(output / 'planned-commands.json', commands)
    records = []
    for i, command in enumerate(commands):
        print('RUN', i, ' '.join(command), flush=True)
        row = {'command': command, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'stdout': f'{i:02d}.stdout', 'stderr': f'{i:02d}.stderr'}
        with (output / row['stdout']).open('w') as stdout, (output / row['stderr']).open('w') as stderr:
            process = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr)
        row.update(exit_code=process.returncode, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        for stream in ('stdout', 'stderr'):
            row[stream + '_sha256'] = sha256(output / row[stream])
        records.append(row)
        save(output / 'commands.json', records)
        print('EXIT', process.returncode, flush=True)
        if process.returncode:
            print((output / row['stdout']).read_text() + (output / row['stderr']).read_text(), flush=True)
            return process.returncode
    assert sources == {str(p.relative_to(ROOT)): sha256(p) for p in sorted(paths)}
    save(output / 'completion.json', {'status': 'passed', 'commands_completed': len(records), 'source_unchanged': True})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
