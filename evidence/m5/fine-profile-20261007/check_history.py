"""Check every matching earlier core-off run; never compare or pool timings."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256


def read(path):
    return json.loads(path.read_text())


config = read(HERE / 'config.json')
pins = read(HERE / 'preflight.json')['historical_evidence_sha256']
checks = []
for case in config['real']:
    diagnostic = HERE / 'runs' / (case['name'] + '-release')
    events = [json.loads(line) for line in (diagnostic / 'stderr.txt').read_text().splitlines()]
    queries = [event['stats'] for event in events if event.get('phase') == 'query']
    current_complete = read(diagnostic / 'process.json')['status'] == 'completed'
    matches = 0
    for manifest_path in sorted((ROOT / 'evidence/m5/core-ablation-20261006/campaign/runs').glob('*/manifest.json')):
        manifest = read(manifest_path)
        if (manifest['graph_sha256'] != case['graph_sha256']
                or manifest['h'] != case['h'] or manifest['k'] != case['k']
                or manifest['algorithm']['options'] != {'core': 'off', 'footprints': 'membership', 'enumeration': 'adjacency'}):
            continue
        previous = manifest_path.parent
        assert manifest['algorithm']['sha256'] == read(HERE / 'binaries.json')[config['production_binary']]
        paths = [manifest_path, previous / 'process.json', previous / 'stderr.txt', previous / 'canonical_output.jsonl']
        for path in paths:
            assert sha256(path) == pins[str(path.relative_to(ROOT))]
        assert read(previous / 'process.json')['status'] == 'completed'
        counters = read(previous / 'stderr.txt')['counters']
        row = {'case': case['name'], 'historical_run': str(previous.relative_to(ROOT)),
               'historical_total_queries': len(counters['queries']), 'compared_query_prefix': len(queries),
               'prefix_equal': queries == counters['queries'][:len(queries)],
               'complete_output_equal': ((diagnostic / 'stdout.txt').read_bytes() == (previous / 'canonical_output.jsonl').read_bytes()) if current_complete else None}
        assert row['prefix_equal'] and row['complete_output_equal'] is not False
        checks.append(row)
        matches += 1
    assert matches == 3
save(HERE / 'historical-consistency.json', {'passed': True, 'checks': checks,
     'scope': 'query-prefix/output consistency only; no historical timing comparison or complete CondMat output claim'})
print(json.dumps({'passed': True, 'matched_runs': len(checks)}))
