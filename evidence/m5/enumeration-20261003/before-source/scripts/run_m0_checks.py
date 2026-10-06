"""Run only bootstrap checks, preserving commands, exit codes and complete logs.

Usage: python scripts/run_m0_checks.py evidence/m0/checks
Requires cmake/ctest/python on PATH (activate the local environment if needed).
The output directory must not already exist. No benchmarks or algorithm tests.
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
    environment = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cwd": str(root), "os": platform.platform(), "machine": platform.machine(),
        "python": sys.version, "python_executable": sys.executable,
        "tools": {name: shutil.which(name) for name in ["cmake", "ctest", "python", "clang++", "make"]},
        "environment": {name: os.environ.get(name) for name in ["PATH", "CC", "CXX", "CXXFLAGS", "LDFLAGS", "CMAKE_GENERATOR", "ASAN_OPTIONS", "UBSAN_OPTIONS"]},
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "git_status": subprocess.check_output(["git", "status", "--short"], cwd=root, text=True),
        "scope": "M0 skeleton only; no dataset, random seed, experiment budget or algorithm campaign",
    }
    (output / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    commands = [
        ["python", "scripts/verify_papers.py"],
        ["cmake", "-S", ".", "-B", "build", "-DCMAKE_BUILD_TYPE=Debug"],
        ["cmake", "--build", "build", "-j2"],
        ["ctest", "--test-dir", "build", "--output-on-failure"],
        ["python", "-m", "pytest", "reference/tests", "-q"],
        ["cmake", "-S", ".", "-B", "build-sanitize", "-DCMAKE_BUILD_TYPE=Debug", "-DVFLHCDS_ENABLE_SANITIZERS=ON"],
        ["cmake", "--build", "build-sanitize", "-j2"],
        ["ctest", "--test-dir", "build-sanitize", "--output-on-failure"],
    ]
    for directory, profile in [("build-release", "Release"), ("build-relwithdebinfo", "RelWithDebInfo")]:
        commands.extend([
            ["cmake", "-S", ".", "-B", directory, f"-DCMAKE_BUILD_TYPE={profile}"],
            ["cmake", "--build", directory, "-j2"],
            ["ctest", "--test-dir", directory, "--output-on-failure"],
        ])
    commands.extend([["build/vflhcds", "print-build-info"],
                     ["build-sanitize/vflhcds", "print-build-info"],
                     ["python", "scripts/verify_papers.py"]])
    records = []
    for index, command in enumerate(commands, start=1):
        log = output / f"{index:02d}.log"
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(f"RUN {shlex.join(command)}", flush=True)
        with log.open("w") as stream:
            result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=False)
        records.append({"command": command, "started_utc": started,
                        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "exit_code": result.returncode, "log": log.name,
                        "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()})
        (output / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
        print(log.read_text(), end="", flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
