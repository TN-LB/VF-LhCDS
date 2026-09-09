# Prompt 04 - Exact Left-First Fixed-k Solver

M3 / P04.1-P04.4; requires M1+M2. Obligations O04,O07-O09; tests T10-T13.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Implement immutable ChainInterval endpoints and cached original mu values.
Compute lambda from `(mu(Y)-mu(X))/(|Y|-|X|)`; call the certified exact oracle;
assert the necessary progress condition X<Z<=Y. Terminality is Z==original Y.

At a nonterminal node visit (X,Z) first, then (Z,Y) only if output is still needed.
At a terminal node extract ordinary components of original G[Y\X] and retain only
those anti-adjacent to all of X. Sort retained components by accepted original-ID
set order. Only retained components are guaranteed to have layer density lambda.
Empty terminal output is valid. A stack implementation pushes right before left.

Support k>=1, k>q, --all, disconnected graphs, isolates and zero layers. Reject k=0.
Emit fixed-k outputs one at a time and stop at k or exhaustion; q is not presumed
known in advance. Tie-inclusive output and all core reductions are deferred.

## Verification

Compare every tested prefix against direct truth, including exact counts/densities
and order. Use the independently constructed chain to test all pair separators.
Verify full basic runs have exactly 2r-1 logical interval queries; cuts may be fewer.
Add human-readable traces for a split, a tie layer, and a non-emitting terminal.
Do not invoke a candidate verifier, run an approximation, or repair wrong output
post hoc. Review-only exhaustive-F scripts do not validate production flow.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
