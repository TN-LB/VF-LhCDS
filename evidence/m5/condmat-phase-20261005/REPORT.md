# D032 CA-CondMat phase diagnosis — 2026-10-05

**Diagnosis complete: the run times out during solving.** Parsing takes
0.042061041 s and adjacency index construction 0.1166765 s. Solving starts at
elapsed 0.158885875 s and completes 137 queries/mincuts before the predeclared
60-second guard interrupts it. There is no accepted real output. The instrumented
run establishes phase boundaries, not the exact inner-operation cost of the
historical production timeout. P11.2/P12.1/O12 gain scoped evidence; M5 remains open.

## Scope and preserved versions

The owner's “好” approved the prior recommendation to locate the CA-CondMat
timeout stage. D032, [authorization](accepted/authorization.json),
[configuration](accepted/config.json) and [environment/source pins](accepted/environment.json)
were recorded before native execution. One real h=3,k=5 case, one repetition,
one worker, 60-second native guard, no imposed memory cap, uncontrolled cache
and no added warm-ups/retries were used. Seed is null because this is one
deterministic instrumented call with no randomized schedule; the stopped D031
campaign retains its original seed 20261003 and all its 313 saved files unchanged.

CA-CondMat's normalized artifact retains n=23,133 declared vertices and m=93,439
edges. SHA-256 `5e48ff6e02d4015364788f606f59adb4dafcc4dbdc92ce33a209a4eeb50c8adb`;
the [raw copied graph](accepted/real/graph.txt) has identical bytes to the approved
input. h=3, k=5, adjacency enumeration, core off, sorted footprint scanning and
automatic exact capacities match the failed D031 call.

The existing phase probe previously defaulted to combinations, so blindly reusing
it would have diagnosed a different workload. The diagnostic-only main now
accepts an explicit combinations|adjacency selector (omission retains combinations)
and uses the existing TraceSink callback to flush completed-query indices/counters.
Its stdout serializer is unchanged; stderr is diagnostic JSONL. No callback,
validator, trace branch or new default is added to production. There is no new
dependency, external technique, proof/reference change or parallel execution.

A separate build directory, build-m5-condmat-phase-probe, preserves the old probe
binary. [Probe provenance](accepted/probe-provenance.json) pins the existing
build-m5-adjacency-release/libvflhcds_lib.a, headers, production binary, source,
compiler flags and link command. Only the diagnostic main is compiled; production
is not rebuilt. Probe SHA-256 `195814649870cf88dfd7959a957221954c54d5abfe7c82b070b9b5aef47d1ae9`; linked library SHA-256 `9e37a3547efb11271ca826cbe35a10e327352f42fb15f6798b1a2f069098dbeb`.

## Actual commands and checks

From the repository root, the [recorded driver](command.json) runs:

```sh
.venv/bin/python evidence/m5/condmat-phase-20261005/launch.py
.venv/bin/python evidence/m5/condmat-phase-20261005/verify_evidence.py
git diff --check
```

The wrapper launches run_diagnostic.py once; it executes exactly two separate
[configure/build commands](accepted/build-commands.json):

```sh
.venv/bin/cmake -S experiments/phase_probe -B build-m5-condmat-phase-probe -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS= -DCMAKE_CXX_COMPILER=/usr/bin/c++ -DVF_LIBRARY=/Users/nost/Documents/VF-LhCDS/build-m5-adjacency-release/libvflhcds_lib.a
.venv/bin/cmake --build build-m5-condmat-phase-probe -j2
```

Both exit **0**. The probe matches Release -O3/-DNDEBUG, C++17 and existing strict
warnings including -Werror. Every real/tiny/validator child command, wall/CPU time,
RSS, exit and resource guard is saved in process.json; [commands.json](commands.json)
links the actual command records.

T-PHASE-ADJ passes on **2/2** named fixtures:

| Fixture | n | Outputs | Phase/query-end markers | Result |
|---|---:|---:|---:|---|
| triangle_and_isolate | 4 | 2 | 8 / 3 | Byte-identical production output/counters; independent definition pass; zero-density isolate retained |
| bridged_triangles | 6 | 1 | 8 / 1 | Byte-identical production output/counters; independent definition pass |

The [smoke records](accepted/smoke-results.json) retain four native successes
(two probes, two production children) and two later external definition-validator
successes, all exit 0. The independent reference checks every proper superset;
it does not call production. Marker order, monotonic timestamps and query indices
are checked, and all query counters equal the production status counters.
These finite checks validate this instrumentation, not a mathematical theorem.

## Observed real boundaries and progress

T-PHASE-CM retains one real native timeout. [Raw stderr](accepted/real/stderr.txt),
[result](accepted/real-result.json), [derived observations](observations.json)
and [query timeline](query-timeline.json) expose the saved measurements:

