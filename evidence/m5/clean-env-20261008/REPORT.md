# Fresh Ubuntu reproduction — 2026-10-08

**Fresh software-environment reproduction passes.** Ubuntu 24.04.5 arm64,
GCC 13.3.0, Python 3.12.3, pytest 8.4.2, CMake 4.4.3 and Boost 1.86.0 were
prepared in a new OrbStack 2.0.1 machine. It shares the Linux kernel/physical Mac;
this is not independent hardware or a performance replication.

| Executed check | Result | Evidence |
|---|---|---|
| New VF strict Release build and eight-patch IPPV build | Both pass; all 23 smoke commands exit 0 | [commands](guest-checked/commands.json), [flags/pins](guest-checked/plan.json) |
| Linux CTest | 16/16 pass, 3.18 s | [log](guest-checked/commands/vf-ctest/stdout.txt) |
| Independent reference/harness/adapter pytest | 164 pass, 3.01 s | [log](guest-checked/commands/python-tests/stdout.txt) |
| Separate definition fixtures | 3 IPPV + 1 VF pass; all four canonical outputs equal macOS | [integrity](integrity.json) |
| Saved aggregate/review regeneration | 26/26 byte-identical; no benchmark reruns | [commands](guest-derived/commands.json), [hashes](guest-derived/completion.json) |
| macOS compatibility after test formatting repairs | Both probes rebuild; 3/3 affected smoke tests pass, 2.85 s | [build](host-commands/19-mac-probe-build/process.json), [tests](host-commands/21-mac-probe-smoke/stdout.txt) |
| Historical evidence/source integrity | 6,074 raw entries, four papers, 40 frozen production hashes and 112 other source/test/fixture files unchanged | [verification log](host-commands/23-final-integrity/stdout.txt) |

The [pre-recorded plan](plan.json), [source bundle identity](source-bundle.json),
[new dependency installation](guest-gcc-first/commands.json), [full package inventory](guest-gcc-first/commands/system-packages/stdout.txt)
and [Python package versions](guest-gcc-first/commands/python-freeze/stdout.txt)
retain the setup. Boost is downloaded and hash-checked; IPPV is newly acquired at
`f61881d4752170c03585e4281f0c49d7ef14aa1e` and all eight locked patches are applied.
No Mac .venv, headers or binaries are copied. The successful source is `5cc0a76`
plus the [three recorded overlays](host-commands/22-linux-source-overlay/stdout.txt).
Final checks use new build/evidence paths and reuse only those newly installed
Linux dependencies. The dedicated guest is stopped and retained after copying evidence.

## Repairs and retained failures

1. The initial OrbStack CLI invocation used an unsupported `--` separator;
   [the command failure](host-commands/03-initial-environment/process.json) is retained.
2. The historical reproduction driver resolved `.venv/bin/python` to system
   Python, bypassing venv packages. Fresh Linux therefore failed at pytest version
   discovery before configuration. [Original attempt/source](guest-first/) and
   [repair plan](repair-plan.json) are preserved. The reusable
   `scripts/reproduce_release.py::main` keeps the executable path without resolving
   interpreter symlinks; the final attempt passes with pytest installed only in the venv.
3. GCC's existing `-Werror=misleading-indentation` rejected adjacent statements in
   `tests/m2_probe.cpp::main`; the same pattern existed in `tests/m3_probe.cpp::main`.
   [Failed build](guest-gcc-first/smoke/commands/vf-build/stderr.txt) and its bootstrap
   remain intact. [Whitespace-only repairs](portability-plan.json) split statements
   onto separate lines. Strict warnings stay enabled; production sources stay frozen.

There is no unresolved semantic conflict or failed final check. Historical failed
attempts are not overwritten. Linux and Mac executable hashes differ as expected;
the measured Mac binaries are unchanged. [Linux binary hashes](guest-checked/completion.json).

## Commands, fixtures and scope

All actual host setup/transfer/build/stop commands are in [host-commands/](host-commands/),
and all successful Linux smoke commands in [the checked plan](guest-checked/plan.json).
The main entry point executed in Linux is:

```sh
/home/repro/vf-lhcds-fixed/.venv/bin/python /home/repro/vf-lhcds-fixed/scripts/reproduce_release.py --build /home/repro/clean-build-checked --evidence /home/repro/clean-evidence-checked
```

It runs CMake configure/build (`-j2`), CTest, reference/harness/adapter pytest,
the pinned baseline builder and external definition checks. `guest_finish.py::main`
regenerates existing tables; `verify.py::main` performs read-only integrity checks.
The changed-file inventory is [file_changes.json](file_changes.json).

Fixture manifest: [IPPV fractional bridge](guest-checked/ippv-fractional/plan.json)
(h=2,k=2), [equal-density bridge](guest-checked/ippv-equality/plan.json) (h=3,k=3),
[ordinary bridged triangles](guest-checked/ippv-bridge/manifest.json) (h=3,k=1),
and [VF triangle plus isolate](guest-checked/vf-definition/manifest.json) (h=3,all).
IPPV retains iterations=10/native p=0. CTest uses existing oracle smoke seed
20260922 and solver/mode smoke seed 20260929; these are correctness fixtures,
not new experimental parameters. Source and input hashes are retained in the plans
and integrity manifest. Zero-density VF output is preserved.

P15.1/O12 gain this evidence. M5 scope closure remains separate: IPPV's known
zero-density limitation, broader datasets/specialty baselines and unavailable
rank/detailed-phase metrics remain. DCLDS is deferred. Full Debug/sanitizer/
differential campaigns, raw performance reruns, independent hardware and publishing
are unrun here; existing D038/B09 evidence is not relabelled as rerun. Finite
definition-test agreement does not prove the mathematical theorem.
