# Correctness and Validation Plan

Revision 2026-09-09. Use direct definitions and independent exhaustive parametric
maximization as separate anchors. Another implementation's output is supporting
evidence, not a replacement for either. Test IDs below are stable task contracts.

## 1. Independent reference

Combination-enumerate cliques; BFS/DFS ordinary connectivity; represent tiny sets
as masks; use exact integers and fractions. A singleton is connected.

```text
compact(S,a/b): connected(S) and
    b*(mu(S)-mu(S\U)) >= a*|U| for EVERY U subseteq S
LhCDS(S): compact(S,d_h(S)) and no proper superset T is compact(T,d_h(S))
F(lambda): enumerate ALL S including empty, maximize b*mu(S)-a*|S|,
           union all maximizers and assert that union is also optimal
```

Maximality quantifies over every proper superset, not only one-vertex extensions.
No reference function may import production clique, closure or traversal code.
A default hard guard `n<=12` prevents accidental exponential work; exceeding it
requires an explicit local test option and is not part of ordinary CI.

The principal-chain reference is mandatory, not optional. Use the independent
cardinality-line construction in audit clarification B. Do not derive the expected
chain by rerunning the proposed recursive solver or only scanning subset densities.

## 2. Named obligations and tests

| ID | Required assertion / witness |
|---|---|
| T01 | Normalization preserves the declared vertex universe, loops/duplicates are handled deterministically, empty input is rejected, singleton and no-clique outputs are exact ordinary components. |
| T02 | Full-superset maximality: at h=3 two triangles joined by one ordinary bridge are jointly 1/3-compact, although extending the first triangle by a single new vertex fails. Direct truth returns the connected six-vertex set. |
| T03 | Independent line-envelope chain includes zero, all true breakpoints and exact midpoint samples; include the outer-density-not-subset-density witness from review results. |
| T04 | C++ clique tuples/counts/incidences equal combination reference; sum of clique degrees is h times clique count. |
| T05 | Exact gcd/comparison, signed objective values, checked near-limit arithmetic and actual automatic multiprecision dispatch; nontrivial large rational queries trigger fallback on a tiny graph. |
| T06 | For every tested nested X,Y and S subseteq Y\X, footprint identity and total weight hold; include boundary-crossing cliques, singleton/repeated footprints, and order independence. |
| T07 | Exact max-flow/min-cut on independently enumerated tiny cuts, multiple cut ties, >64-bit capacities, residual reachability, and both capacity types. |
| T08 | Distinguish restricted/global results; empty global F above all densities; X=F; X=Y; lambda=0 with global Y=V; smaller zero upper bound is labelled restricted; malformed bounds rejected. |
| T09 | Oracle equals the exact LARGEST maximizer, not just the optimal value; test empty/nonempty ties, incomparable tied sets and their union, nested ties and disconnected equal-density sets. |
| T10 | On every tested principal-chain pair, separator returns Y iff consecutive; otherwise X<Z<Y. Arbitrary nested sets are not accepted as certified chain endpoints. |
| T11 | Only ordinary-edge anti-adjacent components of G[Y\X] are emitted; emitted density equals lambda. Include K4 plus pendant vertex, a non-emitting terminal layer, and ordinary bridges with no crossing h-clique. |
| T12 | All fixed-k prefixes for k=1,...,q+2 equal re-ranked direct truth; k=0 rejected; --all equals complete truth; no duplicates; disjoint output sets. |
| T13 | Basic full runs make exactly 2r-1 LOGICAL interval queries; mincut_calls may be smaller, especially at lambda=0. Test measured forward nodes/arcs separately from residual storage. |
| T14 | Seeded end-to-end differentials and deterministic failure reduction save original graph, configuration, exact expectations and minimized reproducer. |
| T15 | Relabel full truth then re-sort before comparing fixed-k prefixes. Test disjoint union, duplicate tied components, added isolates and input-order invariance. |
| T16 | ASan/UBSan, numeric boundary errors, repeated canonical hashes; verify that solver orchestration never invokes a candidate verifier. |
| T17 | Core peeling and restricted/full oracle equality; original lambda/endpoints/terminal comparison remain unchanged. Mandatory non-chain upper-bound witness from audit C; lambda=0 bypass; lower thresholds never reuse an unsafe higher core. |

