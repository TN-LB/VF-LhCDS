"""Independent exact finite-instance nonmaximality witness; no solver import."""
from fractions import Fraction
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'reference'))
from vflhcds_reference.graph import Graph
from vflhcds_reference.io import canonical_graph, graph_sha256, parse_graph


def main():
    folder = HERE / 'diagnosis'
    folder.mkdir(exist_ok=True)
    graph = parse_graph((HERE / 'main/campaign/runs/0090-1/graph.txt').read_text())
    rows = [json.loads(s) for s in (HERE / 'main/campaign/runs/0090-1/canonical_output.jsonl').read_text().splitlines()]
    s = set(rows[12]['vertices'])
    t = {1748, 8265, 13625, 16856, 16859, 21904, 21905, 21906, 21907, 21908}
    assert len(s) == len(t) == 10 and not s & t
    w = s | t
    edges = tuple(e for e in graph.edges if set(e) <= w)
    local = Graph(tuple(sorted(w)), edges)
    edge_set = set(edges)
    for block in (s, t):
        assert all((u, v) in edge_set for u, v in combinations(sorted(block), 2))
    crossing = [e for e in edges if bool(e[0] in s) != bool(e[1] in s)]
    assert crossing == [(1748, 18841)]
    cliques = [c for c in combinations(sorted(w), 4) if all(e in edge_set for e in combinations(c, 2))]
    assert len(cliques) == 420 and all(set(c) <= s or set(c) <= t for c in cliques)
    assert local.connected(local.full_mask)
    # Every deletion is determined by the counts removed from the two K10s:
    # there is no crossing 4-clique. Checking all 121 cardinality classes covers
    # every one of the 2**20 deletion subsets by this exact combinatorial identity.
    checks = []
    for a in range(11):
        for b in range(11):
            loss = 420 - comb(10-a, 4) - comb(10-b, 4)
            assert loss >= 21 * (a+b)
            checks.append({'deleted_from_candidate': a, 'deleted_from_extension': b,
                           'clique_loss': loss, 'required_loss': 21*(a+b)})
    assert Fraction(210, 10) == Fraction(420, 20) == 21
    (folder / 'nonmaximality-witness.graph').write_text(canonical_graph(local))
    result = {'original_graph_sha256': graph_sha256(graph), 'h': 4,
              'candidate': sorted(s), 'extension': sorted(t), 'proper_superset': sorted(w),
              'candidate_density': '21', 'superset_density': '21', 'crossing_edges': crossing,
              'superset_connected': True, 'candidate_is_lhcds': False,
              'reason': 'proper connected superset is 21-compact',
              'cardinality_classes_checked': checks,
              'scope': 'exact nonmaximality witness for this IPPV output; not full original top-k truth or a new theorem proof'}
    (folder / 'nonmaximality-certificate.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cardinality_classes_checked'}, indent=2))


if __name__ == '__main__':
    main()
