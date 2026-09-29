"""Process-boundary evidence runner; optional direct validation occurs AFTER timing.

No timeout/resource budget is silently chosen. Kill/crash/missing status is not
accepted as completed output. This is a correctness/evidence tool, not a benchmark.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference'))
from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.io import parse_graph, graph_sha256, solution_records


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--executable',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,required=True)
    parser.add_argument('--check-reference',action='store_true')
    parser.add_argument('arguments',nargs=argparse.REMAINDER)
    args=parser.parse_args()
    arguments=args.arguments[1:] if args.arguments[:1]==['--'] else args.arguments
    if not arguments:parser.error('missing solver command after --')
    output=args.evidence.resolve();output.mkdir(parents=True,exist_ok=False)
    executable=args.executable.resolve()
    manifest={'schema_version':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'command':[str(executable),*arguments],'cwd':str(Path.cwd()),'platform':platform.platform(),
              'executable_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),
              'validation':{'level':'not_run'},'evidence_type':'single process run; no performance comparison'}
    graph=None
    if '--graph' in arguments:
        path=Path(arguments[arguments.index('--graph')+1])
        if path.is_file():
            text=path.read_text();manifest['input_file_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            try:graph=parse_graph(text);manifest['graph_sha256']=graph_sha256(graph)
            except ValueError:pass  # The executable owns invalid-input status.
    stdout,stderr=output/'stdout.jsonl',output/'stderr.jsonl'
    try:
        with stdout.open('w') as out,stderr.open('w') as err:
            started=time.perf_counter()
            result=subprocess.run(manifest['command'],stdout=out,stderr=err,check=False)
            elapsed=time.perf_counter()-started
        manifest.update(native_exit_code=result.returncode,T_e2e=elapsed)
        try:status=json.loads(stderr.read_text())
        except (ValueError,OSError):status=None
        manifest['native_status']=status
        manifest['status']=status.get('status','incomplete') if isinstance(status,dict) else 'incomplete'
        complete=result.returncode==0 and isinstance(status,dict) and status.get('status')=='completed' and status.get('complete') is True
        manifest['complete']=complete
        if manifest['status']=='completed' and not complete:manifest['status']='incomplete'
        # No failure/signal is silently relabelled timeout or OOM.
        if result.returncode<0:manifest['signal']=-result.returncode
        if args.check_reference and complete:
            validation_start=time.perf_counter()
            try:
                if graph is None or arguments[0]!='solve':raise ValueError('definition check requires a valid solve graph')
                h=int(arguments[arguments.index('--h')+1]);k=int(arguments[arguments.index('--k')+1]) if '--k' in arguments else None
                ref=Reference(graph,h);truth=direct_lhcds(ref,k=k)
                result_path=Path(arguments[arguments.index('--output')+1]) if '--output' in arguments and arguments[arguments.index('--output')+1]!='-' else stdout
                actual=[json.loads(line) for line in result_path.read_text().splitlines()]
                expected=solution_records(ref,truth)
                manifest['validation']={'level':'definition_checked','passed':actual==expected,'expected':expected,'actual':actual}
            except Exception as error:
                manifest['validation']={'level':'not_completed','error':str(error)}
            manifest['T_external_validation']=time.perf_counter()-validation_start
        manifest['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (stdout,stderr)}
    except OSError as error:
        manifest.update(status='io_error',complete=False,error=str(error))
    finally:
        (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,sort_keys=True))
    if not manifest.get('complete'):return 1
    if args.check_reference and not manifest['validation'].get('passed'):return 2
    return 0


if __name__=='__main__':raise SystemExit(main())
