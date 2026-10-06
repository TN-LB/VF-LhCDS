# Authorized adjacency enumeration — 2026-10-03

The bounded enumeration repair is complete. The same CA-GrQc h=3,k=5 diagnostic
that previously timed out now finishes in **0.767723375 s**, returning five
structurally checked results that strictly match the saved IPPV output. The
original combination mode remains the default; enable the new implementation
explicitly with `--clique-enumeration adjacency`. M5 as a whole remains incomplete.

## Implementation and scope

The owner approved the [specific preservation/change plan](../phase-diagnostic-20261003/ENUMERATION_PLAN.md)
with "是，继续". [Before-edit hashes](before.json), saved original sources and the
[named test plan](PLAN.md) precede production edits. No DCLDS reading or imported
external algorithm technique is involved. Papers, accepted decisions, algorithm
specification, audit and independent reference are unchanged.

`CliqueEnumeration` selects `Combinations` (default/control) or `Adjacency` within
the one existing materialized backend. `MaterializedCliques::enumerate_adjacency`
extends increasing clique prefixes using sorted common-neighbor intersections.
An explicit stack avoids adding a recursive call-stack limit; exact cardinality
checks stop branches that cannot reach h. Shared `append` preserves clique IDs
and incidence ordering. The old loop is retained in `enumerate_combinations`.

The [implementation argument](../../../docs/ENUMERATION_IMPLEMENTATION.md) states
the invariant, soundness/completeness/unique-order reasoning, preconditions and
temporary-buffer cost. No semantic decision uses floating point. h>|V| returns
before size_t conversion; all declared vertices and zero-density behavior remain.
No oracle, flow, core reduction, recursion, extraction or serializer code changed.

CLI `operation` validates/passes the new selector for solve and oracle. The
external `load_config`/`run_vf` accept optional `options.enumeration`, preserve old
configuration meaning, and record explicit choices in actual native commands.
No canonical schema/hash, fixed-k ordering, error code, timing boundary or query
counter definition changes. Runtime mode selection is explicit, never heuristic.

Test-only `checked_adjacency_index` constructs both representations and compares
ordered tuples/incidence IDs before returning adjacency for existing M2/M3/M4
probe queries. Expected mathematical truth still comes from the unchanged Python
combination/direct-definition/line-envelope reference. The existing campaign
drivers and frozen seeds are reused without edits.

## Executed checks

Primary commands, from the repository root:

```sh
.venv/bin/cmake -S . -B build-enumeration-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS= -DPython3_EXECUTABLE=/Users/nost/Documents/VF-LhCDS/.venv/bin/python
.venv/bin/cmake --build build-enumeration-debug -j2
.venv/bin/ctest --test-dir build-enumeration-debug --output-on-failure -V
.venv/bin/python -m pytest experiments/test_harness.py baselines/ippv/test_adapter.py reference/tests -q
.venv/bin/python evidence/m5/enumeration-20261003/run_acceptance.py
.venv/bin/python evidence/m5/enumeration-20261003/verify_acceptance.py
.venv/bin/python evidence/m5/enumeration-20261003/run_real.py
```

The [four initial commands](dev/commands.json) all exit 0. Debug CTest is
**14/14**, **8.52 s**; combined pytest is **115 passed in 4.25 s** (24 harness,
17 adapter, 74 reference). T04-CLI executes 121 invocations. T04-ADJ/T04-EDGE
cover order, exact incidence IDs, all-subset counts, large original IDs, zero and
arbitrary-precision h>|V|, depth-128 traversal and actual automatic big-capacity flow.

The [acceptance driver](accepted/commands.json) executes **23/23 commands, exit 0**:
14 differential campaigns, sanitizer/Release builds and CTest, production-only
Release build driver, paper verification and whitespace check. Its production
build driver separately records [two successful CMake commands](accepted/production-build/commands.json).
Full exact argv, UTC timestamps, stdout/stderr names and SHA-256 values are in
the manifests. `accepted/planned-commands.json` was saved before execution.

| Build profile | Configure/build | CTest |
|---|---|---|
| Debug | exit 0 / 0 | 14/14 |
| Debug + ASan/UBSan | exit 0 / 0 | 14/14 |
| Release | exit 0 / 0 | 14/14 |
| Production-only Release | exit 0 / 0 | intentionally no test targets |

All profiles use C++17 and -Wall/-Wextra/-Wpedantic/-Wconversion/-Wsign-conversion/
-Wshadow/-Werror. Sanitizer commands include address+undefined, nonrecoverable
errors and frame pointers. There are no sanitizer findings. Existing numeric
limit tests and nontrivial automatic arbitrary-precision executions pass.

Each of Debug and sanitizer executes these unchanged corpus tiers:

