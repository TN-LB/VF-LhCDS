"""Read the current diagnostic hardware profile after a host-label mismatch."""
import datetime,hashlib,json,os,platform,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
prior=json.loads((ROOT/'evidence/m5/pilot-fixed-20261005/environment.json').read_text())
hardware={}
for key in prior['hardware']:
    cmd=['sysctl','-n',key]
    proc=subprocess.run(cmd,capture_output=True,text=True)
    hardware[key]={'command':cmd,'exit_code':proc.returncode,'stdout':proc.stdout.strip(),'stderr':proc.stderr.strip()}
current={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'python':sys.version,
         'host_id_sha256':hashlib.sha256(platform.node().encode()).hexdigest(),'hardware':hardware,
         'environment':{k:os.environ.get(k) for k in prior['environment']}}
current['profile_matches_prior']=(current['platform']==prior['platform'] and hardware==prior['hardware'] and current['environment']==prior['environment'])
current['host_label_matches_prior']=current['host_id_sha256']==prior['host_id_sha256']
current['identity_note']='platform.node hashes a host label, not a stable hardware identifier. Hardware/profile equality does not independently prove machine identity.'
(HERE/'current-environment.json').write_text(json.dumps(current,indent=2)+'\n')
print(json.dumps({'profile_matches_prior':current['profile_matches_prior'],'host_label_matches_prior':current['host_label_matches_prior'],'hardware':hardware}))
raise SystemExit(0 if current['profile_matches_prior'] else 1)
