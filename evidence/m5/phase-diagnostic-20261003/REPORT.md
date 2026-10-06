# M5 phase diagnosis — 2026-10-03

The authorized phase diagnostic is complete. On the unchanged normalized
CA-GrQc graph (h=3,k=5), parsing completed in **0.0038615 seconds**. The
materialized index constructor was entered and had not returned when the
predeclared 60-second process guard killed the child. **The solver phase was not
reached.** This is a measured boundary observation from this separate diagnostic,
not a retrospectively invented phase trace for earlier failed runs.

P11.2/P11.3/O12 gain scoped diagnostic evidence; the shared real smoke and M5 are
still incomplete. No production enumeration change, completed real output,
comparative speedup, theorem proof or new mathematical conflict is claimed.

## Scope, implementation and input

The owner's "继续" approved the prior [phase proposal](../m4-mode-diagnostic-20261003/NEXT_STEP.md).
[Authorization](accepted/authorization.json), [configuration](accepted/config.json)
and [environment](accepted/environment.json) were saved before native runs.
One real input, one basic-mode invocation, one worker, 60-second timeout, no
imposed memory cap and uncontrolled cache were retained. The single deterministic
case has no randomized schedule; seed is explicitly null, not an unrecorded
choice. Two fixed tiny fixtures verify the new instrumentation before the real run.
No final benchmark policy is selected.

New target `vflhcds_phase_probe` in `experiments/phase_probe` links the **existing**
Release `libvflhcds_lib.a`. `main` calls unchanged parsing, `MaterializedCliques`,
`solve` and `solution_json`; `mark` flushes monotonic begin/end JSONL events for
parse, index, solve and serialize. Basic settings are explicit: core off, sorted
footprints, automatic exact capacities. There is no added candidate verifier.
The probe's stderr is a separate diagnostic format, not the production status
schema. Production code, executable, static library, headers and reference remain
unchanged. The probe uses the same compiler, -O3, C++17 and strict warning flags.

CA-GrQc: n=5,242, m=14,484, all declared vertices retained. Graph SHA-256:
`85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32`.
The [raw input copy](accepted/real/graph.txt) matches the previously normalized
input. Probe SHA-256:
`cf2de3eb7e643305faeb26784b5d6833dbb3ce33ac54f74a3e64f08d158b8e80`.
Linked library SHA-256:
`58695a9b5abb4b72cd400ddfa6ba9f2eaabb4cc51690f5fe8233db99b9f78031`.
Full pins and link/compile commands are in [probe provenance](accepted/probe-provenance.json).

## Actual commands and results

From the repository root:

```sh
.venv/bin/python evidence/m5/phase-diagnostic-20261003/run_diagnostic.py
.venv/bin/python evidence/m5/phase-diagnostic-20261003/verify_evidence.py
git diff --check
```

The driver invokes exactly two [CMake commands](accepted/build-commands.json):

```sh
.venv/bin/cmake -S experiments/phase_probe -B build-m5-phase-probe -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS= -DCMAKE_CXX_COMPILER=/usr/bin/c++ -DVF_LIBRARY=/Users/nost/Documents/VF-LhCDS/build-m5-release/libvflhcds_lib.a
.venv/bin/cmake --build build-m5-phase-probe -j2
```

Both configure and build exit **0**. Only the new probe is compiled and linked;
the original library is not rebuilt. The recorded commands contain resolved
absolute paths. Native and external-validator commands, resources, timestamps and
exit statuses are preserved in each `process.json` under [accepted](accepted/).

T-PHASE-01 passes on **2/2** fixtures at h=3,k=5:

| Fixture | Declared vertices | Exact output count | Markers | Result |
|---|---:|---:|---:|---|
| triangle_and_isolate | 4 | 2 | 8 | zero-density isolate retained; production bytes identical; independent definition check passes |
| bridged_triangles | 6 | 1 | 8 | complete ordered phase markers; production bytes identical; independent definition check passes |

