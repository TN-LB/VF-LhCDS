# M2 exact primitives (P02.1–P03.5)

This records implementation choices under the unchanged mathematical specification,
O01/O05/O06/O11 and D005/D006/D012. It is not a new theory audit. No new proof/spec
conflict was found. See `evidence/m2/REPORT.md` for executed evidence and limitations.

## Ownership and exact data

`Graph` sorts arbitrary-precision signed original IDs numerically, retains their
full explicit universe, maps IDs in both directions and stores sorted adjacency.
`VertexSet` is a sorted unique vector of internal indices, checked by
`Graph::validate_set`; equality compares full vectors. `Membership` is reusable.
`induced_components` traverses ordinary graph edges with a heap-backed queue.
The strict canonical reader rejects loops/duplicates; the separate
`normalize_graph` removes them and records exact counts without dropping vertices.

`MaterializedCliques` enumerates lexicographic combinations and checks all pairs.
It stores each h-clique once and maintains vertex-to-clique incidence. This is the
single simple materialized backend; there is no degeneracy-order optimization,
streaming path or MAX_H. h is exact; h>n returns an empty family. Counts and degrees
use `BigInt` before any flow dispatch. Containers use checked native size indices;
resource failures cannot truncate mathematical IDs or counts.

An immutable `Graph` must outlive its `MaterializedCliques`; an immutable index
must outlive its `ClosureOracle`. Do not assign/mutate either referenced owner
while an index/oracle exists. Certificates must not outlive their originating
oracle. Requests own their bounds and fraction; the oracle reads them through
const references and never changes them.

`BigInt` is Boost.Multiprecision cpp_int with expression templates disabled for
simple value semantics. `Fraction` normalizes gcd, keeps a positive denominator,
compares exact cross products and supports signed objective arithmetic. The oracle
requires nonnegative fractions. `UInt128` is a localized GCC/Clang extension;
checked addition, subtraction, multiplication and conversion throw before overflow.
The SHA-256 routine is a small checksum implementation (modulo-2^32 hash arithmetic,
not semantic graph arithmetic); graph hashes include canonical IDs and isolates.
It is checked against standard vectors and independent Python hashlib.

## Restricted closure and certification

`RestrictedRequest` contains X, Y_oracle and lambda. Both sets must be canonical,
X must be a subset of Y_oracle, and lambda must be nonnegative. Arbitrary valid
bounds always return a result labelled `restricted`, even when accidentally global.
`aggregate_footprints` scans every materialized clique once, retains C subseteq Y,
and groups each nonempty C minus X in an ordered map with exact multiplicity.
Cross-boundary cliques and singleton footprints are included without folding.

`CertifiedGlobalRequest` has a private constructor. The only M2 factory is
`ClosureOracle::full_graph_request`, which fixes X=empty and Y=V. `global_F` also
checks that the certificate belongs to that same oracle. A public enum or a mere
X subseteq Y test cannot certify arbitrary bounds. Chain-separator/core factories
are deferred to M3/M4 validated orchestration. Global F may be empty; X=F and
X=Y are valid restricted requests. There is no separator-specific progress test
inside this general API. N=0 returns X and lambda=0 returns Y without a network.

For positive a,N the network uses exactly L=N+1, source capacities L*b*w,
vertex-to-sink capacities L*a-1 and finite infinity
1 + L*b*total_weight + N*(L*a-1). Residual source reachability gives the added
vertices. Cardinality ties use the L and minus-one terms, never original-ID order.

## Numeric dispatch and flow

All preflight products, sums, node/arc counts and finite infinity are computed in
BigInt. Every original forward capacity is at most finite infinity. For each paired
forward/reverse arc, their residual sum stays equal to its original capacity, so
each residual update stays within that bound. Total flow and the sum of source
capacities are at most the finite-capacity total, strictly below infinity. Thus
infinity<=2^128-1 is sufficient for every capacity and flow accumulator in this
network; all native operations remain checked as a defensive invariant.

`CapacityPolicy::Auto` chooses UInt128 only after that preflight; otherwise it
constructs and executes `Dinic<BigInt>`. `ForceBig` and `ForceUInt128` are C++/test
adapter diagnostics, not CLI parameters. Unsafe forced UInt128 throws before
network construction; it never claims automatic completion. Conservative dispatch
may choose BigInt even when an individual arc would fit, especially with no
footprints. This does not change the returned set.

There is one generic Dinic implementation. BFS constructs levels; explicit path,
bottleneck and current-arc stacks implement blocking flow. Input-length recursion
is absent. Parallel/antiparallel/zero/self-loop arcs have distinct residual pairs.
Each network is single-use: no arcs or second max-flow call after execution.
Generic UInt128 callers must provide a source capacity sum that fits; closure
preflight guarantees this. No saturating infinity, float, alternative algorithm,
core reduction, candidate verification or recursion is present.

## CLI and telemetry

The unchanged version-1 wire contract is now implemented for `inspect-graph` and
`oracle`; `solve` still returns `not_implemented` (M3). Example:

```sh
build/vflhcds inspect-graph --graph reference/fixtures/triangle_and_isolate.graph
build/vflhcds oracle --graph reference/fixtures/triangle_and_isolate.graph --h 3 --lambda 1/3
build/vflhcds oracle --graph reference/fixtures/triangle_and_isolate.graph --h 3 --lambda 0/1 --x reference/fixtures/empty.set --y reference/fixtures/triangle.set
```

The full-graph result is labelled global; the explicit-bounds result is restricted.
Canonical result JSON is separate from stderr status/counters. Graph/IDs/h and
fraction fields remain exact; no floating conversion is used. Output files use an
exclusive sibling temporary and checked flush/close/atomic rename; aliases of any
input (including symlinks and hardlinks) are rejected before output creation.
Implementation currently requires POSIX file operations. Syntax/domains precede
graph access, graph validity precedes bound membership checks.

`QueryStats` reports actual per-query events. Standalone calls leave
logical_interval_queries=0. mincut_calls increments immediately before each actual
Dinic execution, including a positive-lambda network with zero footprints. Zero or
equal-bound shortcuts leave bypassed stages null. For constructed networks,
forward_nodes=N+P+2, forward_arcs=N+P+sum footprint sizes, residual_arcs twice that;
capacity_bit_length measures the largest actual initial forward capacity (sink
capacity alone if P=0, otherwise finite infinity). capacity_backend names the type
actually executed, not the auto policy. No phase timings or solve semantic hashes
are fabricated; those remain P06.1. Failure output retains available query progress.

## Evidence boundary

`tests/m2_probe.cpp` is a test-only persistent adapter, excluded with
BUILD_TESTING=OFF. Its n<=12 all-subset inspection is not production behavior.
`validation/oracle_campaign.py` compares it with the unchanged M1 Python reference,
uses an independent cardinality-line grid, tests arbitrary bounds only against
restricted exhaustive truth, and compares complete largest sets. It retains graph
and query counts separately, all inputs/results, real selected capacity backends,
and failing original/minimized reproducers when a mismatch occurs.

M2 exercises T01 and T04–T09, plus primitive sanitizer checks. It does not complete
solver T10–T16, core T17, an end-to-end correctness freeze, a benchmark or a theorem
proof. No DCLDS or other baseline implementation/technique was consulted/imported.
