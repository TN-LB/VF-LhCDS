"""Recheck saved M3 acceptance evidence; --write refreshes derived manifests."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'evidence/m3'
ACCEPTED = HERE / 'accepted'
ALLOWED_DOC_CHANGES = {'docs/BUILD.md', 'docs/TASKS.md', 'docs/CLAIM_TRACEABILITY.md'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expanded_digest(path):
    result = hashlib.sha256()
    with gzip.open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def load(path):
    return json.loads(path.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def verify(save=False):
    commands = load(ACCEPTED / 'commands.json')
    assert len(commands) == 35
    for command in commands:
        assert command['exit_code'] == 0, command
        for stream in ['stdout', 'stderr']:
            assert digest(ACCEPTED / command[stream]) == command[stream + '_sha256']
    environment = load(ACCEPTED / 'environment.json')
    for name, expected in environment['source_sha256'].items():
        assert digest(ROOT / name) == expected, ('source changed since acceptance', name)
    start = load(HERE / 'preservation_start.json')
    preserved = {}
    for name, expected in start['sha256'].items():
        actual = digest(ROOT / name)
        if name not in ALLOWED_DOC_CHANGES:
            assert actual == expected, ('protected source changed', name)
        preserved[name] = {'before_sha256': expected, 'after_sha256': actual,
                           'unchanged': actual == expected,
                           'allowed_evidence_document': name in ALLOWED_DOC_CHANGES}
    campaigns = {}
    for summary in sorted(ACCEPTED.glob('*/summary.json')):
        data = load(summary)
        assert data['status'] == 'passed', summary
        hashes = data.get('sha256', data.get('evidence_sha256'))
        for name, expected in hashes.items():
            assert digest(summary.parent / name) == expected, (summary, name)
        assert not (summary.parent / 'probe.stderr').read_bytes(), summary
        campaigns[summary.parent.name] = {
            'summary_path': str(summary.relative_to(ROOT)),
            'summary_sha256': digest(summary), 'summary': data,
            'expanded_results_sha256': expanded_digest(summary.parent / 'results.jsonl.gz')}
    assert len(campaigns) == 14
    pairs = []
    for name in campaigns:
        if name.startswith('build-sanitize-'):
            peer = name.replace('build-sanitize-', 'build-', 1)
            assert campaigns[name]['expanded_results_sha256'] == campaigns[peer]['expanded_results_sha256']
            assert (ACCEPTED / name / 'cases.jsonl').read_bytes() == (ACCEPTED / peer / 'cases.jsonl').read_bytes()
            pairs.append([peer, name])
    checks = {}
    for build in ['build', 'build-sanitize', 'build-release', 'build-relwithdebinfo']:
        command = next(c for c in commands if c['command'][:3] == ['ctest', '--test-dir', build])
        output = (ACCEPTED / command['stdout']).read_text()
        assert '100% tests passed' in output and 'out of 9' in output
        assert '74 passed' in output and '37 runtime checks passed' in output
        checks[build] = {'ctest': '9/9 passed', 'log': command['stdout']}
    standalone = next(c for c in commands if c['command'][:4] == ['python', '-m', 'pytest', 'reference/tests'])
    assert '74 passed' in (ACCEPTED / standalone['stdout']).read_text()
    flags = {}
    warnings = ['-std=c++17', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wsign-conversion', '-Wshadow', '-Werror']
    for build in ['build', 'build-sanitize', 'build-release', 'build-relwithdebinfo', 'build-production']:
        entries = load(ROOT / build / 'compile_commands.json')
        for entry in entries:
            assert all(flag in entry['command'].split() for flag in warnings), entry
            if build == 'build-sanitize':
                assert all(flag in entry['command'].split() for flag in [
                    '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-fno-sanitize-recover=all'])
        if build == 'build-production':
            assert not any('/tests/' in entry['file'] for entry in entries)
        flags[build] = entries
    runner = load(ACCEPTED / 'cli-definition-run/manifest.json')
    assert runner['native_exit_code'] == 0 and runner['validation']['passed']
    assert runner['validation']['level'] == 'definition_checked'
    for name, expected in runner['sha256'].items():
        assert digest(ACCEPTED / 'cli-definition-run' / name) == expected
    for name, expected in [('token-move-before.json', 1), ('token-move-after.json', 0)]:
        record = load(HERE / name)
        # These are actual saved subprocess results, not an expected-failure test label.
        assert record[0]['exit_code'] == 0 and record[1]['exit_code'] == expected, record
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    result = {'status': 'passed', 'accepted_commands': 35, 'commands_sha256': digest(ACCEPTED / 'commands.json'),
              'environment_sha256': digest(ACCEPTED / 'environment.json'),
              'accepted_source_files': len(environment['source_sha256']),
              'campaign_directories': len(campaigns), 'identical_debug_sanitizer_pairs': pairs,
              'ctest': checks, 'pytest': '74 passed', 'protected_files_checked': len(preserved),
              'resolved_review_finding': 'R01 before exit 1 / after exit 0',
              'evidence_scope': 'finite implementation validation; no theorem or performance proof'}
    if save:
        write('preservation_final.json', preserved)
        write('fixture_manifest.json', campaigns)
        write('compiler_flags.json', flags)
        write('verification.json', result)
    return result


if __name__ == '__main__':
    print(json.dumps(verify('--write' in sys.argv), indent=2))
