"""Reuse the saved-record comparator against the same frozen sorted-count corpus."""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256

spec = importlib.util.spec_from_file_location('prior_compare', ROOT / 'evidence/m5/enumeration-20261003/verify_acceptance.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def read(path):
    return json.loads(path.read_text())


checks = HERE / 'checks'
assert read(checks / 'completion.json')['status'] == 'passed'
commands = read(checks / 'commands.json')
assert len(commands) == len(read(checks / 'planned-commands.json')) == 25
for row in commands:
    assert row['exit_code'] == 0
    for stream in ('stdout', 'stderr'):
        assert sha256(checks / row[stream]) == row[stream + '_sha256']
    if Path(row['command'][0]).name == 'ctest':
        assert '100% tests passed out of 16' in (checks / row['stdout']).read_text()
for name, digest in read(checks / 'source-sha256.json').items():
    assert sha256(ROOT / name) == digest
before = read(HERE / 'before.json')
for group in ('protected_sha256', 'binaries_sha256'):
    for name, digest in before[group].items():
        assert sha256(ROOT / name) == digest, name
for profile in ('debug', 'sanitize', 'release'):
    build = ROOT / ('build-counting-' + profile)
    rows = read(build / 'compile_commands.json')
    for row in rows:
        assert '-Werror' in row['command'] and '-std=c++17' in row['command']
        if profile == 'sanitize': assert '-fsanitize=address,undefined' in row['command']
        if profile != 'release' and Path(row['file']).name in ('m2_probe.cpp', 'm3_probe.cpp'):
            assert '-DVFLHCDS_TEST_COUNT_MEMBERSHIP' in row['command']
    # Retain the actual compiler flags, not all generated build files.
    (checks / (profile + '-compile_commands.json')).write_bytes((build / 'compile_commands.json').read_bytes())
comparisons, fixtures = {}, {}
for profile in ('debug', 'sanitize'):
    for family, tiers in [('m4', ('smoke', 'exhaustive-small', 'seeded', 'higher-h')),
                          ('m2', ('exhaustive-small', 'seeded', 'higher-h'))]:
        for tier in tiers:
            name = f'{profile}-{family}-{tier}'
            current = checks / name
            previous = ROOT / 'evidence/m5/enumeration-20261003/accepted' / name
            for folder in (current, previous):
                summary = read(folder / 'summary.json')
                assert summary['status'] == 'passed' and summary['automatic_big_flows'] > 0
                assert not (folder / 'probe.stderr').read_bytes()
                for filename, digest in summary.get('sha256', summary.get('evidence_sha256')).items():
                    assert sha256(folder / filename) == digest
            assert (current / 'cases.jsonl').read_bytes() == (previous / 'cases.jsonl').read_bytes()
            filename = 'mode_results.jsonl.gz' if family == 'm4' else 'results.jsonl.gz'
            comparisons[name] = prior.compare(previous / filename, current / filename)
            fixtures[name] = read(current / 'summary.json')
            save(HERE / 'equivalence.json', comparisons)
            print('MATCH', name, comparisons[name]['records'], flush=True)
save(HERE / 'fixture-manifest.json', fixtures)
save(HERE / 'correctness.json', {'status': 'passed', 'ctest': {'Debug': '16/16', 'ASan_UBSan': '16/16', 'Release': '16/16'},
     'pytest': read(HERE / 'pytest.json')['reported_result'], 'campaigns_passed': len(comparisons),
     'previous_response_records_matched': sum(row['records'] for row in comparisons.values()),
     'exclusion': 'core_reduction_seconds only', 'automatic_big_flows_in_every_campaign': True,
     'protected_files_unchanged': len(before['protected_sha256']), 'old_binaries_unchanged': True,
     'scope': 'finite independent-reference and old/new equivalence evidence; not a theorem proof'})
print(json.dumps(read(HERE / 'correctness.json'), indent=2))
