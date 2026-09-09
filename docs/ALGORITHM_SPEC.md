# Algorithm Specification: VF-LhCDS

Authority: `papers/veri_free_lhcds_v3_1_submit.md`. Revision: 2026-09-09.
Proof-to-implementation clarifications are in `THEORY_TO_CODE_AUDIT.md`.
They do not silently rewrite the manuscript.

## 1. Domain and output

Input: finite nonempty simple undirected `G=(V,E)`, fixed integer `h>=2`, and
integer `k>=1` (or an explicit `--all` mode). Reject k=0 and invalid h.
All subgraphs are vertex-induced; connectivity uses ordinary graph edges.
Preserve the complete declared vertex universe, including isolates. Canonical
input declares n or a vertex list; raw-data conversion must not invent missing
isolates or drop vertices that occur only in removed loops.

`mu_h(S)` counts each contained h-clique exactly once; `mu_h(empty)=0`.
For nonempty S, `d_h(S)=mu_h(S)/|S|`. S is an LhCDS exactly when it is connected
and maximal among the h-clique `d_h(S)`-compact sets of G (Defs. 1.1-1.3).

Rank by decreasing exact density, then lexicographic order of sorted original-ID
vectors (D006). Original IDs use one declared total order: numeric for canonical
integer IDs; text IDs require a documented deterministic conversion. Return the
first `min(k,q)` sets. `--all` runs to exhaustion. Isolates and zero-density
solutions are not silently filtered. If no h-clique exists (including h>|V|),
the solutions are exactly the ordinary connected components of G, all of density 0.

The default version is fixed-k only. Tie-inclusive output, if later enabled,
finishes the terminal layer containing the kth output.

## 2. Parametric and interval types

```text
Q_lambda(S) = mu_h(S) - lambda*|S|
F_h(lambda) = union of all global maximizers of Q_lambda
ChainInterval = (X,Y,mu_h(X),mu_h(Y)), with X,Y principal-chain sets and X < Y
OracleBounds = (X,Y_oracle), with X subseteq Y_oracle
```

The chain is `empty=B0 < ... < Br=V` (1.11-1.14). A ChainInterval is not merely
any nested pair. The endpoints are immutable during an oracle query.

Provide two explicit API meanings:

1. `largest_restricted(lambda,X,Y_oracle)`: largest maximizer over
   `X subseteq T subseteq Y_oracle`; valid for arbitrary nested bounds.
2. `global_F(lambda,certified_bounds)`: delegates to the restricted primitive,
   and promises global F only with a recorded containment reason.

Allowed global certificates: full `[empty,V]`; original separator bounds from
Lemma 1.15; or the query-local restriction of a certified query using Lemma 1.22.
A runtime subset check is not itself a proof of global containment. The tiny
reference can independently check containment during tests.

Global standalone queries can return empty or equal X. Only separator-generated
queries require strict progress `X proper-subset F_h(lambda) subseteq Y`.
For arbitrary CLI `--x/--y` bounds, label the result `restricted`; do not advertise
it as global without a valid certificate. See audit O05 for the non-strict extension.

## 3. Exact separator and top-k traversal

```text
visit(X,Y):                         # original principal-chain endpoints
    lambda = Fraction(mu(Y)-mu(X), |Y|-|X|)
    Y_oracle = Y                   # minimum correct version
    if safe_core and lambda > 0:
        Y_oracle = Y intersect core_ceil(lambda)(G)
    Z = global_F(lambda, certified bounds [X,Y_oracle])
    require X proper-subset Z subseteq Y
    if Z == Y:                     # NEVER compare with Y_oracle here
        accepted = []
        for W in connected_components(G[Y\X]):
            if E(W,X) is empty:
                accepted.append(W)
        sort accepted by original-ID subset order
        emit accepted one by one; stop immediately after k outputs in fixed-k mode
    else:
        visit(X,Z)
        if output limit not reached:
            visit(Z,Y)

start with visit(empty,V)
```

An explicit stack pushes right before left. Do not eagerly query the right child
before left processing finishes. Termination and output order follow 1.15-1.17.
Every nonterminal split shrinks both intervals. Empty terminal output is valid:
some layers extend/merge older structure without creating a new leaf.

At a terminal pair, only the components accepted by `E(W,X)=empty` are guaranteed
to have density lambda. Rejected increment components need not have that density.
Compute connectivity and anti-adjacency in the original graph, against all of X.
No deletion-subset/self-denseness/maximality verifier is used by this solver.

## 4. Restricted closure primitive

Require exact reduced `lambda=a/b`, `a>=0`, `b>0`, and `X subseteq Y_oracle`.
Let `N=|Y_oracle\X|`.

