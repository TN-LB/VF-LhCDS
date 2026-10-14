# VF-LhCDS Software Architecture

Revision 2026-09-09. Initial language baseline: C++17 with CMake; Python standard
library for independent truth. Do not require C++20 `std::span` in a C++17 API.

## 1. Minimal module split

```text
reference/                    Direct definitions, exhaustive F, independent chain
include/vflhcds/, src/
  io/                         Declared-vertex graph reader, canonical result writer
  core/                       Graph, canonical vertex sets, fractions, exact integers
  clique/                     Fixed-h enumerator, materialized tuples/incidence
  flow/                       Dinic<Capacity>, residual reachability
  oracle/                     Footprints, restricted closure, certified global wrapper
  solver/                     ChainInterval, terminal extraction, left-first traversal
  telemetry/                  Logical queries, actual cuts, phase times, run metadata
  cli/                        solve, oracle, inspect-graph, print-build-info
validation/                   External checks, not a solver dependency
```

After M3, add `clique/core` and query-bound reduction for M4. Streaming, further
flow algorithms, component scheduling and parallelism are optional extensions.

## 2. Key interfaces and ownership

The following is an illustrative contract, not compile-ready source:

```cpp
// Callback receives a sorted tuple valid for the duration of the call (C++17).
using CliqueCallback = std::function<void(const std::vector<VertexId>&)>;

struct ChainInterval {
    VertexSet x;
    VertexSet y;                  // original chain endpoint; immutable during query
    ExactCount mu_x;
    ExactCount mu_y;
};

struct RestrictedRequest {
    VertexSet x;
    VertexSet y_oracle;            // search bound, not a recursive endpoint
    ExactFraction lambda;
};

enum class BoundOrigin { FullGraph, ChainSeparator, SafeCoreRestriction };
struct CertifiedGlobalRequest {
    RestrictedRequest request;
    BoundOrigin origin;
    // Record the parent chain query / exact threshold for proof-trace provenance.
};

VertexSet largest_restricted(const RestrictedRequest&);
VertexSet global_F(const CertifiedGlobalRequest&);
```

A certificate constructor is internal to validated orchestration; a caller cannot
make arbitrary bounds certified merely by setting an enum. Debug/test builds
compare global containment with the exhaustive reference on tiny instances.
Untrusted CLI bounds use the restricted interface unless independently certified.

The solver owns chain endpoints and endpoint counts. An oracle may return Z and
statistics, but cannot mutate the caller's lambda or endpoints. External output
validators must not be called to accept/reject candidates inside traversal.

## 3. Data structures

Graph: sorted adjacency/CSR, stable internal IDs, explicit vertex universe,
reversible original-ID map, checksummed canonical edges. Sets: sorted vectors and
reusable membership markers. Equality always checks full sets, not hashes alone.

Materialized cliques and incidence are the only required initial storage backend.
Its exact `count(S)` supports sorted inclusion (default) and a per-call membership
array, selected by the index's `CliqueCounting` constructor argument. Both read
the same immutable tuples and accumulate into `BigInt`; the selected mode applies
to chain-point and output-component counts. See `COUNTING_IMPLEMENTATION.md`.
Its combination builder remains the default; optional adjacency extension builds
the same ordered tuples/incidence IDs using common-neighbor intersections and an
explicit stack. This is one storage backend with two enumeration choices, not a
streaming or parallel backend. See [preservation argument](ENUMERATION_IMPLEMENTATION.md).
Footprint keys have sorted unique IDs and support the declared h range; do not
silently cap arbitrary h through an undocumented MAX_H array. A vector/small-vector
key is adequate initially. Count each original clique once.

Store endpoint `mu_h` directly with intervals. A separate global oracle cache is
not required. Measure before adding repeated-query storage and eviction machinery.

## 4. Exact flow and arithmetic

Implement one deterministic generic Dinic algorithm, with checked unsigned-128
and arbitrary-precision capacity instantiations. Provide a true automatic dispatch
path per D005. Exact counts/fractions and signed objective comparisons must remain
safe before dispatch. Use a documented arbitrary-precision dependency where needed.

All reverse-edge indices, capacities, residual updates, total flow and formatting
are tested. Avoid flow DFS recursion proportional to input size unless protected
by an explicit safe stack strategy. Source reachability is computed after max flow.
Record forward arcs separately from residual arcs.

## 5. Output and timing contracts

Example of a self-consistent output record (a triangle at h=3):

```json
{
  "rank": 1,
  "h": 3,
  "vertex_count": 3,
  "clique_count": "1",
  "density_num": "1",
  "density_den": "3",
  "vertices": [1, 4, 9]
}
```

Counts and large exact numerator/denominator fields are decimal strings. A stable
semantic hash covers graph identity, h, ranked sets, counts and exact densities.
Backend traces and timings are separate, not part of semantic equivalence.

Minimum CLI contract:

```text
vflhcds solve --graph G --h 3 --k 20 --core-reduction off --output results.jsonl
vflhcds solve --graph G --h 3 --all --core-reduction off --output all.jsonl
vflhcds oracle --graph G --h 3 --lambda a/b             # full-graph global query
vflhcds oracle --graph G --h 3 --lambda a/b --x X --y Y # labelled restricted query
```

Default core mode is off until M4 is accepted. Default capacity selection is auto,
not "128-bit or abort". Explicit backend forcing is for diagnostics and must fail
clearly rather than claim successful automatic fallback.

Record logical interval queries, actual mincuts, original/reduced interval size,
cliques scanned, unique footprints, forward nodes/arcs, capacity bit length and
selected backend. Phase timing follows `EXPERIMENT_PLAN.md`; timestamps must not
be confused with mathematical correctness evidence.

## 6. Build/release profiles

Debug, RelWithDebInfo, Release, and ASan+UBSan profiles are required. Performance
claims use a recorded release build. TSan/parallel backends are deferred until
parallel implementation exists. Tests compare reference versus production,
128-bit versus arbitrary precision on their shared domain, and later off/on core.
No second clique backend is needed for the first correctness tag.

## M6 observation and planned M7/M8 extension

D045's [cost observation](M6_DIAGNOSTICS_PLAN.md) is implemented in a separate
source-pinned generated build, accepted at `de25116`. Production files are unchanged;
[tooling and scope](../experiments/final_profile/README.md).
[Interval-local clique work](M7_INTERVAL_CLIQUES_PLAN.md) remains planned.
Keep immutable ChainPoints/ChainIntervals. The planned internal frame
adds a certified range in one root ID permutation, depth and traversal identity.
Disjoint child ranges reference immutable global tuples; temporary core eligibility
does not mutate inherited ranges. Derive exact split counts before minting a new
ChainPoint. Standalone arbitrary restricted requests keep the complete global path.

The proposed work-mode switch is separate from existing inclusion predicates and
core mode. Global remains the default/control. Diagnostic observations have a
separate schema and compile out of the uninstrumented control; semantic hashes
exclude them. Final source alignment, Linux limits and formal result allowlists
are [M8 readiness gates](M8_EXPERIMENT_PLAN.md), not assumptions of the current code.
