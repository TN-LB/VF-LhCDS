# Task Tracker

## Phase 0 — semantics and repository

- [ ] Initialize Git and CMake/Python layouts.
- [ ] Add formatting, lint, test, and sanitizer targets.
- [ ] Populate baseline audit with commit and license status.
- [ ] Create initial claim traceability map.

## Phase 1 — exhaustive reference

- [ ] Graph parser/normalizer.
- [ ] Combination-based h-clique enumeration.
- [ ] Exact `mu_h`, density, deletion loss.
- [ ] Exact connectedness and lambda-compact checker.
- [ ] Exhaustive maximality and LhCDS enumeration.
- [ ] Exhaustive largest `F_h(lambda)`.
- [ ] Principal-chain generator for tiny graphs.
- [ ] Random/synthetic graph generators.
- [ ] Truth fixture format and CLI.

## Phase 2 — C++ foundation

- [ ] Graph CSR/sorted adjacency.
- [ ] ID mapping and checksums.
- [ ] Canonical vertex set and membership markers.
- [ ] Exact fraction and checked integer utilities.
- [ ] Degeneracy ordering and fixed-h clique enumerator.
- [ ] Materialized clique/incidence index.
- [ ] Streaming backend interface.
- [ ] C++ versus Python clique/count tests.

## Phase 3 — exact oracle

- [ ] Footprint key and aggregation.
- [ ] Residual-footprint identity tests.
- [ ] Generic max-flow interface.
- [ ] Dinic exact-capacity backend.
- [ ] Closure network constructor.
- [ ] Source-side extraction.
- [ ] Oracle CLI reproducer.
- [ ] Exhaustive oracle differential campaign.
- [ ] Dedicated largest-maximizer tie fixtures.

## Phase 4 — top-k solver

- [ ] Outer-density exact computation.
- [ ] Interval data structure and `mu_h` cache.
- [ ] Left-first recursive/iterative traversal.
- [ ] Terminal connected components.
- [ ] Anti-adjacency test to `X`.
- [ ] Deterministic fixed-k ordering.
- [ ] Tie-inclusive optional mode.
- [ ] End-to-end exhaustive differential tests.

## Phase 5 — correctness release candidate

- [ ] Randomized campaign with saved seeds.
- [ ] Metamorphic tests.
- [ ] Failure minimizer.
- [ ] ASan/UBSan runs.
- [ ] Overflow boundary tests.
- [ ] Freeze regression corpus.
- [ ] Tag correctness release candidate.

## Phase 6 — optimization

- [ ] Add detailed telemetry.
- [ ] `mu_h` and oracle cache.
- [ ] Safe h-clique-core reduction.
- [ ] Footprint/network reductions.
- [ ] Allocation reuse.
- [ ] Alternative exact flow backend.
- [ ] Component-wise processing.
- [ ] Parallel enumeration only after TSan/determinism checks.
- [ ] Full ablation switches.

## Phase 7 — baselines

- [ ] IPPV author-code build and adapter.
- [ ] LDS-Opt/LDS-DC code availability decision.
- [ ] LDScvx build and adapter.
- [ ] LTDScvx code availability decision and adapter.
- [ ] LDSflow and LTDSflow feasibility.
- [ ] DCLDS provenance and algorithm audit.
- [ ] Canonical output validator.
- [ ] Shared toy-instance agreement report.

## Phase 8 — experiments and release

- [ ] Dataset download/preparation manifest.
- [ ] Normalized checksums and clique statistics.
- [ ] Smoke suite.
- [ ] Main runtime/memory suite.
- [ ] k and h sensitivity.
- [ ] Scalability suite.
- [ ] Ablation suite.
- [ ] Raw manifest validation.
- [ ] Aggregation and plots.
- [ ] Correctness, performance, and reproducibility reviews.
- [ ] Release tag and artifact.