| Campaign family | Smoke | Exhaustive-small | Seeded | Higher h |
|---|---:|---:|---:|---:|
| M3/M4 truth plus four core/footprint modes | 31 | 2,198 | 1,000 | 64 |
| M2 exact clique/footprint/global/restricted oracle | covered by CTest | 2,198 | 1,000 | 72 |

Seeds remain 20260929 for solver/M4 and 20260922 for M2; exhaustive-small is all
labelled n=1..5 graphs at h=2,3. Higher-h/named, all-prefix, relabeling and derived
fixture records are in [fixture-manifest.json](fixture-manifest.json) and each
`cases.jsonl`; these counts refer to base graph/h cases, not unique datasets.

The [verifier](verification.json) passes: all **1,392,496** response records in
the 14 new campaigns equal the corresponding saved pre-change M4 responses.
Inputs also match byte-for-byte. Only `core_reduction_seconds` is excluded from
this comparison; mathematical outputs, query traces, counters and backend fields
remain included. [Comparison digests/counts](cross-version-comparisons.json)
retain per-campaign evidence. There were no failing seeds or new reproducers.
These are finite implementation/equivalence checks, not a theorem proof.

## Real diagnostic

The [configuration](real-config.json) and [comparison plan](comparison-plan.json)
were frozen after correctness gates and before launch. Graph: the original
normalized CA-GrQc, 5,242 declared vertices, 14,484 edges, SHA-256
`85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32`.
h=3,k=5, one repetition, one worker, seed 20261003, 60-second native/validation
guard, no imposed memory cap, uncontrolled cache; core off, footprints sorted,
enumeration adjacency. No dataset, resource limit or final benchmark policy changed.

New production binary SHA-256:
`8a8252e31156a75899aa758ba1e357953d1dfee9914287d9970c5f67b921b4f8`.
Source/compiler flags and binary hash are in
[production provenance](accepted/production-build/provenance.json).

The [native process](real/runs/0000-0/process.json) exits **0**:

- wall: **0.7677233750000596 s**; user: **0.7497729999999999 s**;
  system: **0.012157 s**; peak RSS: **48,758,784 bytes**;
- output count: **5**, termination: **k_reached**;
- **48,260** cliques enumerated, **627,380** clique records scanned,
  **13** logical interval queries and **13** mincuts;
- postload: **0.757203709 s**; postindex/core: **0.751462334 s**. The difference
  includes indexing and intervening CLI setup; it is not labelled a pure index timer.

The separate [external validator](real/runs/0000-0/validation/process.json) exits
**0** in **0.1077544167637825 s**. All canonical schema, exact clique count/density,
connectivity, rank/tie order, completion and native semantic-hash checks pass.
Its time/RSS is excluded from the native measurements.

The five [canonical records](real/runs/0000-0/canonical_output.jsonl) have semantic
SHA-256 `c33ccb405e263ae7fcf10f60585c8441dbc821bbc1f7958ba4dd828ac0cf797f`.
They [strictly and tie-aware match](real-comparison.json) the preserved IPPV
five-patch output from the same graph/h/k. This is structural checking and
cross-implementation agreement; maximality/completeness is not independently
exhaustively certified on this real graph. IPPV was not rerun this turn, so its
historical timing is not used as a paired performance comparison.

All earlier timeouts remain recorded, never replaced or relabelled. No speedup
factor can be inferred from a censored old runtime, and one local successful run
does not establish broad scalability. The immediate enumeration blocker is
resolved for this case; no new blocking conflict was found in the authorized work.

## Files, environment and remaining work

The [turn-specific file manifest](files_changed.json) lists exact paths/hashes.
Production changes: the materialized header/implementation and CLI dispatch.
Build/tests: CMake, `enumeration_equivalence.hpp`, `clique_enumeration.cpp`,
`enumeration_cli.py`, M2/M3 probes and external harness/tests. Documentation:
architecture, interface, build, enumeration argument, tasks/traceability,
experiment/phase-probe READMEs and M5 report. Evidence includes original/new source
snapshots, driver scripts, configs, command logs, fixture/response files and checksums.

Environment: macOS 15.7.7 arm64, Apple M1, 8 physical/logical cores, 16 GiB RAM,
Apple Clang 17.0.0.17000603, CMake 4.4.3, Python 3.12.2, pytest 8.4.2 and the
existing Boost 1.86.0. No dependency was added or downloaded. HEAD remains
`56229397903813d3509ecb45b178bbde823e357b`; changes are uncommitted. Four papers,
the reference and all 32 protected paths match the before snapshot. Of the 53
original M4 code paths, six authorized paths changed and 47 are unchanged.
Old M5 executable/library and all historical raw runs remain preserved.

Unrun: a fresh paired VF/IPPV campaign, final dataset/h/k/resource/repeat/cache
configuration, general scalability/speedup conclusions, broader baseline audits,
DCLDS work and clean-host release reproduction. No parallel execution was added;
TSan remains deferred. M5 and full experimental gates are not marked complete.
