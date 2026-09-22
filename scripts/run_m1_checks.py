"""Record final M1 unit/CLI/integration checks in a fresh output directory.

Usage: python scripts/run_m1_checks.py evidence/m1/final
Campaigns are separate commands in validation/reference_campaign.py so recorded
campaigns are not overwritten or silently rerun by this smoke-check driver.
"""

import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONPATH=str(root / "reference"))
    metadata = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "cwd": str(root), "python": sys.version, "platform": platform.platform(),
                "python_executable": sys.executable, "ctest": shutil.which("ctest"),
                "PYTHONPATH": env["PYTHONPATH"],
                "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
                "git_status": subprocess.check_output(["git", "status", "--short"], cwd=root, text=True),
                "package_sha256": {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in sorted((root / "reference/vflhcds_reference").glob("*.py"))}}
    (output / "environment.json").write_text(json.dumps(metadata, indent=2) + "\n")
    prefix = ["python", "-m", "vflhcds_reference"]
    commands = [
        (["python", "-m", "pytest", "reference/tests", "-q", "--junitxml=" + str(output / "pytest.xml")], 0),
        (prefix + ["truth", "--graph", "reference/fixtures/bridged_triangles.graph", "--h", "3", "--all"], 0),
        (prefix + ["truth", "--graph", "reference/fixtures/triangle_and_isolate.graph", "--h", "3", "--k", "1"], 0),
        (prefix + ["oracle", "--graph", "reference/fixtures/triangle_and_isolate.graph", "--h", "3", "--lambda", "1/3"], 0),
        (prefix + ["oracle", "--graph", "reference/fixtures/triangle_and_isolate.graph", "--h", "3", "--lambda", "100/1"], 0),
        (prefix + ["oracle", "--graph", "reference/fixtures/triangle_and_isolate.graph", "--h", "3", "--lambda", "0/1", "--x", "reference/fixtures/empty.set", "--y", "reference/fixtures/triangle.set"], 0),
        (prefix + ["chain", "--graph", "reference/fixtures/outer_breakpoint.graph", "--h", "2"], 0),
        (prefix + ["truth", "--graph", "reference/fixtures/triangle_and_isolate.graph", "--h", "3", "--k", "0"], 2),
        (["ctest", "--test-dir", "build", "--output-on-failure"], 0),
        (["python", "scripts/verify_papers.py"], 0),
        (["git", "diff", "--check"], 0),
    ]
    records = []
    for index, (command, expected_exit) in enumerate(commands, 1):
        print("RUN " + shlex.join(command), flush=True)
        stdout, stderr = output / f"{index:02d}.stdout", output / f"{index:02d}.stderr"
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with stdout.open("w") as out, stderr.open("w") as err:
            result = subprocess.run(command, cwd=root, env=env, stdout=out, stderr=err, check=False)
        record = {"command": command, "started_utc": started,
                  "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  "expected_exit_code": expected_exit, "exit_code": result.returncode,
                  "stdout": stdout.name, "stderr": stderr.name,
                  "stdout_sha256": hashlib.sha256(stdout.read_bytes()).hexdigest(),
                  "stderr_sha256": hashlib.sha256(stderr.read_bytes()).hexdigest()}
        records.append(record)
        (output / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
        if result.returncode != expected_exit:
            print(stdout.read_text() + stderr.read_text(), flush=True)
            raise SystemExit(f"unexpected exit code {result.returncode}")
        if command[:3] == prefix:
            status = json.loads(stderr.read_text())
            assert status["complete"] == (expected_exit == 0)
            if expected_exit == 0:
                assert json.loads(stdout.read_text())["schema_version"] == 1
            else:
                assert stdout.read_text() == "" and status["status"] == "invalid_argument"
        print(f"exit={result.returncode} (expected {expected_exit})", flush=True)


if __name__ == "__main__":
    main()
