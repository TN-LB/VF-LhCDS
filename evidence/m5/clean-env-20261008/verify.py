"""Verify saved Linux reproduction and unchanged experimental evidence."""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    output = HERE / 'integrity.json'
    assert not output.exists()
    original = HERE.parent / 'reproduction-20261008'
    prior = read(original / 'integrity.json')
    counts = {}
    for name in prior['campaign_inventory_entries']:
        folder = ROOT / name
        inventory = read(folder / 'checksums.json')
        for filename, digest in inventory.items():
            assert sha256(folder / filename) == digest, filename
        counts[name] = len(inventory)
    for name, digest in prior['papers_sha256'].items():
        assert sha256(ROOT / name) == digest, name
    changed = read(HERE / 'portability-plan.json')['source_overlay']
    unchanged = {}
    for name, digest in prior['source_test_fixture_sha256'].items():
        if name in changed:
            assert digest == changed[name]['before']
            assert sha256(ROOT / name) == changed[name]['after']
            # These repairs change only whitespace, not C++ tokens or literals.
            old = subprocess.check_output(['git', 'show', prior['unchanged_since_measured_head'] + ':' + name])
            assert b''.join(old.split()) == b''.join((ROOT / name).read_bytes().split())
        else:
            assert sha256(ROOT / name) == digest, name
            unchanged[name] = digest
    overlay = read(HERE / 'host-commands/22-linux-source-overlay/stdout.txt')
    for name, digest in overlay['overlay_sha256'].items():
        assert sha256(ROOT / name) == digest, name
    smoke = HERE / 'guest-checked'
    assert read(smoke / 'completion.json')['passed']
    commands = read(smoke / 'commands.json')
    assert len(commands) == 23 and all(c['status'] == 'completed' and c['exit_code'] == 0 for c in commands)
    production = read(smoke / 'plan.json')['production_source_sha256']
    for name, digest in production.items():
        assert sha256(ROOT / name) == digest, name
    fixture_outputs = {}
    for name in ('ippv-fractional/profile-0/canonical_output.jsonl',
                 'ippv-equality/profile-0/canonical_output.jsonl',
                 'ippv-bridge/canonical_output.jsonl', 'vf-definition/stdout.jsonl'):
        assert sha256(smoke / name) == sha256(original / 'checked' / name), name
        fixture_outputs[name] = sha256(smoke / name)
    for folder in ('guest-first', 'guest-gcc-first'):
        env = read(HERE / folder / 'environment.json')
        assert sha256(HERE / folder / 'bootstrap-failed.py') == env['script_sha256']
        assert not read(HERE / folder / 'completion.json')['passed']
    assert sha256(original / 'run.py') == read(HERE / 'guest-first/smoke/plan.json')['driver_sha256']
    assert sha256(ROOT / 'scripts/reproduce_release.py') == read(smoke / 'plan.json')['driver_sha256']
    regeneration = read(HERE / 'guest-derived/completion.json')
    assert regeneration['passed'] and regeneration['total_artifacts'] == 26
    for suite, files in regeneration['artifact_sha256'].items():
        folder = HERE / 'guest-derived' / ('review' if suite == 'review' else 'aggregate/' + suite)
        for name, digest in files.items():
            assert sha256(folder / name) == digest, name
    config = read(HERE.parent / 'final-main-repaired-20261008/main/campaign/config.json')
    for algorithm in config['algorithms']:
        assert sha256(ROOT / algorithm['executable']) == algorithm['sha256']
    save(output, {'passed': True, 'campaign_inventory_entries': counts,
         'total_inventory_entries_verified': sum(counts.values()), 'papers_sha256': prior['papers_sha256'],
         'production_source_sha256': production, 'unchanged_source_test_fixture_sha256': unchanged,
         'whitespace_only_test_repairs': changed, 'guest_source_overlay': overlay,
         'mac_linux_fixture_output_sha256': fixture_outputs,
         'regenerated_artifacts': 26, 'historical_measured_binaries_unchanged': True,
         'failed_attempt_sources_preserved': True, 'native_benchmark_calls': 0,
         'verifier_sha256': sha256(Path(__file__))})
    print(f'{sum(counts.values())} raw inventory entries verified; {len(unchanged)} source/test/fixture files unchanged')
    print(f'{len(production)} frozen production hashes match; 4 cross-platform fixture outputs match; 26 tables verified')


if __name__ == '__main__':
    main()
