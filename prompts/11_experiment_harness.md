# Prompt 11 — Unified Experiment Harness and Fairness Controls

## Goal

Create a reproducible harness that runs the proposed solver and validated baselines on identical normalized inputs and produces auditable raw results.

## Context to read

- `AGENTS.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/BASELINE_AUDIT.md`
- `docs/REPRODUCIBILITY.md`
- all validated CLI/output contracts

## Deliverables

1. Dataset manifest schema with source, checksum, license/terms, original format, normalization command, normalized fingerprint, `|V|`, `|E|`, and clique statistics where feasible.
2. One normalization pipeline producing a canonical graph consumed by all adapters.
3. Experiment configuration files covering:
   - algorithm and pinned commit;
   - dataset fingerprint;
   - `h`, `k`;
   - repetitions and warm-up policy;
   - CPU/thread affinity;
   - memory and timeout limits;
   - algorithm-specific paper-default parameters;
   - random execution order seed.
4. A runner that captures:
   - command and environment;
   - start/end time;
   - wall/user/system time;
   - peak RSS;
   - exit/status/timeout/OOM;
   - stdout/stderr files;
   - semantic result hash and output-validator result.
5. Randomized algorithm execution order by block, with recorded seed.
6. Raw immutable per-run manifests under `results/raw/` and derived tables under `results/derived/`.
7. Aggregation scripts reporting median and dispersion, not only best time.
8. Correctness gate: a run is performance-valid only when its output passes semantic validation for the relevant comparison.
9. Dry-run and local-small configurations suitable for CI.

## Fairness rules

- Same normalized graph and vertex mapping.
- Same `h`, `k`, output requirement, timeout, and resource cap.
- Distinguish preprocessing-inclusive and solver-only time.
- Distinguish one-time clique-index build from per-query time; report both when amortization is studied.
- Use one thread unless a separate parallel experiment gives every method an equivalent opportunity.
- Preserve timeouts/OOMs in tables.
- Never infer correctness from equal output counts alone.

## Verification

Run a complete small experiment matrix with at least two datasets, two `h` values, two `k` values, and every currently validated applicable algorithm. Re-run aggregation and verify it is deterministic from raw manifests.
