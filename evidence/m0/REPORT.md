# M0 completion record — 2026-09-09

Scope: P00.1-P00.4 only. Base commit
`60321429ef832d7032d1e6ad96965dd2a95b08aa`, uncommitted working-tree delivery.
The owner's pre-existing document edits are recorded in `initial_git_status.txt`
and preserved. That capture also shows `evidence/`, created immediately before
the status capture for this M0 run. No M1+ task or production obligation is marked
complete.

## Individual status

| Task | Result | Evidence |
|---|---|---|
| P00.1 | Complete with explicit provenance: the owner confirmed the earlier SHA-256 snapshot had never been created. Recorded the initial snapshot now; all four files match HEAD and pass snapshot verification before and after the build sequence. This is not verification against a previously existing manifest or evidence of historical priority. | `preservation_start.json`, [snapshot](../../review/source_snapshot_sha256.json), `checks/01.log`, `checks/17.log`, `preservation_final.json` |
| P00.2 | Complete: reviewed existing O01-O12, accepted D001-D015 and revision D016-D026, honoring superseded rows. No genuinely new internal conflict found. No second theory audit or change to proof, specification, audit, decisions, architecture or correctness plan. D005/D006/D012 retained. | Required input reads; protected-file SHA-256 comparisons in `preservation_final.json` |
| P00.3 | Complete: C++17/CMake library, CLI, CTest and independent standard-library Python/pytest skeleton; strict warnings; ASan+UBSan option; all four build profiles executed. | `checks/commands.json`, numbered logs, `compiler_flags.json`, `fixture_manifest.json` |
| P00.4 | Complete as interface freeze: canonical graph/IDs, requests, k>=1/fixed-k order, JSON, failures/completion, timing and counter semantics. Executable contains only diagnostics and unavailable-command failures. | `docs/INTERFACE_CONTRACT.md` from repository root; CLI/C++ smoke tests |

No unresolved blocking conflict. M0 gate is met; neither algorithm implementation
nor mathematical implementation validation is claimed.

## Changes and symbols

`files_changed.json` lists every delivered M0 file and its SHA-256 (the file
manifest and evidence checksum manifest are not self-hashed). Existing files
changed by M0 are only `README.md`, `docs/TASKS.md`, and `docs/CLAIM_TRACEABILITY.md`.

Added build/configuration: `.gitignore`, `CMakeLists.txt`, `cmake/build_info.cpp.in`,
`pyproject.toml`, `requirements-dev.txt`, `docs/BUILD.md`.
Added contract: `docs/INTERFACE_CONTRACT.md`.
Added compiled sources/headers: `include/vflhcds/core/build_info.hpp`,
`include/vflhcds/cli/dispatch.hpp`, `include/vflhcds/io/status.hpp`,
`src/cli/main.cpp`, `src/cli/dispatch.cpp`, `src/io/status.cpp`.
Reserved clique/flow/oracle/solver/telemetry include/source directories and
`src/core` contain README files only.

Build symbols: `vflhcds_lib` (`vflhcds::lib` alias), `vflhcds`,
`vflhcds_skeleton_test`, `VFLHCDS_ENABLE_SANITIZERS`.
C++ symbols: `BuildInfo`, `build_info`, `run_cli`, `RunStatus`, `status_name`,
`exit_code`, `write_failure_status`, `main`.

Added independent reference: `reference/README.md`,
`reference/vflhcds_reference/{__init__,direct,parametric}.py`,
`reference/tests/test_skeleton.py`. The modules have docstrings only; isolated
imports work without production paths. Added tests: `tests/skeleton_test.cpp`,
`tests/cli_smoke.py`. Added external-validation boundary: `validation/README.md`.
Added scripts: `scripts/verify_papers.py`, `scripts/run_m0_checks.py`.
Added initial paper snapshot and this `evidence/m0/` record.

## Commands and actual results

Tools were activated with `. .venv/bin/activate`. Ran
`python scripts/run_m0_checks.py evidence/m0/checks`, which executed the exact
17 argv lists stored with exit codes/timestamps/log hashes in `checks/commands.json`.
All 17 exited 0. Required commands and their observed results:

