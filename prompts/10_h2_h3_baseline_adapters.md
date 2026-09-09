# Prompt 10 - Claim-Scoped h=2/h=3 Baselines

M5 / P10.1; execute only for the claimed specialization strata.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Read `BASELINE_AUDIT.md` and the relevant supplied papers. Prioritize LDS-Opt/LDScvx
for h=2 and the actual LTDScvx implementation for h=3. LDSflow/LTDSflow are optional
diagnostics. An edge repository is not assumed to contain triangle code.

For each selected method pin source/license, build or record an explicit blocker,
audit output/exactness/parameters/timing and wrap common normalized input. Separate
author code from any approved paper-based reimplementation. Never present h=2/3
methods as arbitrary-h solutions.

## Gate

Apply the shared definition-level toy and real smoke validation. Report exact
available output and tie policy, not invented vertex sets reconstructed from a
rounded density. Keep exclusions visible. Do not make all historical baselines or
unavailable code prerequisites for the core correctness release.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
