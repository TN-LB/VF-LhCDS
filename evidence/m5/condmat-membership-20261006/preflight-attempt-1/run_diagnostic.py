"""Freeze and execute one existing membership-mode diagnostic; no retries."""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import file_hashes, save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    assert not (HERE / 'launch.json').exists(), 'No repeated diagnostic launch'
    previous = ROOT / 'evidence/m5/condmat-phase-20261005'
    draft_path = previous / 'draft-membership-config.json'
    draft = read(draft_path)
    config = copy.deepcopy(draft)
    config.update(name='ca-condmat-membership-mode-diagnostic-20261006', scope='diagnostic')
    assert {k for k in config if config[k] != draft[k]} == {'name', 'scope'}
    save(HERE / 'config.json', config)
    assert load_config(HERE / 'config.json') == config
    save(HERE / 'schedule.json', schedule(config))
    old_pins = read(previous / 'preservation-before.json')
    pin_keys = ('paper_sha256', 'reference_sha256', 'production_source_sha256', 'binary_sha256',
                'provenance_sha256', 'pinned_harness_sha256', 'library_sha256', 'old_probe_sha256')
    pins = {k: old_pins[k] for k in pin_keys}
    for group in pins.values():
        for name, digest in group.items():
            assert sha256(ROOT / name) == digest, name
    pins['ippv_source_sha256'] = old_pins['ippv_source_sha256']
    for name, digest in pins['ippv_source_sha256'].items():
        assert sha256(ROOT / '.deps/baselines/ippv' / name) == digest, name
    pins['baseline_lock_sha256'] = old_pins['baseline_lock_sha256']
    assert sha256(ROOT / 'baselines/ippv/source-lock.json') == pins['baseline_lock_sha256']
    pins['historical_evidence_sha256'] = {
        str(base.relative_to(ROOT)): file_hashes(base) for base in
        [ROOT/'evidence/m5/pilot-20261005', ROOT/'evidence/m5/pilot-fixed-20261005', previous]}
    pins['proposal_sha256'] = {str(path.relative_to(ROOT)): sha256(path) for path in [draft_path, previous/'NEXT_STEP.md']}
    pins['documents_before_sha256'] = {name: sha256(ROOT/name) for name in
        ['docs/TASKS.md','docs/CLAIM_TRACEABILITY.md','experiments/README.md','evidence/m5/REPORT.md']}
    pins['config_sha256'] = sha256(HERE/'config.json')
    pins['decision_log_sha256'] = sha256(ROOT/'docs/DECISIONS.md')
    pins['runner_sha256'] = sha256(Path(__file__))
    save(HERE/'preflight.json', pins)
    old_env = read(ROOT/'evidence/m5/pilot-fixed-20261005/environment.json')
    assert platform.platform() == old_env['platform']
    assert hashlib.sha256(platform.node().encode()).hexdigest() == old_env['host_id_sha256']
    environment = {k: os.environ.get(k) for k in old_env['environment']}
    assert environment == old_env['environment']
    save(HERE/'environment.json', {'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'platform':platform.platform(),'python':sys.version,'host_id_sha256':old_env['host_id_sha256'],
        'hardware':old_env['hardware'],'hardware_provenance':'Prior same-host D031 measurement, not a new sysctl read.',
        'environment':environment,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'dirty_tree':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)})
    cmd = [str(ROOT/'.venv/bin/python'), 'experiments/run.py', '--config', str((HERE/'config.json').relative_to(ROOT)),
           '--evidence', str((HERE/'campaign').relative_to(ROOT)), '--stop-on-failure']
    save(HERE/'launch.json', {'command':cmd,'cwd':str(ROOT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'configuration_sha256':sha256(HERE/'config.json'),'preflight_sha256':sha256(HERE/'preflight.json'),
        'environment_sha256':sha256(HERE/'environment.json')})
    print('Preflight passed. Starting one membership-mode child with a 60-second guard.', flush=True)
    start=time.monotonic()
    with (HERE/'driver.stdout').open('w') as out,(HERE/'driver.stderr').open('w') as err:
        proc=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=err)
    result={'command':cmd,'exit_code':proc.returncode,'wall_seconds':time.monotonic()-start,
            'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope':'Entire driver, including external validation and evidence I/O; not native algorithm time.'}
    save(HERE/'completion.json',result)
    print(json.dumps(result),flush=True)
    return proc.returncode

if __name__=='__main__':
    raise SystemExit(main())
