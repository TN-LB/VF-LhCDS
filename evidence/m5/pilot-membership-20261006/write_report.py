"""Write a concise technical report from checked pilot artifacts."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def main():
    totals = read('aggregate/totals.json')
    cells = read('aggregate/cells.json')
    checks = read('verification.json')
    replay = read('regeneration.json')
    assert replay['passed']
    by_key = {(c['case'], c['algorithm']): c for c in cells}
    lines = [
        '# Membership / IPPV repeated pilot — 2026-10-06', '',
        f"Recorded **{totals['recorded_native_runs']}/48 native calls**: "
        f"{totals['native_statuses']}. {totals['external_validators_completed']} separate "
        f"structural validators pass; {totals['unrun_native_runs']} calls remain unrun. "
        f"Completed pairs: {totals['tie_aware_matches']} tie-aware matches, "
        f"{totals['strict_matches']} strict matches, {totals['tie_aware_disagreements']} "
        f"substantive disagreements. {totals['pairs_not_compared']} blocks have no complete comparison.", '',
        'Scope: CA-GrQc (5,242 vertices / 14,484 edges) and CA-CondMat '
        '(23,133 / 93,439), h=3, k={5,10,15,20}, three repetitions, seed 20261003. '
        'VF uses adjacency/membership/core-off; IPPV uses seven patches, iterations=10,p=0. '
        'Apple M1, 16 GiB, macOS 15.7.7, AppleClang 17 Release, Python 3.12.2; '
        'one worker, serial seeded order, 60-second native and separate validator guards, '
        'uncapped memory, uncontrolled cache, no warm-ups or retries.', '',
        '| Graph | k | VF median seconds / outcome | IPPV median seconds / outcome | Tie-aware pairs |',
        '|---|---:|---:|---:|---:|',
    ]
    for graph in ('ca-grqc', 'ca-condmat'):
        for k in (5, 10, 15, 20):
            name = f'{graph}-h3-k{k}'
            vf, ippv = [by_key[(name, a)] for a in ('vf-adjacency-membership', 'ippv-seven-patches')]
            def display(cell):
                if cell['three_repeat_measurements_available']:
                    return f"{cell['wall_median_seconds']:.6f} (3/3 complete)"
                return ', '.join(f'{n} {status}' for status, n in cell['statuses'].items()) or 'unrun'
            lines.append(f"| {graph} | {k} | {display(vf)} | {display(ippv)} | {vf['tie_aware_matches']}/3 |")
    lines += [
        '', 'Medians use all three scheduled successful runs of one algorithm/case. '
        'Timeouts are censored, never substituted as completion times. IPPV timings '
        'beside VF timeouts do not imply output agreement. Native timing includes '
        'each program’s own work, including IPPV candidate verification; separate '
        'external validation is excluded. [All raw timings, ranges and RSS](aggregate/TABLE.md).', '',
        f"All {checks['stable_completed_cells']} cells with completed outputs have stable "
        f"semantic hashes. The {checks['historical_grqc_exact_output_matches']} completed "
        'CA-GrQc outputs also exactly match the earlier repaired-baseline campaign; '
        'historical timings are kept separate. CA-CondMat’s earlier single k=5 VF '
        'completion in 38.525397500 seconds is not a guarantee of repeat completion '
        'under 60 seconds. This campaign does not isolate the cause of timing variation.', '',
        'Changes: `experiments.run.execute` adds explicit timeout continuation while '
        'retaining stops for other failures and substantive disagreement. Ten new '
        'control-path tests plus the existing suite pass: **133 passed**. Algorithm '
        'sources, binaries, four papers, independent reference and historical evidence '
        'remain unchanged. Saved-evidence verification passes; aggregation regenerates '
        f"{len(replay['identical_artifact_sha256'])} identical artifacts without solver reruns. "
        f"Driver exit: {totals['campaign_exit_code']} (non-success outcomes remain visible).", '',
        'Evidence: [config](config.json), [schedule](schedule.json), '
        '[source/data pins](preflight.json), [environment](environment.json), '
        '[native launch](launch.json), [completion](completion.json), '
        '[pytest command/result](pytest-command.json), [check commands](postprocess-commands.json), '
        '[verification](verification.json), [regeneration](regeneration.json), '
        '[changed files](files_changed.json). Raw logs/manifests are under `campaign/runs/`.', '',
        'P11.1/P11.2/P12.1/O12 gain scoped evidence; P14.1/P15.1 gain local review '
        'and table-regeneration evidence only. M5 remains open: no broader h/grid '
        'campaign, controlled ablations, clean-machine smoke, release package or '
        'DCLDS work. C++ builds/CTest/sanitizers were not rerun. Structural checks '
        'and cross-implementation agreement do not establish real-graph maximality '
        'or prove the theorem; IPPV’s known zero-density omission remains.',
    ]
    (HERE / 'REPORT.md').write_text('\n'.join(lines) + '\n')
    print('REPORT.md generated from checked evidence')


if __name__ == '__main__':
    main()
