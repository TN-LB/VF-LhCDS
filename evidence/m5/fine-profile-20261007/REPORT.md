# Fine phase diagnostic — 2026-10-07

**Repeated clique counting is the dominant measured CA-CondMat cost.** In the
289-query prefix recorded before the 60-second timeout, `MaterializedCliques::count`
takes **57.092156 s** of **59.650414 s** accounted solve time (95.71% of that
prefix). Max-flow takes 0.947874 s. This is a partial profile, not a completed-run
percentage or a speedup claim. M5/P12.1 remain open.

| h=3, k=5 | Fresh production | Instrumented Release | Complete output/counter comparison |
|---|---:|---:|---|
| CA-GrQc | 0.501356 s | 0.522205 s | Strictly equal; 13 queries |
| CA-CondMat | Timeout, 60.006917 s | Timeout, 60.003290 s | Unavailable; diagnostic records 289 queries |

| Exclusive bucket | CA-GrQc complete solve | CA-CondMat recorded prefix |
|---|---:|---:|
| Clique counting | 0.158009 s (32.03%) | 57.092156 s |
| Footprint scan/aggregation | 0.115129 s (23.34%) | 0.869581 s |
| Network construction | 0.110463 s (22.39%) | 0.504516 s |
| Max-flow | 0.082164 s (16.66%) | 0.947874 s |
| All remaining buckets | 0.027515 s (5.58%) | 0.236288 s |
| Accounted total | 0.493280 s | 59.650414 s |

The last CA-CondMat snapshot is at 59.811797 s after process-main entry. Work after
that snapshot is unmeasured. Parsing/indexing take 0.043964/0.117266 s, outside
the solve buckets. The prefix includes 151 count calls and 289 flow calls.
The single CA-GrQc diagnostic/control native-time ratio is 1.0416; it mixes
instrumentation overhead, code layout and ordinary runtime variation. Do not
infer a stable overhead or compare these diagnostic times with IPPV.

The counting implementation still runs sorted `subset(clique, set)` for every
materialized clique. Membership footprint scanning changes a different path.
This explains why shrinking networks alone did not target the now-measured
counting cost. A narrowly scoped exact membership-based count is the next
optimization candidate; it has not been implemented here. The source inspection
and profile support this engineering diagnosis, not a mathematical proof or a
measured benefit from a future change.

## Checks and scope

- Ten fixed native calls: **8 completed, 2 timeout, 0 unrun**, no retries.
- Two tiny fixtures (`bridged_triangles`, `triangle_and_isolate`), each h=3,k=5,
  run in production, diagnostic Release and diagnostic ASan/UBSan: six independent
  definition checks pass; four diagnostic/control output and full-counter checks
  pass. The complete GrQc pair adds two structural checks and one strict match.
- All 289 CondMat query counters equal the corresponding prefixes in **all three**
  historical matching core-off runs (304 total queries each). All three matching
  GrQc histories also agree. No historical timing is reused or pooled; this does
  not supply the missing complete CondMat output comparison.
- Release and Debug ASan/UBSan configure/build succeed with strict warnings;
  diagnostic CTest **1/1 passes in each build**, with no sanitizer diagnostics.
  Python reference/harness/adapter/instrumentation tests: **141 passed in 7.63 s**.
- Verification preserves four paper hashes, 23 reference pins, 40 production
  source pins, production binaries/library and **5,243 historical evidence files**.
  Eighteen native/validator process records verify; the aggregate regenerates
  byte-for-byte. Both timeout children exit -9; drivers, builds, checks and
  aggregation exit 0. `native-completion.json` correctly records `passed: false`
  because both real workloads did not complete.

The fixed diagnostic uses Apple M1, 16 GiB, macOS 15.7.7 arm64, AppleClang
17.0.0.17000603, C++17, Boost 1.86.0 and Python 3.12.2. Native runs are serial,
one worker, 60 seconds each, no imposed memory cap, uncontrolled cache, no
warmups; validators run separately. Order is deterministic, with no random seed.
[Configuration and fixture/graph hashes](config.json), [environment](environment.json),
[binary pins](binaries.json), [source/history pins](preflight.json).

## Changes and execution evidence

Added `experiments/fine_profile/{CMakeLists.txt,profile.hpp,instrument.py,main.cpp,
timer_test.cpp,test_instrument.py,README.md}`. Main new symbols: `vf_profile::Scope`,
`switch_phase`, `snapshot`, `instrument`; generated insertions observe
`MaterializedCliques::count`, `aggregate_footprints`, `restricted_impl` and
`execute`. Production files and semantics remain unchanged. Updated
`docs/{DECISIONS,TASKS,CLAIM_TRACEABILITY}.md` and the M5 status report;
P12.1/O12 gain scoped diagnostic evidence, P14.1 a bounded review and P15.1
local regeneration evidence. No milestone or broader gate is newly completed.

Executed the runner's `freeze`, `build`, `tiny`, `profile`, `aggregate`, `verify`
stages and `check_history.py`. The build stage executes CMake configure/build
(`-j2`) and CTest for both separate diagnostic build directories, followed by
pytest on `reference/tests`, `experiments/test_harness.py`,
`baselines/ippv/test_adapter.py` and the four new instrumentation tests.
[Exact command arguments, exits and log paths](commands.json),
[raw runs](runs), [build flags/generated copies](build), [aggregate](aggregate.json),
[history checks](historical-consistency.json), [verification](verification.json),
[changed-file inventory](files_changed.json).

No new proof/specification conflict. CondMat's complete profile/output comparison
remains unavailable at the fixed limit; cross-campaign timing variation remains
unexplained. No optimization, larger-k/general-h campaign, new IPPV/DCLDS run,
full production CTest/numeric-fallback rerun, clean-machine smoke or release
package was executed. Structural checks and finite equality do not prove
maximality or the mathematical theorem.
