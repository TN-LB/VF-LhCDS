"""Reuse the existing strict-ablation aggregator without changing historical files."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256

spec = importlib.util.spec_from_file_location('prior_summary', ROOT / 'evidence/m5/core-ablation-20261006/summarize.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def read(path):
    return json.loads(path.read_text())


def summarize(output):
    prior.HERE = HERE
    prior.summarize(output)
    summary = read(HERE / 'campaign/summary.json')
    config = read(HERE / 'config.json')
    history_checks, within_case = [], {}
    for row in summary['runs']:
        if row['status'] != 'completed':
            continue
        current = HERE / 'campaign' / row['directory']
        manifest = read(current / 'manifest.json')
        case = next(case for case in config['cases'] if case['name'] == row['case'])
        counters = manifest['native_status']['counters']
        data = (current / 'canonical_output.jsonl').read_bytes()
        if row['case'] in within_case:
            assert within_case[row['case']] == (data, counters)
        else:
            within_case[row['case']] = (data, counters)
        matched = 0
        for path in sorted((ROOT / 'evidence/m5/core-ablation-20261006/campaign/runs').glob('*/manifest.json')):
            old = read(path)
            if (old['graph_sha256'] != case['sha256'] or old['h'] != case['h'] or old['k'] != case['k']
                    or old['algorithm']['options']['core'] != 'off'):
                continue
            assert old['status'] == 'completed'
            assert data == (path.parent / 'canonical_output.jsonl').read_bytes()
            assert counters == old['native_status']['counters']
            matched += 1
        assert matched == 3
        history_checks.append({'run': row['directory'], 'matching_historical_outputs_and_counters': matched})
    save(output / 'equivalence.json', {'all_completed_outputs_and_counters_equal_within_case': True,
         'historical_checks': history_checks, 'scope': 'exact output/counters only; no historical timing pooling'})
    save(output / 'wrapper-provenance.json', {'wrapper_sha256': sha256(Path(__file__)),
         'aggregator_sha256': sha256(Path(prior.__file__))})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'aggregate')
    summarize(parser.parse_args().output)
