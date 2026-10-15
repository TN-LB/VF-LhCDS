"""M7 development acceptance; no real-graph benchmark or formal resource freeze."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    output=Path(sys.argv[1]).resolve();output.mkdir(parents=True,exist_ok=False)
    paths=[ROOT/'CMakeLists.txt',ROOT/'cmake/build_info.cpp.in']
    for folder in ('src','include','tests','validation','reference','experiments/final_profile','scripts'):
        paths.extend(p for p in (ROOT/folder).rglob('*') if p.suffix in ('.cpp','.hpp','.py','.json') and p.is_file())
    environment={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'platform':platform.platform(),'python':sys.version,'python_executable':sys.executable,
        'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS'),'UBSAN_OPTIONS':os.environ.get('UBSAN_OPTIONS'),
        'scope':'development-only; one native validation process at a time; no timing conclusion',
        'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}}
    (output/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    cmake=str(ROOT/'.venv/bin/cmake');ctest=str(ROOT/'.venv/bin/ctest');python=sys.executable
    commands=[]
    for name,sanitize in [('debug',False),('sanitize',True)]:
        build='build-m7-'+name
        commands += [[cmake,'-S','.', '-B',build,'-DCMAKE_BUILD_TYPE=Debug',f'-DPython3_EXECUTABLE={python}',
                      '-DVFLHCDS_ENABLE_SANITIZERS='+('ON' if sanitize else 'OFF'),
                      '-DVFLHCDS_TEST_COUNT_MEMBERSHIP='+('ON' if sanitize else 'OFF')],
                     [cmake,'--build',build,'-j2'],[ctest,'--test-dir',build,'--output-on-failure','-V']]
        for tier in ['smoke','exhaustive-small','seeded','higher-h']:
            commands.append([python,'validation/m7_campaign.py','--probe',build+'/vflhcds_m3_probe',
                             '--tier',tier,'--output',str(output/(name+'-'+tier))])
    for name,kind,sanitize in [('release','Release',False),('sanitize','Debug',True)]:
        build='build-m7-profile-'+name
        commands += [[cmake,'-S','experiments/final_profile','-B',build,'-DCMAKE_BUILD_TYPE='+kind,
                      f'-DPython3_EXECUTABLE={python}','-DVFLHCDS_ENABLE_SANITIZERS='+('ON' if sanitize else 'OFF')],
                     [cmake,'--build',build,'-j2'],[ctest,'--test-dir',build,'--output-on-failure','-V'],
                     [python,'experiments/final_profile/verify_build.py',build,'--output',str(output/('profile-'+name+'-identity.json'))],
                     [python,'experiments/final_profile/validate.py','--build',build,'--output',str(output/('profile-'+name)),
                      '--work-modes','global','interval-scan','interval-reuse'],
                     [python,'experiments/final_profile/pack_evidence.py',str(output/('profile-'+name))]]
    commands += [[python,'scripts/verify_papers.py'],['git','diff','--check'],['c++','--version'],[cmake,'--version']]
    (output/'schedule.json').write_text(json.dumps(commands,indent=2)+'\n')
    results=[]
    for i,command in enumerate(commands,1):
        print('RUN '+shlex.join(command),flush=True)
        started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        outpath=output/f'{i:02d}.stdout';errpath=output/f'{i:02d}.stderr'
        with outpath.open('w') as out,errpath.open('w') as err:
            process=subprocess.run(command,cwd=ROOT,stdout=out,stderr=err,check=False)
        results.append({'command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'exit_code':process.returncode,'stdout':outpath.name,'stderr':errpath.name,
            'stdout_sha256':hashlib.sha256(outpath.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(errpath.read_bytes()).hexdigest()})
        (output/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
        print('exit='+str(process.returncode),flush=True)
        if process.returncode:
            print(outpath.read_text()[-8000:]+errpath.read_text()[-8000:],flush=True)
            raise SystemExit(process.returncode)

if __name__=='__main__':main()
