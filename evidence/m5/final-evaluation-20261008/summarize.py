"""Adapt the established core-ablation aggregator to D040 scopes/repeats.

Read immutable manifests only; never launch native processes. Historical
core-ablation-20261006/summarize.py remains unchanged.
"""
from collections import Counter
import argparse
import json
from pathlib import Path
import statistics
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256
HERE = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text())

def summarize(suite, output=None):
    campaign = HERE / suite / 'campaign'
    config, summary, policy = [read(campaign / f'{name}.json') for name in ('config', 'summary', 'execution-policy')]
    inventory = read(campaign / 'checksums.json')
    for name, digest in inventory.items():
        assert sha256(campaign / name) == digest, name
    output = HERE / 'aggregate' / suite if output is None else Path(output)
    output.mkdir(parents=True, exist_ok=False)
    agreement_key = 'prefix_match' if policy.get('require_prefix_agreement') else ('strict_match' if policy['require_strict_agreement'] else 'tie_aware_match')
    rows, telemetry = [], []
    for row in summary['runs']:
        manifest = read(campaign / row['directory'] / 'manifest.json')
        native, validator, checks = manifest['native'], manifest.get('external_validation', {}), manifest['validation']
        assert row['status'] == manifest['status']
        if validator:
            assert native['finished_utc'] <= validator['started_utc']
        rows.append({**row, 'native_exit_code': native['native_exit_code'],
                     'native_wall_seconds': native['wall_seconds'], 'native_peak_rss_bytes': native['peak_rss_bytes'],
                     'native_user_seconds': native['user_seconds'], 'native_system_seconds': native['system_seconds'],
                     'validation_exit_code': validator.get('native_exit_code'),
                     'validation_wall_seconds': validator.get('wall_seconds'),
                     'validation_peak_rss_bytes': validator.get('peak_rss_bytes'),
                     'validation_level': checks['level'], 'validation_passed': checks.get('passed'),
                     'completeness_certified': checks.get('completeness_certified', False),
                     'output_count': checks.get('output_count'), 'phase_wall_seconds': manifest['phase_wall_seconds'],
                     'manifest_sha256': sha256(campaign / row['directory'] / 'manifest.json'),
                     'censored': row['status'] != 'completed'})
        counters = manifest.get('native_status', {}).get('counters')
        if counters is not None:
            queries = counters['queries']
            assert counters['logical_interval_queries'] == sum(q['logical_interval_queries'] for q in queries)
            assert counters['mincut_calls'] == sum(q['mincut_calls'] for q in queries)
            assert counters['cliques_scanned'] == sum(q['cliques_scanned'] or 0 for q in queries)
            telemetry.append({
                'case': row['case'], 'repeat': row['repeat'], 'algorithm': row['algorithm'],
                'directory': row['directory'], 'phase_wall_seconds': manifest['phase_wall_seconds'],
                'logical_interval_queries': counters['logical_interval_queries'],
                'mincut_calls': counters['mincut_calls'], 'cliques_scanned': counters['cliques_scanned'],
                'cliques_enumerated': counters['cliques_enumerated'],
                'capacity_backends': dict(Counter(q['capacity_backend'] for q in queries)),
                'max_forward_nodes': max(((q['forward_nodes'] or 0) for q in queries), default=0),
                'max_forward_arcs': max(((q['forward_arcs'] or 0) for q in queries), default=0),
                'sum_original_interval_sizes': sum(q['original_interval_size'] for q in queries),
                'sum_oracle_interval_sizes': sum(q['oracle_interval_size'] for q in queries),
                'sum_forward_nodes': sum(q['forward_nodes'] or 0 for q in queries),
                'sum_forward_arcs': sum(q['forward_arcs'] or 0 for q in queries),
                'core_reduction_seconds': sum(q['core_reduction_seconds'] or 0 for q in queries),
                'core_queries': sum(q['core'] is not None for q in queries),
                'core_incidence_visits': sum(q['core']['incidence_visits'] if q['core'] else 0 for q in queries),
                'core_cliques_invalidated': sum(q['core']['cliques_invalidated'] if q['core'] else 0 for q in queries),
                'sum_unique_footprints': sum(q['unique_footprints'] or 0 for q in queries),
            })
    executed = {r['directory'] for r in rows}
    unrun = [r for r in policy['planned_runs'] if r['directory'] not in executed]
    stopped = read(campaign / 'stopped.json') if (campaign / 'stopped.json').exists() else None
    assert unrun == (stopped['unrun'] if stopped else [])
    assert all(not (campaign / r['directory']).exists() for r in unrun)
    cells = []
    for case in config['cases']:
        pairs = [p for p in summary['comparisons'] if p['case'] == case['name']]
        for algorithm in config['algorithms']:
            selected = [r for r in rows if r['case'] == case['name'] and r['algorithm'] == algorithm['name']]
            measured = len(selected) == config['repeats'] and all(r['status'] == 'completed' and r['validation_passed'] for r in selected)
            eligible = measured and len(pairs) == config['repeats'] and all(p.get(agreement_key) for p in pairs)
            cell = {'case': case['name'], 'algorithm': algorithm['name'], 'planned_repeats': config['repeats'],
                    'recorded_repeats': len(selected), 'unrun_repeats': config['repeats']-len(selected),
                    'statuses': dict(Counter(r['status'] for r in selected)),
                    'raw_wall_seconds': [r['native_wall_seconds'] for r in selected],
                    'raw_peak_rss_bytes': [r['native_peak_rss_bytes'] for r in selected],
                    'raw_cpu_seconds': [r['native_user_seconds'] + r['native_system_seconds'] for r in selected],
                    'complete_repetitions_available': measured, 'complete_repetitions_agree': eligible,
                    'semantic_hashes': sorted({r['semantic_sha256'] for r in selected if r['semantic_sha256'] is not None}),
                    'pair_comparisons': len(pairs), 'strict_matches': sum(p.get('strict_match', False) for p in pairs),
                    'tie_aware_matches': sum(p.get('tie_aware_match', False) for p in pairs),
                    'required_agreement': agreement_key, 'required_matches': sum(p.get(agreement_key, False) for p in pairs)}
            for field, values in [('wall', cell['raw_wall_seconds']), ('rss', cell['raw_peak_rss_bytes']), ('cpu', cell['raw_cpu_seconds'])]:
                unit = 'bytes' if field == 'rss' else 'seconds'
                for label, function in [('median', statistics.median), ('min', min), ('max', max)]:
                    cell[f'{field}_{label}_{unit}'] = function(values) if measured else None
            cells.append(cell)
    totals = {'planned_native_runs': len(policy['planned_runs']), 'recorded_native_runs': len(rows),
              'native_statuses': dict(Counter(r['status'] for r in rows)),
              'external_validators_completed': sum(r['validation_exit_code'] == 0 for r in rows),
              'structural_passes': sum(r['validation_level'] == 'structural_checked' and r['validation_passed'] for r in rows),
              'unrun_native_runs': len(unrun), 'paired_comparisons': len(summary['comparisons']),
              'strict_matches': sum(p.get('strict_match', False) for p in summary['comparisons']),
              'tie_aware_matches': sum(p.get('tie_aware_match', False) for p in summary['comparisons']),
              'strict_disagreements': sum(p.get('strict_match') is False for p in summary['comparisons']),
              'tie_aware_disagreements': sum(p.get('tie_aware_match') is False for p in summary['comparisons']),
              'pairs_not_compared': sum(p.get('level') == 'not_compared' for p in summary['comparisons']),
              'required_agreement': agreement_key, 'required_matches': sum(p.get(agreement_key, False) for p in summary['comparisons']),
              'required_disagreements': sum(p.get(agreement_key) is False for p in summary['comparisons']),
              'stop_reason': stopped['reason'] if stopped else None, 'completeness_certified': False,
              'raw_inventory_entries_verified': len(inventory),
              'campaign_exit_code': read(HERE / suite / 'completion.json')['exit_code'],
              'campaign_wall_seconds': read(HERE / suite / 'completion.json')['wall_seconds']}
    for name, data in [('runs', rows), ('cells', cells), ('unrun', unrun), ('totals', totals), ('telemetry', telemetry)]:
        save(output / f'{name}.json', data)
    if stopped and rows:
        save(output / 'stop-context.json', {'reason': stopped['reason'], 'case_config': next(c for c in config['cases'] if c['name'] == rows[-1]['case']), 'seed': config['seed'], 'last_record': rows[-1], 'native_process_manifest': str((campaign / rows[-1]['directory'] / 'process.json').relative_to(ROOT)), 'original_graph': str((campaign / rows[-1]['directory'] / 'graph.txt').relative_to(ROOT)), 'diagnosis': 'See saved status and comparison evidence; this aggregation does not assign fault.', 'retry': 'Not run.'})
    lines = ['# All planned measurements', '', 'Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require every scheduled repetition of that algorithm/case to complete and pass validation. The required comparator is recorded per cell: main uses cutoff-tie agreement, core uses strict output, stop uses strict prefix agreement. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.', '', '| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |', '|---|---|---:|---|---|---|---:|']
    for cell in cells:
        timing = f"{cell['wall_median_seconds']:.6f} [{cell['wall_min_seconds']:.6f}, {cell['wall_max_seconds']:.6f}]" if cell['complete_repetitions_available'] else 'unavailable'
        memory = f"{cell['rss_median_bytes']} [{cell['rss_min_bytes']}, {cell['rss_max_bytes']}]" if cell['complete_repetitions_available'] else 'unavailable'
        lines.append(f"| {cell['case']} | {cell['algorithm']} | {cell['recorded_repeats']} / {cell['planned_repeats']} | {cell['statuses']} | {timing} | {memory} | {cell['required_matches']} / {cell['pair_comparisons']} |")
    (output / 'TABLE.md').write_text('\n'.join(lines) + '\n')
    save(output / 'provenance.json', {'script_sha256': sha256(Path(__file__)), 'raw_inventory_sha256': sha256(campaign / 'checksums.json'), 'summary_sha256': sha256(campaign / 'summary.json')})
    print(json.dumps({'suite': suite, **totals}, indent=2))
    return totals

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=('main', 'core', 'stop'), required=True)
    parser.add_argument('--output', type=Path, help='New directory for regeneration; default: aggregate beside this script')
    args = parser.parse_args()
    summarize(args.suite, args.output)
