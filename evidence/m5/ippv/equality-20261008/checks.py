"""Record repair regressions and two original-case correctness replays only."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
from experiments.support import capture, run_ippv, save, sha256, parse_graph
from experiments.validate import compare, parse_records


def read(path):
    return json.loads(path.read_text())


def main():
    binaries = [ROOT / f'build-ippv-equality-{profile}/IPPV' for profile in ('release', 'sanitize')]
    python = str(ROOT / '.venv/bin/python')
    args = [piece for binary in binaries for piece in ('--binary', str(binary))]
    commands = [
        ('equality', [python, str(ROOT / 'baselines/ippv/check_equality.py'), *args, '--evidence', str(HERE / 'regression-equality')], 0),
        ('fractional', [python, str(ROOT / 'baselines/ippv/check_fractional.py'), *args, '--evidence', str(HERE / 'regression-fractional')], 0),
        ('toys', [python, str(ROOT / 'baselines/ippv/check_toys.py'), *args, '--h', '2', '3', '4', '5',
                  '--iterations', '10', '--timeout', '60', '--evidence', str(HERE / 'regression-toys')], 1),
        ('pytest', [python, '-m', 'pytest', str(ROOT / 'baselines/ippv/test_adapter.py'), str(ROOT / 'reference/tests'), '-q'], 0),
        ('certificate', [python, str(ROOT / 'evidence/m5/final-evaluation-20261008/certify_disagreement.py')], 0)]
    logs = HERE / 'checks'
    logs.mkdir()
    records = []
    for name, command, expected_exit in commands:
        path = logs / name
        path.mkdir()
        process = capture(command, path, 180)
        records.append({'name': name, 'process': str((path / 'process.json').relative_to(HERE)),
                        'exit_code': process['native_exit_code'], 'expected_exit': expected_exit})
        save(logs / 'commands.json', records)
        print(name, process['native_exit_code'], flush=True)
        assert process['native_exit_code'] == expected_exit
    toys = read(HERE / 'regression-toys/summary.json')
    assert toys['executed_native_runs'] == 48 and toys['unrun'] == 0
    assert toys['counts'] == {'definition_pass': 32, 'known_zero_density_mismatch': 16}
    campaign = ROOT / 'evidence/m5/final-evaluation-20261008/main/campaign'
    graph = parse_graph((campaign / 'runs/0090-0/graph.txt').read_text())
    expected = parse_records((campaign / 'runs/0090-0/canonical_output.jsonl').read_text(), graph, 4)
    old = parse_records((campaign / 'runs/0090-1/canonical_output.jsonl').read_text(), graph, 4)
    offending = old[12]['vertices']
    replay_plan = {'graph_sha256': read(campaign / 'runs/0090-0/manifest.json')['graph_sha256'],
                   'h': 4, 'k': 15, 'iterations': 10, 'timeout_seconds': 60, 'planned_native_calls': 2,
                   'scope': 'one repair correctness replay per build, no performance comparison or benchmark retry',
                   'reference_output': str((campaign / 'runs/0090-0/canonical_output.jsonl').relative_to(ROOT)),
                   'binaries': [{'path': str(b), 'sha256': sha256(b)} for b in binaries]}
    save(HERE / 'original-replay-plan.json', replay_plan)
    replays = []
    for index, binary in enumerate(binaries):
        path = HERE / f'original-replay-{index}'
        manifest = run_ippv(binary, graph, 4, 15, 10, path, 60, False)
        assert manifest['status'] == 'completed', manifest['status']
        assert not (path / 'stderr.txt').read_text(), 'unexpected sanitizer/native diagnostics'
        result = parse_records((path / 'canonical_output.jsonl').read_text(), graph, 4)
        agreement = compare(expected, result, 15)
        replays.append({'profile': index, **agreement, 'invalid_candidate_removed': offending not in [r['vertices'] for r in result]})
        save(HERE / 'original-replay-summary.json', replays)
        assert agreement['tie_aware_match'] and replays[-1]['invalid_candidate_removed']
        print('original', index, json.dumps(replays[-1]), flush=True)
    save(HERE / 'completion.json', {'passed': True, 'equality_definition_checks': 2,
         'fractional_definition_checks': 2, 'toy_definition_passes': 32, 'known_zero_density_mismatches': 16,
         'original_case_replays': 2, 'original_case_tie_aware_matches': 2,
         'benchmark_reruns': 0, 'production_vf_changed': False})


if __name__ == '__main__':
    main()
