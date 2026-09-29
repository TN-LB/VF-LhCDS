# M3 exact solver and correctness freeze — 2026-09-29

P04.1–P04.4, P05.1–P05.3 and P06.1 pass their executed implementation gates.
P13.1 code/evidence review is complete; R01 is resolved. M3/P13.1 complete: local annotated tag `v0.1.0-m3-correctness` freezes the tested implementation.
Implementation commit: `23a5b3415cf3ae053e55a01b219ca074ffe6fd67`.
Base: owner's M2 commit `0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6`.

No new proof/specification conflict was found. Four papers, accepted decisions
(including D005/D006/D012), theory/spec/interface documents, and independent M1
reference code/tests/fixtures remain unchanged. [Preservation](preservation_final.json)
checks all 44 start-snapshot files; only BUILD/TASKS/CLAIM evidence documentation
is permitted to change. No M4/M5 task, optimization, baseline or benchmark is complete.

## Delivered behavior and symbols

| Tasks / obligations | Code / behavior | Executed evidence |
|---|---|---|
| P04.1 / O03–O05 | Immutable `ChainPoint`, `ChainInterval::lambda`; `ClosureOracle::root_interval`, `global_chain_point`, `chain_interval`, `separator_request`, `separate`; sealed same-owner certified global requests | T10 every independent chain pair, exact original endpoints/counts/lambda, strict progress and terminal equivalence; move/type/owner tests |
| P04.2 / O02,O07 | `solve` explicit left-first stack; terminal iff Z==original Y; ordinary components in original G[Y minus X], anti-adjacency to all X | T11 direct truth, ordinary bridge, K4/pendant and non-emitting terminal traces |
| P04.3 / O08 | `solve` exact density-layer traversal, original-ID lexicographic ties, immediate k stop, zero-density/isolate preservation, full mode | T12 every k=1..q+2, huge k/IDs, k=0 rejection, no eager right query |
| P04.4 / O09 | `SolveStats::record`, logical interval entries, actual mincuts, per-query sizes/backends/scans | T13 full 2r-1 independently checked; zero lambda remains a logical query but performs no cut |
| P05.1 / O01–O09 | `Campaign.variant/inspect_trace`, `minimize_case`, `retain_failure`; independent direct definitions and cardinality-line chain | T14 release tiers below; synthetic missing-zero reducer test; R01 original/fixed reproducer retained |
| P05.2 / O08 | Full truth transformed and re-ranked before comparison; isolate/disjoint union and input-order properties | T15 every base relabeled; 30 smoke and 20 seeded cases each receive isolate/disjoint-edge extensions |
| P05.3 / O05,O06,O11 | Strict warnings; ASan/UBSan; real automatic arbitrary precision; production call-path review | T16 all profiles and M2 regressions; no candidate verifier in solver path |
| P06.1 / O08,O09,O12 | `run_cli`, `solution_json`, `semantic_header`, `solve_stats_json`, `run_solver.main`; canonical results/hash, explicit statuses, separately timed validation | 31 direct + 2 runner CLI invocations per profile; production-only definition-checked run |
| P13.1 / O01–O12 | [Separate code/evidence review](REVIEW.md), accepted log/source hashes and local unoptimized freeze | R01 fixed; final tag/commit provenance recorded after the freeze operation |

The library buffers the requested solution list, and CLI serializes afterward.
It does not implement streaming. `k=q` can terminate as `k_reached`; --all and k>q
finish `exhausted`. No production maximality/compactness verifier or post-hoc result
repair is invoked. Counting emitted cliques populates exact output fields.
Cooperative cancellation preserves available counters; active enumeration/flow
is not interrupted mid-call. Native T_core and T_postload include serialization
and output commit; T_e2e is measured only by the parent runner. External validation
runs after the child exits and has its own timer. No timing enters semantic hashes.

## Actual results

All **35 acceptance commands exit 0** after the R01 fix. Debug, ASan+UBSan,
Release and RelWithDebInfo each build and pass **9/9 CTest**. Standalone independent
pytest: **74 passed**. Production-only Release builds with BUILD_TESTING=OFF and
runs a successful solve; no test/probe/Python discovery is required by that target.
Every compiled translation unit has strict C++17 warnings-as-errors;
ASan+UBSan instrumentation and non-recovery flags are verified in
[compiler flags](compiler_flags.json).

