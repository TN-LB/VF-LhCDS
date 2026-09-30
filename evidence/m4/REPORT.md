# M4 executed implementation and validation report

Date: 2026-09-29. P07.1-P07.3 and P08.1 meet their implementation/test gates.
No unresolved blocking conflict, new proof/specification conflict, production
counterexample or owner decision arose. All 36 final acceptance commands exited 0.
Finite agreement is implementation evidence, not a proof of the mathematical theorem.

The working tree started clean at `5802d5a2a04cae35eaf708aba65f638abf642c8f`.
M4 changes are uncommitted; the tested source is identified by
[53 source hashes](accepted/environment.json) and the
[complete changed-file manifest](files_changed.json). The new O10 implementation's
formal `implementation-tested` ledger label remains pending its implementation
commit, as required by the ledger. M4 requests no new tag. The M3 implementation
tag `v0.1.0-m3-correctness` still resolves to
`23a5b3415cf3ae053e55a01b219ca074ffe6fd67`.

## Implemented scope and changed files

| Task | Status | Symbols and behavior | Obligations/tests |
|---|---|---|---|
| P07.1 | Implemented and tested | `peel_core`, `CoreStats`: exact current h-clique degree, deterministic queue, each clique invalidated once, remaining vertices updated once per invalidated clique | O10, T17 |
| P07.2 | Implemented and tested | `ClosureOracle::global_F`, private `restricted_impl`, `OracleOptions`: certified positive queries use `Y_oracle = original Y intersect core_ceil(lambda)(G)` | O04,O05,O07,O10, T10,T11,T17 |
| P07.3 | Argument written, reviewed and tested | Original interval/chain/endpoints/lambda and extraction retained; four-mode equality; distinct core work/time and reduced-network telemetry | O09,O10,O12, T13,T17 |
| P08.1 | Profiled, implemented and tested | `aggregate_footprints(FootprintMode::Membership)`: one optional membership-marker scan, same ordered weights and exact network | O06,O11, T06,T09,T16,T17 |

The refinement/containment argument is in
[M4_IMPLEMENTATION.md](../../docs/M4_IMPLEMENTATION.md). The separate
[code/evidence review](REVIEW.md) was by the implementing assistant, not independent
human sign-off or a new theory audit.

Production and interface files:

- Added `include/vflhcds/clique/core.hpp` and `src/clique/core.cpp`.
- Changed `include/vflhcds/oracle/closure.hpp`, `src/oracle/closure.cpp`,
  `include/vflhcds/solver/solver.hpp`, `src/solver/solver.cpp`,
  `include/vflhcds/telemetry/query.hpp`, `src/telemetry/query.cpp` and
  `src/cli/dispatch.cpp` to carry options and report actual core work.
- Changed `CMakeLists.txt`: core source, M4 tests/profile target, version 0.2.0.
  Existing C++17 strict warnings and exact numeric backend remain in force.

Test/evidence files:

- Added `tests/m4_core.cpp`, `tests/m4_cli.py`, `tests/m4_profile.cpp`,
  `validation/m4_campaign.py`, `validation/m4_profile.py` and
  `scripts/run_m4_checks.py`.
- Extended the test-only `tests/m3_probe.cpp` with mode/core/footprint commands;
  changed `tests/cli_smoke.py` only for the new version/stage expectation.
- Updated root README, clique/oracle/telemetry module READMEs, validation README,
  `docs/BUILD.md`, `docs/INTERFACE_CONTRACT.md`, `docs/TASKS.md` and
  `docs/CLAIM_TRACEABILITY.md`; added `docs/M4_IMPLEMENTATION.md` and this evidence
  directory. The file manifest enumerates every changed/new file and its SHA-256.

The public solve switches are `--core-reduction off|safe` and
`--footprint-scan sorted|membership`, defaulting to `off/sorted`. The oracle CLI
accepts the footprint switch but does not core-prune arbitrary restricted bounds.
Canonical results, original vertex IDs, exact arithmetic, fixed-k order and
semantic hashes are unchanged. Positive safe queries recompute the core of the
full original index every time; zero bypasses core. No cross-threshold cache,
new clique/flow backend, verifier in the solver, parallel execution or dependency
was added. The original `ChainInterval` and terminal `Z == original Y` remain.

