# VF-LhCDS: Proof-Aligned Implementation and Evaluation Plan

Revision: 2026-09-09. This is a plan revision, not an implementation or benchmark result.
The four files under `papers/` are preserved unchanged.

## 1. Deliverable and proof spine

Implement exact fixed-cardinality top-k LhCDS discovery for the finite, nonempty,
simple undirected input graph in Definitions 1.1-1.3. Keep three claims separate:
mathematical correctness, implementation evidence, and measured performance.
Tests support an implementation claim; they do not replace a proof. Faster or
lower-memory execution than a baseline is a hypothesis, not an acceptance gate.

The correctness dependency is:

```text
Definitions 1.1-1.3
  -> hierarchy and leaves (1.8-1.10)
  -> largest parametric maximizer and principal chain (1.11-1.14)
  -> separator + structural leaf extraction + ordering (1.15-1.17)
  -> exact footprint closure oracle (Eq. 15, 1.19)
  -> complete exact solver (1.18, 1.20, 1.23)
  -> optional query-local core restriction (1.21-1.22)
```

Use `ALGORITHM_SPEC.md` for behavior, `THEORY_TO_CODE_AUDIT.md` for proof
obligations, and `CLAIM_TRACEABILITY.md` for implementation evidence. Do not
maintain a second competing set of semantic decisions in prompts.

## 2. Minimal correct version

The first correctness release has exactly one complete clique backend
(materialized), one generic exact Dinic algorithm instantiated for checked
128-bit and arbitrary-precision capacities, one restricted-closure primitive,
one global-oracle wrapper, and one left-first solver. It includes aggregated
footprints and endpoint clique-count reuse from the start.

It preserves all declared vertices, including isolates; supports zero-density
outputs; rejects `k=0`; and uses the existing lexicographic original-ID set order.
It does not require streaming, tie-inclusive output, additional flow algorithms,
component-wise scheduling, parallelism, heuristic seeding, or baseline builds.
These are not prerequisites for validating the proof-to-code path.

## 3. Milestones and acceptance gates

| Milestone | Required deliverable | Gate / recorded evidence | Prompts |
|---|---|---|---|
| M0: contract and skeleton | Confirm the revised contracts; record proof snapshot hashes; create CMake/Python skeleton and a single evidence map | Every central obligation has a source, precondition, test ID, and unambiguous failure behavior; no fabricated build/test success | 00 |
| M1: independent truth | Direct compactness/maximality checker, exhaustive `F_h`, independent line-envelope chain, named counterexamples | Hand fixtures agree; no production imports; exact all-superset maximality; breakpoint and zero-density coverage | 01 |
| M2: exact primitives | Graph/clique infrastructure, exact arithmetic, aggregated footprints, generic Dinic, restricted/global oracle APIs | Independent clique comparisons; exact objective and largest-set equality; genuine multiprecision fallback tested | 02, 03 |
| M3: exact solver and freeze | Left-first traversal, structural extraction, fixed-k output, minimal CLI/telemetry, regression corpus | Direct-definition output agreement, all tested prefixes, `2r-1` logical calls on full tiny runs, no candidate-verification dependency, sanitizers clean | 04, 05, 06, 13 |
| M4: safe optional optimization | First query-local clique-core restriction; then only measured bottleneck fixes | Written equivalence argument + named preconditions + off/on regression + cost measurements, one change at a time | 07, 08 |
| M5: comparison and release | Validated required baselines, frozen experiment configuration, immutable run records, release instructions | Comparable outputs/scopes; reproducible completed and failed runs; conclusions restricted to measured cases | 09, 09b, 10 as applicable, 11, 12, 14, 15 |

M3 is independently releasable. M4 can be skipped if it does not improve the
measured workload. M5 never retroactively changes mathematical semantics.

## 4. The critical implementation obligations

### A. Independent truth, not a second copy of the proposed solver

