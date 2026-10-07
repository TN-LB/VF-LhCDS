"""Validate aggregation, summarize each suite twice, verify exact regeneration."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import capture, file_hashes, save


def main():
    logs = HERE / 'postprocess'
    logs.mkdir()
    python = str(ROOT / '.venv/bin/python')
    commands = [('tests', [python, '-m', 'pytest', str(HERE / 'test_summary.py'), '-q'])]
    for suite in ('main', 'core', 'stop'):
        for name in ('aggregate', 'aggregate-replay'):
            commands.append((suite + '-' + name, [python, str(HERE / 'summarize.py'), '--suite', suite,
                                                   '--output', str(HERE / name / suite)]))
    records = []
    for name, command in commands:
        output = logs / name
        output.mkdir()
        result = capture(command, output, 180)
        records.append({'name': name, 'process': str((output / 'process.json').relative_to(HERE)),
                        'exit_code': result['native_exit_code']})
        save(logs / 'commands.json', records)
        print(name, result['status'], flush=True)
        if result['status'] != 'completed':
            print((output / 'stdout.txt').read_text() + (output / 'stderr.txt').read_text())
            return 1
    original = file_hashes(HERE / 'aggregate')
    assert original == file_hashes(HERE / 'aggregate-replay')
    save(HERE / 'regeneration.json', {'passed': True, 'identical_artifact_sha256': original,
         'native_algorithm_reruns': 0, 'historical_timing_pooling': False})
    print('Identical aggregates:', len(original))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