## Actual build and test results

Environment: macOS 15.7.7 arm64; AppleClang 17.0.0.17000603; CMake 4.4.3;
Python 3.12.2; pytest 8.4.2; existing Boost.Multiprecision 1.86.0 headers.
The acceptance process used `.venv/bin` on PATH; `python`, `cmake` and `ctest`
resolve there. Environment and exact source hashes are in
[environment.json](accepted/environment.json); actual compiler commands are in
[compiler_flags.json](compiler_flags.json). No ASAN_OPTIONS/UBSAN_OPTIONS overrides
were set. Flags include `-std=c++17 -Wall -Wextra -Wpedantic -Wconversion
-Wsign-conversion -Wshadow -Werror`; the sanitizer build includes
`-fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer`.

| Configuration | Build result | CTest result | CTest elapsed | Log |
|---|---|---|---|---|
| Debug | Passed | 12/12 | 5.51 s | [03.stdout](accepted/03.stdout) |
| Debug ASan+UBSan | Passed | 12/12 | 16.24 s | [13.stdout](accepted/13.stdout) |
| Release | Passed | 12/12 | 6.06 s | [23.stdout](accepted/23.stdout) |
| RelWithDebInfo | Passed | 12/12 | 6.15 s | [26.stdout](accepted/26.stdout) |
| Release, BUILD_TESTING=OFF | Passed | Not applicable | — | [28.stdout](accepted/28.stdout) |

Standalone `python -m pytest reference/tests -q`: **74 passed in 1.37 s**
([30.stdout](accepted/30.stdout)). Each CTest configuration also ran the unchanged
74 independent reference tests, retained M2/M3 tests, 30 new C++ core/mode checks
and 40 M4 CLI invocations. Production-only safe+membership execution on bridged
triangles passed external direct-definition checking
([runner manifest](accepted/cli-definition-run-safe-membership/manifest.json));
validation time is outside native algorithm time.

Both Debug and ASan/UBSan separately completed the following M4 tiers:

| Tier | Base graph/h cases | Distinct base graphs | Checked variants | Independent core requests | Footprint-bound pairs | Four-mode solver executions | Fixed-k prefix requests |
|---|---:|---:|---:|---:|---:|---:|---:|
| exhaustive-small | 2,198 | 1,099 | 4,396 | 22,054 | 42,164 | 153,920 | 14,844 |
| seeded | 1,000 | 860 | 2,040 | 8,492 | 10,200 | 79,968 | 7,956 |
| higher-h | 64 | 60 | 128 | 430 | 1,184 | 4,672 | 456 |
| smoke (includes audit C) | 31 | 27 | 124 | 589 | 1,642 | 4,976 | 498 |

Counts are per build. Tiers overlap; variants include relabeling and declared
isolate/disjoint additions; solver executions include four mode combinations and
auto/forced-BigInt repetitions. Prefix requests are the M3 corpus's distinct
variant/k requests before mode/capacity repetition. These numbers must not be
summed as distinct graphs. Seeded M4 fixtures use seed **20260929**, n=6..8,
200 graph/h cases per random/planted/bridge/tied/disconnected family. The first
20 seeded cases also get isolate/disjoint variants. Every input and count is in
[fixture_manifest.json](fixture_manifest.json) and its referenced cases.jsonl.

The independent core expectation unions every induced subset satisfying the
degree threshold; it does not use production peeling. Reference cliques provide
independent footprint records. Every tested variant covers thresholds
0..maximum initial clique degree+1 and 2^200; nested footprint bounds are exhaustive
for n<=4, with five selected pairs for larger variants. The unchanged independent
M1 direct-definition truth checks full output and every k=1..q+2; the independent
line envelope checks chain pairs. All four core/scan combinations agree on exact
sets, prefixes, hashes and original recursion traces. Reduced N, footprints,
network sizes, capacities, bypasses, core update counters and telemetry are checked.

