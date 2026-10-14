# M6 cost diagnostics and work accounting

Status: initial-source tooling accepted 2026-10-15 at `de25116`, P16.1–P16.6.
[Executed evidence and limitations](../evidence/m6/final-profile-20261014/REPORT.md),
[implemented schema and commands](../experiments/final_profile/README.md).
M7 partition events and P18.4 final-source refresh remain pending.
This milestone implements observation
and machine-generated reports for the three questions in the
[execution plan](M6_M8_EXECUTION_PLAN.md). It does not write thesis analysis.

## Source identity and control builds

`experiments/fine_profile/` is pinned to the source **before** the M5 counting
optimization. Preserve it and its evidence. The separate implemented target
`experiments/final_profile/` uses a manifest of exact production, observer,
schema and build hashes. Generate instrumented copies or use compile-time hooks
that disappear from the uninstrumented build; do not silently retarget historical
source anchors. Fail closed on a changed source hash or ambiguous insertion point.

For every accepted diagnostic source version, build a fresh uninstrumented Release
control from the same production source and compiler/flags. Instrumentation may
observe execution but must not affect sets, capacities, arithmetic policy, branch
decisions, traversal, tie order, object lifetimes or result serialization. Output
and semantic trace equality are mandatory. Preserve the actual automatic big-integer
path. Do not introduce a solver-side candidate verifier.

M6 initially targets the current validated code. M7 adds partition/count-reuse
events to the same observer. P18.4 is the mandatory final-source refresh: rebuild
and rerun observation-equivalence checks after the last M7 change, then freeze both
binaries. No profile of a prior source version is attributed to the final solver.

Diagnostic data use a separate versioned JSONL/artifact schema. Existing semantic
hashes exclude timing, observations, backend traces and implementation work counts.
Use integer work counters without silent overflow. Detailed traces and clocks stay
out of the uninstrumented primary comparison. Measure diagnostic overhead with
paired controls; do not subtract an estimated overhead from phase times.

## Exclusive phase accounting

Use a monotonic clock and nested exclusive scopes: a child pauses its parent and
restores it on normal return and exception. Account for destructor work at its actual
lifetime boundary. Keep outer total time plus an explicit unassigned/timer-boundary
residual; do not force phase percentages to sum to 100 by modifying measurements.

| Phase | Implementation boundary and inclusions |
|---|---|
| Input | Graph/set parsing, validation and input conversion inside the native executable; offline normalization is separate |
| Enumeration/index | `MaterializedCliques` construction, enumeration and incidence creation; retain separate subscopes where measurable |
| Clique count | `MaterializedCliques::count`, separating separator-point, emitted-component and standalone-query call sites; includes membership setup and exact accumulation except separately charged cleanup |
| Core | `peel_core`, degree/live-state initialization and intersection with original Y; report preparation, incidence/peeling work and cleanup |
| Footprint aggregation | `aggregate_footprints`: marker setup, tuple eligibility, residual construction, map aggregation and result materialization, with cleanup charged explicitly |
| Interval partition/reuse | M7 root ID allocation, partition membership setup, ID partitioning and exact endpoint-count derivation; distinct from aggregation and full `count` calls |
| Oracle preparation | Bound checks, interval set construction, capacity preflight and numeric dispatch; excludes nested phases |
| Network build | `execute<Capacity>` allocation, local vertex map, node/source/sink/implication arcs and exact capacity conversion |
| Maximum flow | `Dinic<Capacity>::max_flow` only, for either exact capacity domain |
| Cut extraction | Residual reachability, returned vertex reconstruction and sorting; distinct from terminal component extraction |
| Terminal extraction | Ordinary components of original G[Y\X], adjacency-to-X rejection, accepted-set ordering and solution assembly; nested `count` time remains in clique count |
| Cleanup | Network, footprints, temporary query/partition buffers, pending interval frames, result and index destruction, distinguished by resource owner; no double charging to their parent phases |
| Output/observer | Canonical output serialization/hash/write separately from diagnostic trace formatting, flushing and observer storage |
| Other orchestration | Remaining stack/control/set operations; cannot silently absorb missing large phases |

Per-query records carry stable traversal IDs, parent ID, depth, original endpoints
or their canonical identities, exact lambda, oracle bound size, shortcut/terminal
status and numeric backend. Whole-run records include initialization and final
cleanup that are outside individual queries. Buffered observation storage also
consumes memory: report its volume and keep diagnostic RSS separate from control RSS.

On timeout/crash, retain only committed events and explicit partial coverage. Mark
an interrupted active phase incomplete; do not infer a whole-run breakdown from
completed queries. Event sums and phase totals are checked on completed runs.

## Work counters and precise units

The current `cliques_scanned` field counts **footprint tuple visits only**. Keep its
historical meaning; expose a documented alias such as `footprint_clique_visits`
rather than relabeling it as total clique work.

