# VF-LhCDS Software Architecture

## 1. Two-track design

### Track A: exhaustive reference

Location: `reference/`

Purpose:

- define truth for tiny graphs directly from mathematical definitions;
- validate the exact `F_h(lambda)` oracle independently;
- generate deterministic fixtures and minimized counterexamples.

Recommended language: Python 3, standard library first.

### Track B: production solver

Location: `include/vflhcds/`, `src/`

Purpose:

- exact implementation suitable for real graph experiments;
- modular clique, flow, oracle, recursion, reduction, and telemetry backends;
- deterministic CLI and canonical output.

Recommended language: C++17 or newer with CMake.

## 2. Production module map

```text
io/
  graph_reader.*           Parse, normalize, remap, checksum
  result_writer.*          Canonical JSONL/TSV output

core/
  graph.*                  CSR-like simple undirected graph
  vertex_set.*             Canonical sorted sets and membership markers
  fraction.*               Reduced exact fractions and comparisons
  checked_int.*            Overflow-safe arithmetic and formatting

clique/
  enumerator.*             Fixed-h degeneracy-oriented enumeration
  materialized_index.*     Clique tuples and vertex-to-clique incidence
  streaming_backend.*      Query-local enumeration interface
  clique_core.*            h-clique degree peeling

flow/
  maxflow_interface.*
  dinic128.*               First exact backend
  residual_reachability.*

oracle/
  footprint.*              Canonical residual footprint key
  footprint_aggregator.*
  closure_network.*
  exact_f_oracle.*         F_h(lambda) on interval X,Y

solver/
  mu_cache.*
  interval.*
  terminal_extractor.*
  divide_conquer.*
  topk_order.*

validation/
  output_validator.*       Recompute clique count/density and structure checks
  baseline_normalizer.*

telemetry/
  counters.*
  timers.*
  run_manifest.*

cli/
  main.cpp
```

## 3. Core interfaces

The exact signatures may differ, but responsibilities should remain explicit.

```cpp
struct Fraction {
    UInt numerator;
    UInt denominator;
};

struct CanonicalSubgraph {
    std::vector<VertexId> vertices;
    CliqueCount clique_count;
    Fraction density;
};

class CliqueBackend {
public:
    virtual CliqueCount count_contained(const VertexSet& s) const = 0;
    virtual void for_each_clique_in(
        const VertexSet& y,
        const std::function<void(std::span<const VertexId>)>& fn) const = 0;
    virtual void compute_clique_degrees(
        const VertexSet& s,
        std::vector<CliqueCount>& out) const = 0;
};

struct OracleRequest {
    VertexSet x;
    VertexSet y;
    Fraction lambda;
};

struct OracleStats {
    std::uint64_t cliques_scanned;
    std::uint64_t unique_footprints;
    std::uint64_t closure_nodes;
    std::uint64_t closure_arcs;
    UInt max_capacity;
    double build_seconds;
    double flow_seconds;
};

struct OracleResult {
    VertexSet f;
    OracleStats stats;
};

class ExactFOracle {
public:
    OracleResult solve(const OracleRequest& request);
};

class DivideConquerSolver {
public:
    std::vector<CanonicalSubgraph> solve_top_k(
        const Graph& graph, int h, std::size_t k, OutputMode mode);
};
```

## 4. Graph representation

Use a deterministic simple undirected graph:

- internal IDs `0..n-1`;
- sorted adjacency lists or CSR offsets/neighbors;
- each undirected edge stored twice for adjacency, once in canonical edge list;
- original-to-internal and internal-to-original mapping;
- preprocessing summary and graph checksum.

Required operations:

- adjacency iteration;
- fast edge existence for clique enumeration and anti-adjacency checks;
- induced connected components over a vertex marker;
- degeneracy order/orientation.

For moderate graphs, sorted adjacency plus two-pointer intersections is a strong initial choice. Do not add a global hash table per adjacency list until profiling shows a need.

## 5. Vertex-set representation

Initial recommended representation:

- canonical sorted `std::vector<VertexId>` as ownership format;
- reusable `MembershipMarker` with epoch array for O(1) temporary membership;
- no permanent `n`-bit copy for every recursion node.

This makes equality, serialization, hashing, and subset differences deterministic. Profile before introducing compressed bitsets.