The named [audit-C witness](core_witness.json) saves actual accepted core and solve
responses: K4 disjoint from triangle+pendant has a root core that is not a chain
endpoint, and the pendant is retained later when the query threshold decreases.
Other tests cover cascade invalidation, h-clique versus ordinary degree, zero and
empty cores, huge h/thresholds, foreign/moved certificates and real automatic
arbitrary-precision execution.

The retained M2 oracle regression also passed in both builds: exhaustive-small
2,198 cases / 40,591 requests; seed **20260922** 1,000 cases / 12,000 requests;
higher-h 72 cases / 1,053 requests. All 14 campaign stderr files are empty; no
sanitizer finding or production/reference mismatch occurred in acceptance.

[Integrity verification](verification.json) passed: all 36 command outcomes and
log hashes, all campaign hashes, 53 accepted source hashes, seven complete
Debug/sanitizer response pairs, and three frozen M3 baseline corpus comparisons.
The cross-build comparison excludes measured core time only. The cross-version
M3 comparison excludes test token IDs and newly added core telemetry fields;
inputs, prior response fields and semantic results are identical. Details and
normalized hashes are in [cross_version_comparisons.json](cross_version_comparisons.json).

## Profile-first selection and measured local costs

[profile_workload.json](profile_workload.json) fixed three synthetic inputs and
their hashes, Release/auto/all, one worker, ten solves per process and three
process repetitions before production edits. The M3 baseline library and manual
profile driver compilation plus nine process runs are retained in
[profile-before.json](profile-before.json). [profile-selection.json](profile-selection.json)
records source/library/driver/binary hashes and the decision to test exactly one
additional change: membership scanning for footprint construction.

The actual pre-edit median footprint/solve ratios were 42.10%, 41.72%, and 38.58%.
The selection record's prose said "39-44 percent"; the recorded numeric fields
give the more precise range above and remain unchanged. These separately measured
microphases identify a local cost; they are not an exact additive phase breakdown.

All 36 post-change processes completed and matched the corresponding pre-edit
M3 semantic hash. All runs are retained in [runs.json](accepted/profiles/runs.json),
including overhead and memory variation. Values below are the median of three
process means (ten solves each), in milliseconds:

| Fixture | Pre-edit M3 solve | off/sorted | off/membership | safe/sorted | safe/membership |
|---|---:|---:|---:|---:|---:|
| layered-h3, n=96, 1,320 cliques | 5.058 | 7.403 | 4.069 | 5.015 | 4.005 |
| dense-pendants-h3, n=80, 9,880 cliques | 21.732 | 23.387 | 21.158 | 23.063 | 21.254 |
| layered-h4, n=48, 2,385 cliques | 7.578 | 7.058 | 5.954 | 6.984 | 5.919 |

The pre/post default-path times vary in both directions. The post-change four
mode order was rotated deterministically, but these small three-process samples
do not support a stable general before/after speedup claim. Separate footprint
diagnostics, core cost nested inside solve, and whole-process peak RSS are:

| Fixture | Footprint ms: off sorted/member | Footprint ms: safe sorted/member | Core ms: safe sorted/member | RSS bytes: off sorted/member | RSS bytes: safe sorted/member |
|---|---|---|---|---|---|
| layered-h3 | 2.189 / 1.244 | 2.107 / 1.244 | 0.020801 / 0.018275 | 5,095,424 / 4,571,136 | 4,784,128 / 3,751,936 |
| dense-pendants-h3 | 9.329 / 7.702 | 9.147 / 7.634 | 0.007933 / 0.007067 | 24,510,464 / 27,164,672 | 25,591,808 / 25,362,432 |
| layered-h4 | 2.724 / 1.748 | 2.719 / 1.743 | 0.013516 / 0.012920 | 7,094,272 / 6,946,816 | 8,454,144 / 8,110,080 |

