# Prompt 08 — Profile-Guided Production Optimization

## Goal

Improve runtime and memory after correctness is frozen, while maintaining byte-identical semantic output and exact arithmetic.

## Context to read

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- current profiling data and regression corpus

## Process

1. Establish a baseline benchmark manifest and profile before editing.
2. Rank costs by measured contribution:
   - clique enumeration/materialization;
   - interval membership and clique filtering;
   - residual-footprint aggregation;
   - network construction;
   - max-flow;
   - connected components/adjacency checks;
   - allocation and serialization.
3. Select one optimization at a time.
4. For every optimization, document:
   - expected complexity/memory effect;
   - why semantics are unchanged;
   - files changed;
   - tests run;
   - before/after profile;
   - any new numeric limit.

## Candidate optimizations, only when profiles justify them

- compact interval bitsets or generation-mark arrays;
- small fixed-size footprint keys;
- preallocated arenas and network buffers;
- clique incidence reuse across nested intervals;
- deterministic caching keyed by exact interval fingerprint;
- avoiding materialization when an iterator is sufficient;
- choosing between global clique materialization and on-demand enumeration;
- improved exact max-flow backend behind the same interface;
- safe component-wise processing when proved equivalent;
- single-threaded optimizations first, parallelism only after deterministic semantics are protected.

## Required guardrails

- Keep the no-optimization or debug path runnable.
- Run the entire differential corpus after each semantic-risk optimization.
- No float-based filtering, approximate clique counting, randomized cut, or heuristic stopping in the exact solver.
- No unproved omission of cross-boundary cliques.
- No baseline code copied into the proposed solver.

## Verification

Provide a before/after table for representative small, medium, clique-heavy, and sparse graphs. Include end-to-end time, oracle time, flow time, clique time, peak RSS, network size, and output hash. A speedup without full correctness regression is not accepted.
