# Current-source M6/M7 observer

Implementation for P16.1–P16.6 (T18–T20/T27, O09/O11/O12). Executed acceptance
status belongs in [the task ledger](../../docs/TASKS.md), not this usage contract.
This directory does not replace `../fine_profile` or its historical source pins.
Production files remain unchanged: a fail-closed generator creates diagnostic
copies in the build directory. The ordinary target is the uninstrumented control.

The observer is single-threaded and has no algorithm decisions. Its independent
JSONL stream is selected by `VF_PROFILE_OUTPUT`; canonical stdout/stderr retain
the production CLI contract. No observation belongs in a semantic hash.

## Schema 1 and measurement contract

Each event has `schema: "vflhcds.final_profile", version: 1`, a monotonic sequence
number, event type, elapsed nanoseconds, exclusive phase totals and cumulative
integer work counters. Integers are exact JSON integers, parsed without floating
conversion. `finish` is required for complete coverage. A truncated stream has
only committed-event coverage; its last phase marker is not a completed duration.
The final snapshot contains the outer elapsed time and unassigned residual.

Phases distinguish input, enumeration/index, incidence append, clique count,
core initialization/peeling, footprint aggregation, oracle preparation, network
build, maximum flow, cut extraction, terminal extraction, output, observer,
orchestration and cleanup by owner. Cleanup guard pairs straddle declarations:
they enter cleanup immediately before the original object's destructor and leave
immediately afterwards, on normal and exceptional exit. They do not relocate,
clear early, wrap, copy, or replace that object. A returned object's moved-from
local and its caller-owned value are distinct cleanup boundaries.

Count call sites are separator, emitted component and standalone. Membership
vertex tests and sorted comparison operand visits are different units. Sorted
comparators still perform the same integer `<` comparison in the same standard
algorithm; instrumentation only increments a counter. `cliques_scanned` continues
to mean footprint tuple visits. Count visits are measured separately.

Footprint histograms record unique keys H_s and multiplicity W_s by nonzero size;
no array is allocated using arbitrary h. Coverage is the actual post-core query
bound only. No before-core histogram is inferred. Query records carry original
X/Y, Z, exact endpoint counts/lambda, root-zero depth/parent, bound sizes, backend,
shortcuts and counters. Rank snapshots are internal ready events, not streaming
output latency. A query-end snapshot includes terminal extraction and cleanup.

M7 adds `clique_id_setup`, `clique_partition` and `count_reuse` phases, exact
partition ID/membership visits, left/right sizes, swap calls, marker slots and
reused counts. `partition_reuse: true` identifies this coverage; original M6 streams
retain null. `worklist` events record actual ID/frontier sizes and capacities.
Cleanup of the sole ID vector and pending frames is measured together as
`cleanup_clique_worklists`; container-internal reallocation stays in orchestration. Global enumeration/index construction remains before the first rank.
All accepted components of a terminal layer are extracted/sorted before its first
rank, even when fixed-k later stops part-way through the layer.

No diagnostic clock removes instrumentation overhead. Record paired control RSS
and runtime separately. Serialized observer bytes and metadata high-water marks
describe observer volume; they do not claim exact allocator or phase peak RSS.
This tooling's fixtures and timings are development evidence, excluded from M8.
M7 refreshes pins and checks local source equivalence. P18.4 must repeat final
host/build readiness and shared baseline smoke before M8; this local evidence
does not complete that gate.

## Build, validate and regenerate

From the repository root (use the installed CMake/Python paths on your host):

```sh
.venv/bin/cmake -S experiments/final_profile -B build-m7-profile-release -DCMAKE_BUILD_TYPE=Release -DPython3_EXECUTABLE="$PWD/.venv/bin/python"
.venv/bin/cmake --build build-m7-profile-release -j2
.venv/bin/ctest --test-dir build-m7-profile-release --output-on-failure
.venv/bin/python experiments/final_profile/verify_build.py build-m7-profile-release --output /tmp/final-profile-build.json
.venv/bin/python experiments/final_profile/validate.py --build build-m7-profile-release --output evidence/m7/new-profile-release --work-modes global interval-scan interval-reuse
.venv/bin/python experiments/final_profile/reports.py evidence/m7/new-profile-release/bundle.json --output /tmp/final-profile-reports.json
```

`validate.py` requires a new destination, freezes 28 named/family/seeded fixtures
and its schedule before native execution (224 calls for default global;
672 with `--work-modes global interval-scan interval-reuse`), and stops on any failed check.
Each fixture runs core off/safe and k=1/all, with one control and one diagnostic.
Seed 20261014 generates eight of the fixtures. The independent exhaustive reference
checks every expected output, global separator and line-envelope chain; a separate uninstrumented TraceSink adapter supplies
the control query trace. Raw inputs, stdout/stderr, native status, wait4 wall/RSS,
observer events and control trace requests/results are retained. The 30-second
native guard is a development validation limit; memory is uncapped. These tiny,
single-repeat observations do not estimate real-graph performance. The process
wrapper polls every 5 ms, which especially limits small-fixture time ratios.

