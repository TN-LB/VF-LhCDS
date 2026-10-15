"""T23: work modes are explicit solve-only options and preserve canonical output."""
import itertools
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]; binary=Path(sys.argv[1]).resolve(); calls=0

def run(args,code=0):
    global calls
    calls+=1
    proc=subprocess.run([str(binary),*map(str,args)],capture_output=True,text=True)
    assert proc.returncode==code,(args,proc)
    status=json.loads(proc.stderr)
    assert status['complete']==(code==0)
    if code:assert not proc.stdout
    return proc.stdout,status

for fixture,h in itertools.product(('triangle_and_isolate','bridged_triangles'),(2,3,2**200)):
    base=['solve','--graph',ROOT/'reference/fixtures'/(fixture+'.graph'),'--h',h]
    default=run(base+['--all']);explicit=run(base+['--all','--clique-work','global'])
    assert default[0]==explicit[0] and default[1]['counters']==explicit[1]['counters']
    for enum,count,fp,core,k in itertools.product(('combinations','adjacency'),('sorted','membership'),
            ('sorted','membership'),('off','safe'),('all',1)):
        args=base+['--clique-enumeration',enum,'--clique-count',count,'--footprint-scan',fp,'--core-reduction',core]
        args+=['--all'] if k=='all' else ['--k',k]
        reference=None
        for work in ('global','interval-scan','interval-reuse'):
            output,status=run(args+['--clique-work',work])
            value=(output,status['semantic_sha256'],status['termination'])
            if reference is not None:assert value==reference
            reference=value
            assert status['counters']['clique_work']==work
base=['solve','--graph','absent','--h',3,'--k',1]
for extra in (['--clique-work'],['--clique-work','auto'],
              ['--clique-work','global','--clique-work','interval-reuse']):run(base+extra,2)
run(['oracle','--graph','absent','--h',3,'--lambda','1/2','--clique-work','interval-reuse'],2)
run(['inspect-graph','--graph','absent','--clique-work','global'],2)
run(['solve','--graph','absent','--h',3,'--k',0,'--clique-work','interval-reuse'],2)
print(f'T23 CLI: {calls} invocations passed')
