# Prompt 13 — Independent Correctness Review

## Goal

Perform a read-mostly adversarial review of the release candidate against the manuscript. Prioritize findings; do not start by rewriting code.

## Context to read

- `AGENTS.md`
- `docs/ALGORITHM_SPEC.md`
- `docs/THEORY_TO_CODE_AUDIT.md`
- `docs/CLAIM_TRACEABILITY.md`
- `docs/DECISIONS.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- `papers/veri_free_lhcds_v3_1_submit.md`
- all core solver, arithmetic, flow, clique, reduction, and serialization code

## Review checklist

Audit at least:

1. Definition consistency and graph normalization.
2. Clique counting exactly once, including boundary-crossing cliques.
3. Rational reduction/comparison and overflow behavior.
4. Residual-footprint identity and aggregation.
5. Closure capacities, implication direction, `M_inf`, source-side extraction.
6. Largest-maximizer tie implementation.
7. Interval preconditions for every oracle call.
8. Separator computation and `Z=Y` terminal condition.
9. Left-first recursion, stack ordering, and early stopping.
10. Terminal connected components and `E(W,X)=empty` filter.
11. Safe-core theorem preconditions.
12. Deterministic equal-density order.
13. `lambda=0`, zero-clique graphs, isolated vertices, disconnected graphs, `k>q`.
14. Output validator independence.
15. Whether tests share too much implementation with production code.

## Deliverables

Create `docs/reviews/CORRECTNESS_REVIEW.md` with findings ordered by severity:

- Critical: can change returned vertex sets/rank/exactness.
- High: unhandled valid input, overflow, or invalid theorem precondition.
- Medium: inadequate test oracle, nondeterminism, ambiguous behavior.
- Low: maintainability/documentation issues.

Each finding must include file/line, counterexample or failure mode, theorem/invariant affected, and a proposed validation. Also list areas reviewed with no finding and residual uncertainty.

## Boundaries

- Do not claim correctness merely because tests pass.
- Do not make broad refactors during the review.
- Do not suppress a finding because the case is unlikely.
- Do not use floating tolerance to excuse a mismatch.

## Verification

Run targeted tests only when needed to substantiate findings. Report exactly what was run. After the review, use separate focused tasks to fix accepted findings, then rerun the full regression suite.
