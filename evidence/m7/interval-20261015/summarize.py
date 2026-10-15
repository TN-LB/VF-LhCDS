"""Verify executed acceptance artifacts and summarize finite M7 development work."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'experiments/final_profile'))
from reports import build, load_bundle, profile

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text())
def save(path,value):path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')

def main():
    acceptance=HERE/'acceptance'
    schedule=read(acceptance/'schedule.json');commands=read(acceptance/'commands.json')
    assert [r['command'] for r in commands]==schedule
    assert all(r['exit_code']==0 for r in commands)
    for row in commands:
        for field in ('stdout','stderr'):
            assert digest(acceptance/row[field])==row[field+'_sha256']
    tiers={}
    for build_name in ('debug','sanitize'):
        tiers[build_name]={}
        for tier in ('smoke','exhaustive-small','seeded','higher-h'):
            directory=acceptance/(build_name+'-'+tier);summary=read(directory/'summary.json')
            assert summary['status']=='passed'
            for name,expected in summary['sha256'].items():assert digest(directory/name)==expected
            tiers[build_name][tier]={key:summary[key] for key in (
                'base_graph_h_cases','checked_variants','solver_runs','mode_checks','seed','probe_sha256')}
            if build_name=='sanitize':
                assert digest(directory/'cases.jsonl')==digest(acceptance/('debug-'+tier)/'cases.jsonl')
    diagnostics={};examples=[];final_manifests={}
    for name in ('release','sanitize'):
        directory=acceptance/('profile-'+name)
        checks=read(directory/'checks.json');assert checks['passed'] and not checks['formal_experiment']
        bundle=load_bundle(directory/'bundle.json');report=build(bundle)
        assert report==read(directory/'reports.json')
        assert not report['missing_run_ids']
        assert report['outcomes']['completed']==672
        assert all(row['coverage']=='paired' for row in report['local_cliques'])
        assert all(row['coverage']=='executed_full_suffix' for row in report['early_stop'])
        diagnostics[name]={'native_cli_calls':checks['native_calls'],'control_trace_calls':len(checks['diagnostic_checks']),
            'independent_diagnostic_checks':len(checks['diagnostic_checks']),
            'queries':sum(row['queries'] for row in checks['diagnostic_checks']),
            'max_depth':max(row['maximum_depth'] for row in checks['diagnostic_checks']),
            'core_pairs':len(report['core']),'local_pairs':len(report['local_cliques']),
            'full_suffix_pairs':len(report['early_stop']),'report_regeneration_equal':True,
            'outcomes':report['outcomes']}
        manifest=read(directory/'configuration.json')['source_manifest']
        final_manifests[name]=manifest
        for path,expected in manifest['production'].items():assert digest(ROOT/path)==expected,path
        for path,expected in manifest['observer'].items():assert digest(ROOT/'experiments/final_profile'/path)==expected,path
        for row in bundle['rows']:
            if row['role']=='diagnostic' and row['core']=='off' and row['k']=='all' and row['suite'] in (
                    'development:core_restore','development:nested_density_layers_4','development:isolates'):
                work=profile(row)['work']
                examples.append({'build':name,'fixture':row['suite'].split(':',1)[1],'mode':row['work_mode'],
                    **{key:work[key] for key in ('footprint_clique_visits','partition_clique_visits','count_clique_visits',
                        'count_separator_calls','count_emitted_calls','reused_endpoint_counts','clique_ids_initialized',
                        'clique_id_capacity','clique_id_bytes','frontier_peak_size','frontier_peak_capacity')},
                    'control_process_peak_rss_bytes':next(other['peak_rss_bytes'] for other in bundle['rows']
                        if other['role']=='control' and all(other[key]==row[key] for key in ('suite','h','k','core','work_mode')))
                })
    assert final_manifests['release']['production']==final_manifests['sanitize']['production']
    assert final_manifests['release']['observer']==final_manifests['sanitize']['observer']
    # Production/reference/manuscript boundary, against the task's starting commit.
    unchanged=['papers','reference','src/core','src/flow','include/vflhcds/flow',
               'src/clique','include/vflhcds/clique','baselines','experiments/fine_profile','evidence/m5','evidence/m6']
    subprocess.run(['git','diff','--exit-code','046c553','--',*unchanged],cwd=ROOT,check=True,capture_output=True)
    report={'passed':True,'scope':'finite development validation; no formal M8 result or speedup claim',
        'commands':len(commands),'tiers':tiers,'diagnostics':diagnostics,'work_examples':examples,
        'preserved_paths':unchanged,'production_pins':final_manifests['release']['production'],
        'observer_pins':final_manifests['release']['observer'],
        'total_mode_solver_executions':sum(s['mode_checks']['solve_executions'] for b in tiers.values() for s in b.values()),
        'total_cli_diagnostic_control_calls':sum(s['native_cli_calls'] for s in diagnostics.values()),
        'total_control_trace_calls':sum(s['control_trace_calls'] for s in diagnostics.values())}
    save(HERE/'checks.json',report)
    save(HERE/'fixture_manifest.json',{'solver_tiers':{name:{tier:{'path':str((acceptance/(name+'-'+tier)/'cases.jsonl').relative_to(HERE)),
        'sha256':digest(acceptance/(name+'-'+tier)/'cases.jsonl'),
        'cases':values['checked_variants'],'seed':values['seed']} for tier,values in data.items()} for name,data in tiers.items()},
        'diagnostic_fixture_count':28,'diagnostic_seed':20261014,
        'diagnostic_modes':['global','interval-scan','interval-reuse'],'core':['off','safe'],
        'diagnostic_k':[1,'all'],'solver_footprints':['sorted','membership'],
        'solver_counting':{'debug':'sorted','sanitize':'membership'},
        'enumerators':'Both in T21/T22 and 594 CLI cases per build; adjacency with ordered-combination cross-check in truth tiers'})
    print(json.dumps({key:report[key] for key in ('passed','commands','total_mode_solver_executions',
        'total_cli_diagnostic_control_calls','total_control_trace_calls')},sort_keys=True))

if __name__=='__main__':main()
