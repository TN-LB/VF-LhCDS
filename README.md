# VF-LhCDS: Proof-Aligned Implementation Kit

Revised 2026-09-29. This repository contains the exact basic solver, independent
reference and staged implementation/evaluation plan. The four supplied files under `papers/` are unchanged.

Current status (2026-10-14): M0–M4 and bounded M5 remain complete under D042.
D043 schedules **M6 data/tool preparation and M7 unified formal experiments on
eight real graphs**, within four additional weeks excluding thesis writing.
[Current M6/M7 plan and selected graphs](docs/M6_M7_EXECUTION_PLAN.md).
Both new milestones are planned; exact artifacts, host/resources and the executable
campaign package still need freezing before measurement. D039's solver optimization
stop and D029's DCLDS deferral remain in force.

The two-graph M5 timings and all other earlier local measurements are now
development/preliminary evidence relative to M7. They remain preserved, but cannot
enter M7 formal performance results or ablations. See
[historical measurements and limits](evidence/m5/REPORT.md),
[M5 completed scope](docs/M5_COMPLETION_PLAN.md) and
[historical reproduction](docs/M5_REPRODUCTION.md).

For a plain-language Chinese overview of the milestones, results and limits, see
[项目总体报告（中文核对版）](docs/PROJECT_REPORT_ZH.md).

## Start here

1. `docs/IMPLEMENTATION_PLAN.md`: completed M0–M5 and planned M6/M7; `docs/M6_M7_EXECUTION_PLAN.md`: current four-week scope.
2. `docs/ALGORITHM_SPEC.md`: executable mathematical contracts.
3. `docs/THEORY_TO_CODE_AUDIT.md`: exact theorem numbers, proof obligations and clarifications.
4. `docs/TASKS.md`: dependency-aware tasks and executed milestone gates.
5. `docs/CORRECTNESS_TEST_PLAN.md`: independent truth and concrete test IDs.
6. `docs/PLAN_REVIEW.md`: review findings, changes and the scope of work actually checked.

The primary source is `papers/veri_free_lhcds_v3_1_submit.md`. The other supplied
papers are h=2/theory-organization and baseline references. See `AGENTS.md` for
source priority and decision rules. Accepted D005 (real exact fallback), D006
(original-ID set ordering) and D012 (independent parallel DCLDS study) remain.

## Proof-to-code route

```text
M0 contracts and skeleton
 -> M1 direct exhaustive truth + independent principal chain
 -> M2 graph/cliques + exact footprint closure oracle
 -> M3 left-first fixed-k solver + correctness freeze
 -> M4 optional safe query-local core/profiled optimization
 -> M5 validated baselines + fair experiments + reproducible release
 -> M6 eight-graph data + Linux experiment tooling + configuration freeze
 -> M7 unified formal measurements + reproducible result artifacts
```

M3 requires one materialized clique backend, aggregated footprints, and one generic
Dinic algorithm with checked-128 and arbitrary-precision execution. Streaming,
extra flow algorithms, tie-inclusive output and parallelism are deferred.

Core reduction only shrinks an oracle search bound; it never replaces a recursive
chain endpoint or the original lambda. Standalone global oracle queries may return
empty; the strict-progress invariant belongs to recursive separator queries.
Preserve all declared vertices and zero-density solutions.

## Baselines and evidence

DCLDS and IPPV are the original general-h comparison targets. D029 currently
defers all further DCLDS reading/acquisition/integration; M6/M7 compare VF with IPPV.
h=2/h=3 specialization comparisons remain outside this bounded plan. Preserve
D012's independent-development boundary and historical snapshots.

Small-graph direct-definition truth, structural output checks and agreement between
implementations are distinct evidence levels. No test campaign alone is a proof,
and no fixed-h polynomial bound establishes practical scalability or speedup.

## Repository layout

M0 provides the C++17/CMake skeleton, M1 the independent exact Python reference,
M2 the exact graph/clique/flow oracle, and M3 the basic fixed-k solver. Read
[build instructions](docs/BUILD.md), [wire contracts](docs/INTERFACE_CONTRACT.md),
[M3 APIs and timing](docs/M3_IMPLEMENTATION.md), and
[executed M3 evidence](evidence/m3/REPORT.md). The C++ CLI supports `solve --k K`,
`solve --all`, `oracle`, `inspect-graph`, help and build-info. M4 adds optional
`--core-reduction safe` and `--footprint-scan membership`; defaults remain off/sorted.
See [M4 preservation arguments](docs/M4_IMPLEMENTATION.md) and
[executed M4 evidence](evidence/m4/REPORT.md).

```sh
build/vflhcds solve --graph reference/fixtures/bridged_triangles.graph --h 3 --all
```

For direct-definition truth and independent principal chains, see
[reference usage](reference/README.md). The M1 reference remains independent and
unchanged. M4 mode acceptance and bounded M5 completion are tracked in TASKS.

Plan material lives in `papers/`, `docs/` and `prompts/`; the initial paper hash
snapshot is in `review/`. Future work may add `tools/`, `configs/`, external
`baselines/` and immutable `results/`.
Keep external source trees, build products and dependency archives in ignored
directories. Curated executed evidence and normalized comparison inputs are
tracked under `evidence/` with their provenance; no new raw dataset is bundled.

Use `prompts/README.md` to select the next task. Each completion report names task
and obligation IDs, changed code, executed commands, seeds, actual evidence and
remaining limits. Do not claim a build/test succeeded because a command was listed.

## Review-only mathematical check

```text
python review/math_sanity.py --output review/math_sanity_results.json
```

This script independently checks tiny mathematical examples using exhaustive F;
it is not the production reference, flow implementation, fallback implementation,
sanitizer campaign or benchmark suite. Its results do not close M1-M3 tasks.