Membership scanning reduced this measured footprint phase on all three inputs.
Core's effect on total solve time varied; e.g. dense-pendants membership was
slightly slower with safe core. RSS changes were mixed. macOS RSS is the whole
process peak, including index and diagnostic repeats, not just core allocations.
Core time is already included in solve time; standalone footprint time must not
be added to solve time. Exact unrounded values are in
[profile summary](accepted/profiles/summary.json).

Across ten solves, total oracle N sizes decreased with safe core:
3,040 to 2,020; 1,600 to 1,200; 1,480 to 1,040 respectively. Total network nodes
decreased 43,720 to 42,500; 198,840 to 198,440; 55,530 to 54,390. The node reduction
is smaller than vertex reduction because materialized clique footprints remain.
Both scan modes give the same corresponding counts. Every query rebuilds the core;
its event counters describe full-graph peeling, not merely removed interval vertices.

These are local implementation diagnostics, not M5 benchmarks, scalability evidence,
final experimental parameter choices or a comparison with any external method.
Both optimizations remain optional with defaults off/sorted.

## Retained development findings, preservation and unrun work

Two routine development errors were corrected before acceptance with original
logs retained: `dev-build.log` records a test-probe -Wshadow error (local renamed,
no warning suppressed; `dev-build-2.log` passes). `dev-ctest.log` records 10/11
tests passing and an audit-C fixture rejected for unsorted edges before reaching
the solver. Sorting the fixture fixed construction; `dev-smoke/` then passed.
Neither was a mathematical counterexample, unresolved blocker or semantic decision.
No actual solver mismatch occurred to minimize.

[Preservation](preservation_final.json) verifies all four papers against their
recorded hashes and preserves accepted decisions, theory/spec/audit, the independent
reference and the M3 evidence/tag. Only the declared interface/build/task/evidence
documents among the starting document snapshot were updated. D005, D006 and D012
remain in force. No external baseline implementation or technique was imported.

Unrun/deferred: extended n<=12 production differential tiers, GCC/Linux execution,
real OS OOM-pressure/interrupt stress, TSan (no parallel code), all baseline adapter
work and every M5 benchmark/release task. M5 dataset/resource/thread/timeout policy
still requires its recorded decisions before a campaign. No such decisions were
made here. M4 changes have not been committed or tagged. There is no unresolved
blocking conflict in the executed M4 scope.

## Executed commands

The full acceptance driver was run with the existing repository virtual environment
on PATH: `python scripts/run_m4_checks.py evidence/m4/accepted`.
[accepted-driver.log](accepted-driver.log) and [commands.json](accepted/commands.json)
retain every command, UTC times, exit code, stdout/stderr path and hash. The table
below renders those exact command arguments; every exit code is 0. Before acceptance,
the saved baseline profile and development logs above record the earlier runs.
After report updates, `.venv/bin/python evidence/m4/verify_evidence.py` rechecked
saved evidence and `git diff --check` checked final whitespace; this does not
pretend documentation-only edits reran the test campaign.

