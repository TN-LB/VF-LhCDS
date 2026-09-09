# Correctness and Validation Plan

## 1. Validation philosophy

The implementation needs two independent correctness anchors:

1. **Definition-level truth:** exhaustive checking of h-clique compactness and maximality on tiny graphs.
2. **Parametric truth:** exhaustive maximization of `Q_lambda(S)` over all subsets to validate `F_h(lambda)` and the closure network.

The production solver is accepted only when both anchors agree with it. Matching another implementation or baseline is useful evidence, but it is not a substitute for definition-level truth.

## 2. Exhaustive reference model

For a graph with `n` small enough, represent each subset by a bit mask.

### 2.1 Clique enumeration

Enumerate every `h`-subset of vertices and retain it iff all pairwise edges exist. Store each clique as a bit mask.

Then:

```text
mu_h(S) = number of clique masks C with C subseteq S.
```

### 2.2 Connectivity

A nonempty subset is connected iff a BFS/DFS in the ordinary induced graph reaches all selected vertices. A singleton is connected.

### 2.3 Compactness

For exact `lambda=a/b`, `S` is h-clique lambda-compact iff connected and, for every `U subseteq S`:

```text
b * (mu_h(S)-mu_h(S\U)) >= a * |U|.
```

No floating-point division is required.

### 2.4 Definition-level LhCDS

For every connected nonempty `S`:

1. set `lambda=d_h(S)=mu_h(S)/|S|` in reduced form;
2. verify `S` is h-clique lambda-compact;
3. verify there is no proper superset `T` of `S` that is h-clique lambda-compact.

If all conditions hold, `S` is an LhCDS.

The maximality check must inspect all supersets in the reference implementation. Do not reduce it to only one-vertex extensions unless a separate proof is encoded.

### 2.5 Exhaustive `F_h(lambda)`

For every subset `S`, compare exact values using:

```text
b*mu_h(S) - a*|S|.
```

Collect all maximizers, take their union, and assert that the union is itself a maximizer. Return that union as the inclusion-wise largest maximizer.

This implementation is intentionally different from the closure network.

## 3. Test layers

### Layer A — deterministic unit tests

#### Graph and set utilities

- duplicate edges and reversed duplicates collapse correctly;
- self-loops are removed;
- original-ID mapping round-trips;
- connected components over an induced set are correct;
- set difference, union, subset, equality, hashing, and serialization are canonical.

#### Exact arithmetic

- gcd reduction;
- fraction equality and ordering;
- cross multiplication near numeric limits;
- checked addition and multiplication report overflow;
- decimal rendering of 128-bit values.

#### Clique enumeration

- empty graph, path, cycle, complete graph, complete bipartite graph;
- known triangle and 4-clique counts;
- production clique tuples equal combination brute force;
- every stored clique has sorted unique vertices and all edges;
- incidence counts sum to `h*|Psi_h|`.

#### Flow

- textbook small max-flow networks;
- multiple minimum cuts;
- zero-capacity edges if supported;
- capacities larger than 64-bit but within production type;
- residual source-side extraction.

### Layer B — residual-footprint identity

For each tiny graph, each nested pair `X subseteq Y`, and every `S subseteq Y\X`:

```text
mu_h(X union S)-mu_h(X)
== sum_R w(R)*indicator[R subseteq S].
```

Also assert:

- every footprint is nonempty;
- every footprint lies in `Y\X`;
- `sum_R w(R) = mu_h(Y)-mu_h(X)`;
- aggregating identical footprints is order independent.

### Layer C — closure oracle differential tests

Generate valid requests and compare production oracle output with exhaustive `F_h(lambda)`.

#### Request generation

1. Global queries: `X=empty`, `Y=V`.
2. Chain-derived intervals: enumerate distinct exhaustive `F_h` sets and use nested pairs.
3. Arbitrary valid bounding intervals: choose `X subseteq F_h(lambda) subseteq Y`.
4. Reduced-core intervals after the optimization is implemented.

#### Lambda set

Include:

- zero;
- every density `mu_h(S)/|S|` on the graph;
- every outer density between nested exhaustive chain sets;
- rationals just above and below breakpoints where representable;
- random small rationals.

#### Mandatory tie cases

Construct cases where:

- empty and a nonempty set tie;
- two incomparable sets tie and their union is also a maximizer;
- multiple nested sets tie at a breakpoint;
- equal-density disconnected components produce a large union maximizer.

Assert exact equality with the largest maximizer, not merely equal objective value.

### Layer D — divide-and-conquer structural tests

For each exhaustive principal chain:

- distinct `F_h(lambda)` values are nested;
- critical densities are strictly decreasing after duplicate sets are removed;
- separator query returns `Y` for consecutive pairs;
- separator query returns an intermediate chain set for nonconsecutive pairs;
- left interval densities are strictly larger than right interval densities;
- full recursion uses no more than `2r-1` oracle calls when no optional reductions add calls.

### Layer E — terminal extraction tests

For each terminal interval `(X,Y)`:

- compute components of `G[Y\X]`;
- output exactly components with no edge to `X`;
- compare emitted components with definition-level LhCDSes born at that layer;
- verify all emitted components have the layer density;
- verify rejected components are not incorrectly returned at another rank.

Include examples with cross-boundary h-cliques. The extraction condition depends on ordinary edges to `X`, while the oracle must account for all cross-boundary cliques through footprints.

### Layer F — end-to-end differential tests

For each tiny graph and every supported `h`:

1. compute all LhCDSes by definition;
2. sort by exact density and fixed subset order;
3. run production solver for every `k` from `1` through `q+2`;
4. compare exact vertex sets, clique counts, densities, and order.

Also compare fixed-k and tie-inclusive modes.

## 4. Randomized campaign

Suggested initial envelope, adjusted for runtime:

| h | n range | graph probability range | cases per seed batch |
|---|---:|---:|---:|
| 2 | 1–14 | 0.05–0.95 | high |
| 3 | 1–11 | 0.05–0.95 | high |
| 4 | 1–9 | 0.10–0.95 | medium |
| 5 | 1–8 | 0.15–0.95 | medium |

Use several generators, not only Erdos-Renyi:

- uniform random graph;
- planted clique plus sparse background;
- disjoint dense components;
- dense core with sparse attachment;
- chain of components connected by bridges;
- random graph conditioned on at least one h-clique;
- adversarial equal-density duplicate components.

Every case records:

- generator name and parameters;
- seed;
- normalized edge list;
- `h` and all tested `k` values;
- reference and production outputs;
- oracle trace on failure.

## 5. Metamorphic properties

### Vertex relabeling

A permutation of vertex IDs must permute every output set correspondingly and preserve exact densities.

### Disjoint union

For `G=G1 disjoint-union G2`, outputs must be drawn from components according to their exact global density order. No output may mix vertices across components.

### Isolated vertices

Adding isolated vertices must not alter positive-density LhCDSes. It may add zero-density behavior according to the formal definition; encode the expected result from the reference checker rather than assuming it away.

### Duplicate component

Adding an isomorphic disconnected copy creates corresponding tied outputs. Fixed-k truncation follows the deterministic subset order.

### Input edge order

Reordering, reversing, and duplicating edge-list lines must not change normalized output.

### Backend equivalence

Materialized and streaming clique backends, and all exact flow backends, must return identical outputs and oracle sets.

## 6. Failure minimization

When a randomized test fails:

1. save the original reproducer immediately;
2. attempt deterministic edge deletion while preserving the mismatch;
3. attempt vertex deletion and ID compaction;
4. simplify `lambda`, `X`, and `Y` for oracle failures;
5. write the minimized case under `tests/regressions/`;
6. add a named test before fixing the bug.

Never delete a regression fixture after the bug is fixed.

## 7. Sanitizers and static checks

Run on small and medium suites:

- AddressSanitizer;
- UndefinedBehaviorSanitizer;
- compiler warnings at a strict level;
- optional static analyzer on flow and arithmetic modules.

ThreadSanitizer is required before enabling parallel enumeration.

## 8. Correctness release gate

A correctness release candidate is accepted only when:

- all deterministic tests pass;
- the frozen randomized corpus passes with recorded seeds;
- no sanitizer issue remains;
- overflow tests fail closed as designed;
- materialized and streaming backends agree on their shared feasible corpus;
- `CLAIM_TRACEABILITY.md` maps every central theorem-dependent behavior to code and tests;
- a clean build reproduces the same canonical output hashes.
