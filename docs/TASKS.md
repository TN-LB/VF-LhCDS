# Task Tracker

Revision: 2026-09-09. `[ ]` means implementation evidence is still outstanding.
Document review and `review/math_sanity.py` do not complete these tasks.
Each task must link its command/log/seed evidence before being checked off.

## M0 - Freeze contracts and bootstrap (prompt 00)

- [x] P00.1 Preserve the four proof/reference files and record SHA-256 snapshots; retain D005 and D012. [Evidence](../evidence/m0/REPORT.md): owner confirmed no earlier snapshot existed; initial snapshot now recorded, all four match HEAD and pass before/after SHA-256 verification. D006 also unchanged.
- [x] P00.2 Review `THEORY_TO_CODE_AUDIT.md` obligations O01-O12 and revised decisions; flag only genuinely new semantic choices. [Evidence](../evidence/m0/REPORT.md): no new conflict; no theory/decision changes or second audit.
- [x] P00.3 Create C++17/CMake and independent Python layouts; warnings, CTest, pytest, sanitizer targets. [Executed commands/logs](../evidence/m0/checks/commands.json): Debug, ASan+UBSan, Release, RelWithDebInfo build and pass 3/3 CTest each; standalone pytest 1 passed.
- [x] P00.4 Freeze canonical input/output contracts, error statuses, fixed-k order, and minimal timing/counter definitions. [Frozen contract](INTERFACE_CONTRACT.md), [scope/evidence](../evidence/m0/REPORT.md); future algorithm behavior is documented, not implemented.

Gate: contracts are explicit and the skeleton commands actually run. No solver code yet.
M0 gate met on 2026-09-09. Later milestone statuses are recorded below.

## M1 - Independent exhaustive truth (prompt 01; needs M0)

- [x] P01.1 Combination clique enumeration, ordinary connectivity, `mu_h`, deletion loss, exact compactness. [M1 tests/evidence](../evidence/m1/REPORT.md): T01 and independent induced-combination counts across the declared reference tier.
- [x] P01.2 Direct LhCDS maximality over ALL proper supersets; test multi-vertex-extension witness T02. [Evidence](../evidence/m1/REPORT.md): bridged triangles plus definition/parametric component and hierarchy-leaf comparisons.
- [x] P01.3 Exhaustive largest `F_h(lambda)` including empty maximizers and zero lambda. [Evidence](../evidence/m1/REPORT.md): union-of-all-ties, signed exact objective, empty/equality/zero and explicitly restricted results.
- [x] P01.4 Independent cardinality-line chain; exact intersections/midpoints; outer-density witness T03. [Saved witness](../reference/fixtures/outer_breakpoint.json), [evidence](../evidence/m1/REPORT.md); prior review fixture was absent, so this is a documented new reconstruction.
- [x] P01.5 Canonical fixtures/generators and hard size guard; no imports from production. [Reference usage](../reference/README.md), [fixtures/seeds](../evidence/m1/fixture_manifest.json), [CLI/pytest logs](../evidence/m1/final/commands.json); default n<=12, explicit local override.

Gate: T01-T03 fixtures and the declared truth tier pass; no claim of production correctness.
M1 gate met on 2026-09-17: 74 pytest tests; 2,198 exhaustive-small graph/h cases
(1,099 distinct graphs), plus 100 seeded graph/h cases (96 distinct graphs).
This is reference-only evidence. All M2+ tasks remain open.

## M2 - Exact primitives (prompts 02, 03; needs M0 and M1 for integration)

- [ ] P02.1 Preserve declared vertices; canonical graph and reversible original-ID mapping.
- [ ] P02.2 One deterministic materialized h-clique/incidence backend; differential enumeration T04.
- [ ] P02.3 Exact fractions/counts and checked 128-bit operations; arbitrary-precision path end to end, T05.
- [ ] P03.1 Aggregate residual footprints; all-subset identity T06.
- [ ] P03.2 Generic exact Dinic with 128-bit and arbitrary-precision instantiations; residual-cut tests T07.
- [ ] P03.3 Restricted-closure API plus certified-global wrapper; empty/equality/zero cases T08.
- [ ] P03.4 Preserve `L=N+1` cardinality tie term; exact largest-set differential campaign T09.
- [ ] P03.5 Minimal standalone oracle reproducer and logical-query/mincut counters.

Gate: true global comparisons only use certified bounds; fallback runs rather than merely reporting overflow.

## M3 - Solver and correctness freeze (prompts 04-06, 13; needs M1+M2)

- [ ] P04.1 Immutable principal-chain endpoints and exact outer lambda; separator invariant T10.
- [ ] P04.2 Left-first traversal, original-endpoint terminal test, ordinary-edge leaf extraction T11.
- [ ] P04.3 Fixed-k lexicographic ordering and stop; reject k=0; support k>q and full mode, T12.
- [ ] P04.4 Full run counts: exactly `2r-1` logical interval queries; mincut count reported separately T13.
- [ ] P05.1 Exhaustive/seeded differential tiers, saved failures and deterministic minimizer T14.
- [ ] P05.2 Tie-aware relabeling, isolates, disjoint-union and input-order properties T15.
- [ ] P05.3 ASan/UBSan and numeric boundary suite; no candidate verifier in solver call path T16.
- [ ] P06.1 Minimal canonical CLI/JSON output, timing boundaries, manifests, stable semantic hash.
- [ ] P13.1 Record code symbols + test evidence in traceability and tag the unoptimized correctness release.

Gate: no known semantic mismatch or silent overflow; no streaming/tie-inclusive/baseline requirement.

## M4 - Optional optimization (prompts 07, 08; needs M3)

- [ ] P07.1 Exact clique-core peeling; one update per invalidated clique.
- [ ] P07.2 Query-local `Y_oracle` only; original lambda, endpoints and extraction graph unchanged, T17.
- [ ] P07.3 Written containment argument + off/on equality + separate reduction-cost measurements.
- [ ] P08.1 Profile first; select ONE justified optimization and provide equivalence argument, switch and regression.

Backlog, not the initial release gate: streaming, singleton folding, alternative flow algorithms,
oracle-result caches, component scheduling, parallel enumeration, tie-inclusive output.

## M5 - Baselines, experiments and release (prompts 09, 09b, 10-12, 14-15)

- [ ] P09.1 IPPV: pin commit/license; build; audit output, parameters, preprocessing and timing.
- [ ] P09b.1 DCLDS: preserve D012 freeze boundary; add explicit primary-baseline adapter/audit; no technique import.
- [ ] P10.1 Audit only specialization baselines relevant to intended h=2/h=3 claims; record unavailable/excluded methods.
- [ ] P11.1 Separate definition-checked, structural-checked and cross-implementation-agreement evidence.
- [ ] P11.2 Freeze graph checksums, parameter grid, timeout/memory/thread policy and phase timing in config.
- [ ] P11.3 Run a shared validated smoke configuration before the full suite.
- [ ] P12.1 Runtime/RSS/time-to-result, k/h sensitivity and enabled-feature ablations; retain failed/censored runs.
- [ ] P14.1 Review conclusions against available direct baselines and validation/timing scope.
- [ ] P15.1 Regenerate results from immutable manifests; clean-machine smoke; reproducibility package.

Gate: traceable evidence, not a predetermined speedup or SOTA outcome.
