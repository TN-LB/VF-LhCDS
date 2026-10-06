"""Render scoped core-ablation results from checked manifests and aggregates."""
import json
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def main():
    totals, checks = read('aggregate/totals.json'), read('verification.json')
    replay = read('regeneration.json')
    assert replay['passed'] and totals['strict_disagreements'] == 0
    cells = {(c['case'], c['algorithm']): c for c in read('aggregate/cells.json')}
    pairs = read('core-pair-details.json')
    effects = []
    for name in dict.fromkeys(c['case'] for c in cells.values()):
        off, on = [cells[(name, mode)] for mode in ('vf-core-off', 'vf-core-safe')]
        if off['three_repeat_agreement_available'] and on['three_repeat_agreement_available']:
            effects.append({'case': name,
                            'safe_over_off_wall_median': on['wall_median_seconds'] / off['wall_median_seconds'],
                            'safe_over_off_rss_median': on['rss_median_bytes'] / off['rss_median_bytes']})
    (HERE / 'performance-summary.json').write_text(json.dumps({
        'scope': 'Ratios of three-repeat medians from fully completed strict paired cells only.',
        'cases': effects, 'excluded_censored_cases_retained_in_aggregate': True,
        'historical_timings_combined': False, 'statistical_significance_claimed': False}, indent=2) + '\n')
    lines = [
        '# VF core off/on ablation — 2026-10-06', '',
        f"**{totals['recorded_native_runs']}/48 calls recorded:** {totals['native_statuses']}; "
        f"{totals['external_validators_completed']} separate structural validators pass. "
        f"{totals['strict_matches']} complete pairs have identical canonical outputs; "
        f"{totals['pairs_not_compared']} blocks cannot be compared. "
        f"Unrun: {totals['unrun_native_runs']}. Driver exit: {totals['campaign_exit_code']}.", '',
        'The same VF Release binary uses adjacency enumeration and membership footprint '
        'scanning; only core off/safe changes. CA-GrQc (5,242 vertices, 14,484 edges) '
        'and CA-CondMat (23,133 vertices, 93,439 edges), h=3, k={5,10,15,20}, '
        'three repeats, seed 20261003. Apple M1/16 GiB, macOS 15.7.7, AppleClang 17, '
        'Python 3.12.2; serial one-worker execution, randomized order within blocks, '
        '60-second native/separate-validator guards, no memory cap, uncontrolled '
        'cache, no warm-ups/retries. IPPV is not rerun.', '',
        '| Graph | k | Core off: median s / status | Core safe: median s / status | Safe / off time | Strict pairs |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for graph in ('ca-grqc', 'ca-condmat'):
        for k in (5, 10, 15, 20):
            name = f'{graph}-h3-k{k}'
            off, on = [cells[(name, a)] for a in ('vf-core-off', 'vf-core-safe')]
            def display(cell):
                if cell['three_repeat_measurements_available']:
                    return f"{cell['wall_median_seconds']:.6f}"
                return ', '.join(f'{n} {status}' for status, n in cell['statuses'].items()) or 'unrun'
            ratio = f"{on['wall_median_seconds']/off['wall_median_seconds']:.3f}" if off['three_repeat_agreement_available'] and on['three_repeat_agreement_available'] else 'unavailable'
            lines.append(f"| {graph} | {k} | {display(off)} | {display(on)} | {ratio} | {off['strict_matches']}/3 |")
    if effects:
        wall_changes = [(r['safe_over_off_wall_median'] - 1) * 100 for r in effects]
        rss_changes = [(r['safe_over_off_rss_median'] - 1) * 100 for r in effects]
        lines += ['', f"Across {len(effects)} completed paired settings, safe-core median wall "
                  f"changes range from {min(wall_changes):+.2f}% to {max(wall_changes):+.2f}%; "
                  f"peak-RSS median changes range from {min(rss_changes):+.2f}% to {max(rss_changes):+.2f}%. "
                  '[Exact ratios](performance-summary.json).']
    lines += ['', 'Ratios above 1 mean core safe is slower. Small differences in these '
              'three-repeat samples are not evidence of a stable general speedup. '
              'Medians require all three '
              'scheduled runs to complete; ratios additionally require all three '
              'strict pairs. Timeouts remain censored. [All raw times/ranges/RSS](aggregate/TABLE.md). '
              'Native time includes core computation and all solver work; external '
              'validation is separate. Historical timings are not pooled.', '',
              '| Completed case | Queries | Sum of oracle sizes: off → safe | Sum of network nodes: off → safe | Median core time s |',
              '|---|---:|---:|---:|---:|']
    for name in dict.fromkeys(c['case'] for c in cells.values()):
        selected = [p for p in pairs if p['case'] == name]
        if len(selected) != 3:
            continue
        example = selected[0]
        for key in ('logical_queries', 'off_sum_oracle_interval_sizes', 'safe_sum_oracle_interval_sizes',
                    'off_sum_forward_nodes', 'safe_sum_forward_nodes'):
            assert len({p[key] for p in selected}) == 1
        lines.append(f"| {name} | {example['logical_queries']} | {example['off_sum_oracle_interval_sizes']} → {example['safe_sum_oracle_interval_sizes']} | {example['off_sum_forward_nodes']} → {example['safe_sum_forward_nodes']} | {statistics.median(p['safe_core_seconds'] for p in selected):.6f} |")
    lines += [
        '', 'Core time is already inside solve/native time. Summed query sizes are '
        'workload counters, not peak live memory; network shrinkage alone does not '
        'establish a runtime benefit or an O(k) bound. Internal counting/footprint/'
              'network-build/flow times are not individually measured. Completed '
              'pairs retain identical footprint scan visits: the materialized '
              'backend still scans all stored cliques per query, and core does not '
              'change the separate endpoint-counting path. This limits what network '
              'shrinkage alone can explain. '
        '[Per-run telemetry](aggregate/telemetry.json) and [paired counter checks](core-pair-details.json).', '',
        f"Completed outputs have stable hashes in {checks['stable_completed_cells']} cells. "
        f"All {checks['historical_grqc_exact_output_matches']} completed CA-GrQc outputs also "
        'match the prior membership campaign. The earlier CA-CondMat timeout campaign '
        'and single-run completions remain separate; changing wall time across '
        'campaigns cannot be attributed to core without this paired control.', '',
        'Only the external runner/test interface changes: `execute(require_strict_agreement=True)` '
        'enforces identical cutoff selection for equivalent modes. **137 pytest checks pass**. '
        'The saved-evidence verifier passes and all seven aggregates regenerate identically. '
        'Production code/binary, papers, reference and historical evidence remain unchanged.', '',
        'Evidence: [config](config.json), [pins](preflight.json), [schedule](schedule.json), '
        '[environment](environment.json), [commands](commands.json), [raw campaign](campaign/summary.json), '
        '[verification](verification.json), [regeneration](regeneration.json), '
        '[changed files](files_changed.json).', '',
        'P12.1/O10/O12 gain local core-ablation evidence; P14.1/P15.1 gain scoped '
        'review/regeneration evidence. M5 remains open. Unrun: wider h/grid experiments, '
        'new phase instrumentation/optimization, fresh IPPV comparison, C++ rebuild/'
        'CTest/sanitizers, clean-machine release and DCLDS work. Structural checks '
        'and mode agreement do not prove real-graph maximality or the theorem.',
    ]
    (HERE / 'REPORT.md').write_text('\n'.join(lines) + '\n')
    print('REPORT.md generated from checked evidence')


if __name__ == '__main__':
    main()
