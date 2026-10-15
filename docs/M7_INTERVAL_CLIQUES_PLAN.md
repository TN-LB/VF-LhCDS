# M7 interval-local clique propagation and exact count reuse

Status: implemented and validated under D045; P17.1–P17.7 complete.
[Executed source/commands/fixtures/evidence](../evidence/m7/interval-20261015/REPORT.md). This is an implementation refinement of
the unchanged manuscript, not a new output policy or a manuscript revision.
It adds one selected algorithm increment and retains global scanning as a control.
No claim of first publication or comparison with deferred DCLDS follows.

## Set identity and completeness invariant

For original nested chain endpoints X subseteq Y, define

\[
\mathcal C(X,Y)=\{C\in\Psi_h(Y):C\not\subseteq X\}.
\]

Each interval owns exactly one ID for every clique in this set, without duplicates.
The immutable global materialized clique index remains the source of tuple data.
The root (empty,V) contains all IDs. For a certified proper separator X < Z < Y,

\[
\mathcal C(X,Y)=\mathcal C(X,Z)\;\dot\cup\;\mathcal C(Z,Y).
\]

If a parent clique is contained in Z, it is in the left set because it was not
contained in X. Otherwise it is in the right set. Conversely each child member
is a parent member, and the two membership conditions are disjoint. This identity
holds for nested sets; certification that these sets are global chain points is
still obtained only from the existing oracle/separator contracts.

**A clique crossing Z stays in the right interval**, where its footprint is C\Z.
Never discard it merely because it is not wholly inside Y\Z. For example, with
h=3, X=empty, Z={0,1,2}, Y={0,1,2,3}, and triangles {0,1,2} and {1,2,3}, the first
ID goes left and the second goes right, contributing singleton footprint {3} there.
This is a set/footprint fixture; these arbitrary sets are not asserted to be chain
endpoints. End-to-end separator fixtures must obtain Z independently from truth.

The same invariant yields exact endpoint counts:

\[
\mu_h(Y)-\mu_h(X)=|\mathcal C(X,Y)|,\qquad
\mu_h(Z)=\mu_h(X)+|\mathcal C(X,Z)|.
\]

These counts include crossing cliques as specified by the original outer-density
formula. They are not counts of cliques induced by Y\X or Z\X.

## Representation and control modes

Use one root vector of clique IDs and disjoint half-open index ranges for interval
frames. The private internal frame carries the existing immutable `ChainInterval`,
its ID range and depth; the observer derives traversal/parent identity from query order. Tuple storage is never copied. Partition
the active range in place by `C subseteq Z`; children receive its left/right ranges.
Pending siblings occupy disjoint ranges, so their contents must remain untouched.
Do not reserve a full parent-sized vector for every child or retain ancestor copies.

Only internal root creation and validated splitting may construct a worklist frame.
Bind it to its index/oracle and original endpoints; a public vector, enum or caller
assertion cannot certify completeness or global containment. Test invalid ownership,
missing/duplicate/out-of-range IDs through internal test probes. Keep the standalone
arbitrary restricted-oracle API on its existing complete global-index path.

Implemented solve-only CLI option: `--clique-work global|interval-scan|interval-reuse`,
independent of enumeration, footprint, counting and core switches. Global remains
the default; standalone oracle commands retain complete global scanning.

| Mode | Footprint input | New separator-point count | Purpose |
|---|---|---|---|
| global | Complete global clique index each aggregation | Existing exact `index.count(Z)` | Preserved control and default |
| interval-scan | Original interval's complete ID range, filtered by query-local bound | Existing exact `index.count(Z)` | Isolate local scanning/partition effects |
| interval-reuse | Same interval range and partition | mu(X) plus exact left partition size | Isolate additional endpoint-count reuse; proposed optimized experiment mode |

All three modes retain identical mathematical output, original chain intervals,
lambda, traversal and terminal extraction. Keep global as the program default;
M8 opts into the optimized mode explicitly. An internal ID permutation need not
match global tuple iteration order, but footprint keys/weights and canonical
solutions must. Trace comparison uses semantic intervals and counts, not incidental
permutation order or memory addresses.

## Integration sequence

