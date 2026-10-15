"""Deterministic M6 reports. No synthetic imputation, timing correction or pooling."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile

SCHEMA = 'vflhcds.final_profile'
INVENTORY = {'clique_id_capacity', 'clique_id_bytes', 'frontier_peak_size', 'frontier_peak_capacity'}
STATUSES = {'completed', 'timeout', 'oom', 'error', 'not_run'}


def read_events(path):
    """A killed writer may leave a partial last line. Never treat it as an event."""
    return parse_events(Path(path).read_bytes())


def parse_events(data):
    lines = data.splitlines(keepends=True)
    result = []
    for i, line in enumerate(lines):
        if not line.endswith(b'\n') and i == len(lines) - 1:
            break
        event = json.loads(line)
        if event.get('schema') != SCHEMA or event.get('version') != 1:
            raise ValueError('observer schema/version')
        if event['seq'] != len(result) + 1:
            raise ValueError('noncontiguous event sequence')
        if result and result[-1]['event'] == 'finish':
            raise ValueError('events after finish')
        if event['boundary_residual_ns'] < 0:
            raise ValueError('negative clock-boundary residual')
        if sum(event['phases_ns'].values()) + event['boundary_residual_ns'] != event['elapsed_ns']:
            raise ValueError('phase reconciliation')
        if any(type(v) is not int or v < 0 for v in event['phases_ns'].values()):
            raise ValueError('invalid phase time')
        if any(type(v) is not int or v < 0 for v in event['work'].values()):
            raise ValueError('invalid work counter')
        if result and (event['elapsed_ns'] < result[-1]['elapsed_ns'] or any(
                event['work'].get(k, 0) < v for k, v in result[-1]['work'].items()
                if not k.endswith('_max') and k != 'maximum_depth')):
            raise ValueError('nonmonotone event')
        result.append(event)
    return result


def artifact_bytes(root, bundle, relative, cache):
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('artifact outside bundle')
    if target.is_file():
        return target.read_bytes()
    if relative in cache:
        return cache[relative]
    archive = bundle.get('raw_archive')
    if not archive:
        raise ValueError('missing artifact')
    archive_path = (root / archive['path']).resolve()
    if not archive_path.is_relative_to(root.resolve()):
        raise ValueError('archive outside bundle')
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != archive['sha256']:
        raise ValueError('raw archive hash mismatch')
    # Cache bytes for this load only; never extract archive paths to disk.
    with tarfile.open(archive_path, 'r:gz') as stream:
        for member in stream:
            if not member.isfile() or member.name in cache:
                raise ValueError('non-file/duplicate archive member')
            cache[member.name] = stream.extractfile(member).read()
    return cache[relative]


def complete(events):
    return bool(events and events[-1]['event'] == 'finish' and events[-1]['complete'])


def semantic_trace(events):
    fields = ('x', 'y', 'z', 'mu_x', 'mu_y', 'lambda')
    return [{k: e[k] for k in fields} for e in events if e['event'] == 'separator']


def difference(after, before):
    # Maxima/depth histogram are retained as separately named statistics, not sums.
    return {key: after.get(key, 0) - before.get(key, 0) for key in sorted(set(after) | set(before))
            if not key.endswith('_max') and key != 'maximum_depth' and key not in INVENTORY}


def load_bundle(path, *, formal=False):
    path = Path(path)
    bundle = json.loads(path.read_text())
    if bundle.get('schema') != 1 or bundle.get('scope') not in {'development', 'formal-m8'}:
        raise ValueError('bundle schema/scope')
    if formal and (bundle['scope'] != 'formal-m8' or not bundle.get('freeze_approved')):
        raise ValueError('preliminary/unfrozen data cannot enter formal reports')
    expected = bundle['schedule']
    if len(expected) != len(set(expected)):
        raise ValueError('duplicate scheduled run')
    rows = bundle['rows']
    seen = set()
    cache = {}
    for row in rows:
        run_id = row['run_id']
        if run_id in seen or run_id not in expected:
            raise ValueError('duplicate/unscheduled result')
        seen.add(run_id)
        if row['scope'] != bundle['scope'] or row['host'] != bundle['host']:
            raise ValueError('mixed scope/host')
        pin = bundle['pins'][row['algorithm']]
        if row['source_sha256'] != pin['source_sha256'] or row['binary_sha256'] != pin[row['role']]:
            raise ValueError('mixed version/wrong binary pin')
        if row.get('observer_sha256') != (pin.get('observer_sha256') if row['role'] == 'diagnostic' else None):
            raise ValueError('wrong observer pin')
        if row['status'] not in STATUSES:
            raise ValueError('unknown outcome')
        for field in ('events', 'output'):
            if row.get(field):
                data = artifact_bytes(path.parent, bundle, row[field], cache)
                if row.get('artifact_sha256', {}).get(field) != hashlib.sha256(data).hexdigest():
                    raise ValueError('artifact hash mismatch')
                row[field + '_data'] = parse_events(data) if field == 'events' else [
                    json.loads(line) for line in data.decode().splitlines()]
        if row['status'] == 'completed' and row['role'] == 'diagnostic' and not complete(row.get('events_data', [])):
            raise ValueError('completed diagnostic without complete event coverage')
        if row['status'] == 'completed' and 'output_data' not in row:
            raise ValueError('completed result without canonical output')
        if row['status'] == 'completed' and (row.get('wall_seconds', 0) <= 0 or row.get('peak_rss_bytes', -1) < 0):
            raise ValueError('completed result without process metrics')
    bundle['missing_run_ids'] = sorted(set(expected) - seen)
    return bundle


def identity(row, *, omit=()):
    fields = ('graph_sha256', 'h', 'k', 'core', 'work_mode', 'host', 'repeat')
    return tuple(row[k] for k in fields if k not in omit)


def match(rows, row, **changes):
    wanted = {key: row[key] for key in ('algorithm', 'role', 'graph_sha256', 'h', 'k', 'core', 'work_mode', 'host', 'repeat', 'suite')}
    wanted.update(changes)
    matches = [candidate for candidate in rows if all(candidate[k] == value for k, value in wanted.items())]
    if len(matches) > 1:
        raise ValueError('ambiguous report join')
    return matches[0] if matches else None


def usable(*rows):
    return all(row is not None and row['status'] == 'completed' for row in rows)


def profile(row):
    if not row or not complete(row.get('events_data', [])):
        return None
    events = row['events_data']
    index = next((e for e in events if e['event'] == 'index'), None)
    return {'cliques': index['cliques'] if index else None,
            'work': events[-1]['work'], 'phases_ns': events[-1]['phases_ns'],
            'boundary_residual_ns': events[-1]['boundary_residual_ns']}


def cost_associations(bundle):
    rows = bundle['rows']; result = []
    for vf in rows:
        if vf['algorithm'] != 'VF' or vf['role'] != 'control':
            continue
        diag = match(rows, vf, role='diagnostic')
        ippv = match(rows, vf, algorithm='IPPV')
        result.append({'vf': vf['run_id'], 'ippv': ippv['run_id'] if ippv else None,
                       'coverage': 'paired' if usable(vf, ippv) else 'unavailable_pair',
                       'vf_status': vf['status'], 'ippv_status': ippv['status'] if ippv else 'not_run',
                       'vf_wall_seconds': vf.get('wall_seconds'), 'vf_peak_rss_bytes': vf.get('peak_rss_bytes'),
                       'ippv_wall_seconds': ippv.get('wall_seconds') if ippv else None,
                       'ippv_peak_rss_bytes': ippv.get('peak_rss_bytes') if ippv else None,
                       'vf_diagnostic': profile(diag), 'ippv_internal_phases': None,
                       'interpretation': 'cross-graph association; no internal IPPV causal attribution'})
    return result


def core_cost(bundle):
    rows = bundle['rows']; result = []
    for off in rows:
        if off['algorithm'] != 'VF' or off['role'] != 'control' or off['core'] != 'off':
            continue
        safe = match(rows, off, core='safe')
        d_off = match(rows, off, role='diagnostic')
        d_safe = match(rows, off, role='diagnostic', core='safe')
        valid = usable(off, safe, d_off, d_safe)
        item = {'off': off['run_id'], 'safe': safe['run_id'] if safe else None,
                'coverage': 'paired' if valid else 'unavailable_pair'}
        if valid:
            if off['output_data'] != safe['output_data'] or semantic_trace(d_off['events_data']) != semantic_trace(d_safe['events_data']):
                raise ValueError('core semantic disagreement')
            a, b = profile(d_off), profile(d_safe)
            item.update(work_delta=difference(b['work'], a['work']),
                        phase_delta_ns=difference(b['phases_ns'], a['phases_ns']),
                        process_rss_delta_bytes=safe['peak_rss_bytes'] - off['peak_rss_bytes'],
                        process_time_delta_seconds=safe['wall_seconds'] - off['wall_seconds'],
                        phase_peak_rss=None)
        result.append(item)
    return result


def early_stop(bundle):
    rows = bundle['rows']; result = []
    for fixed in rows:
        if fixed['algorithm'] != 'VF' or fixed['role'] != 'control' or fixed['k'] == 'all':
            continue
        full = match(rows, fixed, k='all')
        d_fixed = match(rows, fixed, role='diagnostic')
        d_full = match(rows, fixed, role='diagnostic', k='all')
        item = {'fixed': fixed['run_id'], 'full': full['run_id'] if full else None,
                'coverage': 'unavailable_suffix'}
        if usable(fixed, full, d_fixed, d_full):
            k = fixed['k']; trace = semantic_trace(d_fixed['events_data'])
            if fixed['output_data'] != full['output_data'][:k] or trace != semantic_trace(d_full['events_data'])[:len(trace)]:
                raise ValueError('early-stop output/trace disagreement')
            boundary = next((e for e in d_full['events_data'] if e['event'] == 'rank_ready' and e['rank'] == k), None)
            if boundary:
                end = next(e for e in d_full['events_data'] if e['event'] == 'solve_end')
                index = next(e for e in d_full['events_data'] if e['event'] == 'index')
                initial = next((e for e in d_full['events_data']
                                if e['event'] == 'worklist' and e['query_id'] == 0), index)
                fixed_work = d_fixed['events_data'][-1]['work']
                if any(fixed_work.get(key, 0) != boundary['work'].get(key, 0)
                       for key in set(fixed_work) | set(boundary['work'])):
                    raise ValueError('fixed-k incurred work differs from the executed full-run prefix')
                item.update(coverage='executed_full_suffix',
                            suffix_work=difference(end['work'], boundary['work']),
                            suffix_phase_ns=difference(end['phases_ns'], boundary['phases_ns']),
                            unavoidable_initial_work=initial['work'],
                            initial_phase_ns=initial['phases_ns'], pending_at_rank=boundary['pending_intervals'],
                            measured_process_saving_seconds=full['wall_seconds'] - fixed['wall_seconds'],
                            interpretation='full-run suffix; not a prediction of end-to-end savings or streaming latency')
            else:
                item['coverage'] = 'exhausted_before_k'
        result.append(item)
    return result


def overhead(bundle):
    result = []
    for row in bundle['rows']:
        if row['role'] != 'diagnostic':
            continue
        control = match(bundle['rows'], row, role='control')
        good = usable(row, control)
        if good and row['output_data'] != control['output_data']:
            raise ValueError('diagnostic/control output disagreement')
        result.append({'diagnostic': row['run_id'], 'control': control['run_id'] if control else None,
                       'coverage': 'paired' if good else 'unavailable_pair',
                       'wall_ratio': row['wall_seconds'] / control['wall_seconds'] if good else None,
                       'diagnostic_peak_rss_bytes': row.get('peak_rss_bytes'),
                       'control_peak_rss_bytes': control.get('peak_rss_bytes') if control else None})
    return result


def local_cliques(bundle):
    rows = bundle['rows']; result = []
    for control in rows:
        if control['algorithm'] != 'VF' or control['role'] != 'control' or control['work_mode'] != 'global':
            continue
        d_control = match(rows, control, role='diagnostic')
        for mode in ('interval-scan', 'interval-reuse'):
            local = match(rows, control, work_mode=mode)
            d_local = match(rows, control, role='diagnostic', work_mode=mode)
            good = usable(control, local, d_control, d_local)
            item = {'global': control['run_id'], 'local': local['run_id'] if local else None,
                    'work_mode': mode, 'coverage': 'paired' if good else 'unavailable_pair'}
            if good:
                if control['output_data'] != local['output_data'] or semantic_trace(d_control['events_data']) != semantic_trace(d_local['events_data']):
                    raise ValueError('local clique semantic disagreement')
                a, b = profile(d_control), profile(d_local)
                item.update(work_delta=difference(b['work'], a['work']),
                            inventory={key: b['work'].get(key) for key in sorted(INVENTORY)},
                            phase_delta_ns=difference(b['phases_ns'], a['phases_ns']),
                            process_rss_delta_bytes=local['peak_rss_bytes']-control['peak_rss_bytes'],
                            process_time_delta_seconds=local['wall_seconds']-control['wall_seconds'],
                            interpretation='Includes partition/setup and remaining counts/core; no guaranteed speedup')
            result.append(item)
    return result


def build(bundle):
    result = {'schema': 1, 'scope': bundle['scope'], 'missing_run_ids': bundle['missing_run_ids'],
            'outcomes': {status: sum(r['status'] == status for r in bundle['rows']) for status in sorted(STATUSES)},
            'vf_ippv': cost_associations(bundle), 'core': core_cost(bundle),
            'early_stop': early_stop(bundle), 'overhead': overhead(bundle)}
    # Keep historical global-only M6 report bytes reproducible.
    if any(row['work_mode'] != 'global' for row in bundle['rows']):
        result['local_cliques'] = local_cliques(bundle)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--formal', action='store_true')
    args = parser.parse_args()
    args.output.write_text(json.dumps(build(load_bundle(args.bundle, formal=args.formal)), sort_keys=True, indent=2) + '\n')


if __name__ == '__main__':
    main()
