"""Solve wire, ordering, timing, failure and process-runner regression checks."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference'))
from vflhcds_reference.io import canonical_graph, graph_sha256, json_line
from vflhcds_reference.graph import Graph


def main():
    executable=Path(sys.argv[1]).resolve();calls=0
    def run(args,code=0,status='completed'):
        nonlocal calls
        calls+=1
        result=subprocess.run([str(executable),*map(str,args)],capture_output=True,text=True)
        assert result.returncode==code,(args,result)
        record=json.loads(result.stderr)
        assert record['status']==status and record['complete']==(code==0),(args,record)
        if code:assert record['semantic_sha256'] is None and not result.stdout
        return result,record
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);path=root/'graph';out=root/'out'
        graph=Graph((-90,-2,5,11,100),((-90,-2),(5,11)))
        path.write_text(canonical_graph(graph));out.write_text('previous output\n')
        base=['solve','--graph',path,'--h','2']
        full,stats=run(base+['--all'])
        records=[json.loads(line) for line in full.stdout.splitlines()]
        assert [r['vertices'] for r in records]==[[-90,-2],[5,11],[100]]
        assert stats['output_count']==3 and stats['termination']=='exhausted'
        assert stats['counters']['logical_interval_queries']==3 and stats['counters']['mincut_calls']==2
        assert stats['timing']['T_e2e'] is None and 0<=stats['timing']['T_core']<=stats['timing']['T_postload']
        header={'schema_version':1,'graph_sha256':graph_sha256(graph),'h':2}
        assert stats['semantic_sha256']==hashlib.sha256((json_line(header)+full.stdout).encode()).hexdigest()
        for k in [1,2,3,4,5,2**200]:
            result,status=run(base+['--k',str(k)])
            assert [json.loads(line) for line in result.stdout.splitlines()]==records[:k]
            assert status['termination']==('k_reached' if k<=3 else 'exhausted')
            assert status['semantic_sha256']==hashlib.sha256((json_line(header)+result.stdout).encode()).hexdigest()
        a,sa=run(base+['--k','1']);b,sb=run(base+['--k','1','--core-reduction','off'])
        assert a.stdout==b.stdout and sa['semantic_sha256']==sb['semantic_sha256']
        assert sa['counters']['logical_interval_queries']==2
        for suffix in [[],['--k','0'],['--k','-1'],['--k','1.0'],['--k','01'],['--k','1','--all'],['--all','--all'],
                       ['--all','--core-reduction','on'],['--all','--capacity','big'],['--all','--tie-inclusive'],['--all','extra'],
                       ['--all','--h','3'],['--all','--output',path]]:
            run(base+suffix,2,'invalid_argument')
            assert out.read_text()=='previous output\n'
        run(['solve','--graph','missing','--h','2','--k','0'],2,'invalid_argument')
        run(['solve','--graph','missing','--h','2','--all'],4,'io_error')
        symlink=root/'alias';symlink.symlink_to(path)
        run(base+['--all','--output',symlink],2,'invalid_argument')
        path.write_text('vflhcds-graph 1 n '+str(2**200)+'\n')
        run(base+['--all','--output',out],5,'resource_limit');assert out.read_text()=='previous output\n'
        path.write_text('vflhcds-graph 1 n 0 m 0\n')
        run(base+['--all','--output',out],3,'invalid_graph');assert out.read_text()=='previous output\n'
        path.write_text(canonical_graph(graph))
        run(base+['--all','--output',root/'missing'/'out'],4,'io_error');assert out.read_text()=='previous output\n'
        saved,save_status=run(base+['--all','--output',out])
        assert not saved.stdout and out.read_text()==full.stdout and save_status['semantic_sha256']==stats['semantic_sha256']
        assert not list(root.glob('*.tmp.*'))
        # Input orientation and ordering change bytes but not graph/output hashes.
        path.write_text('vflhcds-graph 1 n 5 v 100 v 11 v 5 v -2 v -90 m 2 e 11 5 e -2 -90')
        varied,sv=run(base+['--all']);assert varied.stdout==full.stdout and sv['semantic_sha256']==stats['semantic_sha256']
        h_large,sl=run(['solve','--graph',path,'--h',str(2**200),'--all'])
        assert all(r['density_num']=='0' for r in map(json.loads,h_large.stdout.splitlines()))
        assert sl['counters']['logical_interval_queries']==1 and sl['counters']['mincut_calls']==0
        # Genuine child-process run, then separate all-superset reference validation.
        evidence=root/'runner'
        command=[sys.executable,str(ROOT/'validation/run_solver.py'),'--executable',str(executable),'--evidence',str(evidence),'--check-reference','--',*map(str,base),'--all']
        checked=subprocess.run(command,capture_output=True,text=True);assert checked.returncode==0,checked
        manifest=json.loads((evidence/'manifest.json').read_text())
        assert manifest['complete'] and manifest['validation']['passed']
        assert manifest['T_e2e']>=manifest['native_status']['timing']['T_postload']>=0
        assert manifest['T_external_validation']>=0
        failed=root/'runner-failed'
        command=[sys.executable,str(ROOT/'validation/run_solver.py'),'--executable',str(executable),'--evidence',str(failed),'--',*map(str,base),'--k','0']
        checked=subprocess.run(command,capture_output=True,text=True);assert checked.returncode==1,checked
        manifest=json.loads((failed/'manifest.json').read_text())
        assert not manifest['complete'] and manifest['status']=='invalid_argument' and manifest['native_exit_code']==2
    print(f'M3 CLI: {calls} direct invocations and 2 external-runner invocations passed')


if __name__=='__main__':main()