The [smoke results](accepted/smoke-results.json) retain four successful native
children (two probes, two production calls) and two successful external definition
validators. Validation is after native completion with separate time/RSS; reference
code does not call production. These finite checks validate this instrumentation,
not the full algorithm or mathematical theorem.

T-PHASE-02 preserves the real timeout and its flushed markers:

| Boundary | Elapsed seconds from probe main entry |
|---|---:|
| parse begin | 0.000080792 |
| parse end | 0.003942292 |
| index begin | 0.003960667 |
| index end / solve begin | not reached before termination |

The [real process](accepted/real/process.json) has status **timeout**, exit **-9**
(SIGKILL by the timeout runner), wall **60.005256165750325 s**, user CPU
**59.213713 s**, system CPU **0.24073699999999998 s**, peak RSS **4,947,968 bytes**.
Stdout is empty. [Stderr](accepted/real/stderr.txt) contains exactly the three
markers above. No real external validation or output agreement was possible.
No OOM is inferred. Time/RSS describe a truncated instrumented run, not a completed
algorithm run or a formal comparison against IPPV.

The overall [driver](command.json) exits **1**, preserving that unsuccessful
native outcome, after **63.10174912493676 s** including build and smoke work.
Its stderr is empty; the exit is not a driver exception. The integrity verifier
exits **0** and [verification.json](verification.json) records passed assertions
for markers, outputs, native results, all raw hashes, source snapshots, the 53
accepted M4 source hashes, four papers, original executable and library.
`git diff --check` exits **0**.

## Consequence and prepared next change

The constructor still visits all size-h combinations: C(5242,3) equals
23,993,367,880 candidate triples. The diagnostic confirms that index construction
is the immediate blocker at this budget. Both existing M4 switches act after
that constructor. It does **not** establish how long indexing would take to
finish or whether a later solver bottleneck exists.

The [enumeration proposal](ENUMERATION_PLAN.md) is now concrete: retain one
materialized backend and the old combination path; introduce an explicit
adjacency-extension selector; generate only prefixes that remain cliques using
sorted common-neighbor intersections; preserve exact tuple order, incidence IDs,
counts and downstream semantics. It includes its invariant, uniqueness/order
argument, file scope and T04/T06-T17 Debug/Release/sanitizer equivalence gates.
The design is derived from the clique definition and this repository's graph
representation, without reading or importing DCLDS or IPPV techniques.

The proposal is unimplemented. Work stops at the measured blocker under the
owner's stop-on-blocker instruction; the authorized diagnosis and repair-plan
preparation are complete. No runtime limit, algorithm default or final dataset
policy was silently changed.

## Environment, changes and unrun work

Same host: macOS 15.7.7 arm64, Apple M1, 8 physical/logical cores, 16 GiB RAM,
Python 3.12.2, Apple Clang 17.0.0.17000603, CMake 4.4.3, existing Boost 1.86.0.
Hardware is the copied earlier same-host reading, not a newly measured value.
The root HEAD remains `56229397903813d3509ecb45b178bbde823e357b` with preexisting
uncommitted M5 work. No dependencies were acquired or installed.

Changed symbols: diagnostic `mark`, `main`, evidence `run_diagnostic.main` and
`verify_evidence.main`; production symbols are only called, never edited.
Added `experiments/phase_probe/{CMakeLists.txt,main.cpp,README.md}` and this evidence
directory; updated `experiments/README.md`, `docs/TASKS.md`,
`docs/CLAIM_TRACEABILITY.md`, and `evidence/m5/REPORT.md`. The
[turn-specific file manifest](files_changed.json) lists paths and hashes.

Unrun: enumeration repair, new semantic optimization equivalence campaign, full
CTest/pytest/sanitizer regression, completed real VF/IPPV comparison, final
benchmarks, DCLDS work and clean-host release reproduction. The prior 112 pytest
passes are not claimed as a rerun. M5/P11 completion boxes remain open.
