"""T04-CLI: unchanged canonical results, defaults and error behavior."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k not in ('timing', 'core_reduction_seconds')}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def main():
    executable = Path(sys.argv[1]).resolve()
    calls = 0
    def run(args, code=0):
        nonlocal calls
        calls += 1
        result = subprocess.run([str(executable), *map(str, args)], capture_output=True, text=True)
        assert result.returncode == code, (args, result)
        status = json.loads(result.stderr)
        if code:
            assert not result.stdout and status['complete'] is False
        else:
            assert status['complete'] is True
        return result.stdout, clean(status)
    for name in ['triangle_and_isolate', 'bridged_triangles']:
        graph = ROOT / 'reference/fixtures' / (name + '.graph')
        for h in [2, 3, 2**200]:
            base = ['solve', '--graph', graph, '--h', str(h)]
            default = run(base + ['--all'])
            assert default == run(base + ['--all', '--clique-enumeration', 'combinations'])
            for core, scan, k in itertools.product(['off', 'safe'], ['sorted', 'membership'], [1, None]):
                args = base + ['--core-reduction', core, '--footprint-scan', scan]
                args += ['--all'] if k is None else ['--k', str(k)]
                assert run(args + ['--clique-enumeration', 'combinations']) == run(args + ['--clique-enumeration', 'adjacency'])
        with tempfile.TemporaryDirectory() as directory:
            x = Path(directory) / 'x.set'
            x.write_text('vflhcds-set 1 n 0\n')
            # Empty upper bound is a valid restricted query, independent of IDs.
            for bounds in [[], ['--x', x, '--y', x]]:
                args = ['oracle', '--graph', graph, '--h', '3', '--lambda', '1/3', *bounds]
                assert run(args) == run(args + ['--clique-enumeration', 'adjacency'])
    base = ['solve', '--graph', 'absent', '--h', '3', '--k', '1']
    for extra in [['--clique-enumeration', 'fast'], ['--clique-enumeration'],
                  ['--clique-enumeration', 'adjacency', '--clique-enumeration', 'combinations']]:
        run(base + extra, 2)
    run(['inspect-graph', '--graph', 'absent', '--clique-enumeration', 'adjacency'], 2)
    run(['solve', '--graph', 'absent', '--h', '3', '--k', '0', '--clique-enumeration', 'adjacency'], 2)
    print(f'T04-CLI: {calls} invocations passed; outputs, counters, hashes and defaults agree')


if __name__ == '__main__':
    main()
