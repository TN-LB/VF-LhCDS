# Prompt 99 - Preserve, Minimize and Diagnose a Failure

Use on any failed named test or experiment validator. Do not proceed by weakening semantics.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Procedure

Save original graph, h/k, IDs, exact lambda, bounds, bound provenance, configuration,
seed, expected/actual output and logs before edits. Identify the earliest violated
obligation, not just its downstream symptom.

Deterministically remove edges, then vertices, preserving the mismatch. For oracle
failures, also preserve certified containment/request type; if bounds become
uncertified, recompute a certificate or explicitly test the restricted objective.
Simplify parameters only while the same failure remains. Re-rank renamed truth
when fixed-k ties exist. Do not blame a legitimate kth-tie choice for a mismatch.

Create a permanent named regression, explain the source/specification/code conflict,
fix the earliest cause and rerun the original and reduced cases. Never add an
approximate fallback or candidate verifier to suppress an exact solver bug.
If a proof counterexample survives, record it and stop that affected path; do not
silently edit the manuscript. Report what is and is not resolved.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
