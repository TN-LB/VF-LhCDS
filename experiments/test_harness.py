"""Failure-path and evidence-level tests; no production mathematical logic."""
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.prepare_input import prepare
from experiments.run import load_config, run_vf, schedule
from experiments.support import json_line, save, semantic_hash, sha256
from experiments.validate import compare, parse_records, validate
from vflhcds_reference.graph import Graph


def record(vertices, count=1, numerator=1, denominator=2):
    return {'rank': 1, 'h': 2, 'vertex_count': len(vertices), 'clique_count': str(count),
            'density_num': str(numerator), 'density_den': str(denominator), 'vertices': vertices}


def test_exact_ids_and_definition_vs_structural():
    graph = Graph((-10**60, 10**70), ((-10**60, 10**70),))
    text = json_line(record(list(graph.vertices)))
    result, rows = validate(graph, 2, 1, text, definition=True, strict=True)
    assert result['passed'] and result['completeness_certified']
    assert rows[0]['vertices'] == list(graph.vertices)
    structure, _ = validate(graph, 2, 1, text)
    assert structure['passed'] and not structure['completeness_certified']


@pytest.mark.parametrize('bad', [
    lambda t: t.rstrip(),
    lambda t: t.replace('"rank":1', '"rank":1,"rank":1'),
    lambda t: t.replace('[0,1]', '[1,0]'),
    lambda t: t.replace('[0,1]', '[0,0]'),
    lambda t: t.replace('[0,1]', '[0,2]'),
    lambda t: t.replace('"clique_count":"1"', '"clique_count":1'),
    lambda t: t.replace('"density_num":"1","density_den":"2"', '"density_num":"2","density_den":"4"'),
    lambda t: t.replace('"rank":1', '"rank":true'),
])
def test_bad_canonical_records_rejected(bad):
    with pytest.raises(ValueError):
        parse_records(bad(json_line(record([0, 1]))), Graph((0, 1), ((0, 1),)), 2)


def test_tied_selection_and_missing_zero_are_distinct():
    graph = Graph((0, 1, 2, 3, 4), ((0, 1), (2, 3)))
    other = json_line(record([2, 3]))
    tie, _ = validate(graph, 2, 1, other, definition=True)
    strict, _ = validate(graph, 2, 1, other, definition=True, strict=True)
    assert tie['passed'] and not strict['passed']
    assert compare([record([0, 1])], [record([2, 3])], 1)['tie_aware_match']
    incomplete, _ = validate(Graph((4,), ()), 2, 1, '', definition=True)
    assert not incomplete['passed'] and not incomplete['completeness_certified']
    assert not compare([], [], 1)['completeness_certified']


def test_corrupt_exact_count_fails():
    result, _ = validate(Graph((0, 1), ((0, 1),)), 2, 1, json_line(record([0, 1], count=2)))
    assert not result['passed'] and not result['checks']['exact_counts']


def test_structurally_valid_nonmaximal_set_fails_definition():
    graph = Graph((0, 1, 2), ((0, 1), (0, 2), (1, 2)))
    text = json_line(record([0, 1]))
    assert validate(graph, 2, 1, text)[0]['passed']
    assert not validate(graph, 2, 1, text, definition=True)[0]['passed']


def test_normalization_preserves_header_isolates(tmp_path):
    raw = tmp_path / 'raw'; raw.write_text('4 4\n0 1\n1 0\n2 2\n1 2\n')
    result = prepare(raw, tmp_path / 'normalized')
    assert result['vertices'] == 4 and result['edges'] == 2
    assert result['removed_self_loops'] == result['removed_duplicate_edges'] == 1
    assert 'v 3\n' in (tmp_path / 'normalized/graph.txt').read_text()
    with pytest.raises(FileExistsError):
        prepare(raw, tmp_path / 'normalized')


