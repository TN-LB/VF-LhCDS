"""One-time local M3 freeze: preflight, implementation commit/tag, evidence commit.

Default is read-only preflight. --freeze writes Git metadata; it never pushes,
resets, deletes, overwrites a tag, or changes production source.
"""
import datetime
import json
from pathlib import Path
import subprocess
import sys

from verify_evidence import ROOT, HERE, digest, load, verify, write

BASE = '0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6'
TAG = 'v0.1.0-m3-correctness'
MANIFEST = HERE / 'files_changed.json'
DOCS = ['docs/TASKS.md', 'docs/CLAIM_TRACEABILITY.md', 'evidence/m3/REPORT.md']


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def changed_paths():
    tracked = git('diff', '--name-only', BASE).splitlines()
    untracked = git('ls-files', '--others', '--exclude-standard').splitlines()
    return sorted(set(tracked + untracked) - {'evidence/m3/files_changed.json'})


def refresh_manifest():
    write('files_changed.json', {'base_commit': BASE,
        'note': 'All M3 changes from base; this manifest excludes its own contents.',
        'sha256': {name: digest(ROOT / name) for name in changed_paths()}})


def main():
    verify()
    assert git('rev-parse', 'HEAD') == BASE, 'Base changed; review required before freeze'
    assert not git('diff', '--cached', '--name-only'), 'Unexpected staged changes'
    assert not git('tag', '--list', TAG), 'Tag already exists; never overwrite it'
    manifest = load(MANIFEST)
    assert set(changed_paths()) == set(manifest['sha256']), 'Changed-file set differs'
    for name, expected in manifest['sha256'].items():
        assert digest(ROOT / name) == expected, ('Changed-file hash differs', name)
    for name in DOCS:
        text = (ROOT / name).read_text()
        assert 'M3_FREEZE_PENDING' in text and 'M3_COMMIT_PENDING' in text
    print('Preflight passed: 35 commands, accepted sources/evidence, protected files, diff and explicit file list.', flush=True)
    if '--freeze' not in sys.argv:
        return
    records = []
    def execute(*args):
        command = ['git', *args]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        records.append({'command': command, 'exit_code': completed.returncode,
                        'stdout': completed.stdout, 'stderr': completed.stderr})
        if completed.returncode:
            write('freeze-failure.json', records)
            raise RuntimeError(completed.stderr)
        return completed.stdout.strip()
    execute('add', '--', *manifest['sha256'], 'evidence/m3/files_changed.json')
    execute('commit', '-m', 'Implement M3 exact fixed-k solver and correctness evidence')
    commit = git('rev-parse', 'HEAD')
    execute('tag', '-a', TAG, commit, '-m',
            'Unoptimized M3 correctness freeze: T10-T16 and retained M1/M2 gates passed. Finite implementation evidence, not a theorem or performance proof.')
    assert git('rev-parse', TAG + '^{commit}') == commit
    for name in DOCS:
        path = ROOT / name
        text = path.read_text().replace('M3_COMMIT_PENDING', '`' + commit + '`')
        text = text.replace('M3_FREEZE_PENDING', 'M3/P13.1 complete: local annotated tag `' + TAG + '` freezes the tested implementation.')
        text = text.replace('planned (M3 tests passed; commit gate pending)', 'implementation-tested (finite M3 scope)')
        text = text.replace('- [ ] P13.1 ', '- [x] P13.1 ')
        text = text.replace('local freeze pending.', 'local annotated freeze recorded below.')
        text = text.replace('P13.1\'s review is\ncomplete', 'P13.1\'s review and local freeze are\ncomplete')
        path.write_text(text)
    write('RELEASE.json', {'schema_version': 1, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'base_commit': BASE, 'implementation_commit': commit, 'annotated_tag': TAG,
        'tag_object': git('rev-parse', TAG), 'scope': 'Unoptimized M3 finite correctness evidence; no theorem/performance proof',
        'remote_push': False, 'commands': records,
        'provenance': 'Tag points to implementation and complete accepted evidence. A following documentation-only commit records this tag and closes P13.1 without changing tested source.'})
    verify(save=True)
    refresh_manifest()
    execute('add', '--', *DOCS, 'evidence/m3/RELEASE.json', 'evidence/m3/preservation_final.json',
            'evidence/m3/files_changed.json', 'evidence/m3/fixture_manifest.json',
            'evidence/m3/compiler_flags.json', 'evidence/m3/verification.json')
    execute('commit', '-m', 'Record M3 correctness freeze and completed evidence ledger')
    assert not git('status', '--porcelain'), 'Unexpected post-freeze changes'
    assert not git('diff', TAG, 'HEAD', '--', 'CMakeLists.txt', 'include', 'src', 'tests', 'validation', 'scripts')
    print(json.dumps({'implementation_commit': commit, 'evidence_commit': git('rev-parse', 'HEAD'),
                      'tag': TAG, 'worktree_clean': True, 'remote_push': False}, indent=2))


if __name__ == '__main__':
    main()
