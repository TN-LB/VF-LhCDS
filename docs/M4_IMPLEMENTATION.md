# M4 optimization contracts and preservation arguments

Scope P07.1-P07.3/O10/T17 and P08.1, built on the frozen M3 version.
Execution evidence belongs in evidence/m4; this document is an implementation
argument, not a claim that unrun tests passed. No paper or accepted choice changes.

## Exact peeling and containment

For a nonnegative integer t, initialize the active set to original V and each
degree to its materialized h-clique incidence count. Queue vertices of degree<t.
When removing a queued vertex, invalidate each still-active incident clique once;
decrement only its remaining vertices. Queue a vertex once on crossing below t.
The active degree invariant equals the number of fully active incident cliques:
the first removed vertex invalidates a clique, and the active flag prevents every
later removed endpoint from updating it again. All updates are exact; size_t
degrees are bounded by the actual stored clique count and only checked-decremented.
Thresholds and event counters are arbitrary precision.

No qualifying induced vertex set can contain the next removed vertex: if the
qualifying set is contained in the current active set, its incidence degree at
that vertex cannot exceed the current degree<t. Induction preserves every
qualifying set. At termination all remaining degrees are at least t; consequently
the remainder is the unique largest clique core in Definition 1.21. Deterministic
queue/incidence order changes neither this characterization nor original graph.

For a certified request with X subseteq F(lambda) subseteq Y and lambda>0,
Lemma 1.22 gives F(lambda) subseteq core_ceil(lambda)(G). Thus replacing the
search bound by Y_oracle=Y intersect core preserves X subseteq F subseteq Y_oracle.
Every restricted maximizer is global because F remains feasible, and the largest
restricted maximizer equals F (audit A). The core certificate is derived only
inside the global wrapper from an existing sealed full-graph/separator certificate;
arbitrary CLI bounds remain restricted and are never automatically core-pruned.

The oracle computes the ceiling from the exact numerator/denominator. Peeling
starts from the full original index for every query. There is no cache or state
that can reuse a higher-threshold core at a lower threshold. Lambda=0 bypasses
core work and preserves V. The solver keeps original immutable X,Y, endpoint
counts, lambda, Z==Y terminality, children and original ordinary-edge extraction.
Only N,L,footprints and capacities use the smaller query bound. Therefore the
same Z is obtained at each visited interval; by induction every split, terminal
event, ranked output and fixed-k stop agrees with M3.

## One measured P08.1 change: membership footprint scanning

Before production edits, the frozen local workload in
evidence/m4/profile_workload.json was run against the M3 Release library.
The saved profile-before.json records compile and nine process runs. The chosen
bottleneck and measured medians are in profile-selection.json. These diagnostics
do not freeze M5 experimental parameters or imply a large-graph speedup.

The sorted mode retains M3's includes/set_difference scan. The optional membership
mode creates exact membership markers for X and Y_oracle once per aggregation.
For each unchanged materialized clique C, all its vertices are in Y_oracle iff
the sorted includes check would pass. Selecting exactly the members not in X
produces C minus X in the same canonical order, because clique tuples are sorted.
The same ordered map increments the same nonempty keys by one; empty keys are
discarded identically. Scanned count, total multiplicities, ordered footprints,
capacities, residual cut and global set are therefore unchanged. No clique
enumerator, tie rule, cache, flow algorithm or component schedule is changed.

Preconditions are the already-validated canonical sets X subseteq Y_oracle and
immutable materialized tuples. The extra cost is two O(|V|) marker arrays and
their initialization on each call. This overhead is included in timings and RSS;
small calls may regress. The mode remains explicit and the original path remains
available. Full mode combinations must be compared on the same correctness corpus.

## Interfaces and evidence boundaries

Core mode: off (default) or safe. Footprint scan: sorted (default) or membership.
These switches select equivalent computations; result schema, fixed-k semantics,
canonical hashes and exact-capacity policy remain unchanged. Original/reduced
interval sizes are distinct. Core threshold, removed vertices, invalidated cliques,
incidence visits, degree decrements and measured reduction time describe actual
query-local work; bypassed core fields are null. Timing never affects decisions.

The mandatory audit-C fixture is K4 disjoint from a triangle with a pendant.
Its root 2-core is not a chain endpoint; output must retain the pendant in the
later lower-density component. Tests also cover zero/h>n, cascades, threshold
recovery, exact large rationals/fallback, all-subset reference core definitions,
all independent chain pairs, all prefixes, relabeling and clique-boundary effects.
