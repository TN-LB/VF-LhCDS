# Prompt 00 - Contract Review and Repository Bootstrap

M0 / P00.1-P00.4. No production algorithm implementation in this task.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Review the populated proof obligations O01-O12, rather than creating a second
inconsistent audit. Preserve all four `papers/` files and snapshot hashes.
Retain D005, D006 and D012; read the new specified-in-revision decisions and resolve
only real remaining conflicts. Confirm vertex preservation, k>=1, restricted/global
oracle semantics, immutable chain endpoints, exact fallback and timing/evidence scopes.

Create the minimal C++17/CMake library/CLI/CTest skeleton and independent Python
package/pytest skeleton from `ARCHITECTURE.md`. Add strict warnings and sanitizer
build configuration. Do not add optional backends or dependencies for future use.

## Boundary and gate

Do not implement clique enumeration, closure, recursion or baselines yet. Do not
copy external code or rewrite the proof. Run and record:

```text
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j2
ctest --test-dir build --output-on-failure
python -m pytest reference/tests -q
```

These are expected commands, not pre-existing results. M0 completes only after
contracts are explicit and the skeleton commands run. New experimental budgets
need not be decided to bootstrap the mathematical implementation.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