Each CTest profile includes 37 M3 runtime checks plus certificate type assertions;
1,458 M2 primitive assertions, 135 tiny cut/backend runs and a 20,000-node flow path;
31 direct + 2 external-runner M3 CLI invocations; 56 retained M2 CLI invocations;
M3/M2 smoke campaigns; a deterministic synthetic failure reducer; and the same
74 reference tests (not extra independent mathematical coverage).

Both Debug and ASan/UBSan run these M3 tiers with identical case files and
byte-identical decompressed result streams:

| Tier | Base graph/h cases | Distinct base graphs | Explicit oracle requests | Independent chain pairs | Solver runs (auto + BigInt) | Fixed-k prefix requests |
|---|---:|---:|---:|---:|---:|---:|
| Smoke | 30 | 26 | 492 | 47 | 1,200 | 480 |
| Exhaustive-small | 2,198 | 1,099 | 37,825 | 4,140 | 38,480 | 14,844 |
| Seeded | 1,000 | 860 | 16,610 | 1,651 | 19,992 | 7,956 |
| Higher-h | 64 | 60 | 985 | 74 | 1,168 | 456 |

Exhaustive-small contains all labelled graphs n=1..5 at h=2,3. Seed 20260929
has 1,000 distinct graph/h cases n=6..8, 200 each random/planted/bridge/tied/
disconnected. Higher-h includes h=4,5 and h>n. Every base also has an order-reversing
large-original-ID variant; named and first 20 seeded cases add isolate/disjoint
edge variants. Full --all requests number 120 / 4,396 / 2,040 / 128 respectively,
each run under both capacity policies. Prefix counts are requests across variants,
each likewise run twice. Explicit separator requests include both policies;
independent pair counts do not. Tiers overlap: do not add distinct-graph counts.

M3 exhaustive-small solver totals per build: 69,848 logical queries and 50,172
actual cuts. Seeded: 31,514 logical queries and 16,540 cuts. These are campaign totals
with backend/prefix repeats, not a claim about one top-k run or an O(k) bound.
Automatic >128-bit global queries execute actual arbitrary-precision flow:
2,198 exhaustive-small, 1,000 seeded, 64 higher-h and 30 smoke per build.
Forced BigInt solver outputs also agree with automatic outputs throughout.

Full retained M2 tiers run in both builds: exhaustive-small 2,198 cases / 40,591
requests; seed 20260922 1,000 cases / 12,000 requests; higher-h 72 cases / 1,053
requests. The reference, flow and footprint implementations remain unchanged.
All 14 saved campaign probe.stderr files are empty, and no sanitizer diagnostic
or production/reference output mismatch appears in the accepted runs.

[Fixture manifest](fixture_manifest.json) embeds actual per-tier summaries,
seeds, graph/result/log hashes and decompressed-stream hashes. Each cases.jsonl
retains exact original graphs, expected ranks and independent chain; compressed
results retain requests, outputs, traces and counters. [Verification](verification.json)
rechecks 45 accepted source files, all command/campaign hashes and seven
Debug/sanitizer result pairs.

## Review finding, traces and evidence provenance

**R01 (medium, resolved):** moving a global certificate could drain its bound
vectors while leaving its owner pointer valid. Reusing that moved-from object
returned empty on a zero global query. [Original run](token-move-before.json)
exits 1 (`transferred size=2, original size=0`). Immutable const payloads preserve
source validity across moves; [fixed run](token-move-after.json) exits 0 (both 2).
The same rule protects chain points/intervals. The full acceptance campaign was
rerun after this fix. `final/` and dev logs are retained preliminary evidence,
not substituted for `accepted/`. No open review finding remains within this scope.

[Named traces](accepted/build-smoke/named_traces.json) show:
- K4 plus pendant: root lambda 7/5 splits; K4 terminal emits density 3/2;
  right terminal lambda 1 rejects the pendant because it touches X, emitting nothing.
- Two tied edges plus isolate: tied sets [-90,-2] then [5,11], density 1/2;
  isolate [100] emits at zero. Full traversal has 3 logical queries and 2 cuts.
- Outer-breakpoint witness: terminal outer lambda 2 is absent from nonempty
  induced densities; its increment is rejected, rather than assigned that density.

