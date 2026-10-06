"""Independent instance certificate; no production or baseline solver calls.

For lambda=56/13, directly check every deletion of the candidate. At a smaller
theta, a feasible integer flow matching a closure cut certifies a global
maximizer F. Every lambda-compact W lies in F: adding W\F would otherwise improve
Q_theta by at least (lambda-theta)|W\F|, using clique supermodularity. If the
ordinary connected component of F containing the candidate is exactly it, no
connected proper lambda-compact superset exists anywhere in the original graph.
"""
from collections import deque
from fractions import Fraction
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'reference'))
from vflhcds_reference.graph import Graph
from vflhcds_reference.io import parse_graph
from vflhcds_reference.direct import Reference, direct_compact


def main():
    start = time.monotonic()
    graph = parse_graph((ROOT / 'evidence/m5/pilot-20261005/aggregate/failure/original.graph').read_text())
    candidate = set(json.loads((HERE / 'candidate-inspection.json').read_text())['vertices'])
    adj = {v: set() for v in graph.vertices}
    for u, v in graph.edges:
        adj[u].add(v); adj[v].add(u)
    triangles = [(u, v, w) for u in graph.vertices for v in sorted(adj[u]) if u < v
                 for w in sorted(adj[u] & adj[v]) if v < w]
    local = Graph(tuple(sorted(candidate)), tuple(e for e in graph.edges if set(e) <= candidate))
    ref = Reference(local, 3, max_vertices=13)
    lam = ref.density(local.full_mask)
    assert lam == Fraction(56, 13) and direct_compact(ref, local.full_mask, lam)
    theta = lam - Fraction(1, 13 * (graph.n + 1))
    p, q = theta.numerator, theta.denominator
    source, sink = 0, 1
    vertex_ids = {v: i + 2 for i, v in enumerate(graph.vertices)}
    network = [[] for _ in range(2 + graph.n + len(triangles))]
    infinity = q * len(triangles) + 1

    def add(u, v, capacity):
        forward = [v, len(network[v]), capacity]
        backward = [u, len(network[u]), 0]
        network[u].append(forward); network[v].append(backward)
        return forward

    links = []
    for i, triangle in enumerate(triangles):
        node = 2 + graph.n + i
        add(source, node, q)
        links.append([add(node, vertex_ids[v], infinity) for v in triangle])
    for node in vertex_ids.values():
        add(node, sink, p)
    sys.setrecursionlimit(len(network) + 100)
    flow = 0
    while True:
        levels = [-1] * len(network); levels[source] = 0
        todo = deque([source])
        while todo:
            u = todo.popleft()
            for v, _, capacity in network[u]:
                if capacity and levels[v] < 0:
                    levels[v] = levels[u] + 1; todo.append(v)
        if levels[sink] < 0:
            break
        current = [0] * len(network)

        def send(u, amount):
            if u == sink:
                return amount
            while current[u] < len(network[u]):
                edge = network[u][current[u]]
                v, reverse, capacity = edge
                if capacity and levels[v] == levels[u] + 1:
                    pushed = send(v, min(amount, capacity))
                    if pushed:
                        edge[2] -= pushed
                        network[v][reverse][2] += pushed
                        return pushed
                current[u] += 1
            return 0

        while True:
            pushed = send(source, infinity)
            if not pushed:
                break
            flow += pushed
    selected = {v for v, node in vertex_ids.items() if levels[node] >= 0}
    allocation = [[infinity - edge[2] for edge in edges] for edges in links]
    # Certificate checks use only exact sums/inequalities and graph connectivity.
    loads = {v: 0 for v in graph.vertices}
    for triangle, values in zip(triangles, allocation):
        assert all(value >= 0 for value in values) and sum(values) <= q
        for v, value in zip(triangle, values):
            loads[v] += value
    assert all(value <= p for value in loads.values())
    cut = q * sum(not set(t) <= selected for t in triangles) + p * len(selected)
    assert sum(loads.values()) == flow == cut
    assert candidate <= selected
    component = {min(candidate)}; todo = list(component)
    while todo:
        u = todo.pop()
        for v in (adj[u] & selected) - component:
            component.add(v); todo.append(v)
    assert component == candidate, 'certificate does not establish global maximality'
    certificate = {'lambda': str(lam), 'theta': str(theta), 'p': p, 'q': q,
                   'triangles': triangles, 'clique_to_vertex_flow': allocation,
                   'global_optimum_vertices': sorted(selected),
                   'flow_value': flow, 'cut_capacity': cut,
                   'candidate_component': sorted(component)}
    (HERE / 'original-maximality-certificate.json').write_text(json.dumps(certificate) + '\n')
    summary = {'candidate': sorted(candidate), 'h': 3, 'vertices': graph.n,
               'triangles': len(triangles), 'candidate_triangles': 56,
               'deletion_subsets_checked': 8192, 'compact': True,
               'global_maximality_certified': True, 'lambda': str(lam),
               'theta': str(theta), 'global_optimum_size': len(selected),
               'feasible_flow_equals_cut': True, 'flow_value': flow,
               'scope': 'This candidate on this finite graph; not full top-20 truth or a theorem proof.',
               'wall_seconds': time.monotonic() - start}
    (HERE / 'original-maximality-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
