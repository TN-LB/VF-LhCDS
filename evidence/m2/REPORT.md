# M2 completion report — 2026-09-22

P02.1–P02.3 and P03.1–P03.5 are complete at the declared M2 scope. No unresolved
proof/specification conflict or known oracle mismatch remains. No theory/decision
change was made. M3 and later milestones are not implemented or marked complete.
Finite implementation agreement is not a mathematical proof or performance claim.

Base commit: `1a4829a9348dae299ae074717928909598b11af6` (owner's committed M1).
M2 is an **uncommitted working tree**, identified by [source hashes](source_hashes.json)
and [changed-file manifest](files_changed.json); there is no new implementation
commit/tag. The traceability ledger consequently withholds its formal new-M2
`implementation-tested` label until a commit exists, while recording all executed
work. No baseline/DCLDS code or techniques were consulted/imported (D012).

## Individual task status and symbols

| Task | Status | Delivered behavior / main symbols |
|---|---|---|
| P02.1 | Complete | `Graph`, `VertexSet`, `Membership`, `normalize_graph`, `parse_graph`, `parse_set`, `canonical_graph`, `sha256`: explicit universe, arbitrary-size original IDs, reversible map, sorted adjacency, ordinary induced components, strict input and separate raw normalization |
| P02.2 | Complete | `MaterializedCliques`, `count`, `degree`, `incidence`: one deterministic materialized combination backend; exact counts, no MAX_H; h>n valid |
| P02.3 | Complete | `BigInt`, `Fraction`, `parse_integer`, `checked_add/sub/mul`, `scaled_objective`: reduced exact fractions, signed objectives, checked native boundaries and real arbitrary-precision execution |
| P03.1 | Complete | `aggregate_footprints`: exact multiplicities for every nonempty C minus X inside Y, including crossing cliques and singleton/repeated footprints |
| P03.2 | Complete | `Dinic<UInt128>` / `Dinic<BigInt>`, `max_flow`, `reachable`: one generic algorithm, explicit path stacks, exact residual capacities and checked native arithmetic |
| P03.3 | Complete | `RestrictedRequest`, private `CertifiedGlobalRequest`, `full_graph_request`, `largest_restricted`, `global_F`: scope separation and valid empty/equality/zero results |
| P03.4 | Complete | Closure capacity construction: L=N+1, exact minus-one cardinality tie term and finite infinity; complete largest-set differential checks |
| P03.5 | Complete | `run_cli`, `oracle_json`, `atomic_write`, `QueryStats`, `query_stats_json`: standalone oracle/inspection, reproducer inputs, status JSON, logical-query versus actual-cut telemetry |

Relevant obligations: O01 support; O03 largest-F support; O05 restricted/global;
O06 footprints/network/ties; O11 exact arithmetic; O09 standalone/network counters
only. The solver query-bound portion of O09 and all solver/core obligations remain
open. See [implementation contracts](../../docs/M2_IMPLEMENTATION.md).

## Changed files

The complete path/SHA-256 list is [files_changed.json](files_changed.json).
Main changes are:

- `include/vflhcds/core/{exact,graph}.hpp`, `src/core/{exact,graph}.cpp`.
- `include/vflhcds/clique/materialized.hpp`, `src/clique/materialized.cpp`.
- `include/vflhcds/flow/dinic.hpp`.
- `include/vflhcds/oracle/closure.hpp`, `src/oracle/closure.cpp`.
- `include/vflhcds/telemetry/query.hpp`, `src/telemetry/query.cpp`.
- `include/vflhcds/io/graph.hpp`, `src/io/{graph,sha256}.cpp`, `src/cli/dispatch.cpp`.
- `tests/{m2_primitives.cpp,m2_probe.cpp,cli_smoke.py}`,
  `validation/oracle_campaign.py`, `scripts/{fetch_boost.py,run_m2_checks.py}`.
- `CMakeLists.txt`, `.gitignore`, `README.md`, module/validation README files;
  `docs/{BUILD,DEPENDENCIES,M2_IMPLEMENTATION,TASKS,CLAIM_TRACEABILITY}.md`.
- `evidence/m2/`: predeclared scope, environment, inputs/results, command/exit/log
  manifests, development/failure logs, final evidence and preservation hashes.

The four papers, accepted decisions (including D005/D006/D012), architecture,
algorithm/audit/test-plan contracts and all 22 snapshotted M1 reference code/test/
fixture files are unchanged. [Preservation check](preservation_final.json): 39
protected entries unchanged; only the three expected engineering/evidence docs
in the starting snapshot changed. Four paper hashes pass the recorded snapshot
check. No reference import calls production code.

## Commands actually executed and environment

Environment: macOS 15.7.7 arm64, AppleClang 17.0.0.17000603, C++17, Python 3.12.2,
pytest 8.4.2, CMake/CTest 4.4.3. Existing `.venv` was activated. See
[environment](final/environment.json), [compiler invocations](compiler_commands.json)
and tool version logs `final/24.stdout`–`26.stdout`.

Boost.Multiprecision 1.86.0 headers were downloaded from the official archive,
SHA-256 verified and extracted with their BSL-1.0 license under ignored `.deps/`.
No compiled library/global install was added. [Pin/license](../../docs/DEPENDENCIES.md).
The first sandbox attempt failed DNS; the approved Python retry failed certificate
validation; the system-curl retry retained TLS verification and succeeded. All
three logs are retained (`dependency-fetch*.log`); final archive SHA-256 is
`1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b`.

The exact argv, timestamps, exits, stdout/stderr paths and hashes are in
[full-run commands](final/commands.json) and [final follow-up commands](io-final/commands.json).
The full driver was executed as:

```sh
. .venv/bin/activate
python scripts/run_m2_checks.py evidence/m2/final
```

It actually ran the following command families, not merely documented them:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j2
ctest --test-dir build --output-on-failure -V
python -m pytest reference/tests -q
cmake -S . -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DVFLHCDS_ENABLE_SANITIZERS=ON
cmake --build build-sanitize -j2
ctest --test-dir build-sanitize --output-on-failure -V
cmake -S . -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --build build-release -j2
ctest --test-dir build-release --output-on-failure -V
cmake -S . -B build-relwithdebinfo -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build-relwithdebinfo -j2
ctest --test-dir build-relwithdebinfo --output-on-failure -V
python scripts/verify_papers.py
git diff --check
```

For each probe `build/vflhcds_m2_probe` and `build-sanitize/vflhcds_m2_probe`, it
executed `python validation/oracle_campaign.py --probe <probe> --tier <tier>
--output <fresh-directory>` for **smoke, exhaustive-small, seeded and higher-h**.
All eight complete argv/output paths are retained in the command manifest.

After the I/O regression fix, all four profiles were reconfigured, rebuilt and
ran their complete CTest suite. The following additional production-only commands
also executed successfully:

```sh
cmake -S . -B build-production -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
cmake --build build-production -j2
build-production/vflhcds oracle --graph reference/fixtures/bridged_triangles.graph --h 3 --lambda 1/3
```

The last command returns exactly vertices [0,1,2,3,4,5], clique_count "2", global
scope, completed status, logical_interval_queries=0 and mincut_calls=1. The
production-only build has no Python discovery or test probe.

## Exact executed results

| Profile / test | Actual result | Final log |
|---|---|---|
| Debug configure/build/CTest | exit 0; 5/5 passed | `io-final/01`–`03.stdout` |
| ASan+UBSan configure/build/CTest | exit 0; 5/5 passed; no sanitizer findings | `io-final/04`–`06.stdout` |
| Release configure/build/CTest | exit 0; 5/5 passed | `io-final/07`–`09.stdout` |
| RelWithDebInfo configure/build/CTest | exit 0; 5/5 passed | `io-final/10`–`12.stdout` |
| BUILD_TESTING=OFF Release | configure/build/oracle exit 0 | `io-final/13`–`15.stdout`, `15.stderr` |
| Independent reference pytest | 74 passed in 2.61 s; exit 0 | `final/21.stdout` |
| Paper snapshot / final diff check | all four hashes match; exit 0 / exit 0 | `closing_checks.json` |

Each final CTest contains 1,458 runtime primitive checks (assertions remain active
in Release), 135 independent tiny-cut/backend runs, one 20,000-node path,
56 CLI invocations, the 28-case differential smoke and the independent reference
pytest suite. These are overlapping test invocations, not additional distinct
mathematical cases.

The same full campaigns passed in **both Debug and ASan+UBSan**:

| Tier | Graph/h cases | Distinct graphs | Oracle requests | Backend executions | Automatic BigInt flow executions |
|---|---:|---:|---:|---:|---:|
| Exhaustive-small n=1..5, h=2,3 | 2,198 | 1,099 | 40,591 | 119,575 | 2,198 |
| Seeded n=6..8, seed 20260922 | 1,000 | 870 | 12,000 | 35,000 | 1,000 |
| Higher-h incl. h=4,5,h>n | 72 | 67 | 1,053 | 3,087 | 72 |
| Smoke | 28 | 24 | 537 | 1,583 | 28 |

Counts in this table are **per build**, not totals across repeated runs; tiers
also overlap. Each query ran auto and forced BigInt, plus forced UInt128 when
safe or shortcut-only. Auto fallback on a huge rational executes real flow,
including nontrivial nonempty edge/tie examples; it is not just a constructor or
overflow exception test. The seeded tier includes exactly 200 graph/h cases per
random/planted/bridge/tied/disconnected family, 4,000 global and 8,000 explicitly
restricted requests. Backend repetitions are not extra distinct oracle requests.

Exhaustive-small checks all 4,140 independent-chain endpoint pairs, all 10,842
nested bound pairs across n<=4/h=2,3, 67,732 induced subset counts and 152,506
footprint subset identities. Seeded adds 148,288 induced-count comparisons and
251,828 footprint identities. Footprint checks cover every S for every tested
bound pair, with crossing, singleton and aggregated repeated footprints.

The [fixture/campaign manifest](fixture_manifest.json) links every summary,
`cases.jsonl`, and compressed exact request/expected/actual/counter stream.
Corresponding decompressed result streams are byte-identical across Debug and
sanitizers. All eight `probe.stderr` files are empty. No oracle semantic mismatch,
production numeric overflow or sanitizer diagnostic occurred.

## Retained development failure and final regression

A review probe found that a directory passed as a graph returned invalid_graph
(exit 3) instead of io_error (exit 4). The first buffered-stream-only fix still
failed the new test on this macOS library: `io-regression/03.stdout` records
4/5 CTest passed and CLI failure, driver exit 8. The final fix checks filesystem
directory status before reading and keeps read/flush errors explicit. All final
profiles then pass 5/5; original/minimal I/O reproducer and cause are retained in
[io-directory-reproducer.json](io-directory-reproducer.json). No failed run was
removed or silently counted as passing.

The full oracle campaigns preceded that I/O-only follow-up and the explicit Boost
version check. All mathematical primitive and campaign source bytes are unchanged;
the final sources were rebuilt and all profile tests/oracle smoke rerun.
[Final source hashes](source_hashes.json) and the explicitly labelled
[retrospective pre-follow-up source hashes](full_campaign_source_hashes.json)
distinguish these versions. The full large tiers were not redundantly rerun after
a file-read/status-only fix.

## Remaining limits / unrun work

- No unresolved blocking conflict. `solve` remains explicitly unavailable; M3
  recursion, chain certificates, fixed-k extraction/order, solver timings/semantic
  hashes and end-to-end correctness freeze are unimplemented and unrun.
- M4 core certificates/reduction and optimizations, baselines, benchmark campaigns,
  TSan/parallel execution and extended n<=12 tiers are unrun. No new experimental
  parameters or performance conclusions were introduced.
- Only full-graph global certificates exist in M2. Arbitrary user X,Y use the
  restricted API; no claim of arbitrary bounded-global certification is made.
- GCC/Linux and non-macOS execution were not tested; MSVC/no-native-128/non-POSIX
  configurations are explicitly unsupported by this implementation.
- No allocation-failure injection/cancellation campaign was run. The oracle
  mismatch minimizer was not triggered because the oracle campaign had no
  mismatches; its failure-only reduction path is not claimed tested. The separate
  observed I/O failure has a persistent regression and minimal reproducer.
- The materialized combination backend is intentionally unoptimized; resource
  scalability and empirical speedups are not established by these tests.
