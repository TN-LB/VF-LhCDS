# Prompt 03 - Exact Restricted Closure and Global Oracle

M2 / P03.1-P03.5; requires M1 fixtures and P02. Obligations O05,O06,O11; T05-T09.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Implement `largest_restricted(lambda,X,Y_oracle)` and a distinct certified
`global_F` wrapper. Use full-graph, chain-separator or proved core-origin bounds
as certificates; arbitrary nested CLI bounds are restricted queries. Global F may
be empty or equal X. Strict X<F progress is not a general API prerequisite.

Aggregate every nonempty residual `C\X` for cliques inside Y_oracle, including
boundary-crossing cliques. Test Eq. 15 independently. For positive a,N use exactly
`L=N+1`, source capacities `L*b*w`, sink capacities `L*a-1`, and
`M_inf=1+sum(L*b*w)+N*(L*a-1)`. Return X plus residual-source-reachable vertices.
Handle N=0 and a=0 without a flow as specified; global zero requires Y_oracle=V.

Implement one generic exact Dinic algorithm with checked unsigned-128 and real
arbitrary-precision instantiations. Exact preflight decides safe dispatch. Exercise
fallback with huge rational inputs on tiny graphs; an interface or test-only
big-integer constructor is insufficient. Never use floats or saturating infinity.

## Verification and boundary

Test cuts against independently enumerated tiny cuts, then compare exact largest
sets against global or restricted exhaustive truth under the correct request
contract. Include every T08/T09 tie/empty/equality/zero case and numeric boundaries.
Run the oracle campaign in the centralized test plan; log graph and query counts
separately. Add minimal reproducer CLI and logical-query/actual-cut telemetry.
Do not implement recursion, core reduction or alternative flow algorithms yet.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
