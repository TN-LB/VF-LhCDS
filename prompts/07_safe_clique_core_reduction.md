# Prompt 07 - Safe Query-Local Clique-Core Restriction

M4 / P07.1-P07.3; requires M3 correctness freeze. O10, test T17.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Implement deterministic current h-clique-degree peeling, invalidating each clique
once and updating only remaining incidences. Prove the implemented restriction
matches Lemma 1.22; differential agreement is supporting evidence, not the proof.

For original chain endpoints X,Y, compute the original lambda first. For positive
lambda use lambda_0=lambda initially, and set
`Y_oracle=Y intersect core_ceil(lambda_0)(G)`. Certify containment from the original
query plus Lemma 1.22. Build footprints and N,L from Y_oracle. Bypass at lambda=0.

Never overwrite Y; never recompute lambda from Y_oracle; never compare Z to
Y_oracle for terminality; never extract from a core-reduced graph. Children remain
(X,Z),(Z,Y), and terminal extraction uses original G[Y\X]. A cached high-threshold
core is not automatically safe for a lower query. Do not assert unknown global
containment as though a runtime check alone proved it.

## Verification

Use off/safe modes with canonical output equality. T17 must include K4 disjoint
from a triangle with a pendant vertex: the root 2-core is not a chain set, and
the lower-density output must retain the pendant vertex. Test exact oracle
set equality, clique degree updates, lower thresholds, zero queries, and boundary
cliques. Report reduction cost and benefit separately. No heuristic pruning.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
