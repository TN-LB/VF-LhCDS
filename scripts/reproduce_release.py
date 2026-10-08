"""Rebuild the frozen release with the selected virtualenv interpreter intact."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "evidence/m5/reproduction-20261008"
sys.path.insert(0, str(ROOT))
from experiments.support import capture, save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    args = parser.parse_args()
    HERE = args.evidence.resolve()
    measured = PACKAGE.parent / 'final-main-repaired-20261008'
    assert read(measured / 'main/completion.json')['exit_code'] == 0, 'wait for measurement completion'
    build = args.build.resolve()
    assert not HERE.exists(), 'use a fresh evidence directory'
    assert not build.exists(), 'use a fresh local build directory'
    build.mkdir()
    HERE.mkdir(parents=True)
    logs = HERE / 'commands'
    logs.mkdir()
    python, cmake, ctest = [str(ROOT / '.venv/bin' / n) for n in ('python', 'cmake', 'ctest')]
    production = read(PACKAGE.parent / 'counting-20261007/checks/production-build/provenance.json')['source_sha256']
    for name, digest in production.items():
        assert sha256(ROOT / name) == digest
    lock = read(ROOT / 'baselines/ippv/source-lock.json')
    patch_paths = [str(ROOT / p['path']) for p in lock['patches']]
    source = build / 'ippv-source'
    vf, ippv = build / 'vf', build / 'ippv'
    commands = [
        ('papers', [python, 'scripts/verify_papers.py']),
        ('cmake-version', [cmake, '--version']),
        ('compiler-version', ['c++', '--version']),
        ('pytest-version', [python, '-m', 'pytest', '--version']),
        ('vf-configure', [cmake, '-S', str(ROOT), '-B', str(vf), '-DCMAKE_BUILD_TYPE=Release',
                          '-DBUILD_TESTING=ON', '-DVFLHCDS_TEST_COUNT_MEMBERSHIP=ON',
                          '-DVFLHCDS_ENABLE_SANITIZERS=OFF', '-DCMAKE_CXX_FLAGS=',
                          '-DPython3_EXECUTABLE='+python]),
        ('vf-build', [cmake, '--build', str(vf), '-j2']),
        ('vf-ctest', [ctest, '--test-dir', str(vf), '--output-on-failure']),
        ('python-tests', [python, '-m', 'pytest', 'reference/tests', 'experiments/test_harness.py',
                           'baselines/ippv/test_adapter.py', '-q']),
        ('ippv-local-clone', ['git', 'clone', '--no-hardlinks', '--no-checkout',
                              str(ROOT / '.deps/baselines/ippv'), str(source)]),
        ('ippv-checkout', ['git', '-C', str(source), 'checkout', '--detach', lock['commit']]),
    ]
    commands += [(f'ippv-patch-{i:02d}', ['git', '-C', str(source), 'apply', patch])
                 for i, patch in enumerate(patch_paths, 1)]
    commands += [
        ('ippv-build', [python, 'baselines/ippv/build.py', '--source', str(source), '--build', str(ippv),
                        '--evidence', str(HERE / 'ippv-build'), '--cmake', cmake,
                        '--boost', str(ROOT / '.deps/boost_1_86_0')]),
        ('ippv-fractional', [python, 'baselines/ippv/check_fractional.py', '--binary', str(ippv / 'IPPV'),
                             '--evidence', str(HERE / 'ippv-fractional')]),
        ('ippv-equality', [python, 'baselines/ippv/check_equality.py', '--binary', str(ippv / 'IPPV'),
                           '--evidence', str(HERE / 'ippv-equality')]),
        ('ippv-bridge', [python, 'baselines/ippv/adapter.py', 'run', '--executable', str(ippv / 'IPPV'),
                         '--graph', 'reference/fixtures/bridged_triangles.graph', '--h', '3', '--k', '1',
                         '--iterations', '10', '--timeout', '60', '--definition',
                         '--evidence', str(HERE / 'ippv-bridge')]),
        ('vf-definition', [python, 'validation/run_solver.py', '--executable', str(vf / 'vflhcds'),
                            '--evidence', str(HERE / 'vf-definition'), '--check-reference', '--', 'solve',
                            '--graph', 'reference/fixtures/triangle_and_isolate.graph', '--h', '3', '--all',
                            '--clique-enumeration', 'adjacency', '--footprint-scan', 'membership',
                            '--clique-count', 'membership', '--core-reduction', 'off']),
    ]
    # The shared capture function runs in each log directory, not the repository.
    # Make executables absolute without following interpreter symlinks: resolving
    # .venv/bin/python would bypass pyvenv.cfg and accidentally select system Python.
    commands = [(name, [str(Path(shutil.which(command[0]) or command[0]).absolute()),
                        *[str(ROOT / arg) if not Path(arg).is_absolute() and (ROOT / arg).exists() else arg
                          for arg in command[1:]]]) for name, command in commands]
    save(HERE / 'plan.json', {'scope': 'fresh local build/source directories on the same host; existing Python/Boost and local Git object source reused',
         'clean_machine': False, 'new_benchmark_measurements': 0,
         'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
         'platform': platform.platform(), 'python': sys.version, 'driver_sha256': sha256(Path(__file__)),
         'production_source_sha256': production, 'ippv_lock_sha256': sha256(ROOT / 'baselines/ippv/source-lock.json'),
         'commands': [{'name': name, 'command': command} for name, command in commands]})
    records = []
    for name, command in commands:
        folder = logs / name
        folder.mkdir()
        print('Running', name, flush=True)
        result = capture(command, folder, 900)
        records.append({'name': name, 'process': str((folder / 'process.json').relative_to(HERE)),
                        'exit_code': result['native_exit_code'], 'status': result['status']})
        save(HERE / 'commands.json', records)
        if result['status'] != 'completed':
            print((folder / 'stdout.txt').read_text() + (folder / 'stderr.txt').read_text())
            save(HERE / 'completion.json', {'passed': False, 'failed_command': name, 'clean_machine': False})
            return 1
    for name, digest in production.items():
        assert sha256(ROOT / name) == digest
    for name, digest in lock['patched_source_sha256'].items():
        assert sha256(source / name) == digest
    (HERE / 'vf-compile-commands.json').write_bytes((vf / 'compile_commands.json').read_bytes())
    save(HERE / 'completion.json', {'passed': True, 'commands_completed': len(records),
         'clean_machine': False, 'new_benchmark_measurements': 0,
         'all_eight_patches_applied_to_fresh_local_checkout': True,
         'production_source_unchanged': True, 'vf_executable_sha256': sha256(vf / 'vflhcds'),
         'ippv_executable_sha256': sha256(ippv / 'IPPV')})
    print('Fresh local smoke completed; clean-machine gate remains open.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
