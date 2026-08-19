# Prompt 01 — Exhaustive Python Reference Oracle

## Goal

Implement an independent, definition-level Python oracle for tiny graphs. It is the correctness anchor for every later C++ component.

## Context to read

- `AGENTS.md`
- `docs/ALGORITHM_SPEC.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- `docs/THEORY_TO_CODE_AUDIT.md`
- `docs/DECISIONS.md`
- the definitions and characterization theorems in `papers/veri_free_lhcds_v3_1_submit.md`

## Required behavior

Implement under `reference/vflhcds_ref/`:

1. Deterministic undirected simple graph normalization.
2. Exact h-clique enumeration by combinations.
3. Exact `mu_h(S)` and `d_h(S)` using `fractions.Fraction`.
4. Connectivity of induced subgraphs.
5. Deletion loss `Delta_h(U; S)`.
6. Direct test of h-clique `lambda`-compactness by enumerating every `U subseteq S`.
7. Compactness `eta_h(S)` by exhaustive minimization.
8. Direct LhCDS test:
   - connected;
   - `d_h(S)`-compact;
   - no proper induced supergraph is also `d_h(S)`-compact.
9. Exhaustive enumeration of all LhCDSes and deterministic top-k ordering.
10. Exhaustive largest maximizer `F_h(lambda)` over all vertex subsets, with inclusion-wise largest tie rule.
11. Optional exhaustive principal-chain extraction for diagnostics.
12. Canonical JSON serialization containing original vertex IDs, exact numerator/denominator, clique count, and output rank.

Use a hard size guard, default `n <= 12`, to prevent accidental exponential runs. The implementation must not import or call production C++ code.

## Tests

Add deterministic tests for:

- empty clique family (`h > clique number`);
- a single clique;
- disconnected union of cliques;
- path, cycle, complete graph, complete bipartite graph;
- isolated vertices;
- equal-density/tie cases;
- `h=2` specialization;
- `k=1`, `k=q`, and `k>q`;
- relabeling invariance;
- exact rational comparisons.

For graphs up to a practical small `n`, cross-check:

- `eta_h(S) <= d_h(S)`;
- self-denseness characterization;
- every reported LhCDS satisfies the direct definition;
- pairwise disjointness of distinct outputs;
- exhaustive `F_h(lambda)` is inclusion-wise largest among all maximizers.

## Boundaries

- Clarity is more important than speed.
- Do not reuse the future closure-network algorithm to compute truth.
- Do not use float for any semantic decision.
- Do not skip disconnected or zero-clique cases.
- Do not silently choose a subset tie order; use the approved decision or leave a failing/xfail test linked to `DECISIONS.md`.

## Verification

Run:

```bash
python -m pytest reference/tests -q
python -m vflhcds_ref.cli --help
```

Report test count, any xfails, and the maximum graph size covered by exhaustive tests. Update `docs/CLAIM_TRACEABILITY.md`, `docs/TASKS.md`, and `docs/REPRODUCIBILITY.md`.
