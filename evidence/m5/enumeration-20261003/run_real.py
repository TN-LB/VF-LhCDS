"""One predeclared 60-second adjacency diagnostic after correctness gates."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import save, sha256, parse_graph
from experiments.validate import parse_records, compare


def load(path):
    return json.loads(path.read_text())


def main():
    assert load(HERE / 'verification.json')['status'] == 'passed'
    binary = ROOT / 'build-m5-adjacency-release/vflhcds'
    previous = load(ROOT / 'evidence/m5/m4-mode-diagnostic-20261003/config.json')
    config = dict(previous, name='adjacency-enumeration-basic-diagnostic',
                  algorithms=[{'name': 'vf-adjacency-basic', 'kind': 'vf',
                               'executable': str(binary.relative_to(ROOT)), 'sha256': sha256(binary),
                               'options': {'core': 'off', 'footprints': 'sorted', 'enumeration': 'adjacency'}}])
    assert not (HERE / 'real-config.json').exists()
    save(HERE / 'real-config.json', config)
    baseline = ROOT / 'evidence/m5/harness-20261003/shared-real/runs/0000-1'
    baseline_manifest = load(baseline / 'manifest.json')
    assert baseline_manifest['status'] == 'completed' and baseline_manifest['validation']['passed']
    assert baseline_manifest['graph_sha256'] == config['cases'][0]['sha256']
    assert baseline_manifest['h'] == 3 and baseline_manifest['k'] == 5
    for name, digest in baseline_manifest['sha256'].items():
        assert sha256(baseline / name) == digest
    save(HERE / 'comparison-plan.json', {
        'reference_run': str(baseline.relative_to(ROOT)),
        'reference_manifest_sha256': sha256(baseline / 'manifest.json'),
        'reference_output_sha256': sha256(baseline / 'canonical_output.jsonl'),
        'scope': 'Compare only completed structurally checked outputs; historical IPPV timing is not a paired performance measurement.',
        'failure_policy': 'Retain timeout/error/mismatch; stop affected path without increasing the guard or changing another mechanism.'})
    command = [sys.executable, str(ROOT / 'experiments/run.py'), '--config', str(HERE / 'real-config.json'),
               '--evidence', str(HERE / 'real')]
    record = {'command': command, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'config_sha256': sha256(HERE / 'real-config.json')}
    save(HERE / 'real-command.json', record)
    with (HERE / 'real-driver.stdout').open('x') as so, (HERE / 'real-driver.stderr').open('x') as se:
        process = subprocess.run(command, cwd=ROOT, stdout=so, stderr=se)
    record.update(exit_code=process.returncode, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save(HERE / 'real-command.json', record)
    manifest = load(HERE / 'real/runs/0000-0/manifest.json')
    result = {'vf_status': manifest['status'], 'reference': str(baseline.relative_to(ROOT)),
              'maximality_or_completeness_proven': False, 'performance_comparison': 'not_performed'}
    if manifest['status'] == 'completed' and manifest['validation']['passed']:
        graph = parse_graph((ROOT / config['cases'][0]['graph']).read_text())
        left = parse_records((HERE / 'real/runs/0000-0/canonical_output.jsonl').read_text(), graph, 3)
        right = parse_records((baseline / 'canonical_output.jsonl').read_text(), graph, 3)
        result.update(compare(left, right, 5))
    else:
        result.update(level='not_compared', reason='VF did not produce a completed validated output')
    save(HERE / 'real-comparison.json', result)
    print(json.dumps(result, indent=2), flush=True)
    return 0 if process.returncode == 0 and result.get('tie_aware_match') else 1


if __name__ == '__main__':
    raise SystemExit(main())
