"""Build a separate matching probe, check two fixtures, diagnose one bounded case."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import capture, file_hashes, save, sha256


def read(path):
    return json.loads(path.read_text())


def preserved():
    before = read(HERE / 'preservation-before.json')
    for key in ('paper_sha256', 'reference_sha256', 'production_source_sha256', 'binary_sha256', 'provenance_sha256', 'pinned_harness_sha256', 'library_sha256', 'old_probe_sha256'):
        for name, digest in before[key].items():
            assert sha256(ROOT / name) == digest, name
    for name, digest in before['ippv_source_sha256'].items():
        assert sha256(ROOT / '.deps/baselines/ippv' / name) == digest, name
    assert sha256(ROOT / 'baselines/ippv/source-lock.json') == before['baseline_lock_sha256']
    old = ROOT / 'evidence/m5/pilot-fixed-20261005'
    assert file_hashes(old) == before['historical_pilot_sha256']
    return before


def events(directory):
    values = [json.loads(line) for line in (directory / 'stderr.txt').read_text().splitlines()]
    assert all(v['diagnostic_schema']==1 and v['elapsed_seconds']>=0 for v in values)
    assert all(a['elapsed_seconds']<=b['elapsed_seconds'] for a,b in zip(values,values[1:]))
    return values


def main():
    accepted = HERE / 'accepted'
    accepted.mkdir(exist_ok=False)
    before = preserved()
    production = ROOT / 'build-m5-adjacency-release/vflhcds'
    library = ROOT / 'build-m5-adjacency-release/libvflhcds_lib.a'
    build = ROOT / 'build-m5-condmat-phase-probe'
    assert not build.exists(), 'Preserve historical and prior diagnostic builds'
    binary = build / 'vflhcds_phase_probe'
    old_config = read(ROOT / 'evidence/m5/pilot-fixed-20261005/config.json')
    case = next(c for c in old_config['cases'] if c['name']=='ca-condmat-h3-k5')
    assert sha256(ROOT / case['graph'])==case['sha256']
    prior_env = read(ROOT / 'evidence/m5/pilot-fixed-20261005/environment.json')
    assert platform.platform()==prior_env['platform']
    assert hashlib.sha256(platform.node().encode()).hexdigest()==prior_env['host_id_sha256']
    config = {'scope':'phase_diagnostic', 'real_case':case, 'real_repeats':1,
              'timeout_seconds':60, 'threads':1, 'memory_limit_bytes':None,
              'cache_policy':'uncontrolled', 'seed':None,
              'seed_reason':'One deterministic real case; no random schedule.',
              'mode':{'core':'off','footprints':'sorted','enumeration':'adjacency','capacity':'auto'},
              'smoke_tests':[{'id':'T-PHASE-ADJ/'+name, 'graph':'reference/fixtures/'+name+'.graph',
                              'sha256':sha256(ROOT / 'reference/fixtures' / (name+'.graph')), 'h':3,'k':5}
                             for name in ('triangle_and_isolate','bridged_triangles')],
              'real_test':'T-PHASE-CM/flushed-boundaries',
              'timing_scope':'Separate instrumented diagnostic; not a benchmark or retry measurement.'}
    save(accepted / 'config.json', config)
    save(accepted / 'authorization.json', {'decision_id':'D032', 'owner_reply':'好',
         'scope':'One bounded CA-CondMat phase diagnosis following the last report recommendation; two tiny instrumentation checks first.',
         'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'config_sha256':sha256(accepted / 'config.json'),
         'production_change_authorized':False,'formal_benchmark':False,
         'stop_after_one_real_call':True})
    sources=[Path(__file__),ROOT/'experiments/phase_probe/main.cpp',ROOT/'experiments/phase_probe/CMakeLists.txt',
             ROOT/'experiments/support.py',ROOT/'experiments/validate.py',ROOT/'baselines/ippv/process.py']
    for path in sources:
        target=accepted/'source'/path.relative_to(ROOT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
    save(accepted / 'environment.json', {'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'platform':platform.platform(),'python':sys.version,
         'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'dirty_tree':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
         'source_sha256':{str(p.relative_to(ROOT)):sha256(p) for p in sources},
         'prior_same_host_environment':prior_env,
         'hardware_note':'Previously measured same-host D031 profile, not a fresh sysctl reading.',
         'configuration_sha256':sha256(accepted/'config.json'),
         'decision_log_sha256':sha256(ROOT/'docs/DECISIONS.md')})
    compiler=shlex.split(read(ROOT/'build-m5-adjacency-release/compile_commands.json')[0]['command'])[0]
    cmake=str(ROOT/'.venv/bin/cmake')
    commands=[
        [cmake,'-S',str(ROOT/'experiments/phase_probe'),'-B',str(build),'-DCMAKE_BUILD_TYPE=Release',
         '-DCMAKE_CXX_FLAGS=','-DCMAKE_CXX_COMPILER='+compiler,'-DVF_LIBRARY='+str(library)],
        [cmake,'--build',str(build),'-j2']]
    builds=[]
    for i,cmd in enumerate(commands):
        record={'command':cmd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cwd':str(ROOT)}
        with (accepted/f'build-{i}.stdout').open('w') as out,(accepted/f'build-{i}.stderr').open('w') as err:
            proc=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=err)
        record.update(exit_code=proc.returncode,stdout=f'build-{i}.stdout',stderr=f'build-{i}.stderr')
        builds.append(record);save(accepted/'build-commands.json',builds)
        if proc.returncode:return proc.returncode
    shutil.copyfile(build/'compile_commands.json',accepted/'compile_commands.json')
    shutil.copyfile(build/'CMakeFiles/vflhcds_phase_probe.dir/link.txt',accepted/'link.txt')
    compile_command=shlex.split(read(accepted/'compile_commands.json')[0]['command'])
    assert all(flag in compile_command for flag in ['-O3','-DNDEBUG','-std=c++17','-Werror'])
    save(accepted/'probe-provenance.json',{'executable':str(binary),'executable_sha256':sha256(binary),
        'library':str(library),'library_sha256':sha256(library),'production_sha256':sha256(production),
        'compile_commands_sha256':sha256(accepted/'compile_commands.json'),
        'link_command_sha256':sha256(accepted/'link.txt'),
        'source_sha256':{str(p.relative_to(ROOT)):sha256(p) for p in sources}})
    expected=[(phase,event) for phase in ('parse','index','solve','serialize') for event in ('begin','end')]
    tests=[]
    for fixture in config['smoke_tests']:
        graph=ROOT/fixture['graph'];assert sha256(graph)==fixture['sha256']
        base=accepted/'smoke'/fixture['id'].split('/')[1]
        probe_dir,native_dir,valid_dir=[base/name for name in ('probe','production','validation')]
        for directory in (probe_dir,native_dir,valid_dir):directory.mkdir(parents=True)
        probe=capture([str(binary),str(graph),'3','5','adjacency'],probe_dir,60)
        assert probe['status']=='completed',probe
        markers=events(probe_dir)
        assert [(e['phase'],e['event']) for e in markers if e['phase']!='query']==expected
        query_markers=[e for e in markers if e['phase']=='query']
        native=capture([str(production),'solve','--graph',str(graph),'--h','3','--k','5',
                       '--core-reduction','off','--footprint-scan','sorted','--clique-enumeration','adjacency'],native_dir,60)
        assert native['status']=='completed',native
        status=read(native_dir/'stderr.txt');assert status['complete']
        assert (probe_dir/'stdout.txt').read_bytes()==(native_dir/'stdout.txt').read_bytes()
        assert [e['query_index'] for e in query_markers]==list(range(1,len(query_markers)+1))
        assert [e['stats'] for e in query_markers]==status['counters']['queries']
        assert len(query_markers)==status['counters']['logical_interval_queries']
        validation=capture([sys.executable,str(ROOT/'experiments/validate.py'),'--graph',str(graph),
                            '--records',str(probe_dir/'stdout.txt'),'--h','3','--k','5','--definition','--strict'],valid_dir,60)
        assert validation['status']=='completed'
        result=read(valid_dir/'stdout.txt')
        assert result['passed'] and result['level']=='definition_checked'
        tests.append({'id':fixture['id'],'status':'passed','output_count':result['output_count'],
             'phase_markers':8,'query_markers':len(query_markers),'query_counters_match_production':True,
             'production_output_identical':True,'definition_validation':result,
             'probe_process':probe,'production_process':native,'external_validator':validation})
        save(accepted/'smoke-results.json',tests)
        print(json.dumps({'test':fixture['id'],'status':'passed'}),flush=True)
    preserved()
    assert sha256(binary)==read(accepted/'probe-provenance.json')['executable_sha256']
    real=accepted/'real';real.mkdir()
    shutil.copyfile(ROOT/case['graph'],real/'graph.txt')
    assert sha256(real/'graph.txt')==case['sha256']
    save(accepted/'real-invocation.json',{'test':config['real_test'],'h':3,'k':5,
        'enumeration':'adjacency','graph_sha256':case['sha256'],'probe_sha256':sha256(binary),
        'timeout_seconds':60,'config_sha256':sha256(accepted/'config.json'),
        'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    print('Starting the single CA-CondMat diagnostic (60-second guard).',flush=True)
    process=capture([str(binary),str(real/'graph.txt'),'3','5','adjacency'],real,60)
    markers=events(real)
    boundaries=[e for e in markers if e['phase']!='query']
    assert [(e['phase'],e['event']) for e in boundaries]==expected[:len(boundaries)]
    queries=[e for e in markers if e['phase']=='query']
    assert [e['query_index'] for e in queries]==list(range(1,len(queries)+1))
    last=boundaries[-1] if boundaries else None
    result={'test':config['real_test'],'process':process,'events':markers,
            'last_phase_boundary':last,'completed_queries':len(queries),
            'incomplete_phase':last['phase'] if last and last['event']=='begin' else None,
            'external_validation':'not_run','evidence_scope':'Separate bounded phase diagnosis only.'}
    save(accepted/'real-result.json',result)
    preserved()
    save(accepted/'preservation-final.json',{'status':'passed','pins_source':str((HERE/'preservation-before.json').relative_to(ROOT))})
    save(accepted/'checksums.json',file_hashes(accepted))
    print(json.dumps({'native_status':process['status'],'incomplete_phase':result['incomplete_phase'],
                     'completed_queries':len(queries),'last_boundary':last}),flush=True)
    return 0 if process['status']=='completed' else 1

if __name__=='__main__':
    raise SystemExit(main())