1. Write the preservation argument and T21/T22 tests before changing solver behavior.
   Audit `ChainInterval`, `ClosureOracle::separate/restricted_impl`,
   `aggregate_footprints`, `MaterializedCliques::count` and `solve`.
2. Add private frame/range construction and a local aggregation iterator. Iterate
   every ID in the range, retaining only cliques contained in Y_oracle and using
   residual C\X with the original X. Existing multiplicity aggregation and exact
   network construction are unchanged. Never replace the source index with an
   induced graph or enumerate only cliques of Y\X.
3. Obtain the oracle result Z using the original lambda. Validate existing separator
   invariants. If Z equals original Y, return the stored endpoint without splitting
   or recounting it. Otherwise partition the original parent range into the two
   complete child ranges; interval-scan still computes `index.count(Z)`.
4. Enable interval-reuse: derive mu(Z) from mu(X)+left-size with exact integer
   conversion/accumulation. Refactor the private separator return path as needed
   so the count is available **before minting the immutable ChainPoint**. Do not
   create a temporary point with an invented count and patch it afterward. Debug
   and independent tests compare the derived count with fresh exact truth.
5. Push right then left so the next query remains left-first. Partitioning prepares
   both ID ranges but must not eagerly execute the right child's oracle. Preserve
   zero-clique and lambda-zero shortcuts, exhaustion, k>q and k=0 rejection.
6. Keep emitted-component counts on the existing exact count function in this
   increment. Reusing terminal density to eliminate them would be a separate
   change. Standalone global queries also retain their current count path.
7. Add the safe-core interaction only after core-off local equivalence passes,
   then run the full required compatibility acceptance before M7 completion.

## Query-local core must not become inherited state

The stored range always represents C(X,Y) for **original** endpoints. A safe core
query filters eligible cliques to C subseteq Y_oracle during aggregation only.
It does not mutate or shrink the owned range. After obtaining Z, partition the
entire original range, including cliques excluded from this query's reduced bound.
Children can use lower thresholds and need those cliques again.

Given X subseteq Y_oracle subseteq Y, every clique eligible for the old aggregation
either lies inside X and has empty residual, or appears in C(X,Y). Thus the local
view produces exactly the same nonempty footprint multiset as the global scan.
Its weights, network/capacities, largest restricted/global maximizer and numeric
dispatch are unchanged for the same bounds. This does not provide a new containment
certificate; it consumes the existing safe-core certificate.

Retain original endpoint counts/lambda, terminal comparison Z==original Y, ordinary
components of original G[Y\X] and adjacency tests against all X. Include audit C's
lower-threshold recovery witness; permanently dropping cliques after core filtering
must fail a regression. Core peeling itself remains a whole-index operation here.

## Work and storage analysis to accompany implementation

Let M be total materialized cliques, A the visited queries that actually aggregate,
I the visited proper-split queries and L_j=|C(X_j,Y_j)|. With the current global
scan, footprint tuple visits are M*|A|. Local aggregation visits sum(j in A) L_j;
partitioning adds sum(j in I) L_j ID tests. Record both rather than reporting only
the reduced aggregation number. Counting reuse removes eligible full scans but
does not remove emission counts, standalone counts or global core work.

At each depth the active intervals' clique sets are disjoint. If the maximum
visited depth is D with the root at zero, each clique visits at most one node per
depth, so sum over all visited L_j <= M*(D+1). This bounds each subset sum above;
it does not prove logarithmic depth. Only an independently justified balanced-tree
condition permits D=O(log r). Skewed trees can have D=O(r); no unconditional
O(M log r), O(k) query bound or runtime speedup is claimed.

These are tuple/ID-visit bounds. Membership tests may inspect up to h vertices per
clique; marker initialization, exact arithmetic, map operations, flow and cleanup
are additional costs. Track them with M6. Zero/empty query shortcuts do not perform
aggregation merely to make a formula fit.

One ID permutation uses O(M) additional ID storage; range metadata on the DFS
frontier is O(D+1). Verify actual allocated capacity and peak resident memory, not
just logical list sizes. This statement excludes existing endpoint vertex sets,
the materialized tuples/incidences, networks and observation buffers. Root ID setup
adds work and storage; it does not eliminate initial enumeration. In core-off mode
the root footprint network is unchanged, so no root-network memory reduction is
promised. Early-stop cleanup must release remaining frames without invalid access.

