"""Process-boundary contracts, independent of reference implementation internals."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    executable = str(Path(sys.argv[1]).resolve())
    calls = 0
    def run(args, code=0, status="completed"):
        nonlocal calls
        calls += 1
        result = subprocess.run([executable, *map(str, args)], capture_output=True, text=True)
        assert result.returncode == code, (args, result)
        record = json.loads(result.stderr)
        assert record["status"] == status and record["complete"] == (code == 0), (args, result)
        assert record["semantic_sha256"] is None
        if code:
            assert not result.stdout, result
        return result, record
    for command in ["--help", "help", "print-build-info"]:
        calls += 1
        result = subprocess.run([executable, command], capture_output=True, text=True)
        assert result.returncode == 0 and "M2" in result.stdout and not result.stderr
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        graph, x, y, output = (root / name for name in ["graph", "x", "y", "output"])
        canonical = "vflhcds-graph 1\nn 5\nv -10\nv -1\nv 5\nv 9\nv 20\nm 2\ne -10 -1\ne 5 9\n"
        graph.write_text(canonical)
        x.write_text("vflhcds-set 1\nn 0\n")
        y.write_text("vflhcds-set 1\nn 2\nv -1\nv -10\n")
        output.write_text("existing output\n")
        base = ["oracle", "--graph", graph, "--h", "2", "--lambda", "1/2"]
        answer, stats = run(base)
        assert answer.stdout == '{"scope":"global","h":2,"lambda_num":"1","lambda_den":"2","vertex_count":4,"clique_count":"2","vertices":[-10,-1,5,9]}\n'
        assert stats["counters"]["capacity_backend"] == "uint128"
        assert stats["counters"]["logical_interval_queries"] == 0 and stats["counters"]["mincut_calls"] == 1
        inspected, _ = run(["inspect-graph", "--graph", graph])
        assert json.loads(inspected.stdout) == {"graph_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
                                              "vertex_count": 5, "edge_count": 2, "vertices": [-10,-1,5,9,20]}
        restricted, _ = run(base + ["--x", x, "--y", y])
        assert json.loads(restricted.stdout)["scope"] == "restricted"
        assert json.loads(restricted.stdout)["vertices"] == [-10, -1]
        equal, st = run(base + ["--x", y, "--y", y])
        assert json.loads(equal.stdout)["vertices"] == [-10,-1] and st["counters"]["mincut_calls"] == 0
        zero, st = run(base[:-1] + ["0/999"])
        assert json.loads(zero.stdout)["vertices"] == [-10,-1,5,9,20]
        assert st["counters"]["capacity_backend"] is None and st["counters"]["unique_footprints"] is None
        empty, _ = run(base[:-1] + ["99/1"])
        assert json.loads(empty.stdout)["vertices"] == []
        huge, st = run(base[:-1] + [f"{2**130+1}/{2**131+3}"])
        assert json.loads(huge.stdout)["vertices"] == [-10,-1,5,9]
        assert st["counters"]["capacity_backend"] == "arbitrary_precision"
        assert st["counters"]["capacity_bit_length"] > 128
        no_cliques, _ = run(["oracle", "--graph", graph, "--h", str(2**200), "--lambda", "1/2"])
        assert json.loads(no_cliques.stdout)["vertices"] == []
        for args in [[], ["unknown"], ["--help", "extra"], ["print-build-info", "extra"], ["oracle"], ["inspect-graph"],
                     base + ["--lambda", "1/2"], base + ["--x", x], base + ["--capacity", "big"],
                     base + ["--output"], ["oracle", "--graph", "missing", "--h", "1", "--lambda", "0/1"]]:
            run(args, 2, "invalid_argument")
        for value in ["1/0", "-1/2", "1.0", "1", "01/2", "+1/2", "1/02", "1/2/3"]:
            run(base[:-1] + [value], 2, "invalid_argument")
        run(["solve", "--graph", "missing", "--output", output], 8, "not_implemented")
        for suffix in [["--output", graph], ["--x", x, "--y", y, "--output", y]]:
            run(base + suffix, 2, "invalid_argument")
        symlink, hardlink = root / "symlink", root / "hardlink"
        symlink.symlink_to(graph)
        hardlink.hardlink_to(graph)
        for alias in [symlink, hardlink]:
            run(base + ["--output", alias], 2, "invalid_argument")
        run(base + ["--x", y, "--y", x], 2, "invalid_argument")
        for text in ["vflhcds-set 1 n 2 v -1 v -1", "vflhcds-set 1 n 1 v 99", "vflhcds-set 1 n 0 extra"]:
            x.write_text(text)
            run(base + ["--x", x, "--y", y], 2, "invalid_argument")
        for text in ["", "vflhcds-graph 2 n 1 v 0 m 0", "vflhcds-graph 1 n 0 m 0",
                     "vflhcds-graph 1 n 2 v 0 v 0 m 0", "vflhcds-graph 1 n 1 v 0 m 1 e 0 0",
                     "vflhcds-graph 1 n 1 v 0 m 1 e 0 1", "vflhcds-graph 1 n 2 v 0 v 1 m 2 e 0 1 e 1 0",
                     "vflhcds-graph 1 n 1 v -0 m 0", canonical + "garbage", "vflhcds-graph 1 n 01 v 0 m 0"]:
            graph.write_text(text)
            run(base + ["--output", output], 3, "invalid_graph")
            assert output.read_text() == "existing output\n"
        run(["inspect-graph", "--graph", root / "missing"], 4, "io_error")
        run(["inspect-graph", "--graph", root], 4, "io_error")
        graph.write_text(canonical)
        run(base + ["--output", root / "missing" / "out"], 4, "io_error")
        run(base + ["--output", root], 4, "io_error")
        assert output.read_text() == "existing output\n"
        saved, _ = run(base + ["--output", output])
        assert not saved.stdout and output.read_text() == answer.stdout
        assert not list(root.glob("*.tmp.*"))
        varied = " vflhcds-graph 1 n 5 v 20 v 9 v -1 v 5 v -10 m 2 e 9 5 e -1 -10\t"
        graph.write_text(varied)
        ordered, _ = run(base)
        assert ordered.stdout == answer.stdout
        graph.write_text(f"vflhcds-graph 1 n 2 v {2**200} v {-2**200} m 1 e {2**200} {-2**200}")
        exact, _ = run(base)
        assert json.loads(exact.stdout)["vertices"] == [-2**200, 2**200]
    print(f"M2 CLI: {calls} invocations passed; canonical JSON/IDs/statuses, real fallback, aliases and atomic output")


if __name__ == "__main__":
    main()
