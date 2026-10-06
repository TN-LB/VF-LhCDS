"""Synthetic failure reduction is separate from real solver agreement evidence."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'validation'))
from solver_campaign import minimize_case, Graph, Reference, direct_lhcds


def main():
    original={'vertices':[0,1,2,3], 'edges':[[0,1],[1,2]],'h':3,'k':4,'kind':'solve','policy':'auto'}
    def missing_zero(candidate):
        graph=Graph(tuple(candidate['vertices']),tuple(map(tuple,candidate['edges'])))
        ref=Reference(graph,candidate['h'])
        truth=direct_lhcds(ref,k=candidate['k'])
        faulty=tuple(mask for mask in truth if ref.density(mask)>0)
        return truth!=faulty
    reduced=minimize_case(original,missing_zero)
    assert reduced['vertices']==[3] and reduced['edges']==[] and reduced['h']==2 and reduced['k']==1
    assert reduced['kind']=='solve' and reduced['policy']=='auto' and missing_zero(reduced)
    assert original['vertices']==[0,1,2,3] and len(original['edges'])==2
    assert minimize_case(original,missing_zero)==reduced
    full=dict(original,k=None)
    reduced_full=minimize_case(full,lambda candidate:len(candidate['vertices'])>=1)
    assert reduced_full['k'] is None and len(reduced_full['vertices'])==1
    print('T14 synthetic missing-zero reducer: deterministic, original retained, fixed-k/all scope preserved; no production failure claimed')


if __name__=='__main__':main()
