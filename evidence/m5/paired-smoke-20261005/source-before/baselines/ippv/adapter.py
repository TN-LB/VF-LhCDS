"""External IPPV adapter. Keep author selection/order; validation is a later child.

The native file prints rounded densities, so exact counts/densities are recomputed
from its actual vertex sets outside native timing. No missing set is synthesized.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'reference'))
from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.io import canonical_graph, graph_sha256, parse_graph
from process import capture, sha256

INT_MAX = 2**31 - 1


def native_input(graph):
    if graph.n > INT_MAX or len(graph.edges) > INT_MAX:
        raise ValueError('input exceeds audited IPPV int index/loop domain')
    index = {v: i for i, v in enumerate(graph.vertices)}
    return f'{graph.n} {len(graph.edges)}\n' + ''.join(f'{index[u]} {index[v]}\n' for u, v in graph.edges)


def parse_native(text, graph):
    lines = text.splitlines()
    if len(lines) % 2:
        raise ValueError('incomplete native record')
    sets, rounded = [], []
    for i in range(0, len(lines), 2):
        header = lines[i].split()
        if len(header) != 2 or not re.fullmatch(r'[1-9][0-9]*', header[0]):
            raise ValueError('invalid native count/density header')
        if not re.fullmatch(r'[0-9]+\.[0-9]{4}', header[1]):
            raise ValueError('invalid native rounded density')
        tokens = lines[i + 1].split()
        if any(not re.fullmatch(r'0|[1-9][0-9]*', token) for token in tokens):
            raise ValueError('invalid native vertex ID')
        internal = [int(token) for token in tokens]
        if len(internal) != int(header[0]) or len(set(internal)) != len(internal):
            raise ValueError('native vertex count or duplicate mismatch')
        if any(v >= graph.n for v in internal):
            raise ValueError('undeclared native vertex ID')
        vertices = tuple(sorted(graph.vertices[v] for v in internal))
        if vertices in sets:
            raise ValueError('duplicate native result set')
        sets.append(vertices)
        rounded.append(header[1])
    return sets, rounded


def count_cliques(graph, mask, h):
    """Exact external structural count; not part of IPPV or the M1 reference."""
    def visit(candidates, remaining):
        if candidates.bit_count() < remaining:
            return 0
        if remaining == 1:
            return candidates.bit_count()
        count = 0
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            count += visit(candidates & graph.adjacency[bit.bit_length() - 1], remaining - 1)
        return count
    return visit(mask, h)


def validate(graph, h, k, text, definition=False):
    if h < 2 or k < 1:
        raise ValueError('h>=2 and k>=1 required')
    sets, rounded = parse_native(text, graph)
    masks = [graph.mask(vertices) for vertices in sets]
    counts = [count_cliques(graph, mask, h) for mask in masks]
    densities = [Fraction(count, mask.bit_count()) for count, mask in zip(counts, masks)]
    checks = {
        'at_most_k': len(sets) <= k,
        'connected': all(graph.connected(mask) for mask in masks),
        'density_nonincreasing': all(a >= b for a, b in zip(densities, densities[1:])),
        # Audit only the printed approximation, never use it for ranking/equivalence.
        'rounded_density_consistent': all(abs(Fraction(text) - exact) <= Fraction(1, 20000)
                                         for text, exact in zip(rounded, densities)),
    }
    result = {'level': 'structural_checked', 'checks': checks,
              'completeness_certified': False, 'native_rounded_densities': rounded,
              'strict_order_compatible': False, 'output_count': len(sets)}
    if definition:
        ref = Reference(graph, h)
        truth = direct_lhcds(ref)
        expected = truth[:k]
        cutoff = ref.density(expected[-1]) if expected else None
        checks.update(
            every_set_definition_valid=all(mask in truth for mask in masks),
            required_count=len(masks) == min(k, len(truth)),
            higher_density_complete=set(mask for mask in truth if ref.density(mask) > cutoff).issubset(masks)
                if cutoff is not None else not masks,
            cutoff_respected=all(ref.density(mask) >= cutoff for mask in masks)
                if cutoff is not None else not masks,
        )
        result.update(level='definition_checked', truth_count=len(truth),
                      expected=[list(graph.ids(mask)) for mask in expected],
                      strict_match=masks == list(expected), completeness_certified=all(checks.values()))
    result['passed'] = all(checks.values())
    records = [{'rank': i, 'h': h, 'vertex_count': len(vertices), 'clique_count': str(count),
                'density_num': str(density.numerator), 'density_den': str(density.denominator),
                'vertices': list(vertices)}
               for i, (vertices, count, density) in enumerate(zip(sets, counts, densities), 1)]
    return result, records


def run(executable, graph, h, k, iterations, output, timeout, definition=False):
    for name, value, minimum in [('h', h, 2), ('k', k, 1), ('iterations', iterations, 1)]:
        if type(value) is not int or not minimum <= value <= INT_MAX:
            raise ValueError(f'{name} outside audited positive int range')
    if definition and graph.n > 12:
        raise ValueError('definition validation requires n<=12')
    executable = Path(executable).resolve()
    provenance = json.loads(executable.with_suffix('.provenance.json').read_text())
    if provenance['executable_sha256'] != sha256(executable):
        raise ValueError('baseline binary differs from build provenance')
    encoded = native_input(graph)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / 'dataset').mkdir()
    (output / 'output').mkdir()
    (output / 'graph.txt').write_text(canonical_graph(graph))
    (output / 'dataset/input.txt').write_text(encoded)
    (output / 'vertex_map.json').write_text(json.dumps(list(graph.vertices)) + '\n')
    command = [str(executable), '-g', './dataset/input.txt', '-h', str(h), '-t', str(iterations),
               '-k', str(k), '-p', '0']
    native = capture(command, output, timeout)
    manifest = {'schema_version': 1, 'algorithm': 'IPPV-author-with-disclosed-patches',
                'build_provenance': provenance,
                'native': native, 'graph_sha256': graph_sha256(graph),
                'normalized_input_sha256': sha256(output / 'graph.txt'),
                'converted_input_sha256': sha256(output / 'dataset/input.txt'),
                'vertex_map_sha256': sha256(output / 'vertex_map.json'),
                'h': h, 'k': k, 'iterations': iterations, 'pattern': 0,
                'status': native['status'], 'validation': {'level': 'not_run'},
                'phase_wall_seconds': {'postload': None, 'postindex': None},
                'phase_note': 'Author prints clock() CPU times; not comparable wall phases',
                'evidence_scope': 'single reproduction/validation run; no benchmark claim'}
    result_file = output / f'output/input-{k}.txt'
    if native['status'] == 'completed':
        counts = re.findall(r'^num of LhCDS ([0-9]+)$', (output / 'stdout.txt').read_text(), re.M)
        if not result_file.exists() or len(counts) != 1:
            manifest['status'] = 'output_incomplete'
        else:
            manifest['native_output_sha256'] = sha256(result_file)
            validation_dir = output / 'validation'
            validation_dir.mkdir()
            command = [sys.executable, str(Path(__file__).resolve()), 'validate', '--graph', str(output / 'graph.txt'),
                       '--native-output', str(result_file), '--h', str(h), '--k', str(k),
                       '--records', str(output / 'canonical_output.jsonl'), '--declared-count', counts[0]]
            if definition:
                command.append('--definition')
            external = capture(command, validation_dir, timeout)
            manifest['external_validation'] = external
            try:
                manifest['validation'] = json.loads((validation_dir / 'stdout.txt').read_text())
            except (ValueError, OSError):
                manifest['validation'] = {'level': 'not_completed'}
            if external['status'] != 'completed':
                manifest['status'] = 'validation_error'
            elif not manifest['validation'].get('passed'):
                manifest['status'] = 'semantic_mismatch' if definition else 'structural_mismatch'
    manifest['sha256'] = {str(path.relative_to(output)): sha256(path) for path in sorted(output.rglob('*'))
                          if path.is_file()}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command', required=True)
    start = commands.add_parser('run')
    start.add_argument('--executable', type=Path, required=True)
    start.add_argument('--evidence', type=Path, required=True)
    start.add_argument('--iterations', type=int, required=True)
    start.add_argument('--timeout', type=float, required=True)
    check = commands.add_parser('validate')
    check.add_argument('--native-output', type=Path, required=True)
    check.add_argument('--records', type=Path, required=True)
    check.add_argument('--declared-count', type=int, required=True)
    for sub in (start, check):
        sub.add_argument('--graph', type=Path, required=True)
        sub.add_argument('--h', type=int, required=True)
        sub.add_argument('--k', type=int, required=True)
        sub.add_argument('--definition', action='store_true')
    args = parser.parse_args()
    graph = parse_graph(args.graph.read_text())
    if args.command == 'run':
        result = run(args.executable, graph, args.h, args.k, args.iterations,
                     args.evidence, args.timeout, args.definition)
    else:
        result, records = validate(graph, args.h, args.k, args.native_output.read_text(), args.definition)
        result['checks']['stdout_count_matches_file'] = len(records) == args.declared_count
        result['passed'] = all(result['checks'].values())
        if args.definition:
            result['completeness_certified'] = result['passed']
        args.records.write_text(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in records))
    print(json.dumps(result, sort_keys=True))
    # The validator exits 0 when a check was completed, including a reported mismatch.
    return 0 if args.command == 'validate' or result['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
