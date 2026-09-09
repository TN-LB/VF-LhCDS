# Prompt 11 - Experiment Harness and Evidence Levels

M5 / P11.1-P11.3; requires executable solver and at least the relevant baseline adapter.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Read `EXPERIMENT_PLAN.md` and `REPRODUCIBILITY.md`. Freeze a machine/configuration
record containing actual datasets/checksums, h/k grid, repeats, seed, thread count,
timeout and memory budgets before runs. Do not invent confirmations or select
favorable settings after observing performance.

Run algorithms on losslessly converted common input; randomized order within each
block; immutable command/log/manifest/output records; explicit completed, timeout,
OOM, error and incomplete-output statuses. Preserve all outcomes.

Separate definition-checked, structural-checked and cross-implementation-agreement
evidence. Strict order comparisons need compatible total ordering; kth ties need
audited cutoff/count behavior. Unknown q or incomplete ties cannot be certified by
rounded density agreement.

Time process-launch-to-output end to end; post-load includes enumeration; post-index
is only a scope-qualified diagnostic. External validation time/RSS is separate;
internal baseline verification remains timed. Missing phase values are unavailable,
not zero. Run a small shared smoke configuration before the main suite.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