The direct reference checks every deletion subset and every proper superset.
The exhaustive parametric reference maximizes over all subsets and unions all
maximizers. Its principal chain is constructed from intersections of cardinality
objective lines, not from the production separator recursion. See test `T03`.
Scanning only induced-subgraph densities can miss outer-density breakpoints.

### B. Restricted optimum versus global `F_h`

The closure primitive returns the largest maximizer over `[X,Y_oracle]`.
It equals global `F_h(lambda)` only with certified containment. The public global
query with bounds `[empty,V]` may return empty, even though a solver separator
query guarantees `X proper-subset F_h(lambda)`. Do not impose the solver's strict
progress invariant on all standalone oracle queries.

### C. Preserve recursive endpoints during core restriction

For chain endpoints `(X,Y)`, compute lambda from their original counts and sizes.
Core reduction may replace only the oracle search upper bound by `Y_oracle`.
Never recompute lambda from `Y_oracle`, test terminality against it, extract leaves
from it, or store it as a child chain endpoint. It need not be a chain set.

### D. Exact arithmetic is a complete path

Retain accepted decision D005: use the fast checked backend only when safe;
automatically dispatch to arbitrary-precision exact arithmetic otherwise.
A generic interface or a test-only multiprecision backend is not sufficient.
Overflow checks cover counting, fraction operations, capacities, residual updates,
and total flow. Resource exhaustion is explicit; it is never an approximate answer.

### E. A theorem is not an empirical gate

Record a written argument for each semantic optimization. Test output equality,
but do not call it a proof. Distinguish structural output checking from exhaustive
LhCDS validation, and keep external validators out of the solver's decision path.

## 5. Testing scope and completion evidence

Use the fixed tiers in `CORRECTNESS_TEST_PLAN.md`, rather than the phrases
"many random graphs" or "all feasible graphs". A task is complete only with:

```text
task_id / prerequisite / source obligation
changed code symbols / test IDs
command / environment / seed or fixture manifest / result
remaining limitation / evidence location
```

A passing review-only mathematical script does not complete M1-M3. Production
compilation, max-flow testing, fallback testing, and sanitizer execution remain
separate work. All implementation checkboxes stay open until those commands run.

## 6. Optional optimization order

1. Query-local clique-core restriction from Lemma 1.22, with original endpoints
   intact and `lambda_0=lambda` as the simplest certified threshold.
2. Allocation reuse and footprint construction improvements, if profiling warrants.
3. Singleton folding only with its algebraic weight/sign derivation.
4. Streaming or alternative exact flow algorithms only after memory/time evidence.
5. Component-wise scheduling, parallel enumeration, and tie-inclusive output only
   as separately specified extensions.

Do not require oracle-result caching by default: a basic recursion visits distinct
intervals, so repeated identical query hits are not guaranteed. Endpoint count
reuse is already part of the minimum version.

## 7. Baseline and experiment scope

D012 already records DCLDS as an independent parallel study with substantial
overlap. Preserve that decision and the uploaded snapshot before detailed
comparison; do not reopen ownership as an unresolved question. DCLDS and IPPV
are the primary general-h comparison targets, subject to commit/license/build/
semantic validation. Specialized h=2/h=3 methods are required only for claims
about those respective strata. Unavailable methods receive an explicit exclusion
record; do not block M3 on their source availability or reimplement all of them.

First run a frozen smoke configuration. Expand to the paper suite only after
resource limits, timing boundaries, validation levels, datasets, and parameters
are recorded. A negative performance result still completes a valid experiment.

## 8. Parallelism and risks

M1 and the M2 flow implementation may progress independently after M0; oracle
integration depends on M1 fixtures and the graph/clique foundation. Baseline
metadata/build work and the experiment harness may run in parallel after their
contracts are fixed. M3 needs M1+M2. M4 needs the M3 correctness tag.

Main risks: clique/materialized-network size, incorrect tie semantics, incorrect
core endpoint substitution, numeric overflow, shared reference bugs, incomparable
baseline outputs, and overclaiming practical scalability from a fixed-h polynomial
bound. Each has an explicit contract and test in the linked specifications.
