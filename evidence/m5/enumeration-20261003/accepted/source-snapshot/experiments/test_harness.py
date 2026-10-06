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
