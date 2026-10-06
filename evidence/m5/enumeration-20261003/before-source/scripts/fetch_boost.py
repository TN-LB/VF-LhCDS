"""Fetch only Boost headers/license from a pinned, SHA-256-verified release.

No package manager, configure-time network, compiled Boost libraries or global
installation. Source/hash metadata: archives.boost.io/release/1.86.0/source/.
"""

import hashlib
from pathlib import Path
import shutil
import tarfile
import subprocess

VERSION = "boost_1_86_0"
URL = "https://archives.boost.io/release/1.86.0/source/boost_1_86_0.tar.bz2"
SHA256 = "1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b"


def main():
    destination = Path(__file__).resolve().parents[1] / ".deps"
    destination.mkdir(exist_ok=True)
    archive = destination / (VERSION + ".tar.bz2")
    if not archive.exists():
        partial = archive.with_suffix(".partial")
        subprocess.run(["curl", "--fail", "--location", "--connect-timeout", "60",
                        "--output", str(partial), URL], check=True)
        partial.replace(archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != SHA256:
        raise SystemExit(f"Boost archive SHA-256 mismatch: {digest}")
    with tarfile.open(archive, "r:bz2") as bundle:
        for member in bundle:
            if not (member.name.startswith(VERSION + "/boost/") or member.name == VERSION + "/LICENSE_1_0.txt"):
                continue
            path = (destination / member.name).resolve()
            if not path.is_relative_to(destination.resolve()) or not (member.isdir() or member.isfile()):
                raise SystemExit("Unsafe archive entry")
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with bundle.extractfile(member) as source, path.open("wb") as target:
                    shutil.copyfileobj(source, target)
    print(f"Boost 1.86.0 headers and BSL-1.0 license: {destination / VERSION}")
    print(f"archive_sha256={digest}")


if __name__ == "__main__":
    main()
