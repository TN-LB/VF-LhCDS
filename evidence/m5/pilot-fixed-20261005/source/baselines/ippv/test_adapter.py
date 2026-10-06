import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapter import count_cliques, native_input, parse_native, validate
from process import capture
from vflhcds_reference.direct import Reference
from vflhcds_reference.graph import Graph


def test_lossless_ids_and_isolate():
    graph = Graph((-10**80, 4, 10**90), ((-10**80, 4),))
    assert native_input(graph) == '3 1\n0 1\n'
    assert parse_native('2 0.5000\n1 0\n', graph)[0] == [(-10**80, 4)]


@pytest.mark.parametrize('text', [
    '2 0.5000\n', '2 0.5000\n0\n', '2 0.5000\n0 0\n', '2 0.5000\n0 3\n',
    '2 nan\n0 1\n', '2 0.5000\n-1 0\n', '2 0.5000\n0 1\n2 0.5000\n1 0\n',
])
def test_malformed_output(text):
    with pytest.raises(ValueError):
        parse_native(text, Graph((0, 1), ((0, 1),)))


def test_tie_aware_preserves_author_selection():
    graph = Graph((0, 1, 2, 3), ((0, 1), (2, 3)))
    result, records = validate(graph, 2, 1, '2 0.5000\n2 3\n', True)
    assert result['passed'] and not result['strict_match']
    assert records[0]['vertices'] == [2, 3]


def test_zero_results_are_not_synthesized():
    graph = Graph((0, 1), ())
    result, records = validate(graph, 3, 2, '', True)
    assert not result['passed'] and not result['checks']['required_count']
    assert records == [] and result['truth_count'] == 2


def test_nonmaximal_bridge_triangle_rejected():
    graph = Graph(tuple(range(6)), ((0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)))
    result, _ = validate(graph, 3, 1, '3 0.3333\n0 1 2\n', True)
    assert not result['checks']['every_set_definition_valid']


@pytest.mark.parametrize('h', [2, 3, 4, 5])
def test_structural_count_matches_independent_combinations(h):
    graph = Graph(tuple(range(5)), ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4)))
    ref = Reference(graph, h)
    for mask in range(1, graph.full_mask + 1):
        assert count_cliques(graph, mask, h) == ref.mu_h(mask)


def test_capture_native_failure_and_immutable_files(tmp_path):
    result = capture([sys.executable, '-c', 'import sys; print("partial"); sys.exit(7)'], tmp_path, 2)
    assert result['native_exit_code'] == 7 and result['status'] == 'error'
    assert result['peak_rss_bytes'] > 0
    assert (tmp_path / 'stdout.txt').read_text() == 'partial\n'
    with pytest.raises(FileExistsError):
        capture([sys.executable, '-c', 'pass'], tmp_path, 2)


def test_capture_timeout(tmp_path):
    result = capture([sys.executable, '-c', 'import time; time.sleep(10)'], tmp_path, 0.05)
    assert result['status'] == 'timeout' and result['signal'] == 9
    assert json.loads((tmp_path / 'process.json').read_text()) == result