| Counter family | Required fields and meaning |
|---|---|
| Enumeration | Total stored cliques M; tuple/incidence storage size; initial construction time |
| Count functions | `count_calls`, `count_clique_visits`, inclusion-test vertex visits, matches and call-site category; repeated visits count repeatedly, not as distinct cliques |
| Footprints | Calls, input-ID/tuple visits, core-filtered tuples, nonempty residual contributions, total multiplicity, unique keys and vertex membership checks |
| Footprint sizes | For each size s, unique-key histogram H_s and multiplicity-weighted histogram W_s; both before/after core where explicitly measured, never conflated |
| Partition/reuse | Root IDs initialized, IDs tested/moved, left/right sizes, eligible endpoint-count reuses, exact count scans actually executed, active/pending ID ranges and storage capacity |
| Core | Invocation/initialization counts, original/reduced vertices, incidence visits, cliques invalidated and degree decrements; report remaining global work even in interval mode |
| Networks | Per-query forward nodes/arcs, residual arcs, unique footprints, capacity bit length/backend; report sums and maxima separately |
| Traversal | Logical queries, aggregation calls and mincuts separately; internal/terminal intervals; terminal layers emitting zero components; accepted/rejected component counts; outputs emitted |
| Depth/frontier | Root depth zero, maximum visited depth, depth histogram and pending unqueried interval count; non-output layers are terminal nodes, not internal split nodes |
| Prefix work | Cumulative phase/work snapshots at each emitted rank and query completion, plus stop reason and pending worklist sizes |

Histogram checks: sum H_s = unique footprints P; sum W_s = total nonempty
clique contribution weight; sum s*H_s = implication forward arcs. For a materialized
network with N eligible vertices, nodes = N+P+2 and forward arcs = N+P+sum s*H_s.
No network is fabricated for zero/empty shortcuts. Distinguish absent/unobserved
fields from observed zero work. Avoid arrays sized by arbitrary h when h>n.

Do not simply add tuple visits, incidence visits and vertex tests into an unexplained
"total work" scalar. Report each category and pass multiplicity. A total tuple-visit
metric, if supplied, lists exactly the loops included and excludes unlike units.

## Report builders for the three questions

P16.4 implements scripts, not manually transcribed conclusions:

1. **VF versus IPPV:** join matching graph/h/k/host/version outcomes; retain M,
   VF query/mincut counts, sums/maxima of network sizes and the diagnostic phase
   breakdown alongside uninstrumented paired runtime/RSS. Relate footprint visits
   to aggregation calls, not all logical queries. IPPV fields without matching
   instrumentation stay unavailable. Associations across graphs do not establish
   which internal IPPV operation caused a difference.
2. **Core cost:** within identical source/work mode/output scope, compare off/safe
   outputs and original interval traces, core preparation/peeling cost and downstream
   aggregation/build/flow/cleanup changes. RSS is measured for the whole native
   process; phase times cannot be converted into phase peak-memory claims. Core's
   temporary arrays, repeated initialization and whole-index visits must be visible.
3. **Early stopping:** compare fixed-k with the corresponding full run prefix under
   the same mode. Count the full run's suffix after its kth output: queries, cuts,
   footprint/count/partition visits, nodes/arcs, terminal layers and extra extraction.
   Record that full input parsing, global enumeration/incidence construction and
   root ID initialization occur before the first solution in this design. Earlier
   queries/partitions on the prefix also remain necessary. Pending subtree count
   alone does not reveal its future work; only an executed full trace can supply it.

Preparing an unqueried right child's ID range is already incurred partition work.
Likewise, the current solver extracts/sorts all accepted components of a terminal
layer before emitting its kth result; do not label that completed extraction as
saved suffix work. Attribute only operations actually omitted by the fixed-k run.

Rank-ready timestamps are **internal** events. The current CLI buffers results;
these timestamps are not user-visible streaming latency. Compare measured process
times separately from diagnostic full-run suffix times; stopping changes cleanup
and output costs, so suffix time is not an exact prediction of runtime savings.

## Acceptance and task sequence

| Task | Deliverable | Test / obligation |
|---|---|---|
| P16.1 | Phase/counter schema, call-site inventory, final-source/control build protocol | T18, O09/O12 |
| P16.2 | Exclusive observer, actual cleanup boundaries, partial-event handling and compiled-out control | T18/T20, O11/O12 |
| P16.3 | Separate count/footprint/core counters, reserved M7 partition/reuse schema, histograms and depth/non-output/prefix records; P17.6 supplies actual partition events | T19, O09/O12 |
| P16.4 | Three deterministic report builders with input identities and coverage labels | T19/T27, O12 |
| P16.5 | Independent small fixtures and diagnostic/control semantic/trace equivalence; numeric fallback and ASan/UBSan checks | T18–T20 plus T05/T16, O01/O08/O11/O12 |
| P16.6 | Initial source-pinned development diagnostic/control run and reproducible artifacts; explicit final-refresh handoff to P18.4 | T20/T27, O12 |

Use named fixtures for zero-clique/empty shortcuts, split and terminal queries,
non-output layers, tied outputs, core cascades, h>n, exception unwinding and real
arbitrary-precision execution. Add deterministic graph families varying clique
concentration, equal-density regions, ordinary bridges, nested layers and core
peeling cascades. Record generation parameters/seed and measured structure; do
not label a family "balanced" or "deep" without checking its actual traversal.

New tests T18–T20 and report checks in T27 must pass before M6 tooling acceptance.
Known historical diagnostics do not close these tasks. Final optimized-source
profiling remains a separate mandatory P18.4 gate after M7 acceptance.
