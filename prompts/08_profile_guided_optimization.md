# Prompt 08 - One Profile-Justified Optimization

M4 / P08.1; requires M3 and the relevant baseline measurements.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Process

Profile a frozen workload before edits. Choose ONE measured bottleneck. State the
semantic invariant and a written preservation argument, implement behind a switch,
run the same correctness corpus, then compare runtime/memory including its overhead.
Do not require a speedup if the evidence is mixed; retain an off mode or revert.

Optional candidates: footprint allocation reuse; singleton folding with derived
new signed vertex weights; streaming for demonstrated clique-memory pressure;
another exact flow algorithm; caches with measured hits and memory; component
scheduling with exact global ordering. Endpoint-count reuse and aggregated
footprints already belong to B0, not a new optimization.

Do not introduce all optional backends, parallelism, warm-flow reuse or heuristic
seeding together. Each additional semantic mechanism needs its own argument/tests.
Do not import DCLDS techniques under D012 without separate approval. Canonical
outputs, not timing or backend trace IDs, must remain equal.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
