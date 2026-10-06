"""Verify saved phase evidence and preservation, without launching algorithms."""
import json
from pathlib import Path
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import file_hashes, save, sha256


def load(path):
    return json.loads(path.read_text())


def main():
    accepted = HERE / 'accepted'
    inventory = load(accepted / 'checksums.json')
    assert set(file_hashes(accepted)) == set(inventory) | {'checksums.json'}
    for name, digest in inventory.items():
        assert sha256(accepted / name) == digest, name
    before = load(accepted / 'preservation-start.json')
    assert load(accepted / 'preservation-final.json')['sha256'] == before
    for name, digest in before.items():
        assert sha256(ROOT / name) == digest, name
    environment = load(accepted / 'environment.json')
    for name, digest in environment['source_sha256'].items():
        assert sha256(ROOT / name) == digest
        assert sha256(accepted / 'source-snapshot' / name) == digest
    config = load(accepted / 'config.json')
    assert config['timeout_seconds'] == 60 and config['real_repeats'] == 1
    assert environment['configuration_sha256'] == sha256(accepted / 'config.json')
    assert all(r['exit_code'] == 0 for r in load(accepted / 'build-commands.json'))
    compile_rows = load(accepted / 'compile_commands.json')
    assert len(compile_rows) == 1
    flags = shlex.split(compile_rows[0]['command'])
    assert all(f in flags for f in ['-O3', '-DNDEBUG', '-std=c++17', '-Wall', '-Wextra',
                                   '-Wpedantic', '-Wconversion', '-Wsign-conversion', '-Wshadow', '-Werror'])
    provenance = load(accepted / 'probe-provenance.json')
    assert sha256(Path(provenance['executable'])) == provenance['executable_sha256']
    assert sha256(Path(provenance['library'])) == provenance['library_sha256']
    assert provenance['library'] in (accepted / 'link.txt').read_text()
    smoke = load(accepted / 'smoke-results.json')
    assert len(smoke) == 2
    expected = [(p, e) for p in ['parse', 'index', 'solve', 'serialize'] for e in ['begin', 'end']]
    for row in smoke:
        assert row['status'] == 'passed' and row['definition_validation']['passed']
        directory = accepted / 'smoke' / row['id'].split('/')[1]
        events = [json.loads(line) for line in (directory / 'probe/stderr.txt').read_text().splitlines()]
        assert [(e['phase'], e['event']) for e in events] == expected
        assert all(a['elapsed_seconds'] <= b['elapsed_seconds'] for a, b in zip(events, events[1:]))
        assert (directory / 'probe/stdout.txt').read_bytes() == (directory / 'production/stdout.txt').read_bytes()
        assert all(row[name]['native_exit_code'] == 0 for name in
                   ['probe_process', 'production_process', 'external_validation_process'])
    real = load(accepted / 'real-result.json')
    assert real['process'] == load(accepted / 'real/process.json')
    assert real['native_status'] == 'timeout' and real['process']['native_exit_code'] == -9
    assert real['incomplete_phase'] == 'index'
    assert [(e['phase'], e['event']) for e in real['events']] == expected[:3]
    assert not (accepted / 'real/stdout.txt').read_bytes()
    assert real['external_validation'] == 'not_run'
    assert sha256(accepted / 'real/graph.txt') == config['real_case']['sha256']
    assert load(HERE / 'command.json')['exit_code'] == 1
    assert not (HERE / 'driver.stderr').read_bytes()
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    result = {'status': 'passed', 'scope': 'diagnostic and record-integrity assertions only',
              'configure_and_build_exit_codes': [0, 0], 'smoke_tests_passed': 2,
              'smoke_native_processes_completed': 4, 'external_definition_validators_completed': 2,
              'real_native_status': 'timeout', 'real_incomplete_phase': 'index',
              'real_solve_phase_reached': False,
              'parse_seconds': real['events'][1]['elapsed_seconds'] - real['events'][0]['elapsed_seconds'],
              'real_process': real['process'], 'm4_source_files_unchanged': 53, 'papers_unchanged': 4,
              'production_binary_and_library_unchanged': True, 'git_diff_check': 0,
              'full_correctness_suites_rerun': False, 'production_optimization_implemented': False}
    save(HERE / 'verification.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
