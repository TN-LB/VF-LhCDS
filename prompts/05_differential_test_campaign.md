# Prompt 05 - Differential Campaign and Failure Reduction

M3 / P05.1-P05.3; requires a working M3 solver. Tests T01-T16 as applicable.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver and verify

Run the explicit smoke, exhaustive-small, higher-h and seeded tiers in
`CORRECTNESS_TEST_PLAN.md`. Report distinct graphs/h pairs and oracle requests
separately; preserve all seeds, graphs and expected/actual outputs. Do not replace
missing exhaustive coverage with a larger random-query count.

Implement failure reduction that preserves the failure and oracle request contract.
Save the original first, then deterministic edge/vertex deletions; simplify h,
bounds/lambda only while the same preconditions hold. Keep fixed regressions.

Test relabeling by transforming full truth and re-ranking (not blindly mapping a
fixed-k tie prefix), disjoint unions, isolate additions and input order. Canonical
semantic hashes exclude timestamps, timing and backend-specific trace fields.

Run ASan/UBSan and exact arithmetic/fallback boundaries. No central xfail or silent
overflow passes. Leave unrun coverage visible and the gate open. Optional backends
and modes are not missing requirements for M3. Prepare, but do not fabricate, the
correctness tag evidence for review prompt 13.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