Repeat the same build/CTest/validation commands in a separate Debug directory with
`-DVFLHCDS_ENABLE_SANITIZERS=ON`. The boundary test deliberately kills its own test
process to verify partial-event coverage, checks controlled cancellation, and runs
a real automatic arbitrary-precision max-flow. CTest also runs existing primitive
and core suites against both libraries. There is no parallel solver or TSan claim.

For a standalone diagnostic use the ordinary production CLI, for example:

```sh
VF_PROFILE_OUTPUT=/tmp/new-events.jsonl build-m7-profile-release/vflhcds_final_profile solve --graph reference/fixtures/triangle_and_isolate.graph --h 3 --all --clique-enumeration adjacency --clique-count membership --footprint-scan membership
```

The observer path must be new and cannot alias graph/set/result paths. Session
startup, final event serialization and filesystem close have an explicit outer
coverage boundary: `finish.elapsed_ns` ends at the final snapshot, before writing
that final record. External wait4 timing covers the entire native process.
`boundary_residual_ns` is the difference between an independently sampled outer
clock and the exclusive bucket snapshot; `unassigned` retains unscope-covered work.
Neither is distributed back over phases. Counter increments/timer transitions
still perturb instrumented phases; `observer` captures explicit trace formatting,
flushing and diagnostic-only scans, not an estimate of all instrumentation cost.

The generated named component-vector temporary has exactly the original range-for
lifetime: construction immediately before the loop, destruction immediately after
it, before accepted-set sorting. Other guards surround existing declarations.
Named owner destruction is separately timed; library-internal temporaries and
container-internal releases remain in the enclosing operation. Moved-from local
results and their caller-owned values are not double-counted.

## Counter inventory and coverage

| Family | Units / sites |
|---|---|
| `count_*` | Calls, whole-index tuple visits, matches, membership vertex tests or sorted-comparison operand visits; totals and `separator_`, `emitted_`, `standalone_` categories |
| `footprint_*` | Aggregation calls; visited/eligible/upper-rejected tuples; nonempty contributions; unique keys; membership tests or sorted operand visits |
| `footprint_core_filtered_tuples` | Tuples in original Y but outside Y_oracle; classification runs in `observer` and its extra tuple visits are named `observer_core_classification_tuples` |
| `core_*` | Calls; initialized logical vertex/clique records; actual incidence visits, invalidations, decrements and removals; whole-index initialization remains visible |
| `network_*` | Node, forward-arc and residual-arc sums and separate maxima; maximum capacity bit length; per-oracle backend and shortcuts stay in `stats` |
| Traversal | Logical queries, internal/terminal/non-output layers, accepted/rejected components, mincuts, outputs, `depth_d` histogram and maximum visited depth |
| `partition_*` / `reused_endpoint_counts` | Actual ID predicate visits, membership tests, left/right totals, swap calls, marker initialization slots and eliminated separator count calls; no core-filtered ID is erased |
| ID/frontier storage | Root initialized slots, actual reserved ID capacity and payload bytes (`sizeof(size_t)` per slot), frame size/capacity peaks; excludes endpoint sets and allocator overhead |
| Enumeration/storage | Appended tuples/incidences, stored and reserved tuple/incidence slots; explicit enumeration/index and incidence-append phases |

Counters with observed no work are zero. Before-core histograms remain null; an unbuilt network's per-query fields are null.
Storage slots are element counts, not allocator bytes. Observer output byte volume,
pending-stack size/capacity and map key counts are recorded; diagnostic RSS still
includes all observer allocations. There is no phase-specific peak RSS measurement.

Report builders include `cost_associations`, `core_cost`, `early_stop` and M7
`local_cliques`, plus paired observer overhead. Local comparisons require strict
output/trace equality and include partition/setup/count costs. Capacity/peak
inventories are reported separately, never summed as suffix work.
They expose unavailable IPPV/diagnostic/full-suffix data instead of inventing it.
Core pairs require strict outputs and original interval trace equality. Stopping
pairs additionally reconcile fixed-k counters against the executed full-run rank
snapshot, before computing suffix work. Rank events already include full-layer
extraction/sorting. The initial snapshot includes root ID setup when the new
worklist event is present; original M6 streams fall back to their index snapshot.
Pending intervals are not an estimate of their unexecuted work.

Bundle schema 1 records a frozen schedule, scope, host, source/observer/binary pins,
unique run IDs, graph/h/k/mode/repeat, outcomes, artifact hashes and process metrics.
All completed and censored rows remain present; missing scheduled IDs are reported.
`--formal` rejects development or unfrozen bundles. This is M6 input validation,
not implementation of M8's actual resource enforcement or preregistration gate.
No IPPV run is required for a development bundle; paired baseline inputs must
identify their pinned source/binary and use the same graph/h/k/host/repeat/suite.

`pack_evidence.py DIRECTORY` losslessly archives runner-created raw directories,
compares every byte before removing the loose copies, then checks byte-equivalent
report regeneration. Report loading supports the hash-checked archive directly,
without extracting paths. Configuration, checks, reports and graph fixtures remain
readable alongside the archive. Preserve earlier attempts and their source manifests.
