# Prompt 02 — Graph and h-Clique Infrastructure

## Goal

Implement deterministic C++ graph I/O/normalization and exact h-clique infrastructure, independently verified against the Python oracle.

## Context to read

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/ALGORITHM_SPEC.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- `docs/THEORY_TO_CODE_AUDIT.md`
- `reference/`

## Deliverables

1. `Graph` representation with:
   - stable 0-based internal IDs;
   - reversible mapping to original IDs;
   - sorted, deduplicated adjacency;
   - deterministic connected components and induced-subgraph operations.
2. Input normalization that records:
   - self-loops removed;
   - parallel edges collapsed;
   - direction symmetrization policy;
   - isolated vertices retained or handled according to `DECISIONS.md`.
3. A simple exact h-clique enumerator for fixed `h`:
   - deterministic clique ordering;
   - no duplicates;
   - support at least `h=2,3,4,5` on test graphs;
   - explicit error/guard for unsupported pathological parameters, if needed.
4. A clique incidence/index interface sufficient for:
   - total `mu_h(V)`;
   - `mu_h(S)` for test/diagnostic use;
   - per-vertex h-clique degree;
   - clique-core peeling later;
   - enumerating cliques contained in an interval `Y`.
5. A debug CLI/tool that prints normalized graph statistics and clique counts.
6. Unit tests and Python-vs-C++ differential tests on generated tiny graphs.

Start with the simplest exact implementation. Do not introduce advanced clique libraries or parallel enumeration in this phase.

## Required invariants

- Every h-clique is emitted exactly once in sorted internal-ID order.
- `h=2` emits each normalized undirected edge exactly once.
- The normalized graph and clique list are deterministic across runs.
- Counts use checked integer types.
- No graph operation may depend on unordered-container iteration order.

## Boundaries

- Do not implement max-flow or the closure oracle.
- Do not optimize by dropping cliques that cross a future interval boundary.
- Do not precompute all subsets or use the reference implementation inside production code.
- Do not add parallelism yet.

## Verification

Run C++ unit tests, CTest, and a differential script that generates at least 1,000 fixed-seed small graphs over multiple `h` values. On failure, save the graph, seed, expected cliques, and actual cliques.

Update `docs/CLAIM_TRACEABILITY.md`, `docs/TASKS.md`, and `docs/REPRODUCIBILITY.md`.