The synthetic reducer test deliberately removes a zero solution and minimizes
to a one-vertex h=2,k=1 case; it is clearly separate from production results.
No solver mismatch triggered automatic production-failure reduction. R01 is an
API-level reproducer retained directly, not an automatically minimized solver case.
Review was a separate pass by the implementing assistant, not human sign-off.

## Environment and executed commands

macOS 15.7.7 arm64; AppleClang 17.0.0.17000603; CMake 4.4.3;
Python 3.12.2; pytest 8.4.2; existing pinned Boost 1.86.0 headers.
No new dependency or benchmark parameter was introduced. Actual environment and
source hashes are in [environment.json](accepted/environment.json).
The full driver ran with the existing virtual environment:

```sh
. .venv/bin/activate
python scripts/run_m3_checks.py evidence/m3/accepted
python evidence/m3/verify_evidence.py --write
```

Driver commands below actually executed; stdout/stderr SHA-256 and UTC start/end
are recorded in [commands.json](accepted/commands.json). R01 compile/run commands
are recorded in the before/after JSON files above. Freeze commands are recorded
separately in RELEASE.json after they execute.

| # | Command | Exit | Logs |
|---|---|---:|---|
| 01 | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 | [stdout](accepted/01.stdout) / [stderr](accepted/01.stderr) |
| 02 | `cmake --build build -j2` | 0 | [stdout](accepted/02.stdout) / [stderr](accepted/02.stderr) |
| 03 | `ctest --test-dir build --output-on-failure -V` | 0 | [stdout](accepted/03.stdout) / [stderr](accepted/03.stderr) |
| 04 | `python validation/solver_campaign.py --probe build/vflhcds_m3_probe --tier smoke --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-smoke` | 0 | [stdout](accepted/04.stdout) / [stderr](accepted/04.stderr) |
| 05 | `python validation/solver_campaign.py --probe build/vflhcds_m3_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-exhaustive-small` | 0 | [stdout](accepted/05.stdout) / [stderr](accepted/05.stderr) |
| 06 | `python validation/solver_campaign.py --probe build/vflhcds_m3_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-seeded` | 0 | [stdout](accepted/06.stdout) / [stderr](accepted/06.stderr) |
| 07 | `python validation/solver_campaign.py --probe build/vflhcds_m3_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-higher-h` | 0 | [stdout](accepted/07.stdout) / [stderr](accepted/07.stderr) |
| 08 | `python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-m2-exhaustive-small` | 0 | [stdout](accepted/08.stdout) / [stderr](accepted/08.stderr) |
| 09 | `python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-m2-seeded` | 0 | [stdout](accepted/09.stdout) / [stderr](accepted/09.stderr) |
| 10 | `python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-m2-higher-h` | 0 | [stdout](accepted/10.stdout) / [stderr](accepted/10.stderr) |
| 11 | `cmake -S . -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DVFLHCDS_ENABLE_SANITIZERS=ON` | 0 | [stdout](accepted/11.stdout) / [stderr](accepted/11.stderr) |
| 12 | `cmake --build build-sanitize -j2` | 0 | [stdout](accepted/12.stdout) / [stderr](accepted/12.stderr) |
| 13 | `ctest --test-dir build-sanitize --output-on-failure -V` | 0 | [stdout](accepted/13.stdout) / [stderr](accepted/13.stderr) |
| 14 | `python validation/solver_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier smoke --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-smoke` | 0 | [stdout](accepted/14.stdout) / [stderr](accepted/14.stderr) |
| 15 | `python validation/solver_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-exhaustive-small` | 0 | [stdout](accepted/15.stdout) / [stderr](accepted/15.stderr) |
| 16 | `python validation/solver_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-seeded` | 0 | [stdout](accepted/16.stdout) / [stderr](accepted/16.stderr) |
| 17 | `python validation/solver_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-higher-h` | 0 | [stdout](accepted/17.stdout) / [stderr](accepted/17.stderr) |
| 18 | `python validation/oracle_campaign.py --probe build-sanitize/vflhcds_m2_probe --tier exhaustive-small --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-m2-exhaustive-small` | 0 | [stdout](accepted/18.stdout) / [stderr](accepted/18.stderr) |
| 19 | `python validation/oracle_campaign.py --probe build-sanitize/vflhcds_m2_probe --tier seeded --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-m2-seeded` | 0 | [stdout](accepted/19.stdout) / [stderr](accepted/19.stderr) |
| 20 | `python validation/oracle_campaign.py --probe build-sanitize/vflhcds_m2_probe --tier higher-h --output /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/build-sanitize-m2-higher-h` | 0 | [stdout](accepted/20.stdout) / [stderr](accepted/20.stderr) |
| 21 | `cmake -S . -B build-release -DCMAKE_BUILD_TYPE=Release` | 0 | [stdout](accepted/21.stdout) / [stderr](accepted/21.stderr) |
| 22 | `cmake --build build-release -j2` | 0 | [stdout](accepted/22.stdout) / [stderr](accepted/22.stderr) |
| 23 | `ctest --test-dir build-release --output-on-failure -V` | 0 | [stdout](accepted/23.stdout) / [stderr](accepted/23.stderr) |
| 24 | `cmake -S . -B build-relwithdebinfo -DCMAKE_BUILD_TYPE=RelWithDebInfo` | 0 | [stdout](accepted/24.stdout) / [stderr](accepted/24.stderr) |
| 25 | `cmake --build build-relwithdebinfo -j2` | 0 | [stdout](accepted/25.stdout) / [stderr](accepted/25.stderr) |
| 26 | `ctest --test-dir build-relwithdebinfo --output-on-failure -V` | 0 | [stdout](accepted/26.stdout) / [stderr](accepted/26.stderr) |
| 27 | `cmake -S . -B build-production -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF` | 0 | [stdout](accepted/27.stdout) / [stderr](accepted/27.stderr) |
| 28 | `cmake --build build-production -j2` | 0 | [stdout](accepted/28.stdout) / [stderr](accepted/28.stderr) |
| 29 | `python -m pytest reference/tests -q` | 0 | [stdout](accepted/29.stdout) / [stderr](accepted/29.stderr) |
| 30 | `python validation/run_solver.py --executable build-production/vflhcds --evidence /Users/nost/Documents/VF-LhCDS/evidence/m3/accepted/cli-definition-run --check-reference -- solve --graph reference/fixtures/bridged_triangles.graph --h 3 --all` | 0 | [stdout](accepted/30.stdout) / [stderr](accepted/30.stderr) |
| 31 | `python scripts/verify_papers.py` | 0 | [stdout](accepted/31.stdout) / [stderr](accepted/31.stderr) |
| 32 | `git diff --check` | 0 | [stdout](accepted/32.stdout) / [stderr](accepted/32.stderr) |
| 33 | `build/vflhcds print-build-info` | 0 | [stdout](accepted/33.stdout) / [stderr](accepted/33.stderr) |
| 34 | `cmake --version` | 0 | [stdout](accepted/34.stdout) / [stderr](accepted/34.stderr) |
| 35 | `c++ --version` | 0 | [stdout](accepted/35.stdout) / [stderr](accepted/35.stderr) |

