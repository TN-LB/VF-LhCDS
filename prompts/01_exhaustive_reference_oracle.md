# Prompt 01 - Independent Exhaustive Reference

M1 / P01.1-P01.5; requires M0. Obligations O01-O03; tests T01-T03.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Implement standard-library-first Python graph normalization, combination clique
enumeration, ordinary induced connectivity, exact counts/densities/deletion loss,
compactness and direct LhCDS enumeration. Check ALL deletion subsets and ALL proper
supersets; do not reduce maximality to one-vertex additions.

Implement exhaustive global F by comparing signed integer values `b*mu(S)-a*|S|`,
including empty S, and union all maximizing sets. Also expose exhaustive restricted
maximization for arbitrary nested bounds, clearly labelled as restricted.

Implement the mandatory independent principal chain from cardinality-line
intersections and exact midpoint samples (audit B). Do not use the production
separator recursion, or just scan induced-subgraph densities. Serialize canonical
truth, exact fractions, IDs, seeds and expected ranks. Default hard guard: n<=12.

## Tests and gate

Run T01-T03, including both-triangles-with-a-bridge maximality, zero-clique ordinary
components, largest ties and the outer-breakpoint witness. Test relabeling by
transforming COMPLETE truth and re-sorting before truncation. Reference code must
not import production or closure code. Run pytest and the reference CLI smoke;
report actual graph coverage and any unmet tier. No central semantic xfail passes.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