def test_schedule_reproducible_and_complete():
    config = {'seed': 42, 'repeats': 3, 'algorithms': ['a', 'b', 'c'], 'cases': [{'name': 'one'}, {'name': 'two'}]}
    a = schedule(config)
    assert a == schedule(config) and len(a) == 6
    assert all(sorted(block['algorithm_indices']) == [0, 1, 2] for block in a)
    assert len({tuple(block['algorithm_indices']) for block in a}) > 1


def test_draft_config_cannot_launch(tmp_path):
    path = tmp_path / 'config.json'
    save(path, {'schema_version': 1, 'name': 'draft', 'scope': 'draft', 'seed': 0, 'repeats': 1,
                'threads': 1, 'timeout_seconds': 60, 'memory_limit_bytes': None, 'cache_policy': 'uncontrolled',
                'algorithms': [], 'cases': []})
    with pytest.raises(ValueError, match='draft'):
        load_config(path)


def fake_binary(tmp_path, body):
    binary = tmp_path / 'fake'
    binary.write_text('#!' + sys.executable + '\n' + body)
    binary.chmod(0o700)
    save(binary.with_suffix('.provenance.json'), {'executable_sha256': sha256(binary)})
    return {'name': 'fault-injection', 'executable': str(binary), 'options': {'core': 'off', 'footprints': 'sorted'}}


@pytest.mark.parametrize('body,status,exit_code', [
    ('print("partial")\n', 'output_incomplete', 0),
    ('import sys\nprint("partial")\nsys.exit(7)\n', 'error', 7),
    ('import sys,json\nprint(json.dumps({"status":"oom","complete":False}),file=sys.stderr)\nsys.exit(6)\n', 'oom', 6),
    ('import os,signal\nos.kill(os.getpid(),signal.SIGKILL)\n', 'error', -9),
    ('import time\ntime.sleep(10)\n', 'timeout', -9),
])
def test_native_failure_never_accepts_partial_output(tmp_path, body, status, exit_code):
    algorithm = fake_binary(tmp_path, body)
    # Ordinary interpreter startup must not race the timeout-specific assertion.
    timeout = .2 if status == 'timeout' else 5
    result = run_vf(algorithm, Graph((0, 1), ((0, 1),)), {'h': 2, 'k': 1, 'definition': True}, tmp_path / 'run', timeout)
    assert result['status'] == status and result['native']['native_exit_code'] == exit_code
    assert result['validation']['level'] == 'not_run'
    assert not (tmp_path / 'run/canonical_output.jsonl').exists()


def test_native_hash_mismatch_rejected_outside_algorithm_time(tmp_path):
    rows = json_line(record([0, 1]))
    status = {'schema_version': 1, 'status': 'completed', 'complete': True, 'output_count': 1, 'semantic_sha256': 'bad'}
    body = 'import sys\nsys.stdout.write(' + repr(rows) + ')\nsys.stderr.write(' + repr(json.dumps(status)) + ')\n'
    result = run_vf(fake_binary(tmp_path, body), Graph((0, 1), ((0, 1),)), {'h': 2, 'k': 1, 'definition': True}, tmp_path / 'run', 3)
    assert result['status'] == 'semantic_mismatch'
    assert not result['validation']['checks']['native_hash']
    assert result['native']['native_exit_code'] == result['external_validation']['native_exit_code'] == 0
    assert result['native']['finished_utc'] <= result['external_validation']['started_utc']


