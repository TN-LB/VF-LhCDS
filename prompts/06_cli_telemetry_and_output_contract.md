# Prompt 06 - Minimal CLI, Output and Evidence

M3 / P06.1; minimal oracle reproducer/counters already exist from P03.5.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Finalize solve (--k or --all), global-or-restricted oracle, graph inspection and
build-info commands. Use exact decimal count/fraction fields and self-consistent
complete vertex sets. Validate argument domains and provide explicit error,
resource-limit, OOM and incomplete statuses. No partial output is exact completion.

Default core off, fixed-k output, materialized cliques and automatic exact-capacity
selection. Do not expose a nonexistent streaming or tie-inclusive mode.

Record logical interval queries, actual cuts, original/reduced sizes, cliques,
footprints, forward/residual sizes, capacity bit length and backend. Keep trace and
timing records separate from canonical semantic hashes.

Define end-to-end, post-load (includes enumeration), and post-index timing as in
`EXPERIMENT_PLAN.md`. External validation is separately timed; native baseline
verification cannot be subtracted. Phase timers must not double-count nested work.

## Verification

Round-trip output/schema fixtures; repeat runs for semantic determinism; test zero,
empty-global-oracle, malformed inputs and resource-error reporting. No timing or
validation-status label may overstate what was actually run.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
