"""Frozen shared-input runs with separate validation and no outcome filtering."""
import argparse
import datetime
import json
import math
from pathlib import Path
import platform
import random
import signal
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.support import ROOT, canonical_graph, capture, file_hashes, graph_sha256, parse_graph, run_ippv, save, semantic_hash, sha256
from experiments.validate import compare, compare_prefix, parse_records
from experiments.environment import snapshot, power_change


def load_config(path):
    config = json.loads(Path(path).read_text())
    keys = {'schema_version', 'name', 'scope', 'seed', 'repeats', 'threads', 'timeout_seconds',
            'memory_limit_bytes', 'cache_policy', 'algorithms', 'cases'}
    if set(config) != keys or config['schema_version'] != 1:
        raise ValueError('configuration schema/keys mismatch')
    if config['scope'] not in ('diagnostic', 'approved_campaign'):
        raise ValueError('draft configurations cannot run; approval must be recorded first')
    for key, minimum in [('seed', 0), ('repeats', 1), ('threads', 1)]:
        if type(config[key]) is not int or config[key] < minimum:
            raise ValueError('invalid ' + key)
    if config['threads'] != 1 or config['memory_limit_bytes'] is not None or config['cache_policy'] != 'uncontrolled':
        raise ValueError('currently supports single-worker, uncapped memory, uncontrolled cache only')
    timeout = config['timeout_seconds']
    if type(timeout) not in (float, int) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('finite positive timeout required')
    if not config['algorithms'] or not config['cases']:
        raise ValueError('algorithms and cases cannot be empty')
    names = set()
    for algorithm in config['algorithms']:
        if set(algorithm) != {'name', 'kind', 'executable', 'sha256', 'options'}:
            raise ValueError('algorithm schema mismatch')
        if algorithm['name'] in names:
            raise ValueError('duplicate algorithm name')
        names.add(algorithm['name'])
        binary = (ROOT / algorithm['executable']).resolve()
        if sha256(binary) != algorithm['sha256']:
            raise ValueError('binary checksum mismatch')
        provenance = json.loads(binary.with_suffix('.provenance.json').read_text())
        if provenance['executable_sha256'] != algorithm['sha256']:
            raise ValueError('binary provenance mismatch')
        options = algorithm['options']
        if algorithm['kind'] == 'vf':
            if (not {'core', 'footprints'} <= set(options)
                    or not set(options) <= {'core', 'footprints', 'enumeration', 'counting', 'output'}
                    or options['core'] not in ('off', 'safe') or options['footprints'] not in ('sorted', 'membership')
                    or options.get('enumeration', 'combinations') not in ('combinations', 'adjacency')
                    or options.get('counting', 'sorted') not in ('sorted', 'membership')
                    or options.get('output', 'fixed') not in ('fixed', 'all')):
                raise ValueError('invalid VF switches')
            for name, digest in provenance['source_sha256'].items():
                if sha256(ROOT / name) != digest:
                    raise ValueError('VF source differs from recorded build')
        elif algorithm['kind'] == 'ippv':
            if set(options) != {'iterations'} or type(options['iterations']) is not int or options['iterations'] < 1:
                raise ValueError('invalid IPPV iterations')
            lock = json.loads((ROOT / 'baselines/ippv/source-lock.json').read_text())
            if any(provenance[key] != lock[key] for key in ('commit', 'patches', 'patched_source_sha256')):
                raise ValueError('IPPV provenance does not match source lock')
        else:
            raise ValueError('unknown algorithm')
    names.clear()
    for case in config['cases']:
        if set(case) != {'name', 'graph', 'sha256', 'h', 'k', 'definition'} or case['name'] in names:
            raise ValueError('case schema or duplicate name')
        names.add(case['name'])
        if type(case['h']) is not int or case['h'] < 2 or type(case['k']) is not int or case['k'] < 1 or type(case['definition']) is not bool:
            raise ValueError('invalid case parameters')
        graph = parse_graph((ROOT / case['graph']).read_text())
        if graph_sha256(graph) != case['sha256']:
            raise ValueError('graph checksum mismatch')
        if case['definition'] and graph.n > 12:
            raise ValueError('definition corpus exceeds independent-reference guard')
        # A predeclared local smoke may use structural checks on real input.
        # Only an approved campaign may be used for final performance conclusions.
    return config


