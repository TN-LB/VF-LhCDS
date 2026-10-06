"""Freeze and run the prepared 48-child pilot once; retain every outcome."""
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

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from experiments.run import load_config,schedule
from experiments.support import file_hashes,save,sha256

def read(path):return json.loads(path.read_text())

def main():
    assert not (HERE/'launch.json').exists(),'No automatic retry'
    prior=ROOT/'evidence/m5/condmat-pair-20261006'
    draft=read(prior/'next-pilot-draft.json')
    config=copy.deepcopy(draft)
    config.update(name='two-graphs-membership-ippv-h3-pilot-20261006',scope='approved_campaign')
    assert {k for k in config if config[k]!=draft[k]}=={'name','scope'}
    save(HERE/'config.json',config)
    assert load_config(HERE/'config.json')==config
    save(HERE/'schedule.json',schedule(config))
    old_pins=read(prior/'preflight.json')
    keys=('paper_sha256','reference_sha256','production_source_sha256','binary_sha256',
          'provenance_sha256','pinned_harness_sha256','library_sha256','old_probe_sha256')
    pins={key:old_pins[key] for key in keys}
    before=read(HERE/'files-before.json')
    changes={}
    for name in ('experiments/run.py','experiments/test_harness.py'):
        assert pins['pinned_harness_sha256'][name]==before[name]
        changes[name]={'before_sha256':before[name],'after_sha256':sha256(ROOT/name)}
        pins['pinned_harness_sha256'][name]=sha256(ROOT/name)
    assert read(HERE/'pytest-command.json')['exit_code']==0
    for group in pins.values():
        for name,digest in group.items():assert sha256(ROOT/name)==digest,name
    lock=read(ROOT/'baselines/ippv/source-lock.json')
    assert len(lock['patches'])==7
    for patch in lock['patches']:assert sha256(ROOT/patch['path'])==patch['sha256']
    for name,digest in lock['patched_source_sha256'].items():
        assert sha256(ROOT/'.deps/baselines/ippv'/name)==digest,name
    pins['harness_changes']=changes
    pins['pytest_command_sha256']=sha256(HERE/'pytest-command.json')
    pins['ippv_source_sha256']=lock['patched_source_sha256']
    pins['ippv_patches']=lock['patches']
    pins['baseline_lock_sha256']=sha256(ROOT/'baselines/ippv/source-lock.json')
    pins['historical_evidence_sha256']={base:file_hashes(ROOT/base) for base in old_pins['historical_evidence_sha256']}
    pins['historical_evidence_sha256'][str(prior.relative_to(ROOT))]=file_hashes(prior)
    for base,inventory in old_pins['historical_evidence_sha256'].items():
        assert pins['historical_evidence_sha256'][base]==inventory,base
    pins['draft_sha256']=sha256(prior/'next-pilot-draft.json')
    pins['configuration_sha256']=sha256(HERE/'config.json')
    pins['decision_log_sha256']=sha256(ROOT/'docs/DECISIONS.md')
    pins['runner_sha256']=sha256(Path(__file__))
    save(HERE/'preflight.json',pins)
    old_env=read(prior/'environment.json')
    hardware={}
    for key in old_env['hardware']:
        cmd=['sysctl','-n',key]
        proc=subprocess.run(cmd,capture_output=True,text=True)
        hardware[key]={'command':cmd,'exit_code':proc.returncode,'stdout':proc.stdout.strip(),'stderr':proc.stderr.strip()}
    environment={key:os.environ.get(key) for key in old_env['environment']}
    snapshot={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'platform':platform.platform(),'python':sys.version,'hardware':hardware,'environment':environment,
              'host_label_sha256':hashlib.sha256(platform.node().encode()).hexdigest(),
              'host_label_note':'Recorded label only; not treated as a stable hardware identifier.',
              'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'dirty_tree':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)}
    save(HERE/'environment.json',snapshot)
    assert snapshot['platform']==old_env['platform'] and hardware==old_env['hardware'] and environment==old_env['environment']
    cmd=[str(ROOT/'.venv/bin/python'),'experiments/run.py','--config',str((HERE/'config.json').relative_to(ROOT)),
         '--evidence',str((HERE/'campaign').relative_to(ROOT)),'--stop-on-failure','--continue-on-timeout']
    save(HERE/'launch.json',{'command':cmd,'cwd':str(ROOT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'configuration_sha256':sha256(HERE/'config.json'),'preflight_sha256':sha256(HERE/'preflight.json'),
          'environment_sha256':sha256(HERE/'environment.json')})
    print('Preflight passed; starting the 48-call seeded VF/IPPV pilot; native timeouts are retained and the schedule continues.',flush=True)
    start=time.monotonic()
    with (HERE/'driver.stdout').open('w') as out,(HERE/'driver.stderr').open('w') as err:
        proc=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=err)
    completion={'command':cmd,'exit_code':proc.returncode,'wall_seconds':time.monotonic()-start,
          'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'timing_scope':'Entire driver, including separate validation and evidence I/O.'}
    save(HERE/'completion.json',completion)
    print(json.dumps(completion),flush=True)
    return proc.returncode

if __name__=='__main__':raise SystemExit(main())
