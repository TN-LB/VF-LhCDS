"""Build only the phase probe, check two fixtures, run one bounded real case."""
import datetime
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


def load(path):
    return json.loads(path.read_text())


def phase_events(directory):
    events = [json.loads(line) for line in (directory / 'stderr.txt').read_text().splitlines()]
    assert all(e.get('diagnostic_schema') == 1 and 'elapsed_seconds' in e for e in events)
    assert all(0 <= a['elapsed_seconds'] <= b['elapsed_seconds'] for a, b in zip(events, events[1:]))
    return events


def main():
    accepted = HERE / 'accepted'
    accepted.mkdir(exist_ok=False)
    build = ROOT / 'build-m5-phase-probe'
    binary = build / 'vflhcds_phase_probe'
    production = ROOT / 'build-m5-release/vflhcds'
    library = ROOT / 'build-m5-release/libvflhcds_lib.a'
    prior = ROOT / 'evidence/m5/m4-mode-diagnostic-20261003'
    proposal = prior / 'NEXT_STEP.md'
    previous = load(prior / 'config.json')
    real = previous['cases'][0]
    assert sha256(production) == previous['algorithms'][0]['sha256']
    assert sha256(ROOT / real['graph']) == real['sha256']
    source = load(ROOT / 'evidence/m4/accepted/environment.json')['source_sha256']
    papers = load(ROOT / 'review/source_snapshot_sha256.json')['sha256']
    preserved = {**source, **papers, str(production.relative_to(ROOT)): sha256(production),
                 str(library.relative_to(ROOT)): sha256(library)}
    for name, digest in preserved.items():
        assert sha256(ROOT / name) == digest, name
    save(accepted / 'preservation-start.json', preserved)
    save(accepted / 'authorization.json', {
        'owner_reply': '继续', 'scope': 'Execute the proposed bounded phase diagnostic; prepare a repair plan if indexing remains unfinished.',
        'proposal': str(proposal.relative_to(ROOT)), 'proposal_sha256': sha256(proposal),
        'production_change_authorized': False, 'final_benchmark_approved': False})
    fixture_names = ['triangle_and_isolate', 'bridged_triangles']
    config = {'scope': 'phase_diagnostic', 'real_case': real, 'real_repeats': 1,
              'timeout_seconds': 60, 'threads': 1, 'memory_limit_bytes': None,
              'cache_policy': 'uncontrolled', 'seed': None,
              'seed_reason': 'One deterministic case/mode; no randomized scheduling.',
              'mode': {'core': 'off', 'footprints': 'sorted'},
              'smoke_tests': [{'id': 'T-PHASE-01/' + name, 'graph': 'reference/fixtures/' + name + '.graph',
                               'sha256': sha256(ROOT / 'reference/fixtures' / (name + '.graph')), 'h': 3, 'k': 5}
                              for name in fixture_names],
              'real_test': 'T-PHASE-02/flushed-boundary-on-timeout',
              'separation': 'Instrumented process resources are diagnostic only; external validation runs later.'}
    save(accepted / 'config.json', config)
    snapshot = accepted / 'source-snapshot'
    files = [HERE / 'run_diagnostic.py', ROOT / 'experiments/phase_probe/CMakeLists.txt',
             ROOT / 'experiments/phase_probe/main.cpp', ROOT / 'experiments/support.py',
             ROOT / 'experiments/validate.py', ROOT / 'baselines/ippv/process.py']
    for path in files:
        target = snapshot / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    save(accepted / 'environment.json', {
        'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'platform': platform.platform(), 'python': sys.version,
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'dirty_tree': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in files},
        'configuration_sha256': sha256(accepted / 'config.json')})
    shutil.copyfile(prior / 'hardware-retry.json', accepted / 'hardware-prior-same-host.json')
    shutil.copyfile(production.with_suffix('.provenance.json'), accepted / 'production-provenance.json')
    compiler = shlex.split(load(ROOT / 'build-m5-release/compile_commands.json')[0]['command'])[0]
    cmake = str(ROOT / '.venv/bin/cmake')
    commands = [
        [cmake, '-S', str(ROOT / 'experiments/phase_probe'), '-B', str(build),
         '-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_CXX_FLAGS=', '-DCMAKE_CXX_COMPILER=' + compiler,
         '-DVF_LIBRARY=' + str(library)],
        [cmake, '--build', str(build), '-j2']]
    records = []
    for i, command in enumerate(commands):
        record = {'command': command, 'cwd': str(ROOT),
                  'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        with (accepted / f'build-{i}.stdout').open('w') as stdout, (accepted / f'build-{i}.stderr').open('w') as stderr:
            result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr)
        record.update(exit_code=result.returncode, stdout=f'build-{i}.stdout', stderr=f'build-{i}.stderr')
        records.append(record)
        save(accepted / 'build-commands.json', records)
        if result.returncode:
            return result.returncode
    shutil.copyfile(build / 'compile_commands.json', accepted / 'compile_commands.json')
    shutil.copyfile(build / 'CMakeFiles/vflhcds_phase_probe.dir/link.txt', accepted / 'link.txt')
    save(accepted / 'probe-provenance.json', {
        'executable': str(binary), 'executable_sha256': sha256(binary),
        'library': str(library), 'library_sha256': sha256(library),
        'production_sha256': sha256(production),
        'compile_commands_sha256': sha256(accepted / 'compile_commands.json'),
        'link_command_sha256': sha256(accepted / 'link.txt'),
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in files}})
    expected = [(phase, event) for phase in ['parse', 'index', 'solve', 'serialize'] for event in ['begin', 'end']]
    tests = []
    for fixture in config['smoke_tests']:
        graph = ROOT / fixture['graph']
        assert sha256(graph) == fixture['sha256']
        name = fixture['id'].split('/')[1]
        base = accepted / 'smoke' / name
        probe_dir, native_dir, validation_dir = [base / p for p in ['probe', 'production', 'validation']]
        for directory in [probe_dir, native_dir, validation_dir]:
            directory.mkdir(parents=True)
        probe = capture([str(binary), str(graph), '3', '5'], probe_dir, 60)
        assert probe['status'] == 'completed', probe
        events = phase_events(probe_dir)
        assert [(e['phase'], e['event']) for e in events] == expected
        native = capture([str(production), 'solve', '--graph', str(graph), '--h', '3', '--k', '5',
                          '--core-reduction', 'off', '--footprint-scan', 'sorted'], native_dir, 60)
        assert native['status'] == 'completed', native
        assert load(native_dir / 'stderr.txt')['complete'] is True
        assert (probe_dir / 'stdout.txt').read_bytes() == (native_dir / 'stdout.txt').read_bytes()
        validation = capture([sys.executable, str(ROOT / 'experiments/validate.py'), '--graph', str(graph),
                              '--records', str(probe_dir / 'stdout.txt'), '--h', '3', '--k', '5',
                              '--definition', '--strict'], validation_dir, 60)
        assert validation['status'] == 'completed'
        result = load(validation_dir / 'stdout.txt')
        assert result['passed'] and result['level'] == 'definition_checked'
        tests.append({'id': fixture['id'], 'status': 'passed', 'output_count': result['output_count'],
                      'markers': len(events), 'canonical_output_matches_production': True,
                      'definition_validation': result, 'probe_process': probe,
                      'production_process': native, 'external_validation_process': validation})
        save(accepted / 'smoke-results.json', tests)
        print(json.dumps({'test': fixture['id'], 'status': 'passed'}), flush=True)
    for name, digest in preserved.items():
        assert sha256(ROOT / name) == digest, name
    assert sha256(binary) == load(accepted / 'probe-provenance.json')['executable_sha256']
    assert sha256(ROOT / real['graph']) == real['sha256']
    real_dir = accepted / 'real'
    real_dir.mkdir()
    shutil.copyfile(ROOT / real['graph'], real_dir / 'graph.txt')
    save(accepted / 'real-invocation.json', {'test': config['real_test'], 'h': real['h'], 'k': real['k'],
        'graph_sha256': real['sha256'], 'probe_sha256': sha256(binary), 'timeout_seconds': 60,
        'config_sha256': sha256(accepted / 'config.json')})
    print('Starting the single CA-GrQc phase diagnostic (60-second guard).', flush=True)
    process = capture([str(binary), str(real_dir / 'graph.txt'), str(real['h']), str(real['k'])], real_dir, 60)
    events = phase_events(real_dir)
    observed = [(e['phase'], e['event']) for e in events]
    assert observed == expected[:len(observed)]
    last = events[-1] if events else None
    result = {'test': config['real_test'], 'native_status': process['status'], 'process': process,
              'events': events, 'last_marker': last,
              'incomplete_phase': last['phase'] if last and last['event'] == 'begin' else None,
              'external_validation': 'not_run', 'evidence_scope': 'instrumented phase boundary diagnosis only'}
    save(accepted / 'real-result.json', result)
    for name, digest in preserved.items():
        assert sha256(ROOT / name) == digest, name
    save(accepted / 'preservation-final.json', {'status': 'passed', 'sha256': preserved})
    save(accepted / 'checksums.json', file_hashes(accepted))
    print(json.dumps({'native_status': process['status'], 'incomplete_phase': result['incomplete_phase'],
                      'last_marker': last}), flush=True)
    return 0 if process['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
