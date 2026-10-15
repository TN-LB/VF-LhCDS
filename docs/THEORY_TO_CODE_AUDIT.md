# Theory-to-Code Audit and Proof Obligations

Revision 2026-09-09. Sources below refer to the unchanged
`papers/veri_free_lhcds_v3_1_submit.md`. This document records reasoning obligations;
`CLAIM_TRACEABILITY.md` separately records executed implementation evidence.
Status: obligation specification; accepted M0–M5 evidence is recorded separately
in `CLAIM_TRACEABILITY.md`. M6 observation tooling has finite initial-source
acceptance at `de25116`; M7 has [finite implementation evidence](../evidence/m7/interval-20261015/REPORT.md).
M8 final-host/resource/campaign gates remain planned.

| ID | Source | Obligation / precondition | Observable implementation contract | Tests |
|---|---|---|---|---|
| O01 | Defs. 1.1-1.3 | Connected induced sets; compactness for every deletion subset; maximality against every proper superset | Independent direct-definition truth, preserve vertex universe | T01,T02 |
| O02 | 1.8-1.10 | Connected union preserves compactness; hierarchy leaves are LhCDSes | Do not invent a boundary-clique exclusion assumption | T02,T11,T14 |
| O03 | 1.11-1.14 | All Q maximizers union-closed; largest F, nested chain, exact endpoints | Exhaustive union of maximizers; independent line-envelope chain | T03,T09,T10 |
| O04 | 1.15, Eq. 11-12 | X,Y are principal-chain sets, X<Y | Lambda uses original clique-count difference, including boundary cliques; strict separator progress | T06,T10 |
| O05 | 1.19 proof, Eq. 15 | Restricted optimization on nested bounds; global equality needs certified containment | Separate restricted/global semantics; global empty result allowed | T08,T09 |
| O06 | Eq. 15, 1.19 | Every clique inside oracle upper bound contributes its nonempty footprint exactly once | Aggregate multiplicities; correct implication orientation; L=N+1 cardinality tie term | T06,T07,T09 |
| O07 | 1.16 | Consecutive ORIGINAL chain endpoints | Ordinary induced components; no edge to all of X; equal density only for emitted components | T11,T17 |
| O08 | 1.17 + top-k convention | Left-first traversal; fixed total set order inside a layer | Exact prefix output; no solver-side candidate verification | T12,T15,T16 |
| O09 | 1.18, 1.20 | Full basic traversal and fixed h | Logical queries exactly 2r-1; cuts counted separately; no O(k) or practical-scalability claim | T13 |
| O10 | 1.21-1.22 | Positive certified lower threshold <= current lambda | Change oracle upper bound only; preserve lambda and recursive endpoints | T17 |
| O11 | Engineering refinement of 1.19-1.20; D005 | Machine arithmetic must implement mathematical integers | Checked fast path plus actual automatic arbitrary precision; no silent overflow | T05,T07 |
| O12 | Def. 1.3; experimental evidence | Checking density/connectivity alone does not establish compactness/maximality | Distinct validation evidence levels; test equality is not a proof | T02,T14; experiment smoke |

## Clarification A: the restricted/global oracle boundary (O05)

The manuscript states Theorem 1.19 for `X proper-subset F_h(lambda) subseteq Y`.
That strictness ensures recursion progress; it is stronger than closure needs.
For any `X subseteq Y`, maximize Q over the finite interval `[X,Y]`.
This interval is closed under union/intersection, so the manuscript's
supermodularity argument gives a unique largest restricted maximizer.
For `N>0` and a>0, the same footprint identity and integer domination argument
select it even when it equals X. If N=0, X is the only feasible set. At a=0,
monotonicity plus largest-set ties gives Y. Thus these are explicit API extensions
with the same proof, not a claim that every restricted optimum is global.

If global F lies in `[X,Y]`, the restricted optimum value equals the global value;
every restricted maximizer lies in global F, and F is itself feasible. Therefore
the two largest maximizers coincide. This is the required containment certificate.
In particular, `[empty,V]` supports every nonnegative global lambda, including
values above the maximum density where F is empty. For global lambda=0, Y must
be V. These facts resolve the former conflict between strict oracle prerequisites
and standalone/global test requests.

## Clarification B: independent chain generation (O03)

For each cardinality j, exhaustively compute
`M_j=max{mu_h(S): |S|=j}`, including M_0=0. The global optimum value is the upper
envelope of the n+1 lines `M_j-lambda*j`. All possible nonnegative switches occur
among exact pairwise intersections `(M_j-M_i)/(j-i)`, i<j. Evaluate the exhaustive
subset oracle at all these intersections, at rational midpoints between successive
nonnegative intersections, at 0, and at a sentinel `mu_h(V)+1`.
Deduplicate the resulting sets and order them by containment/size.

