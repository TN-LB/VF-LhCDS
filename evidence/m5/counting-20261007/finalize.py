"""Final integrity checks and changed-file inventory, without rerunning algorithms."""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config
from experiments.support import file_hashes, save, sha256


def read(path):
    return json.loads(path.read_text())


before = read(HERE / 'before.json')
for group in ('protected_sha256', 'binaries_sha256'):
    for name, digest in before[group].items():
        assert sha256(ROOT / name) == digest, name
changed_production = sorted(name for name, digest in before['production_source_sha256'].items()
                            if sha256(ROOT / name) != digest)
assert changed_production == ['CMakeLists.txt', 'include/vflhcds/clique/materialized.hpp',
                              'src/cli/dispatch.cpp', 'src/clique/materialized.cpp']
for name, digest in read(HERE / 'checks/source-sha256.json').items():
    assert sha256(ROOT / name) == digest
commands = read(HERE / 'checks/commands.json')
assert len(commands) == 25
for row in commands:
    assert row['exit_code'] == 0
    for stream in ('stdout', 'stderr'):
        assert sha256(HERE / 'checks' / row[stream]) == row[stream + '_sha256']
    if Path(row['command'][0]).name == 'ctest':
        text = (HERE / 'checks' / row['stdout']).read_text()
        assert '100% tests passed out of 16' in text and 'T04-COUNT-CLI: 217 invocations passed' in text
correct = read(HERE / 'correctness.json')
assert correct['status'] == 'passed' and correct['campaigns_passed'] == 14
assert sum(row['records'] for row in read(HERE / 'equivalence.json').values()) == correct['previous_response_records_matched'] == 1392496
verifier = read(HERE / 'verify-process/process.json')
assert verifier['native_exit_code'] == 0
for name, digest in verifier['sha256'].items(): assert sha256(HERE / 'verify-process' / name) == digest
pins = read(HERE / 'preflight.json')
for name, field in [('config.json', 'config_sha256'), ('plan.json', 'plan_sha256'),
                    ('environment.json', 'environment_sha256'), ('correctness.json', 'correctness_sha256'),
                    ('run_performance.py', 'driver_sha256')]:
    assert sha256(HERE / name) == pins[field]
assert sha256(ROOT / 'docs/DECISIONS.md') == pins['decision_log_sha256']
assert sha256(ROOT / 'experiments/run.py') == pins['runner_sha256']
config = load_config(HERE / 'config.json')
assert config == read(HERE / 'campaign/config.json')
for algorithm in config['algorithms']:
    binary = ROOT / algorithm['executable']
    assert sha256(binary) == pins['binary_sha256']
    assert sha256(binary.with_suffix('.provenance.json')) == pins['provenance_sha256']
raw = read(HERE / 'campaign/checksums.json')
for name, digest in raw.items(): assert sha256(HERE / 'campaign' / name) == digest
totals = read(HERE / 'aggregate/totals.json')
assert totals['native_statuses'] == {'completed': 12} and totals['strict_matches'] == 6
assert totals['external_validators_completed'] == totals['structural_passes'] == 12
assert totals['unrun_native_runs'] == 0 and totals['campaign_exit_code'] == 0
assert file_hashes(HERE / 'aggregate') == file_hashes(HERE / 'aggregate-replay')
assert file_hashes(HERE / 'aggregate') == read(HERE / 'regeneration.json')['identical_artifact_sha256']
for row in read(HERE / 'postprocess-commands.json'):
    assert row['exit_code'] == 0
    for stream in ('stdout', 'stderr'): assert sha256(HERE / row[stream]) == row[stream + '_sha256']
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
save(HERE / 'diff-check.json', {'command': ['git', 'diff', '--check'], 'cwd': str(ROOT),
     'exit_code': diff.returncode, 'stdout': diff.stdout, 'stderr': diff.stderr})
assert diff.returncode == 0
names = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
names += subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
excluded = {str((HERE / name).relative_to(ROOT)) for name in ('files_changed.json', 'final-checks.json')}
inventory = {name: sha256(ROOT / name) for name in sorted(set(names)) if name not in excluded}
save(HERE / 'files_changed.json', {'sha256': inventory, 'self_excluded': sorted(excluded),
     'scope': 'task files before local commit; ignored build artifacts excluded'})
save(HERE / 'final-checks.json', {'passed': True, 'production_files_changed': changed_production,
     'protected_files_unchanged': len(before['protected_sha256']), 'old_binaries_unchanged': True,
     'ctest': correct['ctest'], 'pytest': correct['pytest'], 'differential_campaigns': 14,
     'matched_old_responses': 1392496, 'native_completed': 12, 'native_unrun': 0,
     'strict_pairs': 6, 'structural_validators_passed': 12, 'raw_inventory_entries': len(raw),
     'regenerated_artifacts': len(file_hashes(HERE / 'aggregate')), 'changed_inventory_entries': len(inventory),
     'files_changed_sha256': sha256(HERE / 'files_changed.json'),
     'scope': 'one exact count optimization and bounded mode comparison; M5 remains open'})
print(json.dumps(read(HERE / 'final-checks.json'), indent=2))
