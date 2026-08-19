# Prompt 04 — Exact Left-First Divide-and-Conquer Top-k Solver

## Goal

Build the complete verification-free top-k LhCDS solver around the already validated exact `F_h(lambda)` oracle.

## Context to read

- `AGENTS.md`
- `docs/ALGORITHM_SPEC.md`
- `docs/ARCHITECTURE.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- `docs/THEORY_TO_CODE_AUDIT.md`
- Lemma 1.15, Theorems 1.16–1.17, and Corollary 1.18 in `papers/veri_free_lhcds_v3_1_submit.md`
- validated reference and closure-oracle tests

## Deliverables

1. Solver API accepting normalized graph, fixed `h`, `k`, and deterministic subset-order policy.
2. Exact interval density:
   `lambda = (mu_h(Y)-mu_h(X)) / (|Y|-|X|)`.
3. Recursive or explicit-stack traversal with invariant `X subsetneq F_h(lambda) subseteq Y`.
4. Exact control flow:
   - query `Z=F_h(lambda)`;
   - if `Z != Y`, process `(X,Z)` first, then `(Z,Y)`;
   - if `Z == Y`, enumerate connected components of `G[Y\X]` and emit only those with no ordinary edge to `X`.
5. Early stopping after `min(k,q)` outputs, while preserving deterministic order within a layer.
6. Correct handling of:
   - `k=0` if the public CLI permits it;
   - `k>q`;
   - equal-density outputs in one layer;
   - disconnected input;
   - isolated vertices and zero-clique layers according to approved decisions;
   - `lambda=0`;
   - recursion-depth safety, preferably through an explicit stack.
7. Canonical output records with exact density numerator/denominator, clique count, size, sorted original IDs, layer/trace metadata, and stable output hash.
8. Optional debug trace of interval calls, lambdas, returned `Z`, and terminal emissions.

## Correctness tests

- Full solver vs exhaustive direct LhCDS enumeration on all graphs up to a feasible `n`, then randomized graphs beyond that.
- Every prefix `k` compared against the exhaustive top-k prefix.
- `h=2` specialization against the edge formulation.
- Verify output density/order, not only vertex-set multiset.
- Verify no duplicate output and pairwise disjointness.
- Verify complete runs use at most `2r-1` oracle calls where `r` is obtained from the exhaustive chain on tiny cases.
- Verify terminal output is produced without candidate verification calls.

## Boundaries

- No performance shortcuts beyond already validated components.
- No approximate density or heuristic recursion order.
- No post-hoc verification used to hide a solver bug.
- No safe-core reduction yet.
- Do not weaken output comparison to rounded density.

## Verification

Run all unit tests and a deterministic solver differential campaign. Produce a small human-readable trace for at least three nontrivial graphs, including one with a nonterminal split and one terminal layer with multiple equal-density LhCDSes.

Update traceability, tasks, decisions, and reproducibility documents.