| Boundary | Elapsed time from main entry, seconds |
|---|---:|
| parse begin | 0.000081917 |
| parse end | 0.042142958 |
| index begin | 0.042176958 |
| index end | 0.158853458 |
| solve begin | 0.158885875 |
| query 1 end | 11.393793875 |
| query 2 end | 15.371994208 |
| query 137 end | 59.242462667 |
| solve end / serialization | Not reached before timeout |

Every completed query reports one logical query and one actual mincut. All 137
use uint128 and scan all 173,361 materialized triangles, totaling **23,750,457**
footprint clique visits. Query 1 has 196,496 forward nodes and 716,577 forward
arcs. Later networks can be much smaller: queries 134/136/137 have 12/40/20 nodes
and approximately 0.426/0.426/0.428 s gaps from the preceding completed-query marker.
There is continued progress; no claim of a stuck first query is made.

A gap includes traversal/counting after the previous query, current oracle work,
network construction, flow and marker overhead. It is **not** a standalone flow
or footprint timing. No output-count progress marker is collected. The trace
therefore does not establish how many solutions had been accumulated internally,
how much time remains to finish, or an O(k) bound on query count.

The [native process](accepted/real/process.json) times out with exit **-9**
(signal 9 from the timeout guard), wall **60.00914091710001 s**, user
**59.347137 s**, system **0.329432 s**, peak RSS **150077440 bytes**. Stdout is
empty and external validation is not run. This is an instrumented truncated run;
no partial output is accepted and no OOM is inferred.

The driver exits **1** after **64.193014458 s**, including configure/build and tiny
checks. Its stderr is empty. The verifier exits **0**, and
[verification.json](verification.json) checks all **43** raw inventory entries,
four papers, 23 reference files, 40 production source pins, 13 harness pins,
18 IPPV sources, both binary/provenance pins, the library, old probe binary and
all **313** historical D031 files. No post-timeout native call occurs.

## Source-level interpretation and prepared next step

The measured blocker is solving. Static source inspection also identifies
plausible repeated work: aggregate_footprints scans the entire clique list on
every query, and the sorted path uses includes/set_difference over the query
bounds. MaterializedCliques::count performs another entire-clique scan with
sorted subset tests whenever an endpoint/result count is needed. Clique-visit
counters above cover footprint scanning only, not these additional count scans.
This explains why small closure networks can coexist with nontrivial per-query
gaps, but it is a hypothesis about cost attribution, not a measured percentage.
Large early networks also have genuine network/flow work.

The existing M4 membership footprint mode already has an exact preservation
argument, explicit switch and executed equivalence evidence. The
[concrete next proposal](NEXT_STEP.md) freezes one CA-CondMat h=3,k=5 membership
mode diagnostic at the same 60-second guard, using the same production binary
and no new algorithm code. [Draft config](draft-membership-config.json) remains
non-executable scope=draft and has no native results. Membership does not change
MaterializedCliques::count, so a successful completion or universal speedup is
not assumed. A finer internal profile and a timeout increase are documented
alternatives, not actions already taken.

The current affected path stops at the measured incomplete solver stage under
the owner's stop-on-blocker instruction. No production optimization, new flow
algorithm, changed default, new real mode run, time-limit extension or formal
campaign continuation is performed. No proof/specification conflict was found.

## Environment, changes and unrun work

macOS 15.7.7 arm64, Apple M1 / 16 GiB / eight physical/logical cores, Python 3.12.2,
AppleClang 17.0.0.17000603, existing Boost 1.86.0 and CMake 4.4.3. Platform/host
identity match D031; hardware numbers are its previously measured same-host record,
not a fresh sysctl read. HEAD remains 56229397903813d3509ecb45b178bbde823e357b
with pre-existing M5 changes pinned by content. No dependencies are acquired.

Changed symbols: diagnostic main (enumeration selection and existing completed-query
trace callback); evidence run_diagnostic.main/events/preserved and
verify_evidence.main. Existing mark is called unchanged. Production methods
MaterializedCliques, solve and serializers are called, not edited.

Changed files: experiments/phase_probe/main.cpp and README.md; docs/DECISIONS.md
(D032), docs/TASKS.md, docs/CLAIM_TRACEABILITY.md, experiments/README.md and
evidence/m5/REPORT.md. Added this evidence directory, including authorization,
config/source snapshots/build/process logs, verified observations, report and
proposal. [Complete turn-specific inventory](files_changed.json) records exact
paths/hashes and distinguishes pre-existing repository changes.

Unrun: the proposed membership-mode call, 23 pending formal pilot calls, new
production optimization/benchmark, full CTest/pytest/sanitizer or numeric regression,
additional IPPV runs, DCLDS work and clean-host reproduction. The two tiny
instrumentation checks are the tests actually executed in this continuation.