def schedule(config):
    rng, blocks = random.Random(config['seed']), []
    for case in config['cases']:
        for repeat in range(config['repeats']):
            order = list(range(len(config['algorithms'])))
            rng.shuffle(order)
            blocks.append({'case': case['name'], 'repeat': repeat, 'algorithm_indices': order})
    return blocks


def run_vf(algorithm, graph, case, output, timeout):
    output.mkdir(parents=True, exist_ok=False)
    (output / 'graph.txt').write_text(canonical_graph(graph))
    binary = (ROOT / algorithm['executable']).resolve()
    options = algorithm['options']
    full = options.get('output', 'fixed') == 'all'
    scope_args = ['--all'] if full else ['--k', str(case['k'])]
    command = [str(binary), 'solve', '--graph', str(output / 'graph.txt'), '--h', str(case['h']), *scope_args,
               '--core-reduction', options['core'], '--footprint-scan', options['footprints']]
    if 'enumeration' in options:
        command += ['--clique-enumeration', options['enumeration']]
    if 'counting' in options:
        command += ['--clique-count', options['counting']]
    native = capture(command, output, timeout)
    manifest = {'algorithm': algorithm, 'build_provenance': json.loads(binary.with_suffix('.provenance.json').read_text()),
                'graph_sha256': graph_sha256(graph), 'h': case['h'], 'k': None if full else case['k'], 'native': native,
                'status': native['status'], 'validation': {'level': 'not_run'},
                'phase_wall_seconds': {'postload': None, 'postindex': None}}
    try:
        status = json.loads((output / 'stderr.txt').read_text())
        if not isinstance(status, dict):
            status = {}
    except ValueError:
        status = {}
    manifest['native_status'] = status
    if native['status'] == 'completed':
        if status.get('status') != 'completed' or status.get('complete') is not True:
            manifest['status'] = 'output_incomplete'
        else:
            validation_dir = output / 'validation'
            validation_dir.mkdir()
            cmd = [sys.executable, str(ROOT / 'experiments/validate.py'), '--graph', str(output / 'graph.txt'),
                   '--records', str(output / 'stdout.txt'), '--status', str(output / 'stderr.txt'),
                   '--h', str(case['h']), *scope_args, '--strict']
            if case['definition']:
                cmd.append('--definition')
            external = capture(cmd, validation_dir, timeout)
            manifest['external_validation'] = external
            try:
                manifest['validation'] = json.loads((validation_dir / 'stdout.txt').read_text())
            except ValueError:
                manifest['validation'] = {'level': 'not_completed', 'passed': False}
            if external['status'] != 'completed' or manifest['validation']['level'] == 'not_completed':
                manifest['status'] = 'validation_error'
            elif not manifest['validation']['passed']:
                manifest['status'] = 'semantic_mismatch' if case['definition'] else 'structural_mismatch'
            else:
                (output / 'canonical_output.jsonl').write_bytes((output / 'stdout.txt').read_bytes())
            manifest['phase_wall_seconds'] = {'postload': status.get('timing', {}).get('T_postload'),
                                              'postindex': status.get('timing', {}).get('T_core')}
    elif native['status'] == 'error' and native['native_exit_code'] == 6 and status.get('status') == 'oom':
        manifest['status'] = 'oom'  # Explicit documented native OOM, never guessed from a signal.
    manifest['sha256'] = file_hashes(output)
    save(output / 'manifest.json', manifest)
    return manifest


def validate_comparison(config, require_strict_agreement, require_prefix_agreement):
    algorithms = config['algorithms']
    full = [a for a in algorithms if a['options'].get('output', 'fixed') == 'all']
    if require_prefix_agreement:
        if require_strict_agreement or len(algorithms) != 2 or len(full) != 1 or any(a['kind'] != 'vf' for a in algorithms):
            raise ValueError('prefix agreement requires exactly one fixed/full VF pair, without whole-output strict mode')
        normalized = [{k: v for k, v in a.items() if k != 'name'} for a in algorithms]
        normalized = [{**a, 'options': {k: v for k, v in a['options'].items() if k != 'output'}} for a in normalized]
        if normalized[0] != normalized[1]:
            raise ValueError('prefix pair must differ only in output scope')
    elif full:
        raise ValueError('full-output runs require explicit prefix agreement')


