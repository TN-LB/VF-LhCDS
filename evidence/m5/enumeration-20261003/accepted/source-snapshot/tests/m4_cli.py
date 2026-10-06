"""M4 equivalent CLI modes, exact output hashes and query-local telemetry."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    executable=Path(sys.argv[1]).resolve();calls=0
    def run(args,code=0):
        nonlocal calls
        calls+=1
        result=subprocess.run([str(executable),*map(str,args)],capture_output=True,text=True)
        assert result.returncode==code,(args,result)
        status=json.loads(result.stderr)
        assert status['complete']==(code==0)
        if code:assert status['semantic_sha256'] is None and not result.stdout
        return result.stdout,status
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary);graph=root/'witness.graph'
        edges=[*itertools.combinations(range(4),2),(4,5),(4,6),(5,6),(4,7)]
        graph.write_text('vflhcds-graph 1 n 8 '+''.join(f'v {v} ' for v in range(8))+'m 10 '+''.join(f'e {u} {v} ' for u,v in edges))
        base=['solve','--graph',graph,'--h','2']
        defaults,ds=run(base+['--all'])
        expected=[json.loads(line) for line in defaults.splitlines()]
        assert [item['vertices'] for item in expected]==[[0,1,2,3],[4,5,6,7]]
        for core,scan in itertools.product(['off','safe'],['sorted','membership']):
            options=['--core-reduction',core,'--footprint-scan',scan]
            for k in [1,2,3,2**200,None]:
                out,status=run(base+options+(['--all'] if k is None else ['--k',str(k)]))
                assert [json.loads(line) for line in out.splitlines()]==(expected if k is None else expected[:k])
                if k!=1:assert out==defaults and status['semantic_sha256']==ds['semantic_sha256']
                query=status['counters']['queries'][0]
                assert query['original_interval_size']==8 and query['oracle_interval_size']==(7 if core=='safe' else 8)
                if core=='safe':
                    assert query['core_threshold']==2 and query['core']['vertices_removed']==1
                    assert 0<=query['core_reduction_seconds']<=status['timing']['T_core']
                else:assert query['core'] is None and query['core_reduction_seconds'] is None
            zero,zs=run(['solve','--graph',graph,'--h',str(2**200),'--all',*options])
            assert [item['vertices'] for item in map(json.loads,zero.splitlines())]==[[0,1,2,3],[4,5,6,7]]
            assert all(query['core'] is None for query in zs['counters']['queries'])
            saved=root/'saved';saved.write_text('old')
            out,ss=run(base+['--all',*options,'--output',saved]);assert not out and saved.read_text()==defaults
            assert ss['semantic_sha256']==ds['semantic_sha256']
        oracle=['oracle','--graph',graph,'--h','2','--lambda','5/4']
        a,_=run(oracle);b,_=run(oracle+['--footprint-scan','membership']);assert a==b
        x=root/'x';y=root/'y';x.write_text('vflhcds-set 1 n 0');y.write_text('vflhcds-set 1 n 4 v 4 v 5 v 6 v 7')
        a,_=run(oracle+['--x',x,'--y',y]);b,st=run(oracle+['--x',x,'--y',y,'--footprint-scan','membership'])
        assert a==b and json.loads(a)['scope']=='restricted' and st['counters']['core'] is None
        for extra in [['--core-reduction','on'],['--core-reduction','heuristic'],['--footprint-scan','fast'],
                      ['--footprint-scan','membership','--footprint-scan','sorted'],['--core-reduction','safe','--core-reduction','off']]:
            run(base+['--all',*extra],2)
        run(oracle+['--core-reduction','safe'],2)
        run(['solve','--graph','absent','--h','2','--k','0','--core-reduction','safe'],2)
    print(f'M4 CLI: {calls} invocations passed')


if __name__=='__main__':main()
