"""Executed M3 gates with per-command logs and immutable input/source manifests."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys


def main():
    root=Path(__file__).resolve().parents[1];output=Path(sys.argv[1]).resolve()
    output.mkdir(parents=True,exist_ok=False)
    paths=[Path('CMakeLists.txt')]
    for directory in ['include','src','tests','validation','scripts']:
        paths.extend(p for p in (root/directory).rglob('*') if p.is_file() and p.suffix in {'.cpp','.hpp','.py'})
    metadata={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cwd':str(root),'platform':platform.platform(),
              'python':sys.version,'python_executable':sys.executable,'cmake':shutil.which('cmake'),'ctest':shutil.which('ctest'),
              'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS'),'UBSAN_OPTIONS':os.environ.get('UBSAN_OPTIONS'),
              'source_sha256':{str(p.resolve().relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (output/'environment.json').write_text(json.dumps(metadata,indent=2)+'\n')
    commands=[]
    for build,kind in [('build','Debug'),('build-sanitize','Debug'),('build-release','Release'),('build-relwithdebinfo','RelWithDebInfo'),('build-production','Release')]:
        configure=['cmake','-S','.','-B',build,f'-DCMAKE_BUILD_TYPE={kind}']
        if build=='build-sanitize':configure+=['-DVFLHCDS_ENABLE_SANITIZERS=ON']
        if build=='build-production':configure+=['-DBUILD_TESTING=OFF']
        commands.extend([configure,['cmake','--build',build,'-j2']])
        if build!='build-production':commands.append(['ctest','--test-dir',build,'--output-on-failure','-V'])
        if build in ('build','build-sanitize'):
            for tier in ['smoke','exhaustive-small','seeded','higher-h']:
                commands.append(['python','validation/solver_campaign.py','--probe',build+'/vflhcds_m3_probe','--tier',tier,'--output',str(output/(build+'-'+tier))])
            # M2 oracle/capacity interfaces remain regression gates after extension.
            for tier in ['exhaustive-small','seeded','higher-h']:
                commands.append(['python','validation/oracle_campaign.py','--probe',build+'/vflhcds_m2_probe','--tier',tier,'--output',str(output/(build+'-m2-'+tier))])
    commands.extend([
        ['python','-m','pytest','reference/tests','-q'],
        ['python','validation/run_solver.py','--executable','build-production/vflhcds','--evidence',str(output/'cli-definition-run'),'--check-reference','--','solve','--graph','reference/fixtures/bridged_triangles.graph','--h','3','--all'],
        ['python','scripts/verify_papers.py'],['git','diff','--check'],['build/vflhcds','print-build-info'],['cmake','--version'],['c++','--version']])
    records=[]
    for i,command in enumerate(commands,1):
        print('RUN '+shlex.join(command),flush=True)
        stdout,stderr=output/f'{i:02d}.stdout',output/f'{i:02d}.stderr';start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        with stdout.open('w') as out,stderr.open('w') as err:result=subprocess.run(command,cwd=root,stdout=out,stderr=err,check=False)
        records.append({'command':command,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        'exit_code':result.returncode,'stdout':stdout.name,'stderr':stderr.name,
                        'stdout_sha256':hashlib.sha256(stdout.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(stderr.read_bytes()).hexdigest()})
        (output/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
        if result.returncode:
            print(stdout.read_text()+stderr.read_text(),flush=True);raise SystemExit(result.returncode)
        print('exit=0',flush=True)


if __name__=='__main__':main()