def execute(config_path, output, *, stop_on_failure=False, continue_on_timeout=False,
            require_strict_agreement=False, require_prefix_agreement=False, environment_baseline=None,
            interrupted=None):
    if continue_on_timeout and not stop_on_failure:
        raise ValueError('continue_on_timeout requires stop_on_failure')
    config = load_config(config_path)
    validate_comparison(config, require_strict_agreement, require_prefix_agreement)
    baseline = json.loads(Path(environment_baseline).read_text()) if environment_baseline is not None else None
    agreement_key = 'prefix_match' if require_prefix_agreement else ('strict_match' if require_strict_agreement else 'tie_aware_match')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    save(output / 'config.json', config)
    blocks = schedule(config)
    save(output / 'schedule.json', blocks)
    planned = [{'case': block['case'], 'repeat': block['repeat'],
                'algorithm': config['algorithms'][index]['name'], 'directory': f'runs/{block_id:04d}-{index}'}
               for block_id, block in enumerate(blocks) for index in block['algorithm_indices']]
    save(output / 'execution-policy.json', {'stop_on_failure': stop_on_failure,
                                          'require_strict_agreement': require_strict_agreement,
                                          'require_prefix_agreement': require_prefix_agreement,
                                          'environment_baseline': baseline,
                                          'continue_on_timeout': continue_on_timeout, 'planned_runs': planned})
    save(output / 'environment.json', {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'platform': platform.platform(),
        'python': sys.version, 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'dirty_tree': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'script_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted((ROOT / 'experiments').glob('*.py'))},
        'configuration_sha256': sha256(output / 'config.json'), 'schedule_sha256': sha256(output / 'schedule.json'),
        'execution_policy_sha256': sha256(output / 'execution-policy.json')})
    cases = {case['name']: case for case in config['cases']}
    full_names = {a['name'] for a in config['algorithms'] if a['options'].get('output') == 'all'}
    rows, comparisons = [], []
    save(output / 'summary.json', {'runs': rows, 'comparisons': comparisons})

    def stop(reason):
        recorded = {row['directory'] for row in rows}
        save(output / 'stopped.json', {'reason': reason, 'planned_count': len(planned),
                                      'recorded_count': len(rows),
                                      'unrun': [run for run in planned if run['directory'] not in recorded]})
        save(output / 'checksums.json', file_hashes(output))
        return 1

    for block_id, block in enumerate(blocks):
        stop_reason = None
        if interrupted is not None and interrupted():
            return stop({'kind': 'external_interruption'})
        if baseline is not None:
            before = snapshot()
            save(output / f'block-{block_id:04d}-before.json', before)
            reason = power_change(baseline, before)
            if reason is not None:
                return stop(reason)
        case = cases[block['case']]
        graph = parse_graph((ROOT / case['graph']).read_text())
        if graph_sha256(graph) != case['sha256']:
            raise RuntimeError('input changed after configuration was frozen')
        done = []
        for index in block['algorithm_indices']:
            if interrupted is not None and interrupted():
                stop_reason = {'kind': 'external_interruption'}
                break
            algorithm = config['algorithms'][index]
            run_dir = output / 'runs' / f'{block_id:04d}-{index}'
            # Recheck before every child; provenance mutation cannot silently change a campaign.
            if sha256(ROOT / algorithm['executable']) != algorithm['sha256']:
                raise RuntimeError('binary changed after configuration was frozen')
            try:
                if algorithm['kind'] == 'vf':
                    manifest = run_vf(algorithm, graph, case, run_dir, config['timeout_seconds'])
                else:
                    manifest = run_ippv(ROOT / algorithm['executable'], graph, case['h'], case['k'],
                                        algorithm['options']['iterations'], run_dir, config['timeout_seconds'], case['definition'])
            except (OSError, ValueError, RuntimeError) as error:
                run_dir.mkdir(parents=True, exist_ok=True)
                manifest = {'status': 'driver_error', 'error': str(error), 'validation': {'level': 'not_run'},
                            'sha256': file_hashes(run_dir)}
                save(run_dir / 'driver-error.json', manifest)
            row = {'case': case['name'], 'h': case['h'], 'k': case['k'], 'repeat': block['repeat'],
                   'algorithm': algorithm['name'], 'status': manifest['status'],
                   'output_scope': algorithm['options'].get('output', 'fixed'),
                   'directory': str(run_dir.relative_to(output)), 'graph_sha256': graph_sha256(graph),
                   'semantic_sha256': None, 'rank_latency_seconds': None}
            if manifest['status'] == 'completed':
                records = parse_records((run_dir / 'canonical_output.jsonl').read_text(), graph, case['h'])
                row['semantic_sha256'] = semantic_hash(graph, case['h'], records)
            rows.append(row)
            done.append((row, manifest, run_dir))
            save(output / 'summary.json', {'runs': rows, 'comparisons': comparisons})
            print(json.dumps(row), flush=True)
            # A native timeout is a censored measurement, never accepted output.
            # Validator failures and every other unsuccessful status still stop.
            if stop_on_failure and manifest['status'] != 'completed' and not (
                    continue_on_timeout and manifest['status'] == 'timeout'):
                stop_reason = {'kind': 'unsuccessful_run', 'directory': row['directory'], 'status': row['status']}
                break
        for i, (a, ma, pa) in enumerate(done):
            for b, mb, pb in done[i + 1:]:
                record = {'case': case['name'], 'repeat': block['repeat'], 'algorithms': [a['algorithm'], b['algorithm']]}
                if ma['status'] == mb['status'] == 'completed' and ma['validation'].get('passed') and mb['validation'].get('passed'):
                    left = parse_records((pa / 'canonical_output.jsonl').read_text(), graph, case['h'])
                    right = parse_records((pb / 'canonical_output.jsonl').read_text(), graph, case['h'])
                    if require_prefix_agreement:
                        fixed, full = (right, left) if a['algorithm'] in full_names else (left, right)
                        record.update(compare_prefix(fixed, full, case['k']))
                    else:
                        record.update(compare(left, right, case['k']))
                    if stop_on_failure and not record[agreement_key]:
                        stop_reason = {'kind': 'output_disagreement', 'case': case['name'],
                                       'repeat': block['repeat'], 'algorithms': record['algorithms'],
                                       'required_agreement': agreement_key}
                else:
                    record.update(level='not_compared', reason='one or both runs failed or lacked validation')
                comparisons.append(record)
        save(output / 'summary.json', {'runs': rows, 'comparisons': comparisons})
        if interrupted is not None and interrupted():
            stop_reason = stop_reason or {'kind': 'external_interruption'}
        if baseline is not None:
            after = snapshot()
            save(output / f'block-{block_id:04d}-after.json', after)
            reason = power_change(baseline, after)
            if reason is not None:
                stop_reason = stop_reason or reason
        if stop_reason is not None:
            return stop(stop_reason)
    # Final inventory is written once after all outputs; individual run manifests are immutable.
    save(output / 'checksums.json', file_hashes(output))
    return 0 if all(r['status'] == 'completed' for r in rows) and all(c.get(agreement_key) for c in comparisons) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--stop-on-failure', action='store_true',
                        help='Stop at the first unsuccessful run or tie-aware disagreement; retain the unrun schedule')
    parser.add_argument('--continue-on-timeout', action='store_true',
                        help='With --stop-on-failure, retain native timeouts and continue the frozen schedule; no retries')
    parser.add_argument('--require-strict-agreement', action='store_true',
                        help='Require identical canonical records for equivalent solver modes; default permits cutoff ties')
    parser.add_argument('--require-prefix-agreement', action='store_true',
                        help='Require fixed-k output to equal the strict prefix of the same VF full run')
    parser.add_argument('--environment-baseline', type=Path,
                        help='Record before/after block observations and stop on power-condition changes')
    args = parser.parse_args()
    interruption = {'requested': False}
    def request_stop(signum, frame):
        interruption['requested'] = True
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    raise SystemExit(execute(args.config, args.evidence, stop_on_failure=args.stop_on_failure,
                            continue_on_timeout=args.continue_on_timeout,
                            require_strict_agreement=args.require_strict_agreement,
                            require_prefix_agreement=args.require_prefix_agreement,
                            environment_baseline=args.environment_baseline,
                            interrupted=lambda: interruption['requested']))
