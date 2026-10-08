"""Reuse the checked D040 aggregator; regenerate D041 tables without native runs."""
import argparse
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import capture, file_hashes, save, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aggregate', type=Path)
    args = parser.parse_args()
    source = HERE.parent / 'final-evaluation-20261008/summarize.py'
    if args.aggregate:
        spec = importlib.util.spec_from_file_location('d040_summary', source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.HERE = HERE
        module.summarize('main', args.aggregate)
        return 0
    logs = HERE / 'postprocess'
    logs.mkdir()
    save(logs / 'plan.json', {'driver_sha256': sha256(Path(__file__)),
         'aggregator_sha256': sha256(source), 'native_algorithm_calls': 0})
    records = []
    commands = [(name, [sys.executable, str(Path(__file__)), '--aggregate', str(HERE / name / 'main')])
                for name in ('aggregate', 'aggregate-replay')]
    commands += [(name, [sys.executable, str(HERE / 'review.py'), '--output', str(HERE / name)])
                 for name in ('review', 'review-replay')]
    for name, command in commands:
        folder = logs / name
        folder.mkdir()
        result = capture(command, folder, 180)
        records.append({'name': name, 'process': str((folder / 'process.json').relative_to(HERE)),
                        'exit_code': result['native_exit_code']})
        save(logs / 'commands.json', records)
        if result['status'] != 'completed':
            print((folder / 'stdout.txt').read_text() + (folder / 'stderr.txt').read_text())
            return 1
    hashes = file_hashes(HERE / 'aggregate')
    assert hashes == file_hashes(HERE / 'aggregate-replay')
    review_hashes = file_hashes(HERE / 'review')
    assert review_hashes == file_hashes(HERE / 'review-replay')
    save(HERE / 'regeneration.json', {'passed': True, 'identical_artifact_sha256': hashes,
         'identical_review_sha256': review_hashes,
         'native_algorithm_reruns': 0, 'historical_timing_pooling': False})
    print('Identical aggregate/review files:', len(hashes)+len(review_hashes))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
