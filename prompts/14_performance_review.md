# Prompt 14 - Performance and Comparison Review

M5 / P14.1; requires actual experiment results, not only planned commands.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Review

Inspect raw manifests, environment, dataset/checksum selection, baseline commits/
licenses/patches, timing boundaries, repeats and all completed/censored outcomes.
DCLDS independence is already decided, but build/output/timing validation is not.
Primary competitors must be included or their absence limits conclusions.

Check endpoint reuse/footprint aggregation are not mislabelled optional improvements;
core overhead is included; streaming/re-enumeration work is counted; cache benefits
have real hits; full versus early-stop uses prefix validation; semantic hashes
exclude telemetry. Baseline candidate verification remains algorithm time.

## Deliver

List evidence-backed bottlenecks, fairness issues, result limitations and unsupported
claims. Recommend only changes supported by profiles and separate proofs where
semantics could change. Do not claim SOTA, scalability or speedup from theoretical
oracle counts or a small favorable subset. Do not change the experiment grid to
remove unfavorable results.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