If N=0, return X. If a=0, return Y_oracle without a cut. In a certified global
zero-lambda query, `F_h(0)=V` forces `Y_oracle=V`. A zero query with a smaller
uncertified upper bound returns a restricted, not global, optimum.

For positive a and N, enumerate every clique C contained in Y_oracle but not X.
Aggregate nonempty residual footprints `R=C\X` with multiplicity w(R):

```text
mu_h(X union S)-mu_h(X) = sum_R w(R)*1[R subseteq S],  S subseteq Y_oracle\X
```

Cliques crossing the boundary of X are included. Do not enumerate only within
`Y_oracle\X`. Empty footprint records are never stored.

Set `L=N+1` and construct the theorem's network:

```text
s -> p_R       capacity L*b*w(R)
p_R -> v       capacity M_inf, for each v in R
v -> t         capacity L*a-1
M_inf = 1 + sum_R L*b*w(R) + N*(L*a-1)
```

All interval vertices are represented, even when they have no footprint incidence.
Run exact max flow and take interval vertices reachable from s in the residual
graph. Return their union with X.

The induced closure weight is:

```text
W(S) = L*(b*(mu_h(X union S)-mu_h(X))-a*|S|) + |S|.
```

The primary value is integral, and `L>N`; the secondary term maximizes cardinality
among primary maximizers. Union closure then selects the unique inclusion-wise
largest set. This is NOT lexicographic vertex-ID ordering; that is a separate
output-order rule. Arbitrary min-cut tie handling or a floating epsilon is invalid.

## 5. Numeric contract

Counts, lambda numerators/denominators, objective values, and all semantic
comparisons are exact. Objective comparisons can be negative: do not subtract
unsigned values without a signed/big-integer representation or safe comparison.

D005 requires a real automatic arbitrary-precision path, not only an interface.
Perform exact preflight bounds before selecting the checked unsigned-128 flow
backend. At a positive query, with `W_total=sum_R w(R)`, check at least:

```text
source_total = (N+1)*b*W_total
sink_total   = N*((N+1)*a-1)
M_inf        = 1+source_total+sink_total
```

Check every product/sum and any larger implementation accumulator. Count and
fraction arithmetic must also remain exact before the network is allocated.
For recursive queries, `a<=binom(n,h)`, `b<=n`, `N<=n` provide conservative bounds;
arbitrary standalone rationals need their actual exact values checked.

If unsafe for fixed width, choose arbitrary precision before construction or
restart safely from exact data. Test this dispatch with deliberately oversized
standalone rational parameters, without needing an impossibly large graph.
Never silently round, wrap, saturate infinity, or publish partial results as exact
completion. OOM/resource-limit is an explicit run status, not an alternate answer.

## 6. Query-local safe core restriction

For positive `lambda_0<=lambda`, Lemma 1.22 gives:

```text
F_h(lambda) subseteq core_ceil(lambda)(G) subseteq core_ceil(lambda_0)(G)
Y_oracle = Y intersect core_ceil(lambda_0)(G)
```

Use `lambda_0=lambda` initially; no heuristic threshold estimation is needed.
The certified original query and this containment establish
`X proper-subset F_h(lambda) subseteq Y_oracle subseteq Y`.
Compute N,L,footprints and capacities using Y_oracle, but retain the original
lambda, chain endpoints, terminal comparison and extraction graph.

Y_oracle need not belong to the principal chain. Shrinking the graph globally or
permanently deleting its complement would lose lower-density/zero-density results.
A cached higher-threshold core cannot be reused for a lower query without a proof.
Peeling uses current h-clique degrees and invalidates each clique once; ordinary
vertex degree is a substitute only at h=2.

## 7. Counts, caches, and telemetry

Reuse stored endpoint `mu_h` values. Canonical set equality is exact, not hash-only.
All cache keys include graph identity, h, bounds and lambda as applicable.

Distinguish:
- `logical_interval_queries`: one per visited recursion node, including lambda=0;
- `mincut_calls`: actual positive-network flow executions;
- `global_oracle_cache_hits`, if a later cache exists;
- original interval size and reduced oracle size.

An unmodified complete traversal makes exactly `2r-1` logical queries (1.18).
It may make fewer cuts. A partial top-k traversal has no proven O(k) call bound.
Network telemetry reports logical forward arcs separately from residual arcs:
`N+P+2` nodes and at most `N+(h+1)P` forward arcs (1.20).

## 8. Scope boundary

The first implementation has materialized clique storage and fixed-k output only.
Optional backends/features are tested only once implemented; they do not block the
minimum correctness milestone. Exact theoretical solvability for fixed h is not
a practical scalability promise or a proof of an unimplemented optimization.