@pytest.mark.parametrize('enumeration', [None, 'combinations', 'adjacency'])
def test_enumeration_config_and_native_command(tmp_path, enumeration):
    algorithm = fake_binary(tmp_path, 'print("partial")\n')
    algorithm.update(kind='vf', sha256=sha256(algorithm['executable']))
    save(Path(algorithm['executable']).with_suffix('.provenance.json'),
         {'executable_sha256': algorithm['sha256'], 'source_sha256': {}})
    if enumeration is not None:
        algorithm['options']['enumeration'] = enumeration
    graph_path = tmp_path / 'input.graph'
    graph_path.write_text('vflhcds-graph 1\nn 2\nv 0\nv 1\nm 1\ne 0 1\n')
    config = {'schema_version': 1, 'name': 'enum-test', 'scope': 'diagnostic', 'seed': 0,
              'repeats': 1, 'threads': 1, 'timeout_seconds': 5, 'memory_limit_bytes': None,
              'cache_policy': 'uncontrolled', 'algorithms': [algorithm],
              'cases': [{'name': 'edge', 'graph': str(graph_path), 'sha256': sha256(graph_path),
                         'h': 2, 'k': 1, 'definition': True}]}
    path = tmp_path / 'config.json'
    save(path, config)
    assert load_config(path) == config
    result = run_vf(algorithm, Graph((0, 1), ((0, 1),)), config['cases'][0], tmp_path / 'run', 5)
    command = result['native']['command']
    if enumeration is None:
        assert '--clique-enumeration' not in command
    else:
        assert command[-2:] == ['--clique-enumeration', enumeration]
    algorithm['options']['enumeration'] = 'automatic'
    save(path, config)
    with pytest.raises(ValueError, match='invalid VF switches'):
        load_config(path)


@pytest.mark.parametrize('counting', [None, 'sorted', 'membership'])
def test_counting_config_and_native_command(tmp_path, counting):
    algorithm = fake_binary(tmp_path, 'print("partial")\n')
    algorithm.update(kind='vf', sha256=sha256(algorithm['executable']))
    save(Path(algorithm['executable']).with_suffix('.provenance.json'),
         {'executable_sha256': algorithm['sha256'], 'source_sha256': {}})
    if counting is not None:
        algorithm['options']['counting'] = counting
    graph_path = tmp_path / 'input.graph'
    graph_path.write_text('vflhcds-graph 1\nn 2\nv 0\nv 1\nm 1\ne 0 1\n')
    config = {'schema_version': 1, 'name': 'count-test', 'scope': 'diagnostic', 'seed': 0,
              'repeats': 1, 'threads': 1, 'timeout_seconds': 5, 'memory_limit_bytes': None,
              'cache_policy': 'uncontrolled', 'algorithms': [algorithm],
              'cases': [{'name': 'edge', 'graph': str(graph_path), 'sha256': sha256(graph_path),
                         'h': 2, 'k': 1, 'definition': True}]}
    path = tmp_path / 'config.json'
    save(path, config)
    assert load_config(path) == config
    result = run_vf(algorithm, Graph((0, 1), ((0, 1),)), config['cases'][0], tmp_path / 'run', 5)
    command = result['native']['command']
    if counting is None:
        assert '--clique-count' not in command
    else:
        assert command[-2:] == ['--clique-count', counting]
    for invalid in ('automatic', None):
        algorithm['options']['counting'] = invalid
        save(path, config)
        with pytest.raises(ValueError, match='invalid VF switches'):
            load_config(path)


