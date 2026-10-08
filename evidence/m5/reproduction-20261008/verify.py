"""Final read-only integrity checks of measured evidence and unchanged source."""
import argparse
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    paths = [HERE.parent / 'final-evaluation-20261008' / s / 'campaign' for s in ('main', 'core', 'stop')]
    paths += [HERE.parent / 'final-main-repaired-20261008/main/campaign']
    inventories = {}
    for path in paths:
        inventory = read(path / 'checksums.json')
        for name, digest in inventory.items():
            assert sha256(path / name) == digest, str(path / name)
        inventories[str(path.relative_to(ROOT))] = len(inventory)
    measured = paths[-1]
    preflight = read(measured.parent.parent / 'preflight.json')
    for name, digest in preflight['script_sha256'].items():
        assert sha256(ROOT / name) == digest, name
    paper_hashes = read(ROOT / 'review/source_snapshot_sha256.json')['sha256']
    for name, digest in paper_hashes.items():
        assert sha256(ROOT / name) == digest, name
    config = read(measured / 'config.json')
    rebuild = read(HERE / 'checked/completion.json')
    assert rebuild['passed']
    for algorithm in config['algorithms']:
        assert sha256(ROOT / algorithm['executable']) == algorithm['sha256']
        assert rebuild[algorithm['kind'] + '_executable_sha256'] == algorithm['sha256']
    for case in config['cases']:
        assert sha256(ROOT / case['graph']) == case['sha256']
    commit = read(measured / 'environment.json')['head']
    unchanged = ['CMakeLists.txt', 'include', 'src', 'cmake', 'reference', 'tests', 'validation',
                 'experiments/*.py', 'baselines/ippv/*.py', 'baselines/ippv/source-lock.json',
                 'baselines/ippv/patches', 'baselines/ippv/fixtures']
    subprocess.run(['git', 'diff', '--exit-code', commit, '--', *unchanged], cwd=ROOT, check=True)
    names = subprocess.check_output(['git', 'ls-files', '--', *unchanged], cwd=ROOT, text=True).splitlines()
    source_hashes = {name: sha256(ROOT / name) for name in names}
    for folder, driver in [('accepted', HERE / 'accepted/driver-failed.py'), ('checked', HERE / 'run.py')]:
        assert sha256(driver) == read(HERE / folder / 'plan.json')['driver_sha256']
    save(args.output, {'passed': True, 'campaign_inventory_entries': inventories,
         'total_inventory_entries_verified': sum(inventories.values()), 'papers_sha256': paper_hashes,
         'unchanged_since_measured_head': commit, 'source_test_fixture_sha256': source_hashes,
         'measured_and_rebuilt_binary_hashes_agree': True,
         'failed_and_corrected_reproduction_drivers_preserved': True,
         'native_algorithm_runs': 0, 'verifier_sha256': sha256(Path(__file__))})
    print('Verified inventory entries:', sum(inventories.values()))
    print('Unchanged source/test/fixture files:', len(source_hashes))


if __name__ == '__main__':
    main()
