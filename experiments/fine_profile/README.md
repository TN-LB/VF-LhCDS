# Exclusive phase diagnostic

This is P12.1/O12 profiling, not a new solver mode or an optimization. Production
files and the existing Release binary/library remain untouched. `instrument.py`
checks two source hashes and unique insertion anchors, then generates copies in
the diagnostic build directory. Removing its added include/timer lines recovers
every original byte. CMake reuses the root source list, C++17, strict warnings,
Boost and sanitizer options in a separate build tree.

The inserts only observe a monotonic clock and update a separate single-threaded
collector. They neither read nor change graph sets, capacities, return values,
branches, ordering or solver counters. `Scope` pauses its parent while a child
is active and restores it on normal return and exception. A deterministic fake-
clock test checks nesting, phase transitions, partial snapshots and unwinding.
These checks plus output/counter agreement validate instrumentation; they do not
prove the theorem. Parallel execution is unsupported.

The executable takes `GRAPH H K` and fixes the already implemented adjacency
enumerator, membership footprints, core off and automatic exact capacity backend.
Canonical solutions go to stdout. Flushed phase/query events and final counters
go to stderr; this diagnostic JSONL is not the production status interface.

| Exclusive solve bucket | Boundary |
|---|---|
| `count` | Entire `MaterializedCliques::count`, including set validation and exact accumulation; covers both new chain points and emitted components |
| `footprints` | Entire `aggregate_footprints`, including markers, full clique scan, map aggregation and local cleanup |
| `oracle_other` | Remaining `restricted_impl`: validation, interval construction, capacity preflight/counters and footprint cleanup, excluding nested buckets |
| `network_build` | `execute` entry through network creation, arcs and backend counters |
| `max_flow` | Only `Dinic::max_flow` |
| `cut_extract` | Residual reachability, vertex extraction and sorting |
| `network_cleanup` | Return from `execute`, including destruction of network/local buffers |
| `trace` | Completed-query serialization and flushing; current event snapshots include only the elapsed prefix of their own trace |
| `solver_other` | Remaining solve orchestration, set operations, terminal components and ordering, excluding nested buckets |

Buckets do not overlap and sum to measured solve time up to the outer timer
boundary overhead. Their call counts are timer entries, not replacement semantic
counters. Parsing/indexing/serialization use separate outer markers. A timeout
retains only completed-query snapshots; time after the last snapshot is unknown
and must not become a complete-run percentage. Instrumentation changes code
layout and adds clock/trace costs. One fresh production control per diagnostic
gives a rough overhead check, not a performance distribution or a VF/IPPV result.

Build (from the repository root):

```sh
.venv/bin/cmake -S experiments/fine_profile -B build-m5-fine-profile-release -DCMAKE_BUILD_TYPE=Release -DPython3_EXECUTABLE="$PWD/.venv/bin/python"
.venv/bin/cmake --build build-m5-fine-profile-release --target vflhcds_fine_profile profile_timer_test -j2
.venv/bin/ctest --test-dir build-m5-fine-profile-release --output-on-failure
```

For tiny sanitizer checks, use a separate Debug directory and
`-DVFLHCDS_ENABLE_SANITIZERS=ON`. Do not use sanitizer timings as Release profiles.
The frozen execution/fixture manifest and actual commands live under
`evidence/m5/fine-profile-20261007/`.
