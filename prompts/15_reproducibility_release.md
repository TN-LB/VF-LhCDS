# Prompt 15 - Reproducible Release

M5 / P15.1; requires implementation acceptance and actual comparison evidence.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Assemble build/test/reproduction scripts, pinned dependencies/baseline records,
normalization and dataset manifests, immutable raw results, aggregation scripts,
configuration files, exact output schema and documented limitations. Preserve the
proof snapshot and D012 boundary. No large private/raw datasets are silently bundled.

Run a clean correctness smoke and the included baseline smoke, then regenerate
selected tables from raw manifests. Record environment, commands, checksums and
actual outcomes. Mark unavailable phase metrics and exclusions explicitly.

## Gate

Every reported number must trace to a command, version, dataset checksum, raw log
and aggregation version. Include known failed/censored cases. Review-only scripts
are labelled as such, not release acceptance. Never invent a tested build or claim
all optional modes/baselines exist. Deliver a package only at its actual completed
reproduction level; performance improvement is not a release requirement.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
