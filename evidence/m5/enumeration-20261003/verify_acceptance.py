"""Check executed gates, preservation and full saved response equivalence."""
import gzip
import hashlib
from itertools import zip_longest
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256


def load(path):
    return json.loads(path.read_text())


def strip_time(value):
    if isinstance(value, dict):
        return {k: strip_time(v) for k, v in value.items() if k != 'core_reduction_seconds'}
    if isinstance(value, list):
        return [strip_time(v) for v in value]
    return value


def compare(left, right):
    digest, count = hashlib.sha256(), 0
    with gzip.open(left, 'rt') as a, gzip.open(right, 'rt') as b:
        for count, (x, y) in enumerate(zip_longest(a, b), 1):
            assert x is not None and y is not None, (left, right, count)
            x, y = strip_time(json.loads(x)), strip_time(json.loads(y))
            assert x == y, (left, right, count)
            digest.update((json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n').encode())
    return {'records': count, 'semantic_sha256': digest.hexdigest()}


def main():
    accepted = HERE / 'accepted'
    assert load(accepted / 'completion.json')['status'] == 'passed'
    before = load(HERE / 'before.json')
    for name, digest in before['protected_sha256'].items():
        assert sha256(ROOT / name) == digest, name
    changed = [name for name, digest in before['m4_source_sha256'].items() if sha256(ROOT / name) != digest]
    assert set(changed) == {'CMakeLists.txt', 'include/vflhcds/clique/materialized.hpp',
                            'src/clique/materialized.cpp', 'src/cli/dispatch.cpp',
                            'tests/m2_probe.cpp', 'tests/m3_probe.cpp'}
    sources = load(accepted / 'source-sha256.json')
    for name, digest in sources.items():
        assert sha256(ROOT / name) == digest, name
        assert sha256(accepted / 'source-snapshot' / name) == digest, name
    commands = load(accepted / 'commands.json')
    assert len(commands) == len(load(accepted / 'planned-commands.json')) == 23
    for row in commands:
        assert row['exit_code'] == 0, row
        for stream in ['stdout', 'stderr']:
            assert sha256(accepted / row[stream]) == row[stream + '_sha256']
    dev = HERE / 'dev'
    assert len(load(dev / 'commands.json')) == 4
    assert all(r['exit_code'] == 0 for r in load(dev / 'commands.json'))
    assert '100% tests passed out of 14' in (dev / '2.stdout').read_text()
    assert '115 passed' in (dev / '3.stdout').read_text()
    for row in commands:
        if Path(row['command'][0]).name == 'ctest':
            assert '100% tests passed out of 14' in (accepted / row['stdout']).read_text()
    flags = ['-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wsign-conversion', '-Wshadow', '-Werror', '-std=c++17']
    for build in ['build-enumeration-debug', 'build-enumeration-sanitize', 'build-enumeration-release', 'build-m5-adjacency-release']:
        for row in load(ROOT / build / 'compile_commands.json'):
            assert all(flag in row['command'].split() for flag in flags)
            if build.endswith('sanitize'):
                assert all(flag in row['command'].split() for flag in ['-fsanitize=address,undefined', '-fno-sanitize-recover=all', '-fno-omit-frame-pointer'])
            if build == 'build-m5-adjacency-release':
                assert '/tests/' not in row['file']
    campaigns, comparisons = {}, {}
    old_root = ROOT / 'evidence/m4/accepted'
    for profile in ['debug', 'sanitize']:
        for family, tiers in [('m4', ['smoke', 'exhaustive-small', 'seeded', 'higher-h']),
                              ('m2', ['exhaustive-small', 'seeded', 'higher-h'])]:
            for tier in tiers:
                name = f'{profile}-{family}-{tier}'
                current = accepted / name
                previous = old_root / (('build' if profile == 'debug' else 'build-sanitize') + '-' + ('' if family == 'm4' else 'm2-') + tier)
                summary = load(current / 'summary.json')
                assert summary['status'] == 'passed' and not (current / 'probe.stderr').read_bytes()
                assert summary['automatic_big_flows'] > 0
                for path in [current, previous]:
                    record = load(path / 'summary.json')
                    for filename, digest in record.get('sha256', record.get('evidence_sha256')).items():
                        assert sha256(path / filename) == digest
                assert (current / 'cases.jsonl').read_bytes() == (previous / 'cases.jsonl').read_bytes()
                filename = 'mode_results.jsonl.gz' if family == 'm4' else 'results.jsonl.gz'
                comparisons[name] = compare(previous / filename, current / filename)
                campaigns[name] = summary
                save(HERE / 'cross-version-comparisons.json', comparisons)
                print('MATCH', name, comparisons[name]['records'], flush=True)
    save(HERE / 'fixture-manifest.json', campaigns)
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    result = {'status': 'passed', 'scope': 'finite implementation equivalence and integrity, not theorem proof',
              'dev_commands_passed': 4, 'acceptance_commands_passed': len(commands),
              'ctest': {'Debug': '14/14', 'ASan_UBSan': '14/14', 'Release': '14/14'},
              'pytest_cases_passed': 115, 'differential_campaigns_passed': len(campaigns),
              'old_vs_new_response_comparisons': len(comparisons),
              'old_vs_new_records_matched': sum(v['records'] for v in comparisons.values()),
              'comparison_exclusion': 'core_reduction_seconds only',
              'old_m4_files_changed': changed, 'old_m4_files_unchanged': 53 - len(changed),
              'protected_files_unchanged': len(before['protected_sha256']), 'papers_unchanged': 4,
              'reference_unchanged': True, 'original_m5_binary_and_library_unchanged': True,
              'git_diff_check': 0, 'real_diagnostic': 'separate subsequent evidence'}
    save(HERE / 'verification.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
