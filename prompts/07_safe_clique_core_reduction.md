# Prompt 07 — Safe h-Clique Core Reduction

## Goal

Implement only the high-density reduction justified by the manuscript, and prove behavior equivalence empirically against the unreduced solver.

## Context to read

- `AGENTS.md`
- `docs/ALGORITHM_SPEC.md`, safe-reduction section
- `docs/CORRECTNESS_TEST_PLAN.md`
- Definition 1.21 and Lemma 1.22 in `papers/veri_free_lhcds_v3_1_submit.md`
- current no-reduction solver

## Deliverables

1. Deterministic `(t, Psi_h)`-core peeling using exact current h-clique degrees.
2. Clear API distinguishing:
   - global graph;
   - current interval `X subseteq Y`;
   - certified lower bound `lambda_0`;
   - restricted upper endpoint `Y' = Y intersect core_{ceil(lambda_0),Psi_h}(G)`.
3. Assertions/checks for the theorem preconditions before reduction is used.
4. Mode switch:
   - `off` (correctness reference);
   - `safe` (theorem-backed reduction only).
5. Telemetry for vertices/cliques removed, peeling time, and effect on closure-network size.
6. Unit tests for clique-degree updates and nested cores.
7. Differential tests proving byte-identical semantic output between `off` and `safe` modes on the full regression corpus and broad random campaigns.

## Boundaries

- Do not apply a core based on the current query lambda unless the required containment and endpoint assumptions are established exactly.
- Do not drop `X` vertices.
- Do not use ordinary degree core as a substitute for h-clique core for `h>2`.
- Do not introduce heuristic pruning under the name `safe`.
- Do not change tie behavior when a reduced query is used.

## Verification

Run unreduced-vs-reduced differential tests, targeted cases where `Y'` is not a principal-chain set, and cases with boundary-crossing h-cliques. Report reduction ratios and zero semantic mismatches.
