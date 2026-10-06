"""Verify saved paired evidence and explain output differences; no native runs."""
from fractions import Fraction
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from experiments.run import load_config,schedule
from experiments.support import file_hashes,parse_graph,save,semantic_hash,sha256
from experiments.validate import compare,parse_records
HERE=Path(__file__).resolve().parent

def read(path):return json.loads(path.read_text())

def main():
    pins=read(HERE/'preflight.json');checks={}
    for key in ('paper_sha256','reference_sha256','production_source_sha256','binary_sha256',
                'provenance_sha256','pinned_harness_sha256','library_sha256','old_probe_sha256'):
        for name,digest in pins[key].items():assert sha256(ROOT/name)==digest,name
        checks[key]=len(pins[key])
    for name,digest in pins['ippv_source_sha256'].items():assert sha256(ROOT/'.deps/baselines/ippv'/name)==digest,name
    for patch in pins['ippv_patches']:assert sha256(ROOT/patch['path'])==patch['sha256']
    assert len(pins['ippv_patches'])==7 and sha256(ROOT/'baselines/ippv/source-lock.json')==pins['baseline_lock_sha256']
    assert sha256(ROOT/'docs/DECISIONS.md')==pins['decision_log_sha256']
    assert sha256(HERE/'run_pair.py')==pins['runner_sha256']
    checks['historical_evidence_files']={}
    for directory,inventory in pins['historical_evidence_sha256'].items():
        assert file_hashes(ROOT/directory)==inventory,directory
        checks['historical_evidence_files'][directory]=len(inventory)
    prior=ROOT/'evidence/m5/condmat-membership-20261006'
    assert sha256(prior/'next-pair-draft.json')==pins['draft_sha256']
    draft=read(prior/'next-pair-draft.json');config=load_config(HERE/'config.json')
    assert {key for key in config if config[key]!=draft[key]}=={'name','scope'}
    assert config['scope']=='diagnostic' and config['repeats']==1 and config['timeout_seconds']==60
    campaign=HERE/'campaign';inventory=read(campaign/'checksums.json')
    assert config==read(campaign/'config.json')
    assert schedule(config)==read(HERE/'schedule.json')==read(campaign/'schedule.json')
    for name,digest in inventory.items():assert sha256(campaign/name)==digest,name
    assert set(file_hashes(campaign))==set(inventory)|{'checksums.json'}
    checks['raw_inventory_entries']=len(inventory)
    launch,completion=[read(HERE/f'{n}.json') for n in ('launch','completion')]
    assert completion['exit_code']==0 and launch['command']==completion['command']
    assert launch['configuration_sha256']==sha256(HERE/'config.json')==pins['configuration_sha256']
    assert launch['preflight_sha256']==sha256(HERE/'preflight.json')
    assert launch['environment_sha256']==sha256(HERE/'environment.json')
    env=read(HERE/'environment.json');old_env=read(prior/'current-environment.json')
    assert env['hardware']==old_env['hardware'] and env['platform']==old_env['platform'] and env['environment']==old_env['environment']
    assert all(h['exit_code']==0 for h in env['hardware'].values())
    assert (HERE/'driver.stderr').read_bytes()==b'' and not (campaign/'stopped.json').exists()
    summary=read(campaign/'summary.json');policy=read(campaign/'execution-policy.json')
    assert len(summary['runs'])==len(policy['planned_runs'])==2 and policy['stop_on_failure']
    assert [r['directory'] for r in summary['runs']]==[r['directory'] for r in policy['planned_runs']]
    last_finish=launch['started_utc'];records={};metrics=[]
    for row in summary['runs']:
        run=campaign/row['directory'];manifest=read(run/'manifest.json')
        native,external=manifest['native'],manifest['external_validation']
        assert native==read(run/'process.json') and external==read(run/'validation/process.json')
        assert row['status']=='completed' and native['native_exit_code']==external['native_exit_code']==0
        assert last_finish<=native['started_utc']<=native['finished_utc']<=external['started_utc']<=external['finished_utc']
        last_finish=external['finished_utc']
        assert native['timeout_seconds']==external['timeout_seconds']==60
        algorithm=next(a for a in config['algorithms'] if a['name']==row['algorithm'])
        assert native['executable_sha256']==algorithm['sha256']
        assert manifest['build_provenance']==read((ROOT/algorithm['executable']).with_suffix('.provenance.json'))
        graph=parse_graph((run/'graph.txt').read_text());assert sha256(run/'graph.txt')==config['cases'][0]['sha256']
        record=parse_records((run/'canonical_output.jsonl').read_text(),graph,3)
        assert len(record)==5 and semantic_hash(graph,3,record)==row['semantic_sha256']
        checks_out=manifest['validation']
        assert checks_out['passed'] and checks_out['level']=='structural_checked' and not checks_out['completeness_certified']
        assert all(checks_out['checks'].values())
        records[row['algorithm']]=record
        metrics.append({'algorithm':row['algorithm'],'native_wall_seconds':native['wall_seconds'],
            'peak_rss_bytes':native['peak_rss_bytes'],'native_exit_code':0,'external_validator_exit_code':0,
            'external_validator_wall_seconds':external['wall_seconds'],'phase_wall_seconds':manifest['phase_wall_seconds'],
            'output_count':len(record),'semantic_sha256':row['semantic_sha256']})
    assert last_finish<=completion['finished_utc']
    assert len(summary['comparisons'])==1
    pair=summary['comparisons'][0];expected=compare(*(records[name] for name in pair['algorithms']),k=5)
    assert all(pair[key]==value for key,value in expected.items())
    assert pair['tie_aware_match'] and not pair['strict_match']
    vf=records['vf-adjacency-membership'];ippv=records['ippv-seven-patches']
    density=lambda r:Fraction(int(r['density_num']),int(r['density_den']))
    assert vf[:4]==ippv[:4] and vf[4]['vertices']!=ippv[4]['vertices']
    assert density(vf[4])==density(ippv[4])==22
    assert all(density(r)>22 for r in vf[:4])
    previous=[json.loads(line) for line in (prior/'campaign/runs/0000-0/canonical_output.jsonl').read_text().splitlines()]
    assert vf==previous
    save(HERE/'comparison-details.json',{'strict_match':False,'tie_aware_match':True,'identical_ranks':[1,2,3,4],
        'cutoff_density':'22','different_cutoff_records':{'vf':vf[4],'ippv':ippv[4]},
        'vf_matches_previous_membership_output':True,'completeness_certified':False})
    save(HERE/'result.json',{'case':'ca-condmat-h3-k5','native_runs':2,'external_validators':2,'metrics':metrics,
        'comparison':pair,'unrun_in_this_diagnostic':0,'vf_matches_previous_membership_output':True})
    checks.update(native_successes=2,external_structural_validator_successes=2,paired_comparisons=1,
        strict_match=False,tie_aware_match=True,cutoff_only_difference=True,vf_previous_output_match=True,
        builds_or_test_suites_rerun=False)
    save(HERE/'verification.json',checks)
    print(json.dumps({'metrics':metrics,'comparison':pair,'difference':'Rank 5 only, equal exact density 22; ranks 1-4 identical.'},indent=2))

if __name__=='__main__':main()
