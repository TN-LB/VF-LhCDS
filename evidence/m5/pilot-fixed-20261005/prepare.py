"""Freeze the authorized repaired-baseline rerun; launch no algorithms."""
import copy
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import save, sha256, file_hashes
OUT = Path(__file__).resolve().parent
old = ROOT / 'evidence/m5/pilot-20261005'
previous = json.loads((old / 'preflight.json').read_text())
config = json.loads((old / 'config.json').read_text())
original = copy.deepcopy(config)
config['name'] = 'approved-two-local-graphs-seven-patch-ippv-pilot-20261005'
a = config['algorithms'][1]
a.update(name='ippv-seven-patches', executable='build-ippv-fixed-release/IPPV')
a['sha256'] = sha256(ROOT / a['executable'])
unchanged = copy.deepcopy(config)
unchanged['name'] = original['name']
unchanged['algorithms'][1] = original['algorithms'][1]
assert unchanged == original
assert schedule(config) == json.loads((old / 'schedule.json').read_text())
save(OUT / 'config.json', config)
assert load_config(OUT / 'config.json') == config
save(OUT / 'schedule.json', schedule(config))
pins = {key: previous[key] for key in ('paper_sha256', 'reference_sha256', 'production_source_sha256', 'draft_artifacts_sha256')}
assert pins['paper_sha256'] == json.loads((ROOT / 'review/source_snapshot_sha256.json').read_text())['sha256']
for group in pins.values():
    for name, digest in group.items():
        assert sha256(ROOT / name) == digest, name
lock = json.loads((ROOT / 'baselines/ippv/source-lock.json').read_text())
assert len(lock['patches']) == 7
for patch in lock['patches']:
    assert sha256(ROOT / patch['path']) == patch['sha256']
for name, digest in lock['patched_source_sha256'].items():
    assert sha256(ROOT / '.deps/baselines/ippv' / name) == digest, name
pins['ippv_source_sha256'] = lock['patched_source_sha256']
pins['baseline_lock_sha256'] = sha256(ROOT / 'baselines/ippv/source-lock.json')
pins['patches'] = lock['patches']
pins['binary_sha256'] = {a['executable']: a['sha256'] for a in config['algorithms']}
pins['provenance_sha256'] = {str(Path(a['executable']).with_suffix('.provenance.json')): sha256((ROOT / a['executable']).with_suffix('.provenance.json')) for a in config['algorithms']}
pins['graph_sha256'] = {c['graph']: c['sha256'] for c in config['cases']}
sources = sorted((ROOT / 'experiments').glob('*.py')) + sorted((ROOT / 'baselines/ippv').glob('*.py'))
pins['pinned_harness_sha256'] = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
for p in sources:
    destination = OUT / 'source' / p.relative_to(ROOT)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, destination)
pins['historical_pilot_sha256'] = file_hashes(old)
for name, digest in json.loads((old / 'campaign/checksums.json').read_text()).items():
    assert sha256(old / 'campaign' / name) == digest, name
pins['repair_evidence_sha256'] = {name: sha256(ROOT / name) for name in ['evidence/m5/ippv/disagreement-20261005/REPORT.md', 'evidence/m5/ippv/disagreement-20261005/verification.json']}
pins['documents_before_sha256'] = {name: sha256(ROOT / name) for name in ['docs/DECISIONS.md', 'docs/TASKS.md', 'docs/CLAIM_TRACEABILITY.md', 'evidence/m5/REPORT.md', 'experiments/README.md']}
pins['utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
pins['head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
pins['dirty_tree'] = subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True)
save(OUT / 'preflight.json', pins)
save(OUT / 'approval.json', {'date_local': '2026-10-05', 'recorded_utc': pins['utc'], 'decision_id': 'D031', 'owner_reply': '好的。现在继续跑实验', 'status': 'accepted', 'scope': 'Fresh full 48-call rerun with the repaired seven-patch IPPV; reuse unchanged D030 graphs/grid/resources/seed/repetitions/stop policy. No old/new timings mixed.', 'previous_config': str((old / 'config.json').relative_to(ROOT)), 'previous_config_sha256': sha256(old / 'config.json'), 'config_sha256': sha256(OUT / 'config.json'), 'schedule_sha256': sha256(OUT / 'schedule.json'), 'changed_fields': ['name', 'algorithms[1].name', 'algorithms[1].executable', 'algorithms[1].sha256'], 'stop_on_failure': True, 'planned_native_calls': 48})
print(json.dumps({'preflight': 'passed', 'papers': len(pins['paper_sha256']), 'production_sources': len(pins['production_source_sha256']), 'reference_files': len(pins['reference_sha256']), 'ippv_sources': len(pins['ippv_source_sha256']), 'patches': len(lock['patches']), 'harness_sources': len(sources), 'historical_pilot_files': len(pins['historical_pilot_sha256']), 'planned_calls': 48}))
