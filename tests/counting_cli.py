"""T04-COUNT-CLI: strict old/new output, counters, defaults and error behavior."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
from enumeration_cli import clean

ROOT = Path(__file__).resolve().parents[1]
binary = Path(sys.argv[1]).resolve()
calls = 0


def run(args, code=0):
    global calls
    calls += 1
    process = subprocess.run([str(binary), *map(str, args)], capture_output=True, text=True)
    assert process.returncode == code, (args, process)
    status = json.loads(process.stderr)
    assert status['complete'] == (code == 0)
    if code: assert not process.stdout
    return process.stdout, clean(status)


for fixture in ('triangle_and_isolate', 'bridged_triangles'):
    graph = ROOT / 'reference/fixtures' / (fixture + '.graph')
    for h in (2, 3, 2**200):
        base = ['solve', '--graph', graph, '--h', h]
        assert run(base + ['--all']) == run(base + ['--all', '--clique-count', 'sorted'])
        for enumeration, core, scan, k in itertools.product(
                ('combinations', 'adjacency'), ('off', 'safe'), ('sorted', 'membership'), (1, None)):
            args = base + ['--clique-enumeration', enumeration, '--core-reduction', core, '--footprint-scan', scan]
            args += ['--all'] if k is None else ['--k', k]
            assert run(args + ['--clique-count', 'sorted']) == run(args + ['--clique-count', 'membership'])
    for bounds in ([], ['--x', ROOT/'reference/fixtures/empty.set', '--y', ROOT/'reference/fixtures/empty.set']):
        args = ['oracle', '--graph', graph, '--h', 3, '--lambda', '1/3', *bounds]
        assert run(args) == run(args + ['--clique-count', 'membership'])
base = ['solve', '--graph', 'absent', '--h', 3, '--k', 1]
for extra in (['--clique-count'], ['--clique-count', 'automatic'],
              ['--clique-count', 'sorted', '--clique-count', 'membership']):
    run(base + extra, 2)
run(['inspect-graph', '--graph', 'absent', '--clique-count', 'membership'], 2)
run(['solve', '--graph', 'absent', '--h', 3, '--k', 0, '--clique-count', 'membership'], 2)
print(f'T04-COUNT-CLI: {calls} invocations passed; strict outputs/counters/hashes, modes, defaults, errors')
