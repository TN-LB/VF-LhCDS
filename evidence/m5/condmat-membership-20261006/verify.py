"""Verify the saved single run and preservation pins; launch no native child."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import file_hashes, parse_graph, save, semantic_hash, sha256
from experiments.validate import parse_records
HERE=Path(__file__).resolve().parent

def read(path):return json.loads(path.read_text())

def main():
    pins=read(HERE/'preflight.json'); checks={}
    for key in ('paper_sha256','reference_sha256','production_source_sha256','binary_sha256',
                'provenance_sha256','pinned_harness_sha256','library_sha256','old_probe_sha256','proposal_sha256'):
        for name,digest in pins[key].items():assert sha256(ROOT/name)==digest,name
        checks[key]=len(pins[key])
    for name,digest in pins['ippv_source_sha256'].items():
        assert sha256(ROOT/'.deps/baselines/ippv'/name)==digest,name
    assert sha256(ROOT/'baselines/ippv/source-lock.json')==pins['baseline_lock_sha256']
    assert sha256(ROOT/'docs/DECISIONS.md')==pins['decision_log_sha256']
    assert sha256(HERE/'run_diagnostic.py')==pins['runner_sha256']
    checks['historical_evidence_files']={}
    for directory,inventory in pins['historical_evidence_sha256'].items():
        assert file_hashes(ROOT/directory)==inventory,directory
        checks['historical_evidence_files'][directory]=len(inventory)
    config=load_config(HERE/'config.json');campaign=HERE/'campaign'
    assert config==read(campaign/'config.json')
    assert config['scope']=='diagnostic' and config['repeats']==1 and config['timeout_seconds']==60
    assert schedule(config)==read(HERE/'schedule.json')==read(campaign/'schedule.json')
    draft=read(ROOT/'evidence/m5/condmat-phase-20261005/draft-membership-config.json')
    assert {k for k in config if config[k]!=draft[k]}=={'name','scope'}
    inventory=read(campaign/'checksums.json')
    for name,digest in inventory.items():assert sha256(campaign/name)==digest,name
    assert set(file_hashes(campaign))==set(inventory)|{'checksums.json'}
    checks['raw_inventory_entries']=len(inventory)
    launch,completion=[read(HERE/f'{n}.json') for n in ('launch','completion')]
    assert launch['command']==completion['command'] and completion['exit_code']==0
    assert launch['configuration_sha256']==sha256(HERE/'config.json')==pins['config_sha256']
    assert launch['preflight_sha256']==sha256(HERE/'preflight.json')
    assert launch['environment_sha256']==sha256(HERE/'environment.json')
    environment=read(HERE/'environment.json'); current=read(HERE/'current-environment.json')
    assert current['profile_matches_prior'] and not current['host_label_matches_prior']
    assert environment['hardware']==current['hardware'] and environment['host_id_sha256']==current['host_id_sha256']
    assert read(HERE/'preflight-attempt-1/failure.json')['native_calls']==0
    assert (HERE/'driver.stderr').read_bytes()==b''
    summary=read(campaign/'summary.json');policy=read(campaign/'execution-policy.json')
    assert len(summary['runs'])==len(policy['planned_runs'])==1 and policy['stop_on_failure']
    assert not summary['comparisons'] and not (campaign/'stopped.json').exists()
    row=summary['runs'][0];assert row['status']=='completed'
    run=campaign/row['directory'];manifest=read(run/'manifest.json')
    native,external=manifest['native'],manifest['external_validation']
    assert native==read(run/'process.json') and external==read(run/'validation/process.json')
    assert native['native_exit_code']==external['native_exit_code']==0
    assert launch['started_utc']<=native['started_utc']<=native['finished_utc']<=external['started_utc']<=external['finished_utc']<=completion['finished_utc']
    assert native['timeout_seconds']==external['timeout_seconds']==60
    assert native['executable_sha256']==config['algorithms'][0]['sha256']
    assert native['command'][-6:]==['--core-reduction','off','--footprint-scan','membership','--clique-enumeration','adjacency']
    graph=parse_graph((run/'graph.txt').read_text());assert sha256(run/'graph.txt')==config['cases'][0]['sha256']
    records=parse_records((run/'canonical_output.jsonl').read_text(),graph,3)
    assert len(records)==5 and (run/'canonical_output.jsonl').read_bytes()==(run/'stdout.txt').read_bytes()
    assert semantic_hash(graph,3,records)==row['semantic_sha256']
    validation=manifest['validation'];assert validation==read(run/'validation/stdout.txt')
    assert validation['passed'] and validation['level']=='structural_checked' and not validation['completeness_certified']
    assert all(validation['checks'].values()) and validation['semantic_sha256']==row['semantic_sha256']
    status=manifest['native_status'];assert status['complete'] and status['termination']=='k_reached'
    counters=status['counters'];assert counters['logical_interval_queries']==counters['mincut_calls']==len(counters['queries'])==304
    assert counters['cliques_enumerated']==173361 and counters['cliques_scanned']==52701744
    assert sum(q['cliques_scanned'] for q in counters['queries'])==counters['cliques_scanned']
    old_trace=read(ROOT/'evidence/m5/condmat-phase-20261005/accepted/real-result.json')
    old_queries=[e['stats'] for e in old_trace['events'] if e['phase']=='query']
    assert len(old_queries)==137 and counters['queries'][:137]==old_queries
    result={'case':row['case'],'status':'completed','native_exit_code':0,'native_wall_seconds':native['wall_seconds'],
        'native_peak_rss_bytes':native['peak_rss_bytes'],'phase_wall_seconds':manifest['phase_wall_seconds'],
        'output_count':5,'termination':'k_reached','logical_queries':304,'mincuts':304,'cliques_enumerated':173361,
        'cliques_scanned':52701744,'external_validator_exit_code':0,'external_validator_wall_seconds':external['wall_seconds'],
        'validation_level':'structural_checked','completeness_certified':False,'semantic_sha256':row['semantic_sha256'],
        'prior_sorted_query_counter_prefix_match':137,'prefix_scope':'Recorded counters only; not result-set equality or isolated timing.',
        'native_calls':1,'unrun_in_this_diagnostic':0,'paired_comparisons':0}
    save(HERE/'result.json',result)
    checks.update(native_successes=1,external_structural_validator_successes=1,output_count=5,
                  prior_query_counter_prefix_match=137,builds_or_test_suites_rerun=False)
    save(HERE/'verification.json',checks)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
