"""Capture one explicit clean-environment setup step; never retry or overwrite."""
import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import capture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    parser.add_argument('--timeout', type=int, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    folder = HERE / 'host-commands' / args.name
    folder.mkdir(parents=True, exist_ok=False)
    result = capture(command, folder, args.timeout)
    print(args.name, result['status'], result['native_exit_code'], flush=True)
    for name in ('stdout.txt', 'stderr.txt'):
        content = (folder / name).read_text()
        if content:
            print(content[-3000:])
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
