"""Normalize an explicit-n zero-based edge-list artifact without dropping vertices."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.support import canonical_graph, graph_sha256, save, sha256
from vflhcds_reference.graph import normalize_graph


def prepare(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    tokens = source.read_text().split()
    if len(tokens) < 2:
        raise ValueError('missing n,m header')
    n, m = int(tokens[0]), int(tokens[1])
    if n < 1 or m < 0 or len(tokens) != 2 + 2 * m:
        raise ValueError('invalid counts or incomplete edge records')
    edges = [tuple(map(int, tokens[i:i+2])) for i in range(2, len(tokens), 2)]
    normalized = normalize_graph(tuple(range(n)), edges)
    graph = normalized.graph
    output.mkdir(parents=True, exist_ok=False)
    (output / 'graph.txt').write_text(canonical_graph(graph))
    record = {'source_path': str(source), 'source_sha256': sha256(source),
              'source_format': 'explicit n,m; declared vertices 0..n-1; undirected edges',
              'declared_vertices': n, 'raw_edges': m, 'vertices': graph.n, 'edges': len(graph.edges),
              'removed_self_loops': normalized.removed_self_loops,
              'removed_duplicate_edges': normalized.removed_duplicate_edges,
              'isolate_policy': 'preserve every declared vertex', 'graph_sha256': graph_sha256(graph),
              'script_sha256': sha256(Path(__file__)), 'command': [sys.executable, *sys.argv]}
    save(output / 'normalization.json', record)
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.source, args.evidence)
