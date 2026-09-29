"""Execute and retain M2 builds/tests/campaigns without overwriting prior evidence."""
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
    environment = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "cwd": str(root),
                   "platform": platform.platform(), "python": sys.version, "python_executable": sys.executable,
                   "cmake": shutil.which("cmake"), "ctest": shutil.which("ctest"),
                   "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
                   "git_status": subprocess.check_output(["git", "status", "--short"], cwd=root, text=True),
                   "ASAN_OPTIONS": os.environ.get("ASAN_OPTIONS"), "UBSAN_OPTIONS": os.environ.get("UBSAN_OPTIONS")}
    (output / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    commands = []
    for profile, directory in [("Debug", "build"), ("Debug", "build-sanitize"),
                               ("Release", "build-release"), ("RelWithDebInfo", "build-relwithdebinfo")]:
        configure = ["cmake", "-S", ".", "-B", directory, f"-DCMAKE_BUILD_TYPE={profile}"]
        if directory == "build-sanitize":
            configure += ["-DVFLHCDS_ENABLE_SANITIZERS=ON"]
        commands += [configure, ["cmake", "--build", directory, "-j2"],
                     ["ctest", "--test-dir", directory, "--output-on-failure", "-V"]]
        if directory in ("build", "build-sanitize"):
            for tier in ["smoke", "exhaustive-small", "seeded", "higher-h"]:
                commands.append(["python", "validation/oracle_campaign.py", "--probe", directory+"/vflhcds_m2_probe",
                                 "--tier", tier, "--output", str(output / (directory + "-" + tier))])
    commands += [["python", "-m", "pytest", "reference/tests", "-q"],
                 ["python", "scripts/verify_papers.py"], ["git", "diff", "--check"],
                 ["build/vflhcds", "print-build-info"], ["cmake", "--version"], ["c++", "--version"]]
    records = []
    for i, command in enumerate(commands, 1):
        print("RUN " + shlex.join(command), flush=True)
        stdout, stderr = output / f"{i:02d}.stdout", output / f"{i:02d}.stderr"
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with stdout.open("w") as out, stderr.open("w") as err:
            result = subprocess.run(command, cwd=root, stdout=out, stderr=err, check=False)
        records.append({"command": command, "started_utc": start,
                        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "exit_code": result.returncode, "stdout": stdout.name, "stderr": stderr.name,
                        "stdout_sha256": hashlib.sha256(stdout.read_bytes()).hexdigest(),
                        "stderr_sha256": hashlib.sha256(stderr.read_bytes()).hexdigest()})
        (output / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
        if result.returncode:
            print(stdout.read_text() + stderr.read_text(), flush=True)
            raise SystemExit(result.returncode)
        print("exit=0", flush=True)


if __name__ == "__main__":
    main()
