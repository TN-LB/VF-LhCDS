# Prompt 02 - Graph, Cliques and Exact Data

M2 / P02.1-P02.3; requires M0; comparison fixtures require M1. Tests T01,T04,T05.

## Context

Read `AGENTS.md`, `docs/DECISIONS.md`, the named task in `docs/TASKS.md`,
`docs/ALGORITHM_SPEC.md`, `docs/THEORY_TO_CODE_AUDIT.md`, and the relevant test IDs
in `docs/CORRECTNESS_TEST_PLAN.md`. Reuse accepted decisions; flag only new conflicts.

## Deliver

Build a deterministic C++17 graph with explicit vertex universe, sorted adjacency,
reversible original IDs, canonical edge checksum and induced-component operations.
Preserve isolates and loop-only declared vertices. Add canonical sets and reusable
membership markers; set equality is not hash-only.

Implement one materialized fixed-h clique/incidence backend, with sorted unique
tuples and deterministic enumeration. Support the documented h domain without an
undocumented MAX_H cap; h>n yields an empty clique family. Streaming is deferred.

Implement exact counts/fractions and checked integer helpers, including safe signed
objective comparison and decimal formatting. Keep counts exact before flow dispatch;
an overflow-only abort is not the D005 automatic arbitrary-precision path.

## Tests and boundary

Compare clique tuples, subset counts and incidences against combination reference;
check sum(degrees)=h*clique_count. Run the relevant named tests and declared seeded
tier, recording actual coverage. Do not implement recursion, core reduction,
parallelism or optional clique backends in this task. C++17 interfaces must not
silently require std::span/C++20.

## Completion evidence

Report task/obligation IDs, changed files and code symbols, actual commands and
environment, fixture/seed manifest, results/log paths, and unrun work. Update
`docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` only for executed evidence. Tests
support the implementation; do not describe finite agreement as a proof.
