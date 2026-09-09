"""Verify the four preserved paper bytes against the recorded SHA-256 manifest."""

import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    snapshot = json.loads((root / "review/source_snapshot_sha256.json").read_text())
    expected = snapshot["sha256"]
    actual_paths = {path.relative_to(root).as_posix() for path in (root / "papers").iterdir()}
    if len(expected) != 4 or set(expected) != actual_paths:
        raise SystemExit("Paper file set differs from the four-file snapshot")
    matched = True
    for relative, expected_hash in sorted(expected.items()):
        actual_hash = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        ok = actual_hash == expected_hash
        matched = matched and ok
        print(f"{'OK' if ok else 'MISMATCH'} {relative} {actual_hash}")
    raise SystemExit(0 if matched else 1)


if __name__ == "__main__":
    main()