T17 runs only when core reduction is implemented. Streaming, additional flow
algorithms and tie-inclusive output acquire backend/mode equivalence tests when
implemented; their absence does not block the first correct version.

## 3. Oracle request generation

Global requests always use `[empty,V]` and may return empty. For bounded global
requests, first compute exhaustive global F, then choose `X subseteq F subseteq Y`.
Include equality. Separator-specific tests separately enforce X<F. Uncertified
arbitrary bounds compare against the exhaustive RESTRICTED maximizer instead.

Query parameters include zero, cardinality-line intersections and midpoints,
chain outer densities, and seeded exact rationals. "Just above/below" means an
exact rational between known neighboring breakpoints, never floating epsilon.

A nonnegative exact reduced rational may contain a numerator/denominator beyond
128 bits. Use that to test real fallback without constructing a huge graph.
The failure reducer must preserve the kind of request and its containment
certificate, or reclassify it explicitly as a restricted request.

## 4. Explicit campaign tiers

These are target workloads, not completed results. Record actual coverage and
runtime; do not substitute counts of queries for counts of distinct graphs.

| Tier | Coverage target | Usage |
|---|---|---|
| Smoke | All named deterministic fixtures; every implemented backend; fixed seeds | Every relevant change |
| Exhaustive-small | All labelled simple graphs with 1<=n<=5, h in {2,3}; every k=1,...,q+2; all chain pairs | Correctness release |
| Higher-h | Named h=4,5 fixtures including K_h, boundary cliques and h>n; seeded n<=10 graphs | Correctness release |
| Seeded | 1,000 distinct graph/h cases with n<=10 across random, planted, bridge, tied and disconnected families; at least 10,000 certified or explicitly restricted oracle requests in total | Correctness release |
| Extended | Additional fixed seeds and n<=12 cases, only within recorded budgets | Release extension, not per-commit CI |

Cache reference counts per graph to avoid recomputing truth for every k.
Exhaustive-all-graphs and random graph campaigns are different evidence; report
both. No xfail covering a central semantic obligation passes the release gate.
If a target cannot run under available resources, record the shortfall and keep
the gate open instead of describing it as completed.

## 5. Metamorphic details

**Relabeling:** the full family and densities are equivariant; original-ID-based
fixed-k ties are not necessarily equivariant. Transform complete truth, apply the
new total order and only then take its prefix. A mapped old prefix can differ
legitimately at the kth tie. Two disjoint edges with swapped ID blocks detect this.

**Disjoint union:** the complete solution family is the union of component
families; the global prefix requires exact global sorting. No output mixes
ordinary connected components. Component-wise solver scheduling is a separate
optimization and is not implied by a test of this property.

**Isolates:** positive-density solutions remain; each added isolated vertex is a
new zero-density LhCDS. It may change fixed-k output when k reaches the zero layer.

**Determinism:** compare canonical semantic records (sets/counts/densities/order),
not timing fields, allocation-dependent trace IDs or backend-specific statistics.

## 6. Failure and release protocol

Save failures before minimizing. Attempt deterministic edge/vertex deletion,
then simplify h, bounds and lambda only while retaining the same failure and
valid preconditions. Retain regression fixtures after fixing the bug.

Run ASan/UBSan on applicable small/medium tiers. TSan is required only before
parallel code is enabled. Keep compiler warnings strict; floating-point display
is allowed but no floating-point value may enter a semantic decision.

The M3 gate requires executed core tests, declared finite coverage, no known
mismatch, sanitizer cleanliness, functioning exact fallback and populated
traceability evidence. It does not require performance improvement, baseline
availability, optional modes, or a second clique backend.

## 7. Review-only evidence

`review/math_sanity.py` checks mathematical contracts with exhaustive F and direct
compactness on tiny graphs. It does not implement production max flow, arithmetic
fallback, CLI or sanitizers. Its results support the plan review only; they are not
a substitute for any production acceptance gate above.
