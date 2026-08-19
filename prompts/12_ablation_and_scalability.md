# Prompt 12 — Ablation, Scalability, and Stress Experiments

## Goal

Implement the experiment families needed to explain where VF-LhCDS wins or loses, not only whether it wins on aggregate.

## Context to read

- `AGENTS.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/REPRODUCIBILITY.md`
- current runner and telemetry schema

## Required experiment families

1. Main exact comparison stratified by `h`:
   - `h=2` applicable exact baselines;
   - `h=3` applicable exact baselines;
   - `h=4,5` arbitrary-h exact baselines.
2. Vary `k`, including small-k and all-output where feasible.
3. Vary graph size using deterministic induced-subgraph samples or published scale variants.
4. Vary `h` while reporting the resulting number of h-cliques.
5. Synthetic structural sweeps:
   - sparse-to-dense;
   - planted dense blocks connected by sparse bridges;
   - high clique-overlap;
   - many equal-density leaves;
   - many principal-chain layers;
   - few layers but huge closure networks.
6. Ablations, where implementable without changing semantics:
   - safe core reduction off/on;
   - footprint aggregation off/on;
   - clique cache/index strategy;
   - flow backend;
   - interval cache off/on;
   - full output vs early top-k stopping.
7. Time breakdown and network-size breakdown.
8. Memory scaling and capacity-bit-width statistics.
9. Correctness stress on every ablation.

## Analysis outputs

Generate machine-readable summary tables and plotting-ready CSV/Parquet, but do not hard-code publication claims. Include:

- speedup ratios only when both runs are valid and completed;
- timeout-aware tables;
- oracle-call count and layers emitted;
- footprint count before/after aggregation;
- network nodes/arcs;
- clique enumeration and flow share;
- peak RSS;
- result hash agreement.

## Boundaries

- Do not cherry-pick datasets or repetitions after seeing results.
- Do not use a different `k` or `h` for a slow baseline.
- Do not exclude preprocessing without also reporting end-to-end time.
- Do not present a speedup against a timed-out method as an exact finite ratio unless the convention is explicitly defined.
- Do not conclude SOTA until the direct DCLDS provenance and baseline audit are resolved.

## Verification

Run a small-scale version of every experiment family, validate all outputs, and document the exact commands required for the full campaign.
