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
    if config['scope'] not in ('diagnostic', 'approved_smoke'):
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
            if set(options) != {'core', 'footprints'} or options['core'] not in ('off', 'safe') or options['footprints'] not in ('sorted', 'membership'):
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
        if config['scope'] == 'diagnostic' and not case['definition']:
            raise ValueError('diagnostic runner accepts tiny definition cases only; real smoke requires approval')
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
    native = capture([str(binary), 'solve', '--graph', str(output / 'graph.txt'), '--h', str(case['h']), '--k', str(case['k']),
                      '--core-reduction', options['core'], '--footprint-scan', options['footprints']], output, timeout)
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


def execute(config_path, output):
    config = load_config(config_path)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    save(output / 'config.json', config)
    blocks = schedule(config)
    save(output / 'schedule.json', blocks)
    save(output / 'environment.json', {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'platform': platform.platform(),
        'python': sys.version, 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'dirty_tree': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'script_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in sorted((ROOT / 'experiments').glob('*.py'))},
        'configuration_sha256': sha256(output / 'config.json'), 'schedule_sha256': sha256(output / 'schedule.json')})
    cases = {case['name']: case for case in config['cases']}
    rows, comparisons = [], []
    for block_id, block in enumerate(blocks):
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
        for i, (a, ma, pa) in enumerate(done):
            for b, mb, pb in done[i + 1:]:
                record = {'case': case['name'], 'repeat': block['repeat'], 'algorithms': [a['algorithm'], b['algorithm']]}
                if ma['status'] == mb['status'] == 'completed' and ma['validation'].get('passed') and mb['validation'].get('passed'):
                    left = parse_records((pa / 'canonical_output.jsonl').read_text(), graph, case['h'])
                    right = parse_records((pb / 'canonical_output.jsonl').read_text(), graph, case['h'])
                    record.update(compare(left, right, case['k']))
                else:
                    record.update(level='not_compared', reason='one or both runs failed or lacked validation')
                comparisons.append(record)
        save(output / 'summary.json', {'runs': rows, 'comparisons': comparisons})
    # Final inventory is written once after all outputs; individual run manifests are immutable.
    save(output / 'checksums.json', file_hashes(output))
    return 0 if all(r['status'] == 'completed' for r in rows) and all(c.get('tie_aware_match') for c in comparisons) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(execute(args.config, args.evidence))
