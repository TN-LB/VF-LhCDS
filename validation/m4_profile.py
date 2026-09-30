"""Paired local diagnostics only; all repeats retained, no M5 benchmark claim."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--executable',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    workload=Path('evidence/m4/profile_workload.json');config=json.loads(workload.read_text())
    baseline=json.loads(Path('evidence/m4/profile-before.json').read_text())[1:]
    expected={r['command'][1]:json.loads(r['stdout'])['semantic_sha256'] for r in baseline}
    records=[];groups={}
    modes=[('off','sorted'),('off','membership'),('safe','sorted'),('safe','membership')]
    for fixture in config['fixtures']:
        assert hashlib.sha256(Path(fixture['path']).read_bytes()).hexdigest()==fixture['sha256']
        for repeat in range(config['process_repetitions']):
            # Rotate mode order deterministically; retain every raw repetition.
            ordered=modes[repeat:]+modes[:repeat]
            for core,scan in ordered:
                command=[str(args.executable.resolve()),fixture['path'],str(fixture['h']),core,scan]
                result=subprocess.run(command,capture_output=True,text=True)
                record={'command':command,'repeat':repeat,'core':core,'footprints':scan,'fixture':fixture['name'],
                        'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
                records.append(record)
                (args.output/'runs.json').write_text(json.dumps(records,indent=2)+'\n')
                if result.returncode:raise RuntimeError(record)
                value=json.loads(result.stdout)
                assert value['semantic_sha256']==expected[fixture['path']],record
                groups.setdefault(fixture['name']+'/'+core+'/'+scan,[]).append(value)
    summaries={key:{'repeats':len(values),'semantic_sha256':values[0]['semantic_sha256'],
        **{field:statistics.median(v[field] for v in values) for field in values[0] if field!='semantic_sha256'}} for key,values in groups.items()}
    summary={'status':'passed','scope':'Local fixed synthetic M4 diagnostics only; no final benchmark or scalability claim',
        'raw_runs':len(records),'workload_sha256':hashlib.sha256(workload.read_bytes()).hexdigest(),
        'executable_sha256':hashlib.sha256(args.executable.read_bytes()).hexdigest(),
        'runs_sha256':hashlib.sha256((args.output/'runs.json').read_bytes()).hexdigest(),
        'memory_scope':'whole process peak RSS; macOS bytes; includes index and diagnostic repeat work',
        'timing_scope':'mean over 10 solves per process, then median of 3 processes; core is nested in solve; standalone footprint time is a separate diagnostic estimate',
        'medians':summaries}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':main()
