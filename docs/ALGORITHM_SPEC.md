# Executable Algorithm Specification for VF-LhCDS

This document translates the theory into implementation contracts. It does not replace the proof file. If this document conflicts with `papers/veri_free_lhcds_v3_1_submit.md`, the proof file wins and this document must be corrected.

## 1. Input and output contract

### Input

- finite undirected simple graph `G=(V,E)`, `V` nonempty;
- integer `h >= 2`;
- integer `k >= 1`;
- optional mode:
  - `fixed-k` default: return the first `min(k,q)` LhCDSes;
  - `include-kth-ties`: finish the terminal layer containing the kth result.

The loader may accept non-simple edge lists, but it must deterministically convert them to a simple graph and report removed self-loops and duplicate undirected edges.

### Output

For each result, serialize:

- rank;
- sorted original vertex IDs;
- `|S|`;
- exact `mu_h(S)`;
- exact density numerator and denominator in reduced form;
- deterministic subset hash;
- birth-layer index if available.

Results are ordered by decreasing exact density and then by a fixed total order on subsets. The default engineering choice is lexicographic order of sorted original vertex-ID vectors; record this in `DECISIONS.md`.

## 2. Core definitions

For `S subseteq V`:

```text
Psi_h(S) = { C subseteq S : |C|=h and G[C] is K_h }
mu_h(S)  = |Psi_h(S)|
d_h(S)   = mu_h(S) / |S|, S nonempty
```

For `U subseteq S`:

```text
Delta_h(U;S) = mu_h(S) - mu_h(S\U)
```

A nonempty `S` is h-clique `lambda`-compact iff:

1. `G[S]` is connected; and
2. `Delta_h(U;S) >= lambda * |U|` for every `U subseteq S`.

An LhCDS is a connected induced subgraph whose vertex set `S` is maximal h-clique `d_h(S)`-compact in `G`.

## 3. Parametric maximizer

For exact rational `lambda >= 0`:

```text
Q_lambda(S) = mu_h(S) - lambda * |S|
F_h(lambda) = inclusion-wise largest maximizer of Q_lambda over S subseteq V
```

The distinct values of `F_h(lambda)` form a nested principal chain as lambda decreases:

```text
empty = B_0 proper-subset B_1 proper-subset ... proper-subset B_r = V.
```

The production algorithm does not need to know `r` in advance.

## 4. Exact separator and recursive solver

For two principal-chain sets `X proper-subset Y`, define:

```text
d_h(Y,X) = (mu_h(Y)-mu_h(X)) / (|Y|-|X|).
```

Let `lambda=d_h(Y,X)` and `Z=F_h(lambda)`.

- If `X,Y` are consecutive chain sets, then `Z=Y`.
- Otherwise, `X proper-subset Z proper-subset Y`.

### Reference pseudocode

```text
solve_interval(X, Y, remaining_k):
    if remaining_k == 0:
        return []

    lambda = reduce_fraction(mu_h(Y)-mu_h(X), |Y|-|X|)
    Z = exact_F_oracle(lambda, X, Y)

    if Z == Y:
        candidates = []
        for W in connected_components(G[Y\X]):
            if no_edge_between(W, X):
                candidates.append(W)
        sort candidates by fixed subset order
        return first candidates permitted by remaining_k/tie mode

    results = solve_interval(X, Z, remaining_k)
    if len(results) < remaining_k:
        results += solve_interval(Z, Y, remaining_k-len(results))
    return results
```

Top-level call:

```text
solve_interval(empty, V, k)
```

The left interval must be processed before the right interval because its layers have strictly larger densities.

An iterative stack implementation is allowed only if it is behaviorally identical. To preserve left-first order, push the right child before the left child.

## 5. Exact interval oracle

### 5.1 Preconditions

The oracle receives:

- reduced `lambda=a/b`, `a>=0`, `b>0`;
- sets `X proper-subset Y` satisfying `X proper-subset F_h(lambda) subseteq Y`;
- `N=|Y\X|`.

For the basic solver, recursive chain intervals provide the precondition. A reduction may shrink `Y` only when separately proved safe.

If `a=0`, return `Y` directly.

### 5.2 Residual footprints

For every h-clique `C` contained in `Y` but not contained in `X`, define:

```text
R = C \ X, where empty != R subseteq Y\X.
```

Aggregate equal residual footprints:

```text
w(R) = number of h-cliques C in Psi_h(Y) with C\X = R.
```

The implementation must satisfy, for every `S subseteq Y\X`:

```text
mu_h(X union S) - mu_h(X)
    = sum over residual footprints R of w(R) * indicator[R subseteq S].
```

