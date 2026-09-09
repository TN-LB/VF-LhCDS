# Prompt 13 - Independent Correctness Release Review

M3 / P13.1; after the core implementation/campaign, before M4 optimization.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Review

Inspect actual code, executed test logs and O01-O12. Check complete vertex semantics,
all-superset truth, independently generated chain, restricted/global certificates,
empty/equality/zero queries, boundary footprints, cardinality tie dominance,
original chain endpoints and terminal extraction, left-first ordering, and actual
automatic arbitrary-precision execution. Check fixed-k relabeling ties explicitly.

Inspect call paths: no candidate verifier may hide an incorrect production result.
Logical calls and actual cuts must be distinguished. External structural checks do
not establish maximality. Optional backends/modes are not core gate requirements.

## Deliver

Report severity-ranked findings with file/symbol/test evidence and a reproducer
where possible. Mark each obligation implemented-tested only with executed logs.
Do not certify unrun tests or reuse review-only exhaustive-F checks as max-flow
validation. Freeze the unoptimized correctness tag only when the actual M3 gate
passes. Do not mix performance refactoring into this review.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
