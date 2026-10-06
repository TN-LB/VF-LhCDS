"""Deterministic definition-level IPPV diagnostics, outside benchmark timing."""
import argparse
from collections import Counter
import datetime
import itertools
import json
from pathlib import Path
import sys

from adapter import ROOT, run
from process import sha256
from vflhcds_reference.graph import Graph
from vflhcds_reference.io import canonical_graph, graph_sha256


def fixtures(h):
    # Non-contiguous original IDs include a negative ID; all native IDs are mapped.
    vertices = tuple(-7 + 13 * i for i in range(2 * h))
    left, right = vertices[:h], vertices[h:]
    edges = tuple(itertools.combinations(left, 2))
    both = tuple(sorted(edges + tuple(itertools.combinations(right, 2))))
    yield 'clique', Graph(left, edges), 1
    yield 'tied-cliques-k1', Graph(vertices, both), 1
    yield 'tied-cliques-k2', Graph(vertices, both), 2
    bridge = tuple(sorted(both + ((left[-1], right[0]),)))
    yield 'bridged-cliques', Graph(vertices, bridge), 1
    yield 'clique-isolate', Graph(left + (right[0],), edges), 2
    yield 'singleton', Graph((left[0],), ()), 1


def classify(manifest, name, graph, h, directory):
    if manifest['status'] == 'completed':
        return 'definition_pass'
    if manifest['status'] != 'semantic_mismatch' or name not in ('clique-isolate', 'singleton'):
        return 'unexpected_failure'
    checks = manifest['validation']['checks']
    # Preserve the existing IPPV-B04 failure label. Do not turn it into a pass.
    if checks.get('required_count') is not False or not all(v for k, v in checks.items() if k != 'required_count'):
        return 'unexpected_failure'
    records = [json.loads(line) for line in (directory / 'canonical_output.jsonl').read_text().splitlines()]
    expected_native = [list(graph.vertices[:h])] if name == 'clique-isolate' else []
    if [record['vertices'] for record in records] != expected_native:
        return 'unexpected_failure'
    return 'known_zero_density_mismatch'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, action='append', required=True)
    parser.add_argument('--h', type=int, nargs='+', required=True)
    parser.add_argument('--iterations', type=int, required=True)
    parser.add_argument('--timeout', type=float, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    if any(h not in (2, 3, 4, 5) for h in args.h) or len(set(args.h)) != len(args.h):
        raise ValueError('this tiny diagnostic supports distinct h values from 2,3,4,5')
    binaries = [p.resolve() for p in args.binary]
    if len(set(binaries)) != len(binaries):
        raise ValueError('duplicate binary')
    for binary in binaries:
        provenance = json.loads(binary.with_suffix('.provenance.json').read_text())
        if provenance['executable_sha256'] != sha256(binary):
            raise ValueError('binary does not match provenance')
    if args.iterations < 1 or args.timeout <= 0:
        raise ValueError('positive iterations and timeout required')
    output = args.evidence.resolve()
    output.mkdir(parents=True, exist_ok=False)
    cases = []
    for h in args.h:
        for name, graph, k in fixtures(h):
            path = output / 'fixtures' / f'h{h}-{name}.graph'
            path.parent.mkdir(exist_ok=True)
            path.write_text(canonical_graph(graph))
            cases.append({'name': name, 'graph': graph, 'path': path, 'h': h, 'k': k})
    plan = {
        'scope': 'deterministic tiny definition validation, not a benchmark or final experiment configuration',
        'task': 'P09.1', 'decision': 'D029; continue independent VF-LhCDS/IPPV work',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'command': [sys.executable, *sys.argv], 'cwd': str(Path.cwd()),
        'iterations': args.iterations, 'timeout_seconds': args.timeout,
        'memory_limit_bytes': None, 'algorithm_workers': 1, 'cache': 'uncontrolled',
        'seed': None, 'stop': 'stop on any new failure; retain and count already recorded zero-density omissions',
        'script_sha256': sha256(Path(__file__)),
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted((ROOT / 'baselines/ippv').glob('*.py'))},
        'binaries': [{'path': str(p), 'sha256': sha256(p)} for p in binaries],
        'cases': [{key: value for key, value in case.items() if key not in ('graph', 'path')} |
                  {'fixture': str(case['path'].relative_to(output)), 'graph_sha256': graph_sha256(case['graph'])}
                  for case in cases],
    }
    (output / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    rows = []
    expected = len(cases) * len(binaries)
    for case in cases:
        for profile, binary in enumerate(binaries):
            directory = output / 'runs' / f'h{case["h"]}-{case["name"]}-profile{profile}'
            manifest = run(binary, case['graph'], case['h'], case['k'], args.iterations,
                           directory, args.timeout, definition=True)
            row = {'h': case['h'], 'k': case['k'], 'case': case['name'], 'profile': profile,
                   'manifest': str((directory / 'manifest.json').relative_to(output)),
                   'status': manifest['status'], 'native_exit_code': manifest['native']['native_exit_code'],
                   'classification': classify(manifest, case['name'], case['graph'], case['h'], directory)}
            rows.append(row)
            counts = dict(Counter(row['classification'] for row in rows))
            summary = {'planned_native_runs': expected, 'executed_native_runs': len(rows),
                       'unrun': expected - len(rows), 'counts': counts, 'runs': rows}
            (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
            print(json.dumps(row), flush=True)
            if row['classification'] == 'unexpected_failure':
                return 1
    # Known omissions remain failed semantic checks, including in the exit status.
    return 1 if counts.get('known_zero_density_mismatch') else 0


if __name__ == '__main__':
    raise SystemExit(main())
