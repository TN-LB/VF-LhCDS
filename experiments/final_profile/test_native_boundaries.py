"""Run real signal/cancellation/fallback boundaries; optionally retain raw evidence."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile

from reports import read_events, complete


def check(binary, directory):
    results = []
    for mode in ('kill', 'cancel', 'fallback'):
        path = directory / f'{mode}.jsonl'
        result = subprocess.run([str(binary), mode], env=dict(os.environ, VF_PROFILE_OUTPUT=str(path)),
                                capture_output=True, timeout=30)
        (directory / f'{mode}.stdout').write_bytes(result.stdout)
        (directory / f'{mode}.stderr').write_bytes(result.stderr)
        events = read_events(path)
        assert not result.stderr, result.stderr
        if mode == 'kill':
            assert result.returncode == -signal.SIGKILL and not complete(events)
            assert events[-1]['phase'] == 'test_interrupted_phase'
            assert not any(e['event'] == 'finish' for e in events)
        elif mode == 'cancel':
            assert result.returncode == 7 and not complete(events)
            assert events[-1]['event'] == 'finish' and events[-1]['native_exit'] == 7
        else:
            assert result.returncode == 0 and complete(events)
            oracle = next(e for e in events if e['event'] == 'oracle')
            assert oracle['stats']['capacity_backend'] == 'arbitrary_precision'
            assert oracle['stats']['mincut_calls'] == 1
        results.append({'mode': mode, 'returncode': result.returncode, 'events': len(events),
                        'complete': complete(events), 'passed': True})
    (directory / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('binary', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=False)
        check(args.binary.resolve(), args.output)
    else:
        with tempfile.TemporaryDirectory() as directory:
            check(args.binary.resolve(), Path(directory))


if __name__ == '__main__':
    main()