def execute_fixture(tmp_path, monkeypatch, outcome, *, stop_on_failure, continue_on_timeout=False,
                    require_strict_agreement=False):
    """Exercise scheduling/evidence control with deterministic injected outcomes."""
    import experiments.run as runner

    binary = tmp_path / 'binary'
    binary.write_text('pinned test fixture; never launched')
    graph = tmp_path / 'two-triangles.graph'
    graph.write_text('vflhcds-graph 1\nn 6\nv 0\nv 1\nv 2\nv 3\nv 4\nv 5\nm 6\ne 0 1\ne 0 2\ne 1 2\ne 3 4\ne 3 5\ne 4 5\n')
    config = {'schema_version': 1, 'name': 'stop-control', 'scope': 'diagnostic',
              'seed': 20261003, 'repeats': 3, 'threads': 1, 'timeout_seconds': 5,
              'memory_limit_bytes': None, 'cache_policy': 'uncontrolled',
              'algorithms': [{'name': name, 'kind': 'vf', 'executable': str(binary),
                              'sha256': sha256(binary), 'options': {}} for name in ('a', 'b')],
              'cases': [{'name': 'two-triangles', 'graph': str(graph), 'sha256': sha256(graph),
                         'h': 2, 'k': 1, 'definition': False}]}
    calls = []

    def fake_run(algorithm, graph, case, output, timeout):
        calls.append(algorithm['name'])
        output.mkdir(parents=True)
        (output / 'stdout.txt').write_text('retained raw fixture output\n')
        result = outcome(algorithm['name'], len(calls))
        if isinstance(result, list):
            (output / 'canonical_output.jsonl').write_text(''.join(map(json_line, result)))
            return {'status': 'completed', 'validation': {'passed': True, 'level': 'structural_checked'}}
        if result == 'driver_error':
            raise RuntimeError('injected driver failure')
        return {'status': result, 'validation': {'level': 'not_run'}}

    monkeypatch.setattr(runner, 'load_config', lambda path: config)
    monkeypatch.setattr(runner, 'run_vf', fake_run)
    output = tmp_path / 'campaign'
    code = runner.execute(tmp_path / 'unused-config.json', output, stop_on_failure=stop_on_failure,
                          continue_on_timeout=continue_on_timeout,
                          require_strict_agreement=require_strict_agreement)
    inventory = json.loads((output / 'checksums.json').read_text())
    assert all(sha256(output / name) == digest for name, digest in inventory.items())
    return code, output, calls, json.loads((output / 'summary.json').read_text())


@pytest.mark.parametrize('status', ['timeout', 'error', 'oom', 'semantic_mismatch', 'driver_error'])
def test_stop_on_first_failure_preserves_pending_schedule(tmp_path, monkeypatch, status):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch, lambda name, index: status, stop_on_failure=True)
    assert code == 1 and len(calls) == len(summary['runs']) == 1
    assert summary['runs'][0]['status'] == status
    stopped = json.loads((output / 'stopped.json').read_text())
    assert stopped['reason']['status'] == status
    assert stopped['planned_count'] == 6 and stopped['recorded_count'] == 1
    assert len(stopped['unrun']) == 5
    planned = json.loads((output / 'execution-policy.json').read_text())
    assert planned['stop_on_failure'] is True
    assert stopped['unrun'] == planned['planned_runs'][1:]
    recorded = output / summary['runs'][0]['directory']
    assert (recorded / 'stdout.txt').read_text() == 'retained raw fixture output\n'
    if status == 'driver_error':
        assert 'injected driver failure' in (recorded / 'driver-error.json').read_text()


def test_run_all_failure_policy_remains_available(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch, lambda name, index: 'timeout', stop_on_failure=False)
    assert code == 1 and len(calls) == len(summary['runs']) == 6
    assert not (output / 'stopped.json').exists()
    assert all(row['status'] == 'timeout' for row in summary['runs'])


def test_stop_on_pair_disagreement(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch,
        lambda name, index: [record([0, 1])] if name == 'a' else [record([0, 1, 2], 3, 1, 1)],
        stop_on_failure=True)
    assert code == 1 and len(calls) == 2
    assert summary['comparisons'][0]['tie_aware_match'] is False
    stopped = json.loads((output / 'stopped.json').read_text())
    assert stopped['reason']['kind'] == 'output_disagreement'
    assert stopped['recorded_count'] == 2 and len(stopped['unrun']) == 4


def test_valid_cutoff_tie_does_not_stop_campaign(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch,
        lambda name, index: [record([0, 1, 2], 3, 1, 1)] if name == 'a' else [record([3, 4, 5], 3, 1, 1)],
        stop_on_failure=True)
    assert code == 0 and len(calls) == 6
    assert len(summary['comparisons']) == 3
    assert all(not row['strict_match'] and row['tie_aware_match'] for row in summary['comparisons'])
    assert not (output / 'stopped.json').exists()


