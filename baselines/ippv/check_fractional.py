"""IPPV-B07/B08 native regression against all-superset definition truth."""
import argparse
import json
from pathlib import Path
import sys
import time

from adapter import ROOT, run
from process import sha256
from vflhcds_reference.io import parse_graph, graph_sha256
from vflhcds_reference.direct import Reference, direct_lhcds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, action='append', required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    output = args.evidence.resolve(); output.mkdir(parents=True, exist_ok=False)
    fixture = Path(__file__).parent / 'fixtures/fractional-bridge.graph'
    graph = parse_graph(fixture.read_text())
    # Explicit diagnostic guard for this fixed 13-vertex fixture; the adapter's
    # general exhaustive-size default is unchanged.
    start = time.monotonic()
    ref = Reference(graph, 2, max_vertices=13)
    truth = direct_lhcds(ref)
    expected = {tuple(graph.ids(mask)) for mask in truth}
    assert expected == {(0, 1, 2, 3), (4, 5, 6, 7)}
    assert sorted(str(ref.density(mask)) for mask in truth) == ['3/2', '5/4']
    plan = {'command': [sys.executable, *sys.argv], 'script_sha256': sha256(Path(__file__)),
            'fixture': str(fixture.relative_to(ROOT)), 'graph_sha256': graph_sha256(graph),
            'h': 2, 'k': 2, 'iterations': 10, 'timeout_seconds': 60,
            'scope': 'fixed correctness regression, not benchmark continuation',
            'reference_max_vertices': 13, 'reference_wall_seconds': time.monotonic() - start,
            'expected': [{'vertices': list(graph.ids(mask)), 'density': str(ref.density(mask))} for mask in truth],
            'binaries': [{'path': str(p.resolve()), 'sha256': sha256(p)} for p in args.binary]}
    (output / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    rows = []
    for index, binary in enumerate(args.binary):
        directory = output / f'profile-{index}'
        manifest = run(binary.resolve(), graph, 2, 2, 10, directory, 60, False)
        assert manifest['status'] == 'completed', manifest['status']
        assert not (directory / 'stderr.txt').read_text(), 'unexpected native diagnostics'
        records = [json.loads(line) for line in (directory / 'canonical_output.jsonl').read_text().splitlines()]
        passed = len(records) == len(expected) and {tuple(r['vertices']) for r in records} == expected
        row = {'profile': index, 'passed': passed, 'level': 'definition_checked',
               'all_proper_supersets_checked_by_reference': True, 'native_exit_code': manifest['native']['native_exit_code'],
               'output_count': len(records), 'manifest': str((directory / 'manifest.json').relative_to(output))}
        rows.append(row)
        (output / 'summary.json').write_text(json.dumps({'runs': rows}, indent=2) + '\n')
        assert passed, 'fractional candidate missing or invalid'
        print(json.dumps(row), flush=True)


if __name__ == '__main__':
    main()
