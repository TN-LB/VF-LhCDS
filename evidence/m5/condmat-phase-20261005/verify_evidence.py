"""Verify the saved diagnostic and derive observations without new native calls."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from experiments.support import file_hashes,save,sha256
HERE=Path(__file__).resolve().parent

def read(path):return json.loads(path.read_text())

def hashes(base,values):
    for name,digest in values.items():assert sha256(base/name)==digest,name
    return len(values)

def main():
    before=read(HERE/'preservation-before.json');checks={}
    for key in ('paper_sha256','reference_sha256','production_source_sha256','binary_sha256','provenance_sha256','pinned_harness_sha256','library_sha256','old_probe_sha256'):
        checks[key]=hashes(ROOT,before[key])
    checks['ippv_sources']=hashes(ROOT/'.deps/baselines/ippv',before['ippv_source_sha256'])
    assert sha256(ROOT/'baselines/ippv/source-lock.json')==before['baseline_lock_sha256']
    old=ROOT/'evidence/m5/pilot-fixed-20261005'
    assert file_hashes(old)==before['historical_pilot_sha256']
    checks['historical_fixed_pilot_files']=len(before['historical_pilot_sha256'])
    accepted=HERE/'accepted'
    inventory=read(accepted/'checksums.json')
    checks['raw_inventory_entries']=hashes(accepted,inventory)
    assert set(file_hashes(accepted))==set(inventory)|{'checksums.json'}
    config=read(accepted/'config.json');authorization=read(accepted/'authorization.json')
    assert authorization['owner_reply']=='好' and authorization['decision_id']=='D032'
    assert authorization['config_sha256']==sha256(accepted/'config.json')
    assert config['real_repeats']==1 and config['timeout_seconds']==60 and config['threads']==1
    assert config['seed'] is None and config['memory_limit_bytes'] is None
    assert config['mode']=={'core':'off','footprints':'sorted','enumeration':'adjacency','capacity':'auto'}
    env=read(accepted/'environment.json');hashes(ROOT,env['source_sha256']);hashes(accepted/'source',env['source_sha256'])
    assert env['decision_log_sha256']==sha256(ROOT/'docs/DECISIONS.md')
    provenance=read(accepted/'probe-provenance.json')
    assert sha256(Path(provenance['executable']))==provenance['executable_sha256']
    assert sha256(Path(provenance['library']))==provenance['library_sha256']
    assert provenance['source_sha256']==env['source_sha256']
    assert provenance['compile_commands_sha256']==sha256(accepted/'compile_commands.json')
    assert provenance['link_command_sha256']==sha256(accepted/'link.txt')
    builds=read(accepted/'build-commands.json');assert len(builds)==2 and all(b['exit_code']==0 for b in builds)
    assert '/build-m5-adjacency-release/libvflhcds_lib.a' in (accepted/'link.txt').read_text()
    assert all(str(ROOT/'experiments/phase_probe') in c['file'] for c in read(accepted/'compile_commands.json'))
    expected=[(p,e) for p in ('parse','index','solve','serialize') for e in ('begin','end')]
    last_finish=authorization['recorded_utc']
    smokes=read(accepted/'smoke-results.json');assert len(smokes)==2
    for fixture,result in zip(config['smoke_tests'],smokes):
        assert sha256(ROOT/fixture['graph'])==fixture['sha256']
        assert result['id']==fixture['id'] and result['status']=='passed'
        base=accepted/'smoke'/fixture['id'].split('/')[1]
        events=[json.loads(line) for line in (base/'probe/stderr.txt').read_text().splitlines()]
        assert [(e['phase'],e['event']) for e in events if e['phase']!='query']==expected
        assert all(a['elapsed_seconds']<=b['elapsed_seconds'] for a,b in zip(events,events[1:]))
        query=[e for e in events if e['phase']=='query']
        status=read(base/'production/stderr.txt')
        assert [e['stats'] for e in query]==status['counters']['queries']
        assert [e['query_index'] for e in query]==list(range(1,len(query)+1))
        assert (base/'probe/stdout.txt').read_bytes()==(base/'production/stdout.txt').read_bytes()
        validation=read(base/'validation/stdout.txt')
        assert validation['passed'] and validation['level']=='definition_checked'
        assert validation['completeness_certified']
        for name,key in [('probe','probe_process'),('production','production_process'),('validation','external_validator')]:
            process=read(base/name/'process.json')
            assert process==result[key] and process['native_exit_code']==0
            assert process['started_utc']>=last_finish
            last_finish=process['finished_utc']
    real=read(accepted/'real-result.json');process=read(accepted/'real/process.json')
    assert real['process']==process and process['started_utc']>=last_finish
    assert process['executable_sha256']==provenance['executable_sha256']
    assert process['command'][-3:]==['3','5','adjacency']
    assert process['status']=='timeout' and process['native_exit_code']==-9 and process['signal']==9
    assert process['wall_seconds']>=60 and process['timeout_seconds']==60
    assert (accepted/'real/stdout.txt').read_bytes()==b''
    assert not (accepted/'real/validation').exists()
    assert sha256(accepted/'real/graph.txt')==config['real_case']['sha256']
    assert authorization['recorded_utc']<=read(accepted/'real-invocation.json')['recorded_utc']<=process['started_utc']
    events=[json.loads(line) for line in (accepted/'real/stderr.txt').read_text().splitlines()]
    assert events==real['events']
    assert all(a['elapsed_seconds']<=b['elapsed_seconds'] for a,b in zip(events,events[1:]))
    boundaries=[e for e in events if e['phase']!='query']
    assert [(e['phase'],e['event']) for e in boundaries]==expected[:5]
    query=[e for e in events if e['phase']=='query']
    assert len(query)==137 and [e['query_index'] for e in query]==list(range(1,138))
    assert all(e['event']=='end' and e['stats']['logical_interval_queries']==e['stats']['mincut_calls']==1 for e in query)
    assert all(e['stats']['cliques_scanned']==173361 and e['stats']['capacity_backend']=='uint128' for e in query)
    assert real['incomplete_phase']=='solve' and real['completed_queries']==137
    boundary_times={(e['phase'],e['event']):e['elapsed_seconds'] for e in boundaries}
    previous=boundary_times[('solve','begin')]
    timeline=[]
    for e in query:
        timeline.append({'query_index':e['query_index'],'completed_elapsed_seconds':e['elapsed_seconds'],
             'gap_from_previous_completion_seconds':e['elapsed_seconds']-previous,'stats':e['stats'],
             'timing_note':'Gap includes traversal, counting, oracle work and marker overhead; not an isolated flow/footprint timer.'})
        previous=e['elapsed_seconds']
    save(HERE/'query-timeline.json',timeline)
    summary={'parse_seconds':boundary_times[('parse','end')]-boundary_times[('parse','begin')],
             'index_seconds':boundary_times[('index','end')]-boundary_times[('index','begin')],
             'solve_started_elapsed_seconds':boundary_times[('solve','begin')],
             'completed_queries':137,'completed_mincuts':137,'cliques_scanned_in_completed_queries':137*173361,
             'native_timeout_wall_seconds':process['wall_seconds'],'peak_rss_bytes':process['peak_rss_bytes'],
             'last_completed_query_elapsed_seconds':query[-1]['elapsed_seconds'],
             'output_complete':False,'inner_operation_profile':'Not measured; no attribution of gaps to a single operation.',
             'remaining_phase':'solve','new_real_calls':1,'campaign_continued':False}
    save(HERE/'observations.json',summary)
    assert read(HERE/'command.json')['exit_code']==1 and (HERE/'driver.stderr').read_bytes()==b''
    assert read(accepted/'preservation-final.json')['status']=='passed'
    checks.update(build_commands_passed=2,instrumentation_fixture_passes=2,native_tiny_successes=4,external_definition_validator_passes=2,
           real_calls=1,real_timeout=1,completed_query_markers=137,phase='solve',post_timeout_native_calls=0,
           source_snapshot_files=len(env['source_sha256']),production_semantic_changes=0,full_ctest_pytest_sanitizer_rerun=False)
    save(HERE/'verification.json',checks)
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