## Acceptance tasks

| Task | Required deliverable | Tests / obligations |
|---|---|---|
| P17.1 | Written set/count identities, core preservation, code preconditions and work/storage bounds | T21/T22, O04/O05/O06/O09/O10/O11 |
| P17.2 | Sealed root/frame ID ranges and complete in-place partition, including crossing cliques | T21/T24, O04/O05/O06 |
| P17.3 | interval-scan aggregation/solver path and global control with identical canonical traces | T21/T23, O04–O08 |
| P17.4 | Exact separator count reuse without weakening ChainPoint certification; emitted counts retained | T22/T23, O03/O04/O11 |
| P17.5 | Query-local safe-core view with original ranges/endpoints preserved | T24 plus T17, O05/O07/O10 |
| P17.6 | CLI/config mode records, M6 partition/reuse telemetry and all-mode differential/sanitizer/numeric acceptance | T19/T23–T25 plus T05/T16, O08/O09/O11/O12 |
| P17.7 | Freeze the validated increment, preservation/traceability records and finite development evidence; hand off final profiling and formal ablations to M8 | T20/T25/T27, O12 |

T21 covers all labelled graphs n<=4, h={2,3}, all nested X subseteq Z subseteq Y,
plus named h=4/5 cases. The three work modes crossed with core off/safe use the
existing M3/M4 exhaustive-small, seeded and higher-h truth tiers in Debug and
ASan/UBSan. Cover sorted/membership footprints and counts and both enumerators in
named/all-subset checks; run capacity boundary and real automatic fallback tests.
Force both exact backends on small separator cases for mode equivalence; retain
T05's genuine automatic fallback on suitable oracle/network requests. Do not
invent huge chain counts to force a tiny separator into fallback or report a
forced-big run as automatic fallback.
Record exact fixture/seed manifests, outputs and mode combinations, not just a
command list. A mismatch retains original/minimized reproducers and blocks the
affected path. No finite agreement is called a proof.

## Implementation preconditions (P17.1, 2026-10-15)

`IntervalTraversal` owns the root permutation and all pending frames. Its public
operation advances the existing left-first traversal; callers cannot insert frames,
supply IDs or change endpoints. It is noncopyable/nonmovable and bound to one
`ClosureOracle` and its immutable index. Frames never escape. A temporary private
`CliqueRange` borrows that permutation only during a query and partition; no view
survives a mutation. An internal test friend may inspect or corrupt ranges to test
rejection, but is not a production certification API. Arbitrary restricted queries
continue through the whole index.

Induction starts with the iota permutation of all materialized IDs. At a proper
certified split the one-pass partition tests each parent ID once, swapping only
inside that range. Membership in Z chooses the left side; every other ID stays on
the right. Thus the partition preserves the parent multiset, disjoint siblings and
all pending ranges. Frames for the right and then left children are created only
after the existing progress checks and exact point-count construction. Terminal
queries do not partition or recount Y. Exceptions invalidate the traversal for
further use; destruction releases its sole permutation and pending frames.

The shared aggregation loop receives either all IDs or the active range. It still
filters against Y_oracle and computes C minus the original X. Range completeness
and X subseteq Y_oracle subseteq Y imply identical nonempty weighted footprints.
Core peeling remains whole-index work; it never partitions or erases inherited
IDs. The exact arithmetic/network and largest-set tie mechanism are unchanged.
Count reuse converts the left size to BigInt before adding mu(X); the oracle mints
the immutable point only afterward. Neither cardinality arithmetic nor a worklist
is allowed to certify an arbitrary global point.

T21/T22 tests compare arbitrary nested-set partitions and footprint multisets;
they do not use those sets as chain certificates. T23 independently checks actual
separator chains and outputs. T24 retains the pendant recovery witness. T25 checks
foreign ownership, malformed IDs, capacity/frontier lifetimes, early stop,
cancellation, exceptions and both exact numeric backends. These finite checks
support implementation validation, not a proof of the manuscript.
