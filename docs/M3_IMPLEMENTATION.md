# M3 exact fixed-k solver

M3 adds P04.1–P04.4, P05.1–P05.3, P06.1 and P13.1 on the unchanged theory,
accepted decisions and independent reference. M2 graph, clique, exact arithmetic,
footprint and Dinic implementations remain the primitives. There is no core
reduction, new flow/clique backend, parallel execution, baseline or optimization.

## Certified endpoints and intervals

`ChainPoint` and `ChainInterval` are immutable values with private constructors.
`ClosureOracle::root_interval` mints the proved extremes empty and V, with counts
0 and the number of materialized cliques. `global_chain_point` mints a point only
from an actual certified full-graph query. `separate` mints an interior point only
from a valid separator query. Users cannot certify a VertexSet by selecting an enum,
providing a count, passing a mutable OracleResult, or merely checking inclusion.

`chain_interval` accepts two such same-owner points, checks proper inclusion and
preserves their original sets/counts. `separator_request` computes the exact outer
fraction from these stored endpoints, invoking Lemma 1.15's containment guarantee.
`separate` requires X<Z<=Y; this strict rule does not leak into standalone global
or restricted APIs. An oracle, its immutable index and graph must outlive their
chain/certificate values. Do not mutate referenced graph/index owners.

The certificate/bound payload and chain endpoint fields are const. Copy and move
construction retain complete valid source values; assignment cannot replace
fields piecemeal. This also closes the observed moved-from certificate edge case
recorded in the M3 review. Endpoint count reuse is required basic behavior, not a
new oracle cache or semantic optimization.

## Solver and output

`solve` owns a vector stack of intervals, initialized to [empty,V]. Each iteration
enters one logical query, asks the exact certified oracle and compares Z with the
original Y. Nonterminals push the right child before the left so the left is
executed first; the right child is never eagerly queried.

For a terminal pair, ordinary components are computed in original G[Y minus X].
Only components with no ordinary edge to any vertex of X are retained. Empty
terminal output is valid. Retained components are sorted lexicographically by
internal IDs; because internal IDs follow numeric original-ID order, this is
exactly D006. Left-first traversal supplies decreasing exact density across layers.
There is no final repair/re-sort of the complete result family and no production
compactness, maximality, deletion-subset or candidate verifier.

`Solution` stores the complete vertex set, exact clique count and reduced density.
Only emitted components have the theorem's terminal layer density; rejected
increments receive no such assignment. The library appends results one at a time
and returns immediately at k. It buffers the requested result list; the CLI then
serializes it, so this is not a streaming/time-to-first-result implementation.
`--all` and k>q finish with `exhausted`; hitting k returns `k_reached`, including
k=q without an additional query to establish exhaustion. No q is guessed for a
stopped prefix. k is an unbounded positive integer, k=0 is rejected before I/O.

CLI examples (from repository root):

```sh
build/vflhcds solve --graph reference/fixtures/bridged_triangles.graph --h 3 --all
build/vflhcds solve --graph reference/fixtures/triangle_and_isolate.graph --h 3 --k 1 --core-reduction off
build/vflhcds solve --graph reference/fixtures/triangle_and_isolate.graph --h 3 --k 20 --output results.jsonl
```

The version-1 canonical result format remains unchanged: rank, h, vertex_count,
clique_count, density_num, density_den, vertices. SHA-256 covers the canonical
schema/graph/h header and canonical ordered result lines. k, termination mode,
backend and all timing/telemetry are excluded; different requests producing the
same prefix have identical semantic hashes. Atomic output/input-alias safeguards
from M2 are retained. Errors never receive a successful semantic hash.

## Telemetry, timing and cancellation

`SolveStats` increments logical_interval_queries once per interval entry, records
individual QueryStats and sums actual mincut calls and inspected cliques. It also
records cliques_enumerated from the completed initial materialized index. Zero
queries count as logical entries while bypassed network fields remain null. The
standalone oracle's logical counter stays zero. Network sizes and capacity bit
lengths remain per-query values, not meaningless additive totals.

A complete basic traversal has 2r-1 logical entries, where r is the number of
nonempty increments of the independently checked chain. This does not count cuts,
and no O(k) call bound is claimed for stopped runs.

Steady-clock T_postload begins after graph/map loading; T_core begins after the
initial index. Both end after result serialization, successful flush and any file
commit. Native T_e2e is null because only a parent process can measure launch to
successful process completion. `validation/run_solver.py` measures that boundary,
retains native stdout/stderr/exit and input/binary hashes, and optionally runs the
independent all-superset reference AFTER the timed child exits. External validation
has its own duration and evidence label. Nested durations are never added.

The optional C++ stop callback and CLI SIGINT/SIGTERM flag are polled before/after
loading/indexing, between interval queries, before accepting results and before
committing output. A controlled stop returns incomplete, preserving available
query counters. Cancellation is cooperative: an active enumeration or max-flow
call is not interrupted mid-operation. A kill/crash/missing final status remains
incomplete to the external runner, and SIGKILL is not guessed to mean OOM.
Resource-limit/OOM status tests use explicit failure injection and a real oversized
container-index input; they do not claim an OS memory-pressure campaign.

## Validation and freeze boundary

`tests/m3_probe.cpp` is excluded with BUILD_TESTING=OFF. It calls the same production
solver and exposes exact outputs, semantic hashes, query telemetry and read-only
traces. It is limited to n<=12. `validation/solver_campaign.py` compares against
unchanged M1 direct definitions and its independent cardinality-line chain, every
k=1..q+2, certified endpoint pairs, full-truth relabel/re-sort, isolate additions
and disjoint unions. Auto and forced BigInt are compared. A separate M2 campaign
continues to exercise restricted requests, footprints, native numeric limits and
real automatic fallback on oversized rationals.

Failures are saved before deterministic reduction; graph deletion and h/k
simplification retain the same failing check and fixed-k/all request scope.
Separator-bound failures retain their original certified-query context rather
than silently relabelling it. The reducer is exercised with an explicitly synthetic
missing-zero candidate, separately from actual solver agreement evidence.

The review maps executed evidence to O01–O12, leaves O10/T17 for M4 and keeps
experimental portions of O12 for M5. The unoptimized correctness tag freezes a
reviewed implementation and its finite evidence; it does not prove the theorem,
provide human sign-off, or establish practical scalability or speed superiority.
See `evidence/m3/REPORT.md` and `evidence/m3/REVIEW.md` for actual results.
