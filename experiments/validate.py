"""Exact external output checks. Definition truth is available only for n<=12."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.support import Reference, count_cliques, direct_lhcds, json_line, parse_graph, semantic_hash

KEYS = ('rank', 'h', 'vertex_count', 'clique_count', 'density_num', 'density_den', 'vertices')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def parse_records(text, graph, h):
    records, seen = [], set()
    for rank, line in enumerate(text.splitlines(), 1):
        row = json.loads(line, object_pairs_hook=unique_object)
        if not isinstance(row, dict) or set(row) != set(KEYS):
            raise ValueError('unexpected result schema')
        for key, expected in [('rank', rank), ('h', h)]:
            if type(row[key]) is not int or row[key] != expected:
                raise ValueError('incorrect rank/h')
        ids = row['vertices']
        if not isinstance(ids, list) or not ids or any(type(v) is not int for v in ids):
            raise ValueError('nonempty exact integer vertex list required')
        if ids != sorted(set(ids)) or type(row['vertex_count']) is not int or row['vertex_count'] != len(ids):
            raise ValueError('vertex order/count mismatch')
        mask = graph.mask(ids)
        if mask in seen:
            raise ValueError('duplicate result set')
        seen.add(mask)
        for key in ('clique_count', 'density_num', 'density_den'):
            if not isinstance(row[key], str) or not re.fullmatch(r'0|[1-9][0-9]*', row[key]):
                raise ValueError('canonical nonnegative decimal string required')
        a, b = int(row['density_num']), int(row['density_den'])
        if not b or (Fraction(a, b).numerator, Fraction(a, b).denominator) != (a, b):
            raise ValueError('noncanonical rational density')
        records.append({key: row[key] for key in KEYS})
    if text != ''.join(json_line(row) for row in records):
        raise ValueError('noncanonical or truncated JSONL')
    return records


def validate(graph, h, k, text, *, definition=False, strict=False):
    if type(h) is not int or h < 2 or (k is not None and (type(k) is not int or k < 1)):
        raise ValueError('h>=2 and k>=1 or explicit full output required')
    records = parse_records(text, graph, h)
    masks = [graph.mask(r['vertices']) for r in records]
    counts = [count_cliques(graph, mask, h) for mask in masks]
    densities = [Fraction(count, mask.bit_count()) for count, mask in zip(counts, masks)]
    checks = {'connected': all(graph.connected(mask) for mask in masks),
              'exact_counts': all(int(r['clique_count']) == count for r, count in zip(records, counts)),
              'exact_densities': all(Fraction(int(r['density_num']), int(r['density_den'])) == density
                                     for r, density in zip(records, densities)),
              'density_order': all(a >= b for a, b in zip(densities, densities[1:]))}
    if k is not None:
        checks['at_most_k'] = len(records) <= k
    if strict:
        checks['lexicographic_ties'] = all(a != b or x['vertices'] < y['vertices']
                                          for a, b, x, y in zip(densities, densities[1:], records, records[1:]))
    result = {'level': 'structural_checked', 'checks': checks, 'completeness_certified': False,
              'output_count': len(records), 'semantic_sha256': semantic_hash(graph, h, records)}
    if definition:
        ref = Reference(graph, h)
        truth = direct_lhcds(ref)
        expected = truth[:k]
        cutoff = ref.density(expected[-1]) if expected else None
        checks.update(required_count=len(masks) == len(expected),
                      definition_valid=all(mask in truth for mask in masks),
                      higher_density_complete=all(mask in masks for mask in truth if cutoff is not None and ref.density(mask) > cutoff),
                      cutoff_respected=all(cutoff is not None and ref.density(mask) >= cutoff for mask in masks))
        if strict:
            checks['strict_reference_match'] = masks == list(expected)
        result.update(level='definition_checked', expected_vertices=[list(graph.ids(m)) for m in expected])
        result['completeness_certified'] = all(checks.values())
    result['passed'] = all(checks.values())
    return result, records


def compare(left, right, k):
    """Agreement of independently checked records; not a new maximality proof."""
    def density(r):
        return Fraction(int(r['density_num']), int(r['density_den']))
    strict = left == right
    counts_equal = len(left) == len(right) and len(left) <= k
    if not left or not right:
        tie_match = counts_equal and not left and not right
    else:
        cutoff = density(left[-1])
        high = lambda rows: {tuple(r['vertices']) for r in rows if density(r) > cutoff}
        tie_match = counts_equal and cutoff == density(right[-1]) and high(left) == high(right)
    return {'level': 'cross_implementation_agreement', 'strict_match': strict,
            'tie_aware_match': tie_match, 'completeness_certified': False,
            'note': 'agreement only; input runs retain their own structural/definition evidence'}


def compare_prefix(fixed, full, k):
    """Compare an already validated fixed-k run with its exact full-output prefix."""
    if type(k) is not int or k < 1:
        raise ValueError('positive prefix length required')
    return {'level': 'fixed_full_prefix_agreement', 'prefix_match': fixed == full[:k],
            'fixed_count': len(fixed), 'full_count': len(full),
            'expected_prefix_count': min(k, len(full)), 'completeness_certified': False,
            'note': 'strict prefix agreement only; full-run maximality/completeness is not certified'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', type=Path, required=True)
    parser.add_argument('--records', type=Path, required=True)
    parser.add_argument('--status', type=Path)
    parser.add_argument('--h', type=int, required=True)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--k', type=int)
    scope.add_argument('--all', action='store_true')
    parser.add_argument('--definition', action='store_true')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    try:
        if args.h < 2 or (not args.all and args.k < 1):
            raise ValueError('h>=2,k>=1 required')
        graph = parse_graph(args.graph.read_text())
        result, records = validate(graph, args.h, args.k, args.records.read_text(), definition=args.definition, strict=args.strict)
        if args.status:
            status = json.loads(args.status.read_text(), object_pairs_hook=unique_object)
            result['checks']['native_completion'] = status.get('schema_version') == 1 and status.get('status') == 'completed' and status.get('complete') is True
            result['checks']['native_count'] = type(status.get('output_count')) is int and status.get('output_count') == len(records)
            result['checks']['native_hash'] = status.get('semantic_sha256') == result['semantic_sha256']
            result['passed'] = all(result['checks'].values())
            result['completeness_certified'] = bool(args.definition and result['passed'])
    except (ValueError, TypeError, KeyError, OSError, RuntimeError) as error:
        result = {'level': 'not_completed', 'passed': False, 'completeness_certified': False, 'error': str(error)}
    print(json.dumps(result, sort_keys=True))
    return 0  # A completed check may report failure; consumers must inspect passed.


if __name__ == '__main__':
    raise SystemExit(main())