## Files changed and remaining work

Production: CMakeLists.txt; include/vflhcds/{solver/interval.hpp,solver/solver.hpp,
io/solution.hpp,oracle/closure.hpp,cli/dispatch.hpp}; src/{solver/solver.cpp,
io/solution.cpp,oracle/closure.cpp,cli/dispatch.cpp,cli/main.cpp}.
Tests/tools: tests/m3_solver.cpp, m3_probe.cpp, m3_cli.py, m3_harness.py;
existing tests/skeleton_test.cpp and cli_smoke.py; validation/solver_campaign.py,
run_solver.py; scripts/run_m3_checks.py.
Documentation: README.md, docs/{M3_IMPLEMENTATION.md,BUILD.md,TASKS.md,
CLAIM_TRACEABILITY.md}, solver/oracle/telemetry module READMEs and validation/README.md.
Evidence: evidence/m3/ (plan, review, reports, saved reproducer, command/build/test
logs, graph/result manifests and acceptance/freeze verification helpers).
The complete machine-readable [changed-file manifest](files_changed.json) records
paths and SHA-256, excluding its own recursively unhashable contents.

No unresolved blocking semantic conflict exists. Unrun/deferred: M4 core reduction
and optimizations/T17; M5 external baselines/benchmarks and shared smoke; extended
n<=12 campaigns; GCC/Linux; OS OOM-pressure and signal-delivery stress; TSan and
parallel execution. Cancellation/OOM statuses were tested via controlled injection,
not an OS stress claim. Results establish finite implementation agreement only;
they do not prove the mathematical theorem, scalability or speed superiority.
