"""Small deterministic families; structural labels are checked from actual traces."""
from itertools import combinations
import random


def fixtures():
    cases = [
        ('isolates', 4, [], 3),
        ('split_nonoutput', 5, [*combinations(range(4), 2), (3, 4)], 2),
        ('tied_layer', 5, [(0, 1), (2, 3)], 2),
        ('ordinary_bridge', 6, [*combinations(range(3), 2), *combinations(range(3, 6), 2), (2, 3)], 3),
        ('core_restore', 8, [*combinations(range(4), 2), *combinations(range(4, 7), 2), (4, 7)], 2),
        ('core_cascade', 6, [(i, i + 1) for i in range(5)], 2),
        ('h_above_n', 3, [(0, 1)], 1 << 200),
        ('repeated_footprints', 4, list(combinations(range(4), 2)), 3),
    ]
    # Fixed total n, varying clique concentration and number of equal-density regions.
    for width in (3, 4, 5):
        cases.append((f'concentration_{width}', 8, list(combinations(range(width), 2)), 3))
    for regions in (1, 2, 3):
        edges = [edge for i in range(regions) for edge in combinations(range(3*i, 3*i+3), 2)]
        cases.append((f'equal_regions_{regions}', 9, edges, 3))
    for tail in (1, 2, 3):
        cases.append((f'peeling_tail_{tail}', 4+tail,
                      [*combinations(range(4), 2), *((i, i+1) for i in range(3, 3+tail))], 2))
    # Several distinct clique densities force more than one split depth. Actual
    # depths are recorded/checked, rather than assuming balanced recursion.
    for layers in (2, 3, 4):
        sizes = (4, 3, 2, 1)[:layers]
        edges = []; offset = 0
        for size in sizes:
            edges.extend(combinations(range(offset, offset+size), 2)); offset += size
        cases.append((f'nested_density_layers_{layers}', offset, edges, 2))
    rng = random.Random(20261014)
    for i in range(8):
        cases.append((f'seed_20261014_{i}', 7,
                      [e for e in combinations(range(7), 2) if rng.random() < (i+1)/10], 2+i % 3))
    for name, n, edges, h in cases:
        yield {'name': name, 'vertices': list(range(n)), 'edges': sorted(edges), 'h': h,
               'seed': 20261014 if name.startswith('seed_') else None}
