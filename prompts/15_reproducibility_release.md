# Prompt 15 — Reproducibility and Release Packaging

## Goal

Prepare a release candidate that another researcher can build, validate on tiny graphs, and reproduce selected experiments without hidden state.

## Context to read

- `AGENTS.md`
- `docs/REPRODUCIBILITY.md`
- `docs/BASELINE_AUDIT.md`
- `docs/CLAIM_TRACEABILITY.md`
- correctness and performance reviews
- all build, dataset, experiment, and aggregation scripts

## Deliverables

1. Final root `README.md` with:
   - problem statement and exact scope;
   - build dependencies and commands;
   - input format and normalization;
   - proposed-solver examples;
   - tiny correctness-validation command;
   - experiment quick start;
   - expected outputs;
   - supported numeric limits;
   - citation and license information.
2. Reproducible environment definition, such as container recipe and/or locked package/toolchain versions.
3. `scripts/reproduce_smoke.sh` that builds, runs tests, executes tiny proposed/baseline cases, validates outputs, and produces a small summary.
4. `scripts/reproduce_selected_results.sh` for a documented subset of paper tables/figures.
5. Dataset download/checksum/normalization manifests without redistributing restricted data.
6. Baseline fetch/build scripts pinned to commits, respecting licenses.
7. Versioned result schema and example raw manifests.
8. Release manifest with git commit, submodule commits, compiler, flags, dependencies, and checksums.
9. Archive exclusions for raw large datasets, binaries, caches, and massive logs.
10. Final update to `docs/CLAIM_TRACEABILITY.md`, mapping every released claim to code, tests, configs, and raw result IDs.

## Release gates

- All mandatory correctness tests and sanitizers pass.
- No unresolved Critical/High correctness findings.
- Baseline statuses are explicit.
- Smoke reproduction works from a clean checkout.
- Output hashes are deterministic.
- No secret, local absolute path, or untracked dependency is required.
- The documentation does not claim arbitrary-h support for h=2/h=3 baselines.

## Boundaries

- Do not include third-party source or datasets contrary to license.
- Do not publish fabricated placeholder numbers as results.
- Do not omit known limitations.
- Do not mark the release complete when only the developer's existing build directory works.

## Verification

Run the smoke reproduction from a clean build directory or clean worktree. Record total commands, elapsed time, produced files, checksums, and any intentionally skipped large experiments.
