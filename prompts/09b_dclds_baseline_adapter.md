# Prompt 09b - DCLDS Primary Baseline and Freeze Boundary

M5 / P09b.1. Implements accepted D012; independence is not an open question.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Before detailed comparison

Read D012 and `BASELINE_AUDIT.md`. Preserve the supplied theory/design snapshot,
its hashes and the current implementation version. Do not imply a content hash
proves historical priority. Do not reopen whether DCLDS is independent.

## Deliver

Map the PVLDB 2026 publication to a pinned `s01bvral/DCLDS` commit. Audit license,
build environment, supported h/pattern selection, exact arithmetic/ties, complete
vertex outputs, parameters, graph preprocessing, and time/RSS boundaries.
Produce a separate baseline adapter and a publication/code discrepancy record.

Run the same definition-level toys and real smoke protocol as IPPV. Include the
method in general-h comparisons when validated; otherwise record the blocker and
limit conclusions. Keep it external. Source availability or license permission
alone does NOT authorize importing its algorithmic techniques into VF-LhCDS.

## Boundary

Do not modify the proposed theory/oracle/recursion based on this comparison without
a separate explicitly recorded approval. This task is comparison/audit, not a
request to redesign the proposed algorithm or establish a novelty claim.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
