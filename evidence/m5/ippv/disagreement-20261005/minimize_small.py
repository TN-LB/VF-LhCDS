"""Deterministic edge-then-vertex reduction of the synthetic truncation witness."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'reference'))
sys.path.insert(0, str(ROOT / 'baselines/ippv'))
from adapter import run
from vflhcds_reference.graph import Graph
from vflhcds_reference.io import canonical_graph, parse_graph, graph_sha256
from vflhcds_reference.direct import Reference, direct_lhcds


def main():
    output = HERE / 'minimization'; output.mkdir()
    attempts = []

    def preserves(graph, edit):
        directory = output / f'{len(attempts):04d}'; directory.mkdir()
        (directory / 'graph.txt').write_text(canonical_graph(graph))
        row = {'edit': edit, 'vertices': graph.n, 'edges': len(graph.edges),
               'graph_sha256': graph_sha256(graph), 'accepted': False}
        attempts.append(row)
        ref = Reference(graph, 2, max_vertices=13)
        truth = direct_lhcds(ref)
        ids = {tuple(graph.ids(mask)) for mask in truth}
        row['truth'] = [{'vertices': list(graph.ids(m)), 'density': str(ref.density(m))} for m in truth]
        if len(truth) != 2 or any(ref.density(mask) <= 0 for mask in truth):
            row['reason'] = 'does not retain two positive-density solutions'
        else:
            old = run(ROOT / 'build-ippv-original/IPPV', graph, 2, 2, 10, directory / 'old', 60, False)
            assert old['status'] == 'completed'
            actual = [json.loads(line) for line in (directory / 'old/canonical_output.jsonl').read_text().splitlines()]
            old_ids = {tuple(r['vertices']) for r in actual}
            if len(old_ids) >= 2 or not old_ids <= ids:
                row['reason'] = 'old binary does not retain the missing-positive-solution failure'
            else:
                new = run(ROOT / 'build-ippv-exact-release/IPPV', graph, 2, 2, 10, directory / 'fixed', 60, False)
                assert new['status'] == 'completed'
                fixed = [json.loads(line) for line in (directory / 'fixed/canonical_output.jsonl').read_text().splitlines()]
                row['accepted'] = {tuple(r['vertices']) for r in fixed} == ids
                row['reason'] = 'old omits a positive solution; scaling repair restores full direct truth'
        (directory / 'decision.json').write_text(json.dumps(row, indent=2) + '\n')
        (output / 'attempts.json').write_text(json.dumps(attempts, indent=2) + '\n')
        return row['accepted']

    graph = parse_graph((HERE / 'fractional-bridge.graph').read_text())
    assert preserves(graph, 'starting synthetic witness')
    # Repeat phases to a fixed point: removing a vertex can enable an edge removal.
    while True:
        changed = False
        for edge in graph.edges:
            candidate = Graph(graph.vertices, tuple(e for e in graph.edges if e != edge))
            if preserves(candidate, ['remove_edge', list(edge)]):
                graph = candidate; changed = True; break
        if changed:
            continue
        for vertex in graph.vertices:
            candidate = Graph(tuple(v for v in graph.vertices if v != vertex), tuple(e for e in graph.edges if vertex not in e))
            if preserves(candidate, ['remove_vertex', vertex]):
                graph = candidate; changed = True; break
        if not changed:
            break
    (output / 'minimized.graph').write_text(canonical_graph(graph))
    result = {'attempts': len(attempts), 'vertices': graph.n, 'edges': len(graph.edges),
              'graph_sha256': graph_sha256(graph), 'h': 2, 'k': 2, 'iterations': 10,
              'minimality': 'one-edge/one-vertex irreducible under the recorded failure predicate; not global minimum',
              'origin': 'synthetic same-code-defect witness, not an induced reduction of CA-GrQc'}
    (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
