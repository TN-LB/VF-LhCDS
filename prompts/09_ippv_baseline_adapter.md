# Prompt 09 - IPPV Audit and Adapter

M5 / P09.1; can run after I/O contracts are frozen; not an M3 prerequisite.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Read `BASELINE_AUDIT.md` and supplied `papers/2408.14022v1.md`. Pin the author
repository commit/license; reproduce one documented command before writing a
wrapper. Audit supported h, exactness, preprocessing, iteration/verification flags,
output completeness/ties, enumeration/verification timing, and thread behavior.

Create a lossless canonical-input adapter and a reproducible external build/run.
Capture full command, environment, raw outputs, patches, time/RSS and status.
Parse already-computed vertex sets; never change the baseline's selection to make
it match VF-LhCDS. Keep compatibility/output patches minimal and separately hashed.

## Gate

Run shared direct-definition toy tests and a real smoke case. Report strict or
tie-aware agreement at its actual validation level. Counts/connectivity alone do
not prove LhCDS maximality. Record blocked-source/license, incomplete output or
semantic mismatch honestly. Do not relabel a reimplementation as author code or
subtract native candidate-verification cost from its algorithm time.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
