"""Aggregate saved pilot records only; never launch or repair an algorithm."""
import argparse
import collections
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import statistics


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def density(record):
    return Fraction(int(record['density_num']), int(record['density_den']))


def summarize(output):
    campaign = HERE / 'campaign'
    config, summary = read(campaign / 'config.json'), read(campaign / 'summary.json')
    stopped = read(campaign / 'stopped.json')
    inventory = read(campaign / 'checksums.json')
    for name, expected in inventory.items():
        assert digest(campaign / name) == expected, name
    policy = read(campaign / 'execution-policy.json')
    assert policy['stop_on_failure'] is True
    executed = {row['directory'] for row in summary['runs']}
    unrun = [row for row in policy['planned_runs'] if row['directory'] not in executed]
    assert unrun == stopped['unrun']
    assert all(not (campaign / row['directory']).exists() for row in unrun)
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for row in summary['runs']:
        manifest = read(campaign / row['directory'] / 'manifest.json')
        native, validation = manifest['native'], manifest.get('external_validation', {})
        checks = manifest['validation']
        assert native['native_exit_code'] == validation['native_exit_code'] == 0
        assert manifest['status'] == row['status'] == 'completed' and checks['passed']
        assert native['finished_utc'] <= validation['started_utc']
        rows.append({**row, 'native_exit_code': native['native_exit_code'],
                     'native_wall_seconds': native['wall_seconds'],
                     'native_peak_rss_bytes': native['peak_rss_bytes'],
                     'native_user_seconds': native['user_seconds'],
                     'native_system_seconds': native['system_seconds'],
                     'validation_wall_seconds': validation['wall_seconds'],
                     'validation_peak_rss_bytes': validation['peak_rss_bytes'],
                     'validation_exit_code': validation['native_exit_code'],
                     'validation_level': checks['level'],
                     'completeness_certified': checks['completeness_certified'],
                     'output_count': checks['output_count'],
                     'phase_wall_seconds': manifest['phase_wall_seconds'],
                     'manifest_sha256': digest(campaign / row['directory'] / 'manifest.json')})
    cells = []
    for case in config['cases']:
        comparisons = [c for c in summary['comparisons'] if c['case'] == case['name']]
        for algorithm in config['algorithms']:
            selected = [r for r in rows if r['case'] == case['name'] and r['algorithm'] == algorithm['name']]
            times = [r['native_wall_seconds'] for r in selected]
            rss = [r['native_peak_rss_bytes'] for r in selected]
            eligible = len(selected) == config['repeats'] and len(comparisons) == config['repeats'] and all(c['tie_aware_match'] for c in comparisons)
            cells.append({'case': case['name'], 'algorithm': algorithm['name'],
                          'planned_repeats': config['repeats'], 'recorded_repeats': len(selected),
                          'unrun_repeats': config['repeats'] - len(selected),
                          'statuses': dict(collections.Counter(r['status'] for r in selected)),
                          'raw_wall_seconds': times, 'raw_peak_rss_bytes': rss,
                          'three_repeat_agreement_available': eligible,
                          'wall_median_seconds': statistics.median(times) if eligible else None,
                          'wall_min_seconds': min(times) if eligible else None,
                          'wall_max_seconds': max(times) if eligible else None,
                          'rss_median_bytes': statistics.median(rss) if eligible else None,
                          'rss_min_bytes': min(rss) if eligible else None,
                          'rss_max_bytes': max(rss) if eligible else None,
                          'semantic_hashes': sorted({r['semantic_sha256'] for r in selected}),
                          'strict_matches': sum(c['strict_match'] for c in comparisons),
                          'tie_aware_matches': sum(c['tie_aware_match'] for c in comparisons),
                          'pair_comparisons': len(comparisons)})
    save(output / 'runs.json', rows)
    save(output / 'cells.json', cells)
    save(output / 'unrun.json', unrun)
    totals = {'planned_native_runs': len(policy['planned_runs']), 'recorded_native_runs': len(rows),
              'external_validators_completed': len(rows), 'unrun_native_runs': len(unrun),
              'native_statuses': dict(collections.Counter(r['status'] for r in rows)),
              'paired_comparisons': len(summary['comparisons']),
              'strict_matches': sum(c['strict_match'] for c in summary['comparisons']),
              'tie_aware_matches': sum(c['tie_aware_match'] for c in summary['comparisons']),
              'tie_aware_disagreements': sum(not c['tie_aware_match'] for c in summary['comparisons']),
              'campaign_exit_code': read(HERE / 'completion.json')['exit_code'],
              'campaign_wall_seconds': read(HERE / 'completion.json')['wall_seconds'],
              'stop_reason': stopped['reason'], 'completeness_certified': False,
              'raw_inventory_entries_verified': len(inventory)}
    save(output / 'totals.json', totals)
    # Preserve the original observed disagreement. This is not failure minimization.
    failure = output / 'failure'; failure.mkdir()
    case = next(c for c in config['cases'] if c['name'] == stopped['reason']['case'])
    graph = ROOT / case['graph']; assert digest(graph) == case['sha256']
    shutil.copyfile(graph, failure / 'original.graph')
    pair = [r for r in rows if r['case'] == case['name'] and r['repeat'] == stopped['reason']['repeat']]
    observed, sources = {}, {}
    for row in pair:
        path = campaign / row['directory']
        observed[row['algorithm']] = records(path / 'canonical_output.jsonl')
        shutil.copyfile(path / 'canonical_output.jsonl', failure / (row['algorithm'] + '.jsonl'))
        sources[row['algorithm']] = {'run_directory': str(path.relative_to(ROOT)),
                                    'manifest_sha256': digest(path / 'manifest.json'),
                                    'native_command': read(path / 'process.json')['command'],
                                    'semantic_sha256': row['semantic_sha256']}
    algorithms = list(observed)
    details = {}
    for name, other in [(algorithms[0], algorithms[1]), (algorithms[1], algorithms[0])]:
        other_sets = {tuple(r['vertices']) for r in observed[other]}
        cutoff = min(map(density, observed[name]))
        details[name] = {'cutoff': str(cutoff),
                         'sets_absent_from_other_output': [r for r in observed[name] if tuple(r['vertices']) not in other_sets],
                         'above_cutoff_sets_absent_from_other_output': [r for r in observed[name] if density(r) > cutoff and tuple(r['vertices']) not in other_sets]}
    save(failure / 'reproducer.json', {'case': case, 'repeat': stopped['reason']['repeat'],
                                    'seed': config['seed'], 'algorithm_sources': sources,
                                    'original_graph_sha256': digest(failure / 'original.graph'),
                                    'minimization': 'not run; owner-directed stop at disagreement',
                                    'root_cause': 'unresolved; no algorithm assigned fault',
                                    'details': details})
    lines = ['# Saved pilot measurements', '', 'Three-repeat summaries only where all three pairs have tie-aware agreement. Raw incomplete/mismatching and unrun cells remain in cells.json/runs.json.', '',
             '| Case | Algorithm | Runs / planned | Wall median [min, max] s | RSS median [min, max] bytes | Pair agreement |',
             '|---|---|---:|---|---|---:|']
    for cell in cells:
        timing = f"{cell['wall_median_seconds']:.6f} [{cell['wall_min_seconds']:.6f}, {cell['wall_max_seconds']:.6f}]" if cell['three_repeat_agreement_available'] else 'unavailable'
        memory = f"{cell['rss_median_bytes']} [{cell['rss_min_bytes']}, {cell['rss_max_bytes']}]" if cell['three_repeat_agreement_available'] else 'unavailable'
        lines.append(f"| {cell['case']} | {cell['algorithm']} | {cell['recorded_repeats']} / {cell['planned_repeats']} | {timing} | {memory} | {cell['tie_aware_matches']} / {cell['pair_comparisons']} |")
    (output / 'TABLE.md').write_text('\n'.join(lines) + '\n')
    save(output / 'provenance.json', {'script_sha256': digest(Path(__file__)),
                                    'raw_inventory_sha256': digest(campaign / 'checksums.json'),
                                    'summary_sha256': digest(campaign / 'summary.json'),
                                    'stopped_sha256': digest(campaign / 'stopped.json')})
    print(json.dumps(totals, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New aggregate directory; raw files remain immutable')
    summarize(parser.parse_args().output)