## 6. Clique backends

### 6.1 Materialized backend

Enumerate all h-cliques once and store:

- packed sorted vertex tuples;
- incidence list from vertex to clique IDs;
- per-vertex clique degree.

Advantages:

- fast repeated interval filtering;
- enables exact clique-core peeling;
- straightforward instrumentation.

Risk: memory proportional to `h*|Psi_h|` plus incidence.

### 6.2 Streaming backend

Enumerate h-cliques inside a query's `Y` without storing the global collection.

Advantages:

- lower peak storage when clique count is huge.

Risk:

- repeated enumeration across oracle calls;
- harder incremental clique-core support.

Both backends must produce identical canonical clique tuples on test instances.

## 7. Residual-footprint aggregator

For each clique `C` inside `Y`:

1. test whether all vertices are in `X`; if yes, skip;
2. build sorted `R=C\X`;
3. increment `w(R)`.

Because `|R|<=h`, use a small fixed-capacity key:

```cpp
struct FootprintKey {
    std::uint8_t size;
    std::array<VertexId, MAX_H> vertices;
};
```

If `h` is runtime-unbounded, use an inline-small-vector abstraction or vector key. The supported practical `h` range must be explicit in the CLI and documentation.

A later safe optimization may fold singleton footprints into the corresponding vertex node. It must be derived algebraically and regression-tested before becoming default.

## 8. Flow backend

Start with a self-contained deterministic Dinic implementation using exact unsigned capacity type.

Requirements:

- checked reverse-edge construction;
- no recursion proportional to graph size if stack depth is risky;
- deterministic adjacency insertion order;
- residual source reachability after max flow;
- capacity and total-flow formatting for telemetry;
- unit tests on known cuts and large capacities.

Keep an interface boundary so a push-relabel backend can be added for performance comparison without changing the oracle.

## 9. Solver control flow

The solver owns an interval stack or recursion. Each interval stores:

- canonical `X` and `Y`;
- cached `mu_h(X)` and `mu_h(Y)`;
- optional certified lower threshold for safe core reduction;
- depth and parent query ID for telemetry.

For top-k early stopping, count outputs immediately at terminal intervals. In tie-inclusive mode, remember the kth density and continue only through the same terminal layer.

## 10. CLI design

Suggested command:

```text
vflhcds solve \
  --graph DATASET.txt \
  --h 3 \
  --k 20 \
  --clique-backend materialized \
  --flow-backend dinic128 \
  --core-reduction on \
  --output results.jsonl \
  --manifest run.json
```

Additional commands:

```text
vflhcds inspect-graph ...
vflhcds enumerate-cliques ...
vflhcds oracle --x ... --y ... --lambda a/b ...
vflhcds validate-output ...
vflhcds print-build-info
```

The `oracle` subcommand is especially important for reproducing differential-test failures.

## 11. Canonical result schema

Use JSON Lines or a simple machine-readable format. Example fields:

```json
{
  "rank": 1,
  "h": 3,
  "vertex_count": 17,
  "clique_count": "81",
  "density_num": "81",
  "density_den": "17",
  "vertices": [1, 4, 9],
  "vertex_hash": "...",
  "birth_layer": 2
}
```

Counts are strings if they can exceed JSON's safe integer range.

## 12. Telemetry schema

Per run:

- graph and dataset checksum;
- `n`, `m`, `h`, `k`;
- total h-clique count if known;
- preprocessing, enumeration, solving, validation, total time;
- peak RSS;
- number of oracle calls;
- number of terminal intervals;
- recursion depth;
- total and maximum cliques scanned per oracle;
- total and maximum unique footprints;
- total and maximum closure nodes/arcs;
- total flow time and network build time;
- output latency for each rank;
- configuration switches and code commit.

Per oracle call, write a compact CSV/JSONL row so bottlenecks can be analyzed without rerunning.

## 13. Build profiles

Provide at least:

- `Debug`: assertions, sanitizers optional, no benchmark claims;
- `RelWithDebInfo`: profiling and correctness campaign;
- `Release`: `-O3 -DNDEBUG`, final experiments;
- `Sanitize`: ASan + UBSan on small/medium tests.

Avoid `-ffast-math`; exact decision code should not depend on floating point anyway.
