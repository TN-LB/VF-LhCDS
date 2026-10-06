"""Save all commands for the authorized enumeration equivalence gates."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256


def main():
    output = HERE / 'accepted'
    output.mkdir(exist_ok=False)
    paths = [ROOT / 'CMakeLists.txt']
    for folder in ['src', 'include', 'cmake', 'tests', 'validation', 'experiments']:
        paths += [p for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in ('.cpp', '.hpp', '.py', '.in')]
    sources = {str(p.relative_to(ROOT)): sha256(p) for p in sorted(paths)}
    save(output / 'source-sha256.json', sources)
    for p in paths:
        target = output / 'source-snapshot' / p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    cmake, ctest, python = [str(ROOT / '.venv/bin' / name) for name in ('cmake', 'ctest', 'python')]
    commands = []
    for profile in ['debug', 'sanitize', 'release']:
        build = 'build-enumeration-' + profile
        if profile != 'debug':  # Debug configure/build/CTest already passed in dev/.
            commands += [[cmake, '-S', str(ROOT), '-B', str(ROOT / build),
                          '-DCMAKE_BUILD_TYPE=' + ('Release' if profile == 'release' else 'Debug'),
                          '-DCMAKE_CXX_FLAGS=', '-DPython3_EXECUTABLE=' + python,
                          '-DVFLHCDS_ENABLE_SANITIZERS=' + ('ON' if profile == 'sanitize' else 'OFF')],
                         [cmake, '--build', str(ROOT / build), '-j2'],
                         [ctest, '--test-dir', str(ROOT / build), '--output-on-failure', '-V']]
        if profile != 'release':
            for tier in ['smoke', 'exhaustive-small', 'seeded', 'higher-h']:
                commands.append([python, str(ROOT / 'validation/m4_campaign.py'), '--probe',
                                 str(ROOT / build / 'vflhcds_m3_probe'), '--tier', tier,
                                 '--output', str(output / (profile + '-m4-' + tier))])
            for tier in ['exhaustive-small', 'seeded', 'higher-h']:
                commands.append([python, str(ROOT / 'validation/oracle_campaign.py'), '--probe',
                                 str(ROOT / build / 'vflhcds_m2_probe'), '--tier', tier,
                                 '--output', str(output / (profile + '-m2-' + tier))])
    commands += [[python, str(ROOT / 'experiments/build_vf.py'), '--build', str(ROOT / 'build-m5-adjacency-release'),
                  '--evidence', str(output / 'production-build'), '--cmake', cmake],
                 [python, str(ROOT / 'scripts/verify_papers.py')], ['git', 'diff', '--check']]
    save(output / 'planned-commands.json', commands)
    records = []
    for i, command in enumerate(commands):
        print('RUN', i, ' '.join(command), flush=True)
        record = {'command': command, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'stdout': f'{i:02d}.stdout', 'stderr': f'{i:02d}.stderr'}
        with (output / record['stdout']).open('w') as so, (output / record['stderr']).open('w') as se:
            result = subprocess.run(command, cwd=ROOT, stdout=so, stderr=se)
        record.update(exit_code=result.returncode, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        for stream in ['stdout', 'stderr']:
            record[stream + '_sha256'] = sha256(output / record[stream])
        records.append(record)
        save(output / 'commands.json', records)
        print('EXIT', result.returncode, flush=True)
        if result.returncode:
            print((output / record['stdout']).read_text() + (output / record['stderr']).read_text(), flush=True)
            return result.returncode
    assert sources == {str(p.relative_to(ROOT)): sha256(p) for p in sorted(paths)}
    save(output / 'completion.json', {'status': 'passed', 'commands_completed': len(records),
                                     'source_unchanged_during_checks': True, 'debug_and_pytest_evidence': '../dev/commands.json'})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