This identity is a first-class unit test.

### 5.3 Closure network

Let `L=N+1`. Create:

- source `s`, sink `t`;
- one footprint node `p_R` for every residual footprint with positive weight;
- one vertex node for each `v in Y\X`.

Node weights:

```text
omega(p_R) = L * b * w(R)
omega(v)   = 1 - L * a
```

Closure implications:

```text
p_R -> v for every v in R.
```

Equivalent s-t network:

- `s -> p_R` capacity `L*b*w(R)`;
- `p_R -> v` capacity `M_inf` for every `v in R`;
- `v -> t` capacity `L*a - 1`;

where a safe exact value is:

```text
M_inf = 1 + sum_R L*b*w(R) + N*(L*a-1).
```

All products and sums are checked for overflow before graph construction.

Run a deterministic exact min-cut. Let `S_star` be the interval vertex nodes reachable from `s` in the residual graph after max flow. Return:

```text
F_h(lambda) = X union S_star.
```

### 5.4 Tie semantics

The scaled objective represented by the network is equivalent to:

```text
L*b*(mu_h(X union S)-mu_h(X)-lambda*|S|) + |S|.
```

Because `L=N+1`, the first term dominates every possible cardinality difference. Therefore the oracle first maximizes `Q_lambda` and then maximizes selected cardinality. Since parametric maximizers are union-closed, this selects the unique inclusion-wise largest maximizer.

Do not replace the `+|S|` term with an epsilon float or an arbitrary min-cut tie rule.

## 6. Terminal layer extraction

When `Z=Y`, compute connected components of the induced graph on `Y\X`. For each component `W`, emit it iff:

```text
E(W,X) is empty.
```

Important details:

- Connectivity is ordinary edge connectivity in `G`, not clique adjacency.
- The adjacency test is against all of `X`.
- Components rejected due to an edge to `X` are not candidates requiring later verification; they are internal hierarchy structure.
- Components in the same terminal layer have equal density. Apply the fixed subset order for deterministic fixed-k truncation.

## 7. Safe h-clique-core reduction

For a threshold `t`, the `(t,Psi_h)`-core is the largest induced subgraph in which every vertex belongs to at least `t` h-cliques.

For an oracle query at `lambda`, theory allows restricting to the `ceil(lambda)` h-clique core. In an interval implementation with certified lower bound `lambda_0 <= lambda`, a safe upper set is:

```text
Y_prime = Y intersect core_{ceil(lambda_0),Psi_h}(G)
```

provided the theorem's preconditions are checked and `X subseteq Y_prime` remains true. The optimized oracle must assert:

```text
X proper-subset F_h(lambda) subseteq Y_prime subseteq Y.
```

Keep this optimization disabled until the basic oracle passes exhaustive tests.

## 8. Required exact data types

### Fraction

```text
struct Fraction {
    unsigned integer numerator;
    unsigned integer denominator;  // positive
}
```

Normalize by gcd. Compare using checked cross multiplication or multiprecision integers.

### Counts

`mu_h`, footprint weights, clique degrees, and set sizes are integers. The code must reject an instance if a chosen fixed-width type cannot represent a value; silent wraparound is forbidden.

### Capacities

Recommended production default: checked `unsigned __int128`. Provide decimal formatting utilities. Keep the flow implementation generic enough that a slower multiprecision test backend could be introduced if needed.

## 9. Set and cache semantics

Every set passed to the oracle must be canonical:

- sorted unique internal vertex IDs;
- hash includes graph identity and `h`;
- equality is exact set equality, never hash-only equality.

Useful cache keys:

- `mu_h(S)` by canonical set hash plus collision check;
- oracle result by `(X,Y,a,b,configuration)`;
- membership marker epochs for repeated filtering.

Caches may change performance only, never output.

## 10. Edge cases that require explicit tests

- graph with one vertex;
- graph with no h-cliques;
- disconnected graph;
- isolated vertices;
- complete graph;
- disjoint union of equal-density components;
- multiple maximizers of `Q_lambda` at a breakpoint;
- zero-density terminal layer;
- `h>|V|`;
- `k` larger than the number of LhCDSes;
- many cliques sharing the same residual footprint;
- all residual footprints are singletons;
- `X=empty`, `Y=V`;
- capacity near supported numeric limit.

## 11. Non-goals for the first correct version

Do not include these in the initial correctness milestone:

- approximate clique enumeration;
- sampling;
- floating-point parametric search;
- heuristic candidate verification;
- GPU implementation;
- distributed execution;
- unproved pruning;
- silent fallback to a different objective when memory is exhausted.