def test_timeout_continuation_retains_censoring_and_completes_schedule(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch,
        lambda name, index: 'timeout' if index == 1 else [record([0, 1, 2], 3, 1, 1)],
        stop_on_failure=True, continue_on_timeout=True)
    assert code == 1 and len(calls) == 6
    assert [r['status'] for r in summary['runs']] == ['timeout'] + ['completed'] * 5
    assert summary['runs'][0]['semantic_sha256'] is None
    assert summary['comparisons'][0]['level'] == 'not_compared'
    assert all(p['tie_aware_match'] for p in summary['comparisons'][1:])
    assert not (output / 'stopped.json').exists()
    assert json.loads((output / 'execution-policy.json').read_text())['continue_on_timeout']


@pytest.mark.parametrize('status', ['error', 'oom', 'structural_mismatch', 'semantic_mismatch',
                                   'validation_error', 'output_incomplete', 'driver_error'])
def test_timeout_continuation_still_stops_other_failures(tmp_path, monkeypatch, status):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch, lambda name, index: 'timeout' if index == 1 else status,
        stop_on_failure=True, continue_on_timeout=True)
    assert code == 1 and len(calls) == 2
    assert [r['status'] for r in summary['runs']] == ['timeout', status]
    stopped = json.loads((output / 'stopped.json').read_text())
    assert stopped['reason']['status'] == status and len(stopped['unrun']) == 4


def test_timeout_continuation_still_stops_disagreement(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch,
        lambda name, index: [record([0, 1])] if name == 'a' else [record([0, 1, 2], 3, 1, 1)],
        stop_on_failure=True, continue_on_timeout=True)
    assert code == 1 and len(calls) == 2
    assert summary['comparisons'][0]['tie_aware_match'] is False
    assert json.loads((output / 'stopped.json').read_text())['reason']['kind'] == 'output_disagreement'


def test_timeout_continuation_requires_stop_policy(tmp_path):
    from experiments.run import execute
    with pytest.raises(ValueError, match='requires stop_on_failure'):
        execute(tmp_path / 'absent.json', tmp_path / 'unused', continue_on_timeout=True)
    assert not (tmp_path / 'unused').exists()


@pytest.mark.parametrize('stop', [False, True])
def test_ablation_requires_identical_tie_selection(tmp_path, monkeypatch, stop):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch,
        lambda name, index: [record([0, 1, 2], 3, 1, 1)] if name == 'a' else [record([3, 4, 5], 3, 1, 1)],
        stop_on_failure=stop, require_strict_agreement=True)
    assert code == 1 and len(calls) == (2 if stop else 6)
    assert all(p['tie_aware_match'] and not p['strict_match'] for p in summary['comparisons'])
    assert json.loads((output / 'execution-policy.json').read_text())['require_strict_agreement']
    if stop:
        stopped = json.loads((output / 'stopped.json').read_text())
        assert stopped['reason']['required_agreement'] == 'strict_match' and len(stopped['unrun']) == 4
    else:
        assert not (output / 'stopped.json').exists()


def test_ablation_strict_policy_accepts_identical_outputs_after_timeout(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch,
        lambda name, index: 'timeout' if index == 1 else [record([0, 1, 2], 3, 1, 1)],
        stop_on_failure=True, continue_on_timeout=True, require_strict_agreement=True)
    assert code == 1 and len(calls) == 6
    assert summary['comparisons'][0]['level'] == 'not_compared'
    assert all(p['strict_match'] for p in summary['comparisons'][1:])
    assert not (output / 'stopped.json').exists()


def test_ablation_strict_policy_all_equal_completes(tmp_path, monkeypatch):
    code, output, calls, summary = execute_fixture(
        tmp_path, monkeypatch, lambda name, index: [record([0, 1, 2], 3, 1, 1)],
        stop_on_failure=True, require_strict_agreement=True)
    assert code == 0 and len(calls) == 6
    assert all(p['strict_match'] for p in summary['comparisons'])
    assert not (output / 'stopped.json').exists()
