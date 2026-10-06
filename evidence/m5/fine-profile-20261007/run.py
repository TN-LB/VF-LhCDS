"""One frozen diagnostic, with fresh logs, strict gates and no automatic retry."""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import capture, file_hashes, save, sha256

PYTHON = str(ROOT / '.venv/bin/python')
CMAKE = str(ROOT / '.venv/bin/cmake')
CTEST = str(ROOT / '.venv/bin/ctest')
RELEASE = ROOT / 'build-m5-fine-profile-release'
SANITIZED = ROOT / 'build-m5-fine-profile-sanitized'


def read(path):
    return json.loads(Path(path).read_text())


def command(name, args, timeout=600):
    directory = HERE / 'commands' / name
    directory.mkdir(parents=True, exist_ok=True)
    result = capture(args, directory, timeout)
    print(name, result['status'], result['native_exit_code'], flush=True)
    if result['status'] != 'completed':
        raise RuntimeError(f'command failed: {name}; see preserved logs')
    return result


def freeze():
    if (HERE / 'preflight.json').exists():
        raise FileExistsError('preflight already frozen')
    old = read(ROOT / 'evidence/m5/core-ablation-20261006/preflight.json')
    keys = ('paper_sha256', 'reference_sha256', 'production_source_sha256',
            'binary_sha256', 'provenance_sha256', 'library_sha256', 'old_probe_sha256',
            'pinned_harness_sha256')
    pins = {key: old[key] for key in keys}
    assert pins['paper_sha256'] == read(ROOT / 'review/source_snapshot_sha256.json')['sha256']
    for group in pins.values():
        for path, digest in group.items():
            assert sha256(ROOT / path) == digest, path
    old_names = subprocess.check_output(['git', 'ls-files', 'evidence'], cwd=ROOT, text=True).splitlines()
    pins['historical_evidence_sha256'] = {name: sha256(ROOT / name) for name in old_names
                                         if name != 'evidence/m5/REPORT.md'}
    pins['diagnostic_source_sha256'] = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in sorted((ROOT / 'experiments/fine_profile').glob('*')) if path.is_file()
    }
    pins['configuration_sha256'] = sha256(HERE / 'config.json')
    pins['runner_sha256'] = sha256(Path(__file__))
    pins['decision_log_sha256'] = sha256(ROOT / 'docs/DECISIONS.md')
    save(HERE / 'preflight.json', pins)
    config = read(HERE / 'config.json')
    for case in config['tiny'] + config['real']:
        assert sha256(ROOT / case['graph']) == case['graph_sha256']
    save(HERE / 'source-state.json', {
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'git_status': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'frozen_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    })


def build():
    for name, path, mode, extra in (
            ('release', RELEASE, 'Release', []),
            ('sanitized', SANITIZED, 'Debug', ['-DVFLHCDS_ENABLE_SANITIZERS=ON'])):
        command(name + '-configure', [CMAKE, '-S', str(ROOT / 'experiments/fine_profile'),
                '-B', str(path), '-DCMAKE_BUILD_TYPE=' + mode, '-DPython3_EXECUTABLE=' + PYTHON] + extra)
        command(name + '-build', [CMAKE, '--build', str(path), '--target',
                'vflhcds_fine_profile', 'profile_timer_test', '-j2'])
        command(name + '-ctest', [CTEST, '--test-dir', str(path), '--output-on-failure'])
        saved = HERE / 'build' / name
        saved.mkdir(parents=True)
        for source in [path / 'CMakeCache.txt', path / 'compile_commands.json',
                       *sorted((path / 'instrumented').glob('*'))]:
            shutil.copyfile(source, saved / source.name)
    command('pytest', [PYTHON, '-m', 'pytest', str(ROOT / 'reference/tests'),
            str(ROOT / 'experiments/test_harness.py'), str(ROOT / 'baselines/ippv/test_adapter.py'),
            str(ROOT / 'experiments/fine_profile/test_instrument.py'), '-q'])
    save(HERE / 'binaries.json', {
        str(path.relative_to(ROOT)): sha256(path) for path in (
            ROOT / read(HERE / 'config.json')['production_binary'],
            RELEASE / 'vflhcds_fine_profile', SANITIZED / 'vflhcds_fine_profile')})


def events(directory):
    return [json.loads(line) for line in (directory / 'stderr.txt').read_text().splitlines()]


def measured_run(case, mode, definition):
    config = read(HERE / 'config.json')
    directory = HERE / 'runs' / (case['name'] + '-' + mode)
    directory.mkdir(parents=True)
    graph = ROOT / case['graph']
    if mode == 'production':
        args = [str(ROOT / config['production_binary']), 'solve', '--graph', str(graph),
                '--h', '3', '--k', '5', '--clique-enumeration', 'adjacency',
                '--footprint-scan', 'membership', '--core-reduction', 'off']
    else:
        binary = (RELEASE if mode == 'release' else SANITIZED) / 'vflhcds_fine_profile'
        args = [str(binary), str(graph), '3', '5']
    save(directory / 'manifest.json', {'case': case, 'mode': mode,
         'config_sha256': sha256(HERE / 'config.json'), 'command': args})
    proc = capture(args, directory, config['timeout_seconds'])
    print(case['name'], mode, proc['status'], proc['wall_seconds'], flush=True)
    if proc['status'] == 'timeout' and not definition:
        return False
    if proc['status'] != 'completed':
        raise RuntimeError(f'native failure: {directory.name}')
    validate = [PYTHON, str(ROOT / 'experiments/validate.py'), '--graph', str(graph),
                '--records', str(directory / 'stdout.txt'), '--h', '3', '--k', '5', '--strict']
    if definition:
        validate += ['--definition']
    if mode == 'production':
        validate += ['--status', str(directory / 'stderr.txt')]
    validation = directory / 'validation'
    validation.mkdir()
    checked = capture(validate, validation, config['timeout_seconds'])
    if checked['status'] != 'completed' or not read(validation / 'stdout.txt')['passed']:
        raise RuntimeError(f'validation failure: {directory.name}')
    if mode != 'production':
        output = events(directory)
        summaries = [row for row in output if row.get('phase') == 'summary']
        assert len(summaries) == 1
        summary = summaries[0]
        queries = [row for row in output if row.get('phase') == 'query']
        assert [row['query_index'] for row in queries] == list(range(1, len(queries) + 1))
        assert [row['stats'] for row in queries] == summary['stats']['queries']
        assert summary['exclusive']['max_flow']['calls'] == summary['stats']['mincut_calls']
        assert summary['exclusive']['footprints']['calls'] == summary['stats']['mincut_calls']
        assert all(bucket['nanoseconds'] >= 0 for bucket in summary['exclusive'].values())
        control = HERE / 'runs' / (case['name'] + '-production')
        if read(control / 'process.json')['status'] == 'completed':
            comparison = {
                'strict_output_equal': (directory / 'stdout.txt').read_bytes() == (control / 'stdout.txt').read_bytes(),
                'all_counters_equal': summary['stats'] == read(control / 'stderr.txt')['counters'],
            }
            save(directory / 'comparison.json', comparison)
            if not all(comparison.values()):
                raise RuntimeError(f'instrumentation mismatch: {directory.name}')
    return True


def run_cases(tiny):
    config = read(HERE / 'config.json')
    if not tiny:
        assert read(HERE / 'tiny-gate.json')['passed']
    attempted = []
    for case in config['tiny' if tiny else 'real']:
        for mode in ('production', 'release', 'sanitized') if tiny else ('production', 'release'):
            completed = measured_run(case, mode, tiny)
            attempted.append({'case': case['name'], 'mode': mode, 'completed': completed})
    save(HERE / ('tiny-gate.json' if tiny else 'native-completion.json'),
         {'passed': all(row['completed'] for row in attempted), 'attempted': attempted})


def aggregate():
    rows = []
    for case in read(HERE / 'config.json')['real']:
        row = {'case': case['name']}
        for mode in ('production', 'release'):
            directory = HERE / 'runs' / (case['name'] + '-' + mode)
            proc = read(directory / 'process.json')
            data = {key: proc[key] for key in ('status', 'wall_seconds', 'user_seconds', 'system_seconds', 'peak_rss_bytes')}
            if mode == 'production' and proc['status'] == 'completed':
                data['timing'] = read(directory / 'stderr.txt')['timing']
            if mode == 'release':
                trace = events(directory)
                queries = [event for event in trace if event.get('phase') == 'query']
                data['completed_queries'] = len(queries)
                if queries:
                    data['last_query_elapsed_seconds'] = queries[-1]['elapsed_seconds']
                summary = next((event for event in trace if event.get('phase') == 'summary'), None)
                data['profile_scope'] = 'complete_solve' if summary else 'completed_query_prefix_only'
                data['exclusive'] = summary['exclusive'] if summary else (queries[-1]['exclusive'] if queries else None)
                if summary:
                    data['counters'] = {key: value for key, value in summary['stats'].items() if key != 'queries'}
                    total_ns = sum(bucket['nanoseconds'] for bucket in data['exclusive'].values())
                    data['accounted_solve_seconds'] = total_ns / 1e9
                    data['percent_of_accounted_solve'] = {
                        key: 100 * bucket['nanoseconds'] / total_ns for key, bucket in data['exclusive'].items()}
                    boundaries = {event['event']: event['elapsed_seconds'] for event in trace if event.get('phase') == 'solve'}
                    data['boundary_solve_seconds'] = boundaries['end'] - boundaries['begin']
                    assert data['accounted_solve_seconds'] <= data['boundary_solve_seconds'] + 1e-9
                if (directory / 'comparison.json').exists():
                    data['comparison'] = read(directory / 'comparison.json')
            row[mode] = data
        if row['production']['status'] == row['release']['status'] == 'completed':
            row['diagnostic_to_control_wall_ratio'] = row['release']['wall_seconds'] / row['production']['wall_seconds']
        rows.append(row)
    return {'rows': rows, 'timing_scope': 'diagnostic exclusive buckets, not a baseline performance comparison'}


def verify():
    pins = read(HERE / 'preflight.json')
    checked = {}
    for key, value in pins.items():
        if not isinstance(value, dict):
            continue
        for path, digest in value.items():
            assert sha256(ROOT / path) == digest, path
        checked[key] = len(value)
    assert pins['configuration_sha256'] == sha256(HERE / 'config.json')
    assert pins['runner_sha256'] == sha256(Path(__file__))
    assert pins['decision_log_sha256'] == sha256(ROOT / 'docs/DECISIONS.md')
    for path, digest in read(HERE / 'binaries.json').items():
        assert sha256(ROOT / path) == digest
    regenerated = HERE / 'aggregate.regenerated.json'
    save(regenerated, aggregate())
    assert regenerated.read_bytes() == (HERE / 'aggregate.json').read_bytes()
    for process in (HERE / 'runs').rglob('process.json'):
        for name, digest in read(process)['sha256'].items():
            assert sha256(process.parent / name) == digest
    save(HERE / 'verification.json', {'passed': True, 'unchanged_groups': checked,
         'regeneration_byte_identical': True, 'raw_process_records_verified': len(list((HERE / 'runs').rglob('process.json')))})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['freeze', 'build', 'tiny', 'profile', 'aggregate', 'verify'])
    args = parser.parse_args()
    if args.stage == 'freeze': freeze()
    elif args.stage == 'build': build()
    elif args.stage == 'tiny': run_cases(True)
    elif args.stage == 'profile': run_cases(False)
    elif args.stage == 'aggregate': save(HERE / 'aggregate.json', aggregate())
    else: verify()