| # | Exact command | Result / stdout |
|---|---|---|
| 01 | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | exit 0; [01.stdout](accepted/01.stdout) |
| 02 | `cmake --build build -j2` | exit 0; [02.stdout](accepted/02.stdout) |
| 03 | `ctest --test-dir build --output-on-failure -V` | exit 0; [03.stdout](accepted/03.stdout) |
| 04 | `python validation/m4_campaign.py --probe build/vflhcds_m3_probe --tier smoke --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-smoke` | exit 0; [04.stdout](accepted/04.stdout) |
| 05 | `python validation/m4_campaign.py --probe build/vflhcds_m3_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-exhaustive-small` | exit 0; [05.stdout](accepted/05.stdout) |
| 06 | `python validation/m4_campaign.py --probe build/vflhcds_m3_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-seeded` | exit 0; [06.stdout](accepted/06.stdout) |
| 07 | `python validation/m4_campaign.py --probe build/vflhcds_m3_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-higher-h` | exit 0; [07.stdout](accepted/07.stdout) |
| 08 | `python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-m2-exhaustive-small` | exit 0; [08.stdout](accepted/08.stdout) |
| 09 | `python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-m2-seeded` | exit 0; [09.stdout](accepted/09.stdout) |
| 10 | `python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-m2-higher-h` | exit 0; [10.stdout](accepted/10.stdout) |
| 11 | `cmake -S . -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DVFLHCDS_ENABLE_SANITIZERS=ON` | exit 0; [11.stdout](accepted/11.stdout) |
| 12 | `cmake --build build-sanitize -j2` | exit 0; [12.stdout](accepted/12.stdout) |
| 13 | `ctest --test-dir build-sanitize --output-on-failure -V` | exit 0; [13.stdout](accepted/13.stdout) |
| 14 | `python validation/m4_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier smoke --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-smoke` | exit 0; [14.stdout](accepted/14.stdout) |
| 15 | `python validation/m4_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-exhaustive-small` | exit 0; [15.stdout](accepted/15.stdout) |
| 16 | `python validation/m4_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-seeded` | exit 0; [16.stdout](accepted/16.stdout) |
| 17 | `python validation/m4_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-higher-h` | exit 0; [17.stdout](accepted/17.stdout) |
| 18 | `python validation/oracle_campaign.py --probe build-sanitize/vflhcds_m2_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-m2-exhaustive-small` | exit 0; [18.stdout](accepted/18.stdout) |
| 19 | `python validation/oracle_campaign.py --probe build-sanitize/vflhcds_m2_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-m2-seeded` | exit 0; [19.stdout](accepted/19.stdout) |
| 20 | `python validation/oracle_campaign.py --probe build-sanitize/vflhcds_m2_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/build-sanitize-m2-higher-h` | exit 0; [20.stdout](accepted/20.stdout) |
| 21 | `cmake -S . -B build-release -DCMAKE_BUILD_TYPE=Release` | exit 0; [21.stdout](accepted/21.stdout) |
| 22 | `cmake --build build-release -j2` | exit 0; [22.stdout](accepted/22.stdout) |
| 23 | `ctest --test-dir build-release --output-on-failure -V` | exit 0; [23.stdout](accepted/23.stdout) |
| 24 | `cmake -S . -B build-relwithdebinfo -DCMAKE_BUILD_TYPE=RelWithDebInfo` | exit 0; [24.stdout](accepted/24.stdout) |
| 25 | `cmake --build build-relwithdebinfo -j2` | exit 0; [25.stdout](accepted/25.stdout) |
| 26 | `ctest --test-dir build-relwithdebinfo --output-on-failure -V` | exit 0; [26.stdout](accepted/26.stdout) |
| 27 | `cmake -S . -B build-production -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF` | exit 0; [27.stdout](accepted/27.stdout) |
| 28 | `cmake --build build-production -j2` | exit 0; [28.stdout](accepted/28.stdout) |
| 29 | `python validation/m4_profile.py --executable build-release/vflhcds_m4_profile --output /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/profiles` | exit 0; [29.stdout](accepted/29.stdout) |
| 30 | `python -m pytest reference/tests -q` | exit 0; [30.stdout](accepted/30.stdout) |
| 31 | `python validation/run_solver.py --executable build-production/vflhcds --evidence /Users/nost/Documents/VF-LhCDS/evidence/m4/accepted/cli-definition-run-safe-membership --check-reference -- solve --graph reference/fixtures/bridged_triangles.graph --h 3 --all --core-reduction safe --footprint-scan membership` | exit 0; [31.stdout](accepted/31.stdout) |
| 32 | `python scripts/verify_papers.py` | exit 0; [32.stdout](accepted/32.stdout) |
| 33 | `git diff --check` | exit 0; [33.stdout](accepted/33.stdout) |
| 34 | `build/vflhcds print-build-info` | exit 0; [34.stdout](accepted/34.stdout) |
| 35 | `cmake --version` | exit 0; [35.stdout](accepted/35.stdout) |
| 36 | `c++ --version` | exit 0; [36.stdout](accepted/36.stdout) |
