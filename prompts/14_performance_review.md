# Prompt 14 — Performance, Baseline, and Experimental Fairness Review

## Goal

Review whether measured performance and planned claims are supported by comparable implementations and reproducible evidence.

## Context to read

- `AGENTS.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/BASELINE_AUDIT.md`
- `docs/REPRODUCIBILITY.md`
- `docs/CLAIM_TRACEABILITY.md`
- experiment configs, raw manifests, aggregation scripts, and representative logs

## Review checklist

1. Proposed solver profile and actual bottleneck.
2. Baseline provenance, commit, license, patches, and paper/code correspondence.
3. Correct `h` applicability and exact-vs-approximate labels.
4. Identical normalized graph, output semantics, `h`, and `k`.
5. Compiler, flags, CPU, memory, threads, affinity, and resource limits.
6. End-to-end vs solver-only timing.
7. One-time preprocessing and clique-index accounting.
8. Warm-up/repetition/randomized execution order.
9. Peak RSS and timeout/OOM handling.
10. Output correctness before inclusion in speed tables.
11. Aggregation statistics and missing-data treatment.
12. Whether any result depends on a hand-tuned parameter unique to one dataset.
13. Whether direct overlapping work such as DCLDS has been resolved and included when appropriate.
14. Whether each intended paper claim has a traceable table/figure/raw manifest.

## Deliverables

Create `docs/reviews/PERFORMANCE_REVIEW.md` with prioritized findings and a claim-readiness table:

- claim text;
- scope (`h`, datasets, `k`, hardware);
- supporting experiment IDs;
- baseline validity;
- status: supported / partially supported / unsupported / blocked.

Include concrete rerun instructions for every blocking issue.

## Boundaries

- Do not rewrite claims to sound stronger than evidence.
- Do not ignore timeout/OOM cases.
- Do not compare methods outside their supported `h`.
- Do not infer SOTA from papers alone when code/provenance is unresolved.
