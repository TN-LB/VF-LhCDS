# Prompt 05 — Differential, Metamorphic, and Failure-Minimization Campaign

## Goal

Turn the correctness checks into a durable regression system and search aggressively for semantic bugs before optimization.

## Context to read

- `AGENTS.md`
- `docs/CORRECTNESS_TEST_PLAN.md`
- `docs/ALGORITHM_SPEC.md`
- `reference/`
- current C++ tests and solver

## Deliverables

1. A deterministic test driver that can generate:
   - Erdos-Renyi graphs over a probability grid;
   - disjoint unions;
   - planted cliques/near-cliques;
   - paths connecting dense blocks;
   - graphs with isolated vertices;
   - graphs designed to create equal-density layers.
2. For each generated graph and supported `h`, compare:
   - normalized graph;
   - clique list/counts;
   - selected `F_h(lambda)` queries;
   - full principal-chain diagnostics when feasible;
   - all LhCDSes and every top-k prefix;
   - exact ordering and hashes.
3. Metamorphic tests:
   - vertex relabeling;
   - edge-input permutation and duplicate insertion before normalization;
   - disjoint union;
   - adding isolated vertices;
   - repeating the same run;
   - `h=2` specialization.
4. Failure artifact format containing input, `h`, `k`, seed, expected JSON, actual JSON, oracle trace, compiler/build metadata.
5. An automatic reducer that attempts to remove vertices and edges while preserving a mismatch.
6. A committed small regression corpus for every discovered bug.
7. Sanitizer configurations for ASan, UBSan, and debug assertions.

## Campaign requirements

Run at least:

- all unlabeled graphs up to the largest practical `n` available through a generator, or clearly document the achieved bound;
- 100,000 fixed-seed random graph/h combinations for the full solver where the Python oracle is tractable;
- 100,000 additional C++ invariant-only cases at larger sizes;
- targeted numeric/capacity tests.

If this volume is impractical in one invocation, create deterministic sharded commands and run enough shards to validate the harness now. Do not claim all shards ran when they did not.

## Boundaries

- Do not modify algorithm semantics to make tests pass without explaining the root cause.
- Do not discard failing seeds.
- Do not compare floating-point renderings.
- Do not optimize the solver in this phase except to make the test harness usable without changing behavior.

## Verification

Report commands, shard IDs, number of cases, seeds/ranges, wall time, failures, minimized reproducers, and sanitizer results. Update `docs/CORRECTNESS_TEST_PLAN.md` with the exact recurring CI tiers.
