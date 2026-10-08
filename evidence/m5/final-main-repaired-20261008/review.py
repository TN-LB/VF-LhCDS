"""Descriptive D041 paired results and environment observations; no new runs."""
from collections import Counter
import argparse
import json
import math
from pathlib import Path
import re
import statistics
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256


def read(path):
    return json.loads(path.read_text())


def spread(values):
    return {'median': statistics.median(values), 'min': min(values), 'max': max(values)} if values else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'review')
    target = parser.parse_args().output
    target.mkdir()
    aggregate = HERE / 'aggregate/main'
    campaign = HERE / 'main/campaign'
    config = read(campaign / 'config.json')
    cells, runs = read(aggregate / 'cells.json'), read(aggregate / 'runs.json')
    vf, ippv = [a['name'] for a in config['algorithms']]
    assert config['algorithms'][0]['kind'] == 'vf' and config['algorithms'][1]['kind'] == 'ippv'
    comparisons = []
    for case in config['cases']:
        v, i = [next(c for c in cells if c['case'] == case['name'] and c['algorithm'] == a) for a in (vf, ippv)]
        eligible = v['complete_repetitions_agree'] and i['complete_repetitions_agree']
        row = {'case': case['name'], 'h': case['h'], 'k': case['k'], 'eligible': eligible,
               'graph_sha256': case['sha256']}
        if eligible:
            ratios = []
            for repeat in range(config['repeats']):
                vr, ir = [next(r for r in runs if r['case'] == case['name'] and r['repeat'] == repeat and r['algorithm'] == a) for a in (vf, ippv)]
                ratios.append(ir['native_wall_seconds'] / vr['native_wall_seconds'])
            row.update(vf_wall_seconds=v['wall_median_seconds'], ippv_wall_seconds=i['wall_median_seconds'],
                       ippv_over_vf_median_wall=i['wall_median_seconds'] / v['wall_median_seconds'],
                       paired_ippv_over_vf_wall=ratios, paired_ratio_spread=spread(ratios),
                       vf_peak_rss_bytes=v['rss_median_bytes'], ippv_peak_rss_bytes=i['rss_median_bytes'],
                       vf_cpu_seconds=v['cpu_median_seconds'], ippv_cpu_seconds=i['cpu_median_seconds'],
                       vf_wall_max_over_min=v['wall_max_seconds']/v['wall_min_seconds'],
                       ippv_wall_max_over_min=i['wall_max_seconds']/i['wall_min_seconds'])
        comparisons.append(row)
    save(target / 'paired.json', comparisons)
    eligible = [c for c in comparisons if c['eligible']]
    ratios = [c['ippv_over_vf_median_wall'] for c in eligible]
    save(target / 'coverage.json', {
         'planned_cases': len(comparisons), 'complete_agreeing_five_repeat_cases': len(eligible),
         'lower_vf_wall_median_cases': sum(r > 1 for r in ratios),
         'equal_wall_median_cases': sum(r == 1 for r in ratios),
         'lower_ippv_wall_median_cases': sum(r < 1 for r in ratios),
         'geometric_mean_ippv_over_vf_median_wall': math.exp(statistics.mean(map(math.log, ratios))) if ratios else None,
         'geometric_mean_scope': 'common completed and validated five-repeat cases, no historical pooling',
         'interpretation': 'descriptive observed medians, no significance threshold or significance claim'})
    snapshots = [read(p) for p in sorted(campaign.glob('block-*.json'))]
    swaps = []
    for snapshot in snapshots:
        result = re.search(r'used\s*=\s*([0-9.]+)M', snapshot['observations']['swap']['stdout'])
        if result:
            swaps.append(float(result.group(1)))
    environment = {'observations': len(snapshots),
        'load_1_5_15_minute_ranges': [spread([s['load_average'][i] for s in snapshots]) for i in range(3)],
        'swap_used_reported_M': spread(swaps), 'swap_available_observations': len(swaps),
        'power_sources': dict(Counter(s['power_state']['source'] for s in snapshots)),
        'power_setting_hashes': sorted({s['power_state']['settings_sha256'] for s in snapshots}),
        'temperature': None, 'cpu_frequency': None,
        'scope': 'before/after blocks, not continuous monitoring; nonzero host load and swap are retained, no exclusions'}
    save(target / 'environment.json', environment)
    lines = ['# D041 paired descriptive results', '',
        'Five repeats per cell. Times are native process medians; CPU is user + system. External validation is excluded and native IPPV verification is included. IPPV/VF > 1 means the VF median is lower. These are observations on this host, not significance tests. Full min/max and all raw runs are in ../aggregate/main/TABLE.md and cells.json.', '',
        '| Case | VF wall s | IPPV wall s | IPPV/VF | Paired ratio median [min, max] | VF / IPPV RSS MiB | VF / IPPV CPU s |',
        '|---|---:|---:|---:|---|---:|---:|']
    for c in comparisons:
        if not c['eligible']:
            lines.append(f"| {c['case']} | unavailable | unavailable | unavailable | incomplete or disagreement | unavailable | unavailable |")
            continue
        r = c['paired_ratio_spread']
        lines.append(f"| {c['case']} | {c['vf_wall_seconds']:.4f} | {c['ippv_wall_seconds']:.4f} | {c['ippv_over_vf_median_wall']:.3f} | {r['median']:.3f} [{r['min']:.3f}, {r['max']:.3f}] | {c['vf_peak_rss_bytes']/2**20:.2f} / {c['ippv_peak_rss_bytes']/2**20:.2f} | {c['vf_cpu_seconds']:.4f} / {c['ippv_cpu_seconds']:.4f} |")
    (target / 'TABLE.md').write_text('\n'.join(lines)+'\n')
    sources = [aggregate / n for n in ('cells.json', 'runs.json', 'totals.json')] + [campaign / 'config.json'] + list(campaign.glob('block-*.json'))
    save(target / 'provenance.json', {'script_sha256': sha256(Path(__file__)),
         'source_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted(sources)},
         'native_algorithm_runs': 0})
    print(json.dumps(read(target / 'coverage.json'), indent=2))


if __name__ == '__main__':
    main()