This is independent of Lemma 1.15's recursion. It samples all envelope segments
and their tie endpoints. It is not enough to scan `mu_h(S)/|S|`: a later breakpoint
is an outer density and need not be any induced-subgraph density. A concrete
seven-vertex witness is recorded in `review/math_sanity_results.json`.

## Clarification C: why the core upper bound is not a chain endpoint (O10)

Containment from Lemma 1.22 licenses replacing only the feasible search bound.
Lemma 1.15 and Theorem 1.16 still apply to the original chain interval, not the
reduced upper set. The closure scaling L is based on the reduced bound; lambda
and the terminal test are based on the original interval. No proof grants a
recursive role to an arbitrary induced core intersection.

Named witness: h=2, disjoint union of K4 on {0,1,2,3} and a triangle on {4,5,6}
with pendant edge {4,7}. The chain is empty < K4 < V, with breakpoints 3/2 and 1.
At the root lambda=10/8=5/4; the 2-core is {0,...,6}, which is NOT a chain set.
The correct lower-density LhCDS is {4,5,6,7}, not the triangle alone. Treating the
reduced bound as the graph or recursive endpoint can lose vertex 7 and maximality.

## Clarification D: two tie rules and relabeling (O03,O08)

The oracle's secondary objective is maximum CARDINALITY among primary optima,
which yields the largest maximizer. Output ties use the accepted original-ID
lexicographic order. They are different operations.

Graph isomorphisms preserve the complete family of solutions and their densities,
but need not preserve a fixed-k prefix when the kth density has ties: renaming
IDs changes the secondary output order. Test full-family equivariance, then
re-sort transformed truth under the new IDs before testing its prefix.
Two disjoint edges at h=2 with their ID blocks swapped are a four-vertex witness.

## Clarification E: valid zero and rejected-component behavior (O01,O07)

With no h-cliques, every connected set is 0-compact, so maximal ones are exactly
ordinary connected components. Each is an LhCDS of density 0. Preserve isolates.

For h=2, K4 plus one pendant vertex has final increment equal to that vertex.
Its own density is 0, whereas the layer outer density is 1; it is rejected because
it has an edge to the previous chain set. The equal-density conclusion of 1.16
applies only to emitted components, not every increment component.

## Clarification F: quantitative testing is not a proof (O11,O12)

Use the mathematical proof plus code refinement obligations for correctness.
Direct exhaustive checks provide independent finite evidence. Large-run clique
count, density and connectivity checks do not establish maximal compactness.
Likewise, reduced/full equality on tested graphs does not prove a new reduction.

`review/math_sanity.py` is an independent, review-only check of these mathematical
contracts. It uses exhaustive F, not a flow implementation, and must not be cited
as production max-flow, overflow-fallback, sanitizer, or benchmark validation.

## Refinement G: interval-local clique work and observation

D045 selects [M7's refinement](M7_INTERVAL_CLIQUES_PLAN.md), without changing
manuscript semantics. The set/count identities and their elementary arguments
are written there; production implementation and finite tests are recorded in
[the M7 evidence](../evidence/m7/interval-20261015/REPORT.md).
This table extends code obligations, not the theorem numbering in the papers.

| Obligations | Refinement precondition / required argument | Planned checks |
|---|---|---|
| O04/O06 | Stored IDs are exactly C(X,Y), partitioned by containment in certified Z; crossing cliques remain on the right and produce C\Z. Exact child weights equal global aggregation. | T21/T23 |
| O03/O04/O11 | mu(Z)=mu(X)+left partition size is exact; compute it before constructing immutable certified endpoints. Lambda still uses original endpoint counts. | T22/T23/T25 |
| O05/O10 | Local aggregation filters by temporary Y_oracle but ownership remains for original Y; global containment comes from existing certificates, never from a caller-supplied ID list. | T22/T24 |
| O07/O08 | Original-Y terminal test, ordinary original-graph components, adjacency to all X, left-first traversal and fixed-k ties remain unchanged; no candidate verifier. | T23/T24 plus T11/T12/T15/T16 |
| O09 | Local visits are bounded by per-clique visited path depth; include partition, remaining count/core and initialization costs. Logarithmic depth requires an additional balance condition; O(M) extra IDs excludes other memory owners. | T19/T21/T25 |
| O11/O12 | Observation preserves decisions and exact backends; source-matched final diagnostic/control builds, exclusive clocks and separate work units; finite tests and diagnostic associations are not proofs. | T18–T20/T27 |

Any invariant or proof/specification conflict stops the affected local path. Do
not repair the manuscript or hide a discrepancy through output validation.
