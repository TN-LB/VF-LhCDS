"""IPPV-B09 equal-density ordinary-edge extension, with independent full truth."""
import argparse
import json
from pathlib import Path
import sys

from adapter import ROOT, run
from process import sha256
from vflhcds_reference.io import parse_graph, graph_sha256
from vflhcds_reference.direct import Reference, direct_lhcds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, action='append', required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    output = args.evidence.resolve()
    output.mkdir(parents=True, exist_ok=False)
    fixture = Path(__file__).parent / 'fixtures/equal-density-bridge.graph'
    graph = parse_graph(fixture.read_text())
    # Only this fixed 13-vertex regression exceeds the unchanged default guard.
    ref = Reference(graph, 3, max_vertices=13)
    truth = direct_lhcds(ref)
    expected = [list(graph.ids(mask)) for mask in truth]
    assert expected == [[0, 1, 2, 3, 4]] and ref.density(truth[0]) == 2
    plan = {'command': [sys.executable, *sys.argv], 'script_sha256': sha256(Path(__file__)),
            'fixture': str(fixture.relative_to(ROOT)), 'graph_sha256': graph_sha256(graph),
            'h': 3, 'k': 3, 'iterations': 10, 'timeout_seconds': 60,
            'scope': 'independent all-superset correctness regression, not a benchmark',
            'reference_max_vertices': 13, 'expected_vertices': expected,
            'binaries': [{'path': str(p.resolve()), 'sha256': sha256(p)} for p in args.binary]}
    (output / 'plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    rows = []
    for index, binary in enumerate(args.binary):
        directory = output / f'profile-{index}'
        manifest = run(binary.resolve(), graph, 3, 3, 10, directory, 60, False)
        assert manifest['status'] == 'completed', manifest['status']
        assert not (directory / 'stderr.txt').read_text(), 'unexpected native diagnostics'
        records = [json.loads(line) for line in (directory / 'canonical_output.jsonl').read_text().splitlines()]
        passed = [r['vertices'] for r in records] == expected
        rows.append({'profile': index, 'passed': passed, 'level': 'definition_checked',
                     'all_proper_supersets_checked_by_reference': True,
                     'native_exit_code': manifest['native']['native_exit_code'],
                     'manifest': str((directory / 'manifest.json').relative_to(output))})
        (output / 'summary.json').write_text(json.dumps({'runs': rows}, indent=2)+'\n')
        assert passed, 'equal-density nonmaximal candidate retained'
        print(json.dumps(rows[-1]), flush=True)


if __name__ == '__main__':
    main()