| Command | Result | Log |
|---|---|---|
| `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | Configured/generated successfully | `checks/02.log` |
| `cmake --build build -j2` | All 3 compiled targets built, no compiler warnings/errors | `checks/03.log` |
| `ctest --test-dir build --output-on-failure` | 3/3 passed, 0 failed (0.88 s) | `checks/04.log` |
| `python -m pytest reference/tests -q` | 1 passed (0.03 s) | `checks/05.log` |
| `cmake -S . -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DVFLHCDS_ENABLE_SANITIZERS=ON` | Configured/generated successfully | `checks/06.log` |
| `cmake --build build-sanitize -j2` | All 3 compiled targets built, no compiler warnings/errors | `checks/07.log` |
| `ctest --test-dir build-sanitize --output-on-failure` | 3/3 passed, 0 failed, no ASan/UBSan diagnostics (2.53 s) | `checks/08.log` |
| Release configure/build/CTest, `build-release`, `-DCMAKE_BUILD_TYPE=Release`, `-j2` | All build steps succeeded; 3/3 CTest passed (1.06 s) | `checks/09.log`–`11.log` |
| RelWithDebInfo configure/build/CTest, `build-relwithdebinfo`, `-DCMAKE_BUILD_TYPE=RelWithDebInfo`, `-j2` | All build steps succeeded; 3/3 CTest passed (0.86 s) | `checks/12.log`–`14.log` |
| `build/vflhcds print-build-info`; `build-sanitize/vflhcds print-build-info` | C++17/Debug, AppleClang; sanitizer OFF/ON respectively | `checks/15.log`, `checks/16.log` |
| `python scripts/verify_papers.py` before and after | 4/4 matching SHA-256 hashes on each run | `checks/01.log`, `checks/17.log` |

Additional executed checks: `git diff --check`; inspection of all 20 generated
translation-unit commands for C++17/strict warning flags; sanitizer compile flags
and both executable link commands verified; all 11 protected input files match
their task-start hashes. These inspections produced `compiler_flags.json` and
`preservation_final.json`. No algorithm was added to exercise the sanitizer.

Fixture manifest: `fixture_manifest.json`. CTest names are `m0_cpp_skeleton`,
`m0_cli_contract`, `m0_reference_skeleton`. CLI smoke uses 3 successful diagnostic
commands, 7 explicit failure cases and a temporary pre-existing output sentinel.
There are no graph cases, random seeds, truth fixtures or T01-T17 results in M0.
The repeated reference CTest invocation is the same one pytest import test,
not additional mathematical coverage.

## Environment and setup limitations

macOS/Darwin 24.6.0 arm64; Apple clang 17.0.0 (clang-1700.6.3.2); CMake/CTest
4.4.3; Python 3.12.2; pytest 8.4.2. CMake used `/usr/bin/c++` and Unix Makefiles.
`checks/environment.json` records paths, selected environment and initial dirty
status; `toolchain.log` records full compiler/runtime versions. CPU/memory sysctl
read was denied by the sandbox (exit 1); no machine resource profile is claimed.

Initial PATH had neither `cmake` nor `python`. Executed
`python3 -m venv --system-site-packages .venv` (success), then
`.venv/bin/python -m pip install cmake`. The first install failed due sandbox
network resolution (`tooling-install.log`); approved retry succeeded and installed
CMake 4.4.3 (`tooling-install-retry.log`). Existing pytest was reused. No global
package changes or future solver dependencies were added. `.venv` and builds
are ignored. Tooling setup failure is retained, not omitted from evidence.

The initial snapshot search found no manifest in the checkout or tracked history;
a broader parent-directory search was denied. The owner's subsequent reply
confirmed it had not been created, resolving the missing-input question. Other
pre-existing references to `review/math_sanity.py`/results do not correspond to
files supplied here; M0 neither reruns nor fabricates that earlier review evidence.

## Unrun work and claim limits

All M1+ work remains unimplemented/unrun: reference definitions/exhaustive F/chain,
graph reader/normalizer, clique enumeration, exact fractions/counts and actual
128-bit fallback, footprints, max-flow, certified oracle, recursion/extraction,
fixed-k runtime ordering/domain validation, successful result/hash writer,
algorithm counters/timing, optimizations, baselines, differential campaigns and
benchmark/release work. The output/telemetry/hash rules are contracts for those
milestones, not exercised algorithm behavior.

No T16 sanitizer/numeric campaign, TSan/parallel work, alternate platform/compiler,
multi-configuration-generator or clean-machine reproduction was run. The M0
sanitizer result applies only to the small compiled skeleton. No external baseline
source was read/copied; D012's independent-development boundary is preserved.
Passing these finite bootstrap tests does not prove the theorem or close O01-O12.
