# AGENTS.md — VF-LhCDS Repository Instructions

## Mission

Implement and experimentally evaluate the exact verification-free top-k locally h-clique densest subgraph algorithm specified in `papers/veri_free_lhcds_v3_1_submit.md`.

The project has two equal goals:

1. correctness that is traceable to the proof; and
2. a reproducible performance comparison against exact baselines.

Never trade the first goal for the second.

## Source priority

When sources differ, use this priority order:

1. `papers/veri_free_lhcds_v3_1_submit.md` for definitions, theorem assumptions, tie semantics, oracle construction, recursion, and output ordering;
2. `docs/DECISIONS.md` for explicit engineering choices accepted by the project owner;
3. `papers/2023-icde-lds.md` only as an `h=2` implementation and proof-organization reference;
4. `papers/2408.14022v1.md` and `papers/2504.10937v1.md` only for baseline behavior and experimental methodology.

Do not silently repair, generalize, or reinterpret the theory. Record any ambiguity in `docs/DECISIONS.md` and stop that local implementation path until the ambiguity has a documented resolution. Continue with independent tasks when possible.

## Mathematical invariants

Preserve all of the following:

- The input is a finite undirected simple graph with nonempty vertex set.
- All subgraphs are vertex-induced.
- `h >= 2` is fixed for a solver run.
- `mu_h(S)` counts each h-clique contained in `G[S]` exactly once.
- `d_h(S) = mu_h(S) / |S|` for nonempty `S`.
- `F_h(lambda)` is the unique inclusion-wise largest maximizer of
  `Q_lambda(S) = mu_h(S) - lambda * |S|`.
- Every queried `lambda` is represented as an exact reduced fraction `a/b`.
- The closure network must implement the largest-maximizer tie rule exactly.
- The divide-and-conquer traversal is left first, because the left interval contains strictly higher-density layers.
- A terminal interval emits exactly the connected components `W` of `G[Y \ X]` with no edge to `X`.
- Output ordering is nonincreasing exact density, then the project-wide deterministic subset order.
- When `k` exceeds the number of LhCDSes, return all of them.

Do not use floating-point arithmetic for decisions involving densities, lambdas, capacities, equality, ordering, or stopping conditions.

## Correctness-first workflow

Before optimizing a component:

1. add or identify its reference behavior;
2. add deterministic unit tests;
3. add randomized differential tests where applicable;
4. implement the simplest correct version;
5. run the smallest relevant test suite;
6. only then optimize, preserving the same tests.

A performance optimization is not complete until its output is byte-for-byte identical to the pre-optimization solver on the regression corpus, except for intentionally nonsemantic telemetry fields.

## Required implementation split

Maintain two paths:

- `reference/`: readable exhaustive implementation for tiny graphs and truth generation;
- `src/`: production C++ implementation.

The reference implementation is not optional and must remain independent enough to catch shared bugs. Do not call production code from the exhaustive definition checker.

## Exact arithmetic and overflow

- Prefer reduced rational types for `mu/|S|` and `a/b`.
- Use checked integer arithmetic for cross multiplication and capacities.
- The production flow backend may use `unsigned __int128` only with explicit checked construction and a clear failure message when the instance exceeds the supported range.
- Never allow wraparound, saturation, or conversion through `double`.
- Tests must include values near the chosen capacity limits.

## Engineering conventions

- Default production language: C++17 or newer, built with CMake.
- Keep third-party dependencies minimal and documented.
- Use stable 0-based internal vertex IDs; preserve a reversible map from original IDs.
- Keep graph preprocessing deterministic: remove self-loops, collapse parallel edges, canonicalize undirected edges, and record counts removed.
- Use sorted vertex lists for serialized subgraphs.
- Keep core algorithm modules separate from CLI, logging, and experiment adapters.
- Do not embed dataset-specific constants in solver code.
- Do not commit raw large datasets, generated binaries, or large result logs.

## Expected modules

The production implementation should keep these responsibilities separate:

- graph I/O and normalization;
- h-clique enumeration and optional materialized incidence index;
- exact rational arithmetic;
- max-flow/min-cut;
- residual-footprint aggregation;
- exact `F_h(lambda)` closure oracle;
- divide-and-conquer top-k solver;
- safe clique-core reduction;
- output validation and deterministic serialization;
- metrics and experiment harness.

## Testing requirements

At minimum, maintain tests for:

- graph normalization;
- h-clique enumeration against combination brute force;
- `mu_h(S)` counts;
- residual-footprint identity for every subset on tiny instances;
- closure oracle versus exhaustive maximization of `Q_lambda`;
- largest-maximizer tie cases;
- nestedness of `F_h(lambda)` on test instances;
- separator behavior on known principal-chain intervals;
- terminal leaf extraction;
- full top-k output versus exhaustive LhCDS definition;
- `h=2` specialization versus the edge-based formulation;
- relabeling and disjoint-union metamorphic tests;
- overflow detection.

Randomized tests must log the seed and write a minimized reproducer on failure.

## Baseline and licensing rules

- Pin every baseline to a commit hash and record its license before compiling it.
- Do not copy source from a baseline into the proposed solver unless the license permits it and attribution is recorded.
- Prefer wrapper/adaptor code around an unmodified baseline.
- Keep baseline patches minimal, reviewable, and stored as patch files.
- Never compare an approximate method as though it were an exact LhCDS solver.
- Never compare `h=2` or `h=3`-only methods as though they support arbitrary `h`.

## Experiment integrity

- Use the same normalized input graph for all algorithms.
- Record compiler, flags, CPU, memory, OS, thread count, commit hashes, command, timeout, and seed.
- Report both end-to-end time and solver-only time when available.
- Record peak RSS, output hashes, exact densities, and timeout/OOM status.
- Run algorithms in randomized order and report medians plus dispersion, not only the best run.
- Do not discard completed slow cases or failed cases from aggregate statistics.

## Documentation duties

For each completed task:

- update `docs/TASKS.md`;
- update `docs/CLAIM_TRACEABILITY.md` when code or tests implement a theorem-dependent claim;
- update `docs/DECISIONS.md` for any new semantic or engineering decision;
- update `docs/REPRODUCIBILITY.md` when commands or dependencies change.

## Completion report format

End each substantial Codex task with:

1. Summary of behavior implemented or changed.
2. Files changed.
3. Commands run.
4. Test and benchmark results.
5. Correctness evidence.
6. Remaining risks or unanswered decisions.

Do not claim success when tests were skipped. State exactly what was and was not run.
