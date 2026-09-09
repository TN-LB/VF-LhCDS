# Prompt 12 - Scope-Matched Experiments and Ablations

M5 / P12.1; requires frozen experiment configuration and successful shared smoke.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Run the selected general-h cases with validated DCLDS/IPPV, then claimed h=2/h=3
specializations. Keep graph version, h, k, worker policy and resources comparable.
Do not reduce the task only for a slow baseline. Retain timeout/OOM/failed cases.

Use the corrected ablation table: B0 already materializes cliques and aggregates
footprints. Core off/on is required only when core exists; streaming, folding,
other flow algorithms and extra caches are optional. Change one feature at a time.
Full-chain versus early-stop compares the corresponding fixed-k prefix, NOT equal
whole-output hashes. Log reduction/enumeration/cache overhead, not just flow time.

Analyze end-to-end time, memory, time-to-result and observed query/network size.
No 2r-1 bound implies O(k), and a fixed-h polynomial bound is not evidence of
practical scalability. Scope conclusions to completed/censored evidence; negative
performance remains reportable. Produce aggregates directly from immutable logs.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
