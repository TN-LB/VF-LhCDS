"""Read saved M4 acceptance evidence and write derived integrity manifests."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'evidence/m4'
ACCEPTED=HERE/'accepted'
ALLOWED_DOCS={'docs/BUILD.md','docs/INTERFACE_CONTRACT.md','docs/TASKS.md','docs/CLAIM_TRACEABILITY.md'}


def load(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')


def stream_digest(path,ignored):
    def strip(value):
        if isinstance(value,dict):return {k:strip(v) for k,v in value.items() if k not in ignored}
        if isinstance(value,list):return [strip(v) for v in value]
        return value
    result=hashlib.sha256();lines=0
    with gzip.open(path,'rt') as stream:
        for line in stream:
            result.update((json.dumps(strip(json.loads(line)),sort_keys=True,separators=(',',':'))+'\n').encode())
            lines+=1
    return {'sha256':result.hexdigest(),'records':lines}


def main():
    commands=load(ACCEPTED/'commands.json');assert len(commands)==36
    for command in commands:
        assert command['exit_code']==0,command
        for stream in ['stdout','stderr']:
            assert digest(ACCEPTED/command[stream])==command[stream+'_sha256']
    environment=load(ACCEPTED/'environment.json')
    for path,expected in environment['source_sha256'].items():assert digest(ROOT/path)==expected,path
    preserved={}
    for path,before in load(HERE/'preservation_start.json')['sha256'].items():
        after=digest(ROOT/path)
        if path not in ALLOWED_DOCS:assert before==after,path
        preserved[path]={'before_sha256':before,'after_sha256':after,'unchanged':before==after,
                         'allowed_contract_or_evidence_document':path in ALLOWED_DOCS}
    protected=subprocess.check_output(['git','diff','--name-only','HEAD','--','papers','reference','evidence/m3'],cwd=ROOT,text=True)
    assert not protected
    tag=subprocess.check_output(['git','rev-parse','v0.1.0-m3-correctness^{commit}'],cwd=ROOT,text=True).strip()
    assert tag==load(HERE/'preservation_start.json')['m3_tag']
    campaigns={};comparisons={}
    for summary_path in sorted(ACCEPTED.glob('build*/summary.json')):
        summary=load(summary_path);assert summary['status']=='passed'
        for name,expected in summary.get('sha256',summary.get('evidence_sha256')).items():
            assert digest(summary_path.parent/name)==expected,(summary_path,name)
        assert not (summary_path.parent/'probe.stderr').read_bytes()
        campaigns[summary_path.parent.name]={'summary':summary,'path':str(summary_path.relative_to(ROOT)),
                                          'summary_sha256':digest(summary_path)}
    assert len(campaigns)==14
    # Cross-build full responses agree except measured durations.
    for suffix in ['smoke','exhaustive-small','seeded','higher-h','m2-exhaustive-small','m2-seeded','m2-higher-h']:
        left,right=ACCEPTED/('build-'+suffix),ACCEPTED/('build-sanitize-'+suffix)
        assert (left/'cases.jsonl').read_bytes()==(right/'cases.jsonl').read_bytes(),suffix
        filename='results.jsonl.gz' if suffix.startswith('m2-') else 'mode_results.jsonl.gz'
        a=stream_digest(left/filename,{'core_reduction_seconds'})
        b=stream_digest(right/filename,{'core_reduction_seconds'})
        assert a==b,suffix
        comparisons[suffix]={'debug_vs_sanitizer':a,'excluded_fields':['core_reduction_seconds']}
    # The disabled M4 path reproduces the saved frozen M3 baseline corpus.
    for suffix in ['exhaustive-small','seeded','higher-h']:
        old=ROOT/'evidence/m3/accepted'/('build-'+suffix)
        new=ACCEPTED/('build-'+suffix)
        assert (old/'cases.jsonl').read_bytes()==(new/'cases.jsonl').read_bytes()
        ignored={'token','core','core_threshold','core_reduction_seconds'}
        a=stream_digest(old/'results.jsonl.gz',ignored);b=stream_digest(new/'results.jsonl.gz',ignored)
        assert a==b,suffix
        comparisons[suffix]['frozen_m3_vs_m4_off']=a
        comparisons[suffix]['m3_comparison_exclusions']=sorted(ignored)
    ctests=[]
    for command in commands:
        if command['command'][0]=='ctest':
            text=(ACCEPTED/command['stdout']).read_text()
            assert '100% tests passed' in text and 'out of 12' in text
            assert '74 passed' in text and 'M4 T17/P08: 30 checks passed' in text and 'M4 CLI: 40 invocations passed' in text
            ctests.append(command['command'][2])
    assert len(ctests)==4
    flags={}
    warnings=['-std=c++17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wsign-conversion','-Wshadow','-Werror']
    for build in ['build','build-sanitize','build-release','build-relwithdebinfo','build-production']:
        entries=load(ROOT/build/'compile_commands.json')
        for row in entries:
            assert all(flag in row['command'].split() for flag in warnings),row
            if build=='build-sanitize':assert all(flag in row['command'].split() for flag in ['-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer'])
        if build=='build-production':assert all('/tests/' not in row['file'] for row in entries)
        flags[build]=entries
    profiles=load(ACCEPTED/'profiles/summary.json')
    assert profiles['status']=='passed' and profiles['raw_runs']==36
    assert digest(ACCEPTED/'profiles/runs.json')==profiles['runs_sha256']
    assert digest(HERE/'profile_workload.json')==profiles['workload_sha256']
    assert digest(HERE/'profile_workload.json')==load(HERE/'profile-selection.json')['workload_sha256']
    runner=load(ACCEPTED/'cli-definition-run-safe-membership/manifest.json')
    assert runner['native_exit_code']==0 and runner['validation']['passed']
    for name,expected in runner['sha256'].items():assert digest(ACCEPTED/'cli-definition-run-safe-membership'/name)==expected
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    write('fixture_manifest.json',campaigns);write('cross_version_comparisons.json',comparisons)
    write('preservation_final.json',preserved);write('compiler_flags.json',flags)
    result={'status':'passed','accepted_commands':36,'command_manifest_sha256':digest(ACCEPTED/'commands.json'),
        'source_files_unchanged_since_acceptance':len(environment['source_sha256']),
        'protected_snapshot_files':len(preserved),'m3_tag_unchanged':tag,
        'ctest_profiles':ctests,'ctest_each':'12/12','pytest':'74 passed','campaign_directories':14,
        'mode_pairs_cross_build':7,'m3_frozen_corpus_comparisons':3,'local_profile_processes':36,
        'limitations':'Finite implementation/mode equivalence and local diagnostics only; no theorem, scalability or M5 benchmark proof'}
    write('verification.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
