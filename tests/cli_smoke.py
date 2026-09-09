"""M0 process-boundary checks; deliberately outside the independent reference."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    executable = str(Path(sys.argv[1]).resolve())
    for command in ["--help", "help", "print-build-info"]:
        result = subprocess.run([executable, command], capture_output=True, text=True, check=False)
        assert result.returncode == 0, result
        assert result.stdout and not result.stderr, result
        assert "M0" in result.stdout, result

    cases = [([], 2), (["unknown"], 2), (["--help", "extra"], 2),
             (["print-build-info", "extra"], 2), (["oracle"], 8), (["inspect-graph"], 8)]
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "result.jsonl"
        target.write_text("existing output\n")
        cases.append((["solve", "--graph", "missing", "--h", "3", "--k", "1",
                       "--output", str(target)], 8))
        for args, expected_exit in cases:
            result = subprocess.run([executable, *args], capture_output=True, text=True, check=False)
            assert result.returncode == expected_exit, result
            assert result.stdout == "", result
            record = json.loads(result.stderr)
            assert record == {
                "schema_version": 1,
                "status": "invalid_argument" if expected_exit == 2 else "not_implemented",
                "complete": False, "output_count": 0, "semantic_sha256": None,
            }, record
        assert target.read_text() == "existing output\n"
    print("M0 CLI: 3 successful diagnostics; 7 failures; output preserved")


if __name__ == "__main__":
    main()
