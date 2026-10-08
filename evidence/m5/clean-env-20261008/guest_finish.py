"""Regenerate existing tables after the separate Linux smoke has passed."""
import argparse
import json
from pathlib import Path
import platform
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--smoke', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.repo.resolve(), args.output.resolve()
    assert platform.system() == 'Linux'
    assert json.loads((args.smoke / 'completion.json').read_text())['passed']
    assert not output.exists()
    output.mkdir()
    sys.path.insert(0, str(repo))
    from experiments.support import capture, save, sha256
    python = str(repo / '.venv/bin/python')
    records, derived = [], {}
    main_source = repo / 'evidence/m5/final-main-repaired-20261008'
    ablations = repo / 'evidence/m5/final-evaluation-20261008'
    steps = []
    for suite in ('main', 'core', 'stop'):
        original = main_source if suite == 'main' else ablations
        target = output / 'aggregate' / suite
        command = ([python, str(original / 'postprocess.py'), '--aggregate', str(target)]
                   if suite == 'main' else
                   [python, str(original / 'summarize.py'), '--suite', suite, '--output', str(target)])
        steps.append((suite, command, original / 'aggregate' / suite, target))
    steps.append(('review', [python, str(main_source / 'review.py'), '--output', str(output / 'review')],
                  main_source / 'review', output / 'review'))
    save(output / 'plan.json', {'driver_sha256': sha256(Path(__file__)), 'platform': platform.platform(),
         'commands': [{'name': name, 'command': cmd} for name, cmd, _, _ in steps],
         'smoke_completion_sha256': sha256(args.smoke / 'completion.json'),
         'new_benchmark_calls': 0})
    for name, command, original, target in steps:
        log = output / 'commands' / name
        log.mkdir(parents=True)
        result = capture(command, log, 900)
        records.append({'name': name, 'status': result['status'], 'exit_code': result['native_exit_code']})
        save(output / 'commands.json', records)
        if result['status'] != 'completed':
            save(output / 'completion.json', {'passed': False, 'failed_step': name})
            return 1
        expected = {p.name: sha256(p) for p in original.iterdir() if p.is_file()}
        actual = {p.name: sha256(p) for p in target.iterdir() if p.is_file()}
        if actual != expected:
            save(output / 'completion.json', {'passed': False, 'mismatch': name,
                 'expected': expected, 'actual': actual})
            return 1
        derived[name] = actual
        print(name, len(actual), 'identical artifacts', flush=True)
    save(output / 'completion.json', {'passed': True, 'artifact_sha256': derived,
         'total_artifacts': sum(map(len, derived.values())), 'new_benchmark_calls': 0,
         'fresh_userspace': True, 'independent_kernel_or_hardware': False})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
