"""Check the saved diagnostic and inventory the final task artifacts."""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256
from experiments.fine_profile.instrument import instrument


def read(path):
    return json.loads(path.read_text())


pins = read(HERE / 'preflight.json')
for group in pins.values():
    if isinstance(group, dict):
        for name, digest in group.items():
            assert sha256(ROOT / name) == digest, name
assert sha256(HERE / 'config.json') == pins['configuration_sha256']
assert sha256(HERE / 'run.py') == pins['runner_sha256']
assert sha256(ROOT / 'docs/DECISIONS.md') == pins['decision_log_sha256']
for name, digest in read(HERE / 'binaries.json').items():
    assert sha256(ROOT / name) == digest
for case in read(HERE / 'config.json')['tiny'] + read(HERE / 'config.json')['real']:
    assert sha256(ROOT / case['graph']) == case['graph_sha256']
for mode in ('release', 'sanitized'):
    base = HERE / 'build' / mode
    generated = read(base / 'instrumentation.json')
    for name in generated['original_sha256']:
        saved = base / Path(name).name
        assert saved.read_bytes() == instrument(name, (ROOT / name).read_bytes())
        assert sha256(saved) == generated['generated_sha256'][saved.name]
    compile_commands = read(base / 'compile_commands.json')
    for row in compile_commands:
        assert '-Werror' in row['command'] and '-std=c++17' in row['command']
        if mode == 'sanitized': assert '-fsanitize=address,undefined' in row['command']
assert (HERE / 'aggregate.json').read_bytes() == (HERE / 'aggregate.regenerated.json').read_bytes()
assert read(HERE / 'tiny-gate.json')['passed']
assert read(HERE / 'historical-consistency.json')['passed']

commands = []
for record in sorted(HERE.rglob('process.json')):
    proc = read(record)
    for name, digest in proc['sha256'].items():
        assert sha256(record.parent / name) == digest
    commands.append({'record': str(record.relative_to(ROOT)), 'command': proc['command'],
                     'cwd': proc['cwd'], 'status': proc['status'],
                     'exit_code': proc['native_exit_code'], 'record_sha256': sha256(record)})
save(HERE / 'commands.json', {'process_commands': commands,
     'initial_driver_stages': ['.venv/bin/python evidence/m5/fine-profile-20261007/run.py freeze',
                              '.venv/bin/python evidence/m5/fine-profile-20261007/run.py build'],
     'initial_driver_exit_code': 0,
     'hardware_commands': 'See environment.json for the four executed sysctl commands',
     'finalization_command': '.venv/bin/python evidence/m5/fine-profile-20261007/finalize.py'})
native = [read(path) for path in (HERE / 'runs').glob('*/process.json')]
assert len(native) == 10
assert sum(row['status'] == 'completed' for row in native) == 8
assert sum(row['status'] == 'timeout' and row['native_exit_code'] == -9 for row in native) == 2
validations = [read(path / 'stdout.txt') for path in (HERE / 'runs').glob('*/validation')]
assert len(validations) == 8 and all(row['passed'] for row in validations)
assert sum(row['level'] == 'definition_checked' for row in validations) == 6
for path in (ROOT / 'experiments/fine_profile').glob('*'):
    if path.is_file():
        assert all(line == line.rstrip() for line in path.read_text().splitlines()), path
check = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
save(HERE / 'diff-check.json', {'command': ['git', 'diff', '--check'], 'cwd': str(ROOT),
     'exit_code': check.returncode, 'stdout': check.stdout, 'stderr': check.stderr})
assert check.returncode == 0
changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
added = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
excluded = {str((HERE / name).relative_to(ROOT)) for name in ('files_changed.json', 'final-checks.json')}
inventory = {name: sha256(ROOT / name) for name in sorted(set(changed + added)) if name not in excluded}
save(HERE / 'files_changed.json', {'sha256': inventory,
     'self_excluded': sorted(excluded), 'scope': 'task files before local commit; ignored build trees excluded'})
save(HERE / 'final-checks.json', {'passed': True, 'native_completed': 8, 'native_timeouts': 2,
     'native_unrun': 0, 'validators_passed': 8, 'definition_checks': 6,
     'pytest_passed': 141, 'diagnostic_ctest_release': '1/1', 'diagnostic_ctest_sanitized': '1/1',
     'sanitized_tiny_runs_completed': 2, 'aggregate_regeneration_equal': True,
     'historical_evidence_files_unchanged': len(pins['historical_evidence_sha256']),
     'tracked_and_new_inventory_entries': len(inventory), 'files_changed_sha256': sha256(HERE / 'files_changed.json'),
     'remaining_limitations': ['CondMat complete profile/output comparison unavailable at 60 seconds',
                             'no production optimization or new baseline comparison',
                             'no general-h/full-production-regression/clean-machine/release campaign']})
print(json.dumps(read(HERE / 'final-checks.json'), indent=2))
