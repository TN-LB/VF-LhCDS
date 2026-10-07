"""Frozen shared-input runs with separate validation and no outcome filtering."""
import argparse
import datetime
import json
import math
from pathlib import Path
import platform
import random
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.support import ROOT, canonical_graph, capture, file_hashes, graph_sha256, parse_graph, run_ippv, save, semantic_hash, sha256
from experiments.validate import compare, parse_records


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
                    or not set(options) <= {'core', 'footprints', 'enumeration', 'counting'}
                    or options['core'] not in ('off', 'safe') or options['footprints'] not in ('sorted', 'membership')
                    or options.get('enumeration', 'combinations') not in ('combinations', 'adjacency')
                    or options.get('counting', 'sorted') not in ('sorted', 'membership')):
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
    command = [str(binary), 'solve', '--graph', str(output / 'graph.txt'), '--h', str(case['h']), '--k', str(case['k']),
               '--core-reduction', options['core'], '--footprint-scan', options['footprints']]
    if 'enumeration' in options:
        command += ['--clique-enumeration', options['enumeration']]
    if 'counting' in options:
        command += ['--clique-count', options['counting']]
    native = capture(command, output, timeout)
    manifest = {'algorithm': algorithm, 'build_provenance': json.loads(binary.with_suffix('.provenance.json').read_text()),
                'graph_sha256': graph_sha256(graph), 'h': case['h'], 'k': case['k'], 'native': native,
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
                   '--h', str(case['h']), '--k', str(case['k']), '--strict']
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


def execute(config_path, output, *, stop_on_failure=False, continue_on_timeout=False,
            require_strict_agreement=False):
    if continue_on_timeout and not stop_on_failure:
        raise ValueError('continue_on_timeout requires stop_on_failure')
    config = load_config(config_path)
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
                                          'continue_on_timeout': continue_on_timeout, 'planned_runs': planned})
    save(output / 'environment.json', {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'platform': platform.platform(),
        'python': sys.version, 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'dirty_tree': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'script_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted((ROOT / 'experiments').glob('*.py'))},
        'configuration_sha256': sha256(output / 'config.json'), 'schedule_sha256': sha256(output / 'schedule.json'),
        'execution_policy_sha256': sha256(output / 'execution-policy.json')})
    cases = {case['name']: case for case in config['cases']}
    rows, comparisons = [], []
    for block_id, block in enumerate(blocks):
        stop_reason = None
        case = cases[block['case']]
        graph = parse_graph((ROOT / case['graph']).read_text())
        if graph_sha256(graph) != case['sha256']:
            raise RuntimeError('input changed after configuration was frozen')
        done = []
        for index in block['algorithm_indices']:
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
                    record.update(compare(left, right, case['k']))
                    agreement_key = 'strict_match' if require_strict_agreement else 'tie_aware_match'
                    if stop_on_failure and not record[agreement_key]:
                        stop_reason = {'kind': 'output_disagreement', 'case': case['name'],
                                       'repeat': block['repeat'], 'algorithms': record['algorithms'],
                                       'required_agreement': agreement_key}
                else:
                    record.update(level='not_compared', reason='one or both runs failed or lacked validation')
                comparisons.append(record)
        save(output / 'summary.json', {'runs': rows, 'comparisons': comparisons})
        if stop_reason is not None:
            recorded = {row['directory'] for row in rows}
            save(output / 'stopped.json', {'reason': stop_reason, 'planned_count': len(planned),
                                          'recorded_count': len(rows),
                                          'unrun': [run for run in planned if run['directory'] not in recorded]})
            save(output / 'checksums.json', file_hashes(output))
            return 1
    # Final inventory is written once after all outputs; individual run manifests are immutable.
    save(output / 'checksums.json', file_hashes(output))
    agreement_key = 'strict_match' if require_strict_agreement else 'tie_aware_match'
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
    args = parser.parse_args()
    raise SystemExit(execute(args.config, args.evidence, stop_on_failure=args.stop_on_failure,
                            continue_on_timeout=args.continue_on_timeout,
                            require_strict_agreement=args.require_strict_agreement))
