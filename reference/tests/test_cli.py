"""Reference CLI process smoke and failure boundaries; never invokes production."""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from vflhcds_reference.graph import Graph
from vflhcds_reference.io import canonical_graph


def run_cli(*arguments):
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1]))
    return subprocess.run([sys.executable, "-m", "vflhcds_reference", *map(str, arguments)],
                          env=env, capture_output=True, text=True, check=False)


@pytest.fixture
def graph_file(tmp_path):
    path = tmp_path / "graph.txt"
    path.write_text(canonical_graph(Graph((-2, 1, 4, 9), ((1, 4), (1, 9), (4, 9)))))
    return path


def test_cli_truth_exact_records_and_seed(graph_file):
    result = run_cli("truth", "--graph", graph_file, "--h", "3", "--all", "--seed", "20260917")
    assert result.returncode == 0, result.stderr
    record, status = json.loads(result.stdout), json.loads(result.stderr)
    assert record["seed"] == 20260917
    assert [r["vertices"] for r in record["results"]] == [[1, 4, 9], [-2]]
    assert [r["density_den"] for r in record["results"]] == ["3", "1"]
    assert record["selection"] == {"mode": "all", "k": None}
    assert status["complete"] and status["output_count"] == 1
    prefix = run_cli("truth", "--graph", graph_file, "--h", "3", "--k", "1")
    assert prefix.returncode == 0
    assert json.loads(prefix.stdout)["results"] == record["results"][:1]


def test_cli_chain_global_empty_and_restricted_zero(graph_file, tmp_path):
    chain = run_cli("chain", "--graph", graph_file, "--h", "3")
    assert chain.returncode == 0
    assert json.loads(chain.stdout)["chain"] == [[], [1, 4, 9], [-2, 1, 4, 9]]
    empty = run_cli("oracle", "--graph", graph_file, "--h", "3", "--lambda", "100/1")
    assert empty.returncode == 0
    assert json.loads(empty.stdout)["result"]["vertices"] == []
    x, y = tmp_path / "x.txt", tmp_path / "y.txt"
    x.write_text("vflhcds-set 1 n 0\n")
    y.write_text("vflhcds-set 1 n 1 v -2\n")
    restricted = run_cli("oracle", "--graph", graph_file, "--h", "3", "--lambda", "0/5", "--x", x, "--y", y)
    assert restricted.returncode == 0, restricted.stderr
    record = json.loads(restricted.stdout)["result"]
    assert (record["scope"], record["vertices"], record["lambda_den"]) == ("restricted", [-2], "1")


@pytest.mark.parametrize("args", [
    ["truth", "--h", "2", "--k", "0"], ["truth", "--h", "1", "--all"],
    ["truth", "--h", "2", "--k", "1", "--all"], ["truth", "--h", "2"],
    ["truth", "--h", "2", "--all", "--h", "3"], ["truth", "--h", "2.0", "--all"],
    ["oracle", "--h", "2", "--lambda", "1/0"], ["oracle", "--h", "2", "--lambda", "-1/2"],
    ["oracle", "--h", "2", "--lambda", "0/1", "--x", "missing"],
])
def test_cli_invalid_request_precedes_missing_graph(args):
    result = run_cli(*args, "--graph", "nonexistent-m1-file")
    assert result.returncode == 2, result.stderr
    assert result.stdout == ""
    assert json.loads(result.stderr)["status"] == "invalid_argument"


def test_cli_graph_errors_size_guard_and_preserved_outputs(tmp_path, graph_file):
    output = tmp_path / "output.json"
    output.write_text("preserve me\n")
    big = tmp_path / "big.txt"
    big.write_text(canonical_graph(Graph(tuple(range(13)), ())))
    result = run_cli("truth", "--graph", big, "--h", "2", "--all", "--output", output)
    assert result.returncode == 5
    assert json.loads(result.stderr)["status"] == "resource_limit"
    assert output.read_text() == "preserve me\n"
    malformed = tmp_path / "bad.txt"
    malformed.write_text("vflhcds-graph 1 n 0 m 0\n")
    assert run_cli("truth", "--graph", malformed, "--h", "2", "--all").returncode == 3
    assert run_cli("truth", "--graph", tmp_path / "missing", "--h", "2", "--all").returncode == 4
    # A tiny input exercises explicit guard configuration without an expensive override run.
    assert run_cli("truth", "--graph", graph_file, "--h", "3", "--all", "--max-vertices", "13").returncode == 0
    completed = run_cli("truth", "--graph", graph_file, "--h", "3", "--all", "--output", output)
    assert completed.returncode == 0 and completed.stdout == ""
    assert json.loads(output.read_text())["kind"] == "reference_truth"
    assert not list(tmp_path.glob("output.json.*"))


@pytest.mark.parametrize("alias_type", ["same", "symlink", "hardlink"])
def test_cli_rejects_output_aliasing_inputs(graph_file, tmp_path, alias_type):
    target = graph_file
    if alias_type != "same":
        target = tmp_path / "alias.txt"
        if alias_type == "symlink":
            target.symlink_to(graph_file)
        else:
            target.hardlink_to(graph_file)
    original = graph_file.read_bytes()
    result = run_cli("truth", "--graph", graph_file, "--h", "3", "--all", "--output", target)
    assert result.returncode == 2
    assert graph_file.read_bytes() == original
