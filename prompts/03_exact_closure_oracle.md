# Prompt 03 — Exact Integer-Capacity Closure Oracle for F_h(lambda)

## Goal

Implement the theorem-specified exact oracle returning the unique inclusion-wise largest maximizer `F_h(lambda)` within a certified interval `X subsetneq F_h(lambda) subseteq Y`.

## Context to read

- `AGENTS.md`
- `docs/ALGORITHM_SPEC.md`, especially the closure-oracle section
- `docs/ARCHITECTURE.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- `docs/THEORY_TO_CODE_AUDIT.md`
- Theorem 1.19 and Corollary 1.20 in `papers/veri_free_lhcds_v3_1_submit.md`
- the exhaustive `F_h` implementation under `reference/`

## Deliverables

1. Exact reduced rational type `a/b` with checked comparison and construction.
2. Residual-footprint builder:
   - iterate every h-clique `C` contained in `Y` with `C not subseteq X`;
   - compute nonempty `R=C\X`;
   - aggregate identical footprints into exact integer `w(R)`;
   - deterministic key/order;
   - verify the residual-footprint identity in debug/test mode.
3. A deterministic max-flow/min-cut interface and a first exact Dinic backend.
4. Checked capacity construction exactly matching the manuscript:
   - `N=|Y\X|`, `L=N+1`;
   - `s -> p_R`: `L*b*w(R)`;
   - `p_R -> v`: `M_inf` for every `v in R`;
   - `v -> t`: `L*a-1`;
   - `M_inf = 1 + sum_R L*b*w(R) + N*(L*a-1)`.
5. Return `X union S_star`, where `S_star` is the interval-vertex set reachable from `s` in the residual graph after max-flow.
6. Handle `a=0` exactly as specified; no cut should be built.
7. Telemetry for footprint count, aggregated weight, node/arc count, maximum capacity, build time, and flow time.
8. Unit and differential tests against exhaustive `F_h(lambda)`.

## Numeric policy

- No `double` or epsilon.
- Use checked `unsigned __int128` for the first fast backend, with decimal formatting and explicit overflow failure before network construction.
- Keep the interface generic enough for a slower multiprecision test backend. Add at least construction-level tests beyond 64-bit range.
- Never use a guessed finite infinity. `M_inf` must be the exact formula above.

## Required differential cases

Test all or a broad deterministic sample of:

- tiny graphs, multiple `h`;
- `X=empty`, `Y=V`;
- nonempty `X`;
- footprints of every size from 1 through `h`;
- many cliques sharing one footprint;
- largest-maximizer ties;
- zero-clique and `lambda=0` cases;
- rational lambdas with nontrivial gcd;
- capacities near numeric limits.

For each case, verify not only the returned set but also that it maximizes exact `Q_lambda` and contains every other maximizer.

## Boundaries

- Do not implement divide-and-conquer yet.
- Do not add clique-core reduction.
- Do not replace residual footprints by a boundary heuristic.
- Do not alter the `+1` lexicographic tie mechanism.
- Do not accept a mismatch as numerical tolerance.

## Verification

Run unit tests plus at least 10,000 fixed-seed oracle differential queries. Save minimized reproducers for any mismatch. Report maximum observed capacities and whether any query hit the checked limit.

Update traceability, tasks, decisions, and reproducibility documents.
