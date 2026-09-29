# Claim-to-Code-to-Test Evidence

Revision 2026-09-29. Proof obligations and their arguments live in
`THEORY_TO_CODE_AUDIT.md`; this file is the single implementation evidence ledger.
A code symbol, test command, evidence path and commit are needed before marking
`implementation-tested`. Passing tests do not prove a theorem.

| Obligation | Exact source | Planned owner / symbol | Tests | Evidence / commit | Status |
|---|---|---|---|---|---|
| O01 Definition-level truth | Defs. 1.1-1.3 | reference: direct_compact, direct_maximal_compact, direct_lhcds | T01,T02; unchanged 74 pytest | [M1](../evidence/m1/REPORT.md); `1a4829a9348dae299ae074717928909598b11af6`; [M3 regression](../evidence/m3/accepted/commands.json) | implementation-tested (independent reference scope) |
| O02 Hierarchy/leaves | 1.8-1.10 | reference check_case; solve component extraction | T02,T11,T14 | [M3](../evidence/m3/REPORT.md); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O03 Largest F / independent chain | 1.11-1.14 | exhaustive_F, cardinality_line_chain; global_chain_point, chain_interval | T03,T09,T10 | [M1](../evidence/m1/REPORT.md); [M3](../evidence/m3/REPORT.md); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O04 Exact separator | 1.15; Eq. 11-12 | ChainInterval::lambda; ClosureOracle::separator_request, separate | T06,T10 | [M3 all-pair/trace evidence](../evidence/m3/fixture_manifest.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O05 Restricted/global boundary | 1.19 proof + audit A | largest_restricted, full_graph_request, global_F; immutable CertifiedGlobalRequest and chain points | T08,T09,T10; R01 | [M2](../evidence/m2/REPORT.md), `0a4aef8`; [M3 move/certificate review](../evidence/m3/REVIEW.md); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O06 Exact network / largest ties | Eq. 15; 1.19 | aggregate_footprints; oracle execute; Dinic<Capacity> | T06,T07,T09 | [M2](../evidence/m2/REPORT.md); `0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6`; [M3 regression](../evidence/m3/fixture_manifest.json) | implementation-tested (finite exact-network scope) |
| O07 Terminal extraction | 1.16 | solve; Graph::induced_components; Membership | T11; core T17 remains pending | [M3 named traces](../evidence/m3/accepted/build-smoke/named_traces.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O08 Fixed-k order / verification-free | 1.17; top-k convention | solve; solution_json; reviewed production call path | T12,T15,T16 | [M3](../evidence/m3/REPORT.md), [review](../evidence/m3/REVIEW.md); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O09 Query / network bounds | 1.18; 1.20 | SolveStats::record; solve; QueryStats; largest_restricted | T13; per-query network counts | [M3 independent 2r-1 checks](../evidence/m3/fixture_manifest.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O10 Safe core search bounds | 1.21-1.22 | planned peel_core, certified_core_bounds | T17 | not implemented/run; M4 | planned |
| O11 Exact numeric refinement | 1.19-1.20; D005 | Fraction; checked_add/sub/mul; largest_restricted; Dinic | T05,T07,T16 | [M2](../evidence/m2/REPORT.md); `0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6`; [M3 real auto fallback regression](../evidence/m3/fixture_manifest.json) | implementation-tested (finite numeric scope) |
| O12 Evidence scope / validation | Def. 1.3 + audit F | Campaign.variant/inspect_trace; run_solver.main | T02,T14,T15; M5 shared smoke pending | [M3 manifests](../evidence/m3/fixture_manifest.json), [separate validation](../evidence/m3/accepted/cli-definition-run/manifest.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |

## Evidence record

```text
obligation_id:
implementation_symbol:
implementation_commit:
test_ids:
command:
environment:
seed_or_fixture_manifest:
log_path_and_sha256:
result:
limitations:
```

Allowed states: `planned`, `implemented-untested`, `implementation-tested`,
`blocked`, `regressed`. A semantic optimization additionally needs a reviewed
argument; an off/on test alone is insufficient. Review-only arithmetic checks are
stored separately under `review/` and do not change the statuses above.

## Executed M0 bootstrap evidence (2026-09-09)

P00.1-P00.4 are complete at skeleton/contract scope; none of O01-O12 changes
from `planned` in the table above. No T01-T17 mathematical/production campaign
was run and no finite test is a theorem proof.

| Task | Symbols / artifact | Executed evidence | Scope |
|---|---|---|---|
| P00.1 | `scripts/verify_papers.py:main`; `review/source_snapshot_sha256.json` | [Before](../evidence/m0/checks/01.log), [after](../evidence/m0/checks/17.log), [preservation](../evidence/m0/preservation_final.json) | Four paper hashes match; initial snapshot created after owner clarified none previously existed; also match committed bytes |
| P00.2 | Existing obligations O01-O12 and accepted/revision decisions | [M0 report](../evidence/m0/REPORT.md), [unchanged source hashes](../evidence/m0/preservation_final.json) | Internal-contract consistency review only; no genuinely new conflict, theory change or second audit |
| P00.3 | CMake `vflhcds_lib`, `vflhcds`, `vflhcds_skeleton_test`; `build_info`, `run_cli`; reference namespace | [Command/exit/log manifest](../evidence/m0/checks/commands.json), [compiler flags](../evidence/m0/compiler_flags.json), [fixtures](../evidence/m0/fixture_manifest.json) | Four profiles build; 3/3 CTest each; standalone pytest 1 passed; skeleton sanitizers only |
| P00.4 | `RunStatus`, `status_name`, `exit_code`, `write_failure_status`; [version 1 contract](INTERFACE_CONTRACT.md) | [CLI CTest](../evidence/m0/checks/04.log), [report](../evidence/m0/REPORT.md) | Help/build-info and explicit unavailable-command failures exercised; graph/solver/telemetry contracts frozen as future behavior |

Base commit: `60321429ef832d7032d1e6ad96965dd2a95b08aa`; changes are uncommitted,
on top of the owner's pre-existing dirty tree. This is not an implementation
commit or correctness-release tag. [File manifest](../evidence/m0/files_changed.json)
identifies M0 files and SHA-256 hashes; [environment](../evidence/m0/checks/environment.json)
and [toolchain](../evidence/m0/toolchain.log) record the executed setup. Logs and
their hashes are retained in the evidence directory. No baseline/DCLDS code was
consulted or imported; D012 remains in force.

## Executed M1 independent-reference evidence (2026-09-17)

P01.1-P01.5 are complete at the declared M1 scope. Reference tests have actually
run; the O01-O03 table's formal `implementation-tested` label remains withheld
because this ledger requires an implementation commit as well as logs. Delivery
is currently an uncommitted working tree based on `a779112`, identified by the
[M1 source hashes](../evidence/m1/files_changed.json). This is not an unrun-test
claim. Production portions of the obligations and M2+ acceptance remain open.

| Task / obligations | Implemented symbols | Executed evidence |
|---|---|---|
| P01.1 / O01 | Graph, normalize_graph, combination_cliques, Reference.mu_h/density/deletion_loss, direct_compact, compactness | T01 and hand definition tests; all induced counts compared with an independent per-subset combination count |
| P01.2 / O01,O02 | direct_maximal_compact, direct_lhcds, maximal_compact_sets | T02 bridged triangles; all-superset definition compared with global-F components and hierarchy leaves in the declared reference campaigns |
| P01.3 / O03 (supports future O05) | exhaustive_F, exhaustive_restricted, OracleResult | Largest union of all maximizers; zero/empty/equal bounds; negative scaled objective with >128-bit exact parameter; restricted scope remains explicit |
| P01.4 / O03 | cardinality_line_chain, Chain | T03 exact envelope grid, second grid from direct compactness, all chain endpoint pairs; new seven-vertex outer-breakpoint fixture |
| P01.5 / O01,O03 | check_size, parse_graph/parse_set, solution_records, CLI main, all_labelled_graphs, seeded_cases | 11 persistent hand truth cases, saved T03 witness, n<=12 guard, exact ID/wire tests, dependency/import isolation, reference CLI smoke |

Executed results: [pytest](../evidence/m1/final/01.stdout) 74 passed;
[CTest integration](../evidence/m1/final/09.stdout) 3/3 passed (includes the same
reference suite, not extra mathematical coverage). Standalone reference CLI:
6 successful invocations and one expected invalid-k exit 2, with separate
stdout/stderr in [command manifest](../evidence/m1/final/commands.json).

[Exhaustive-small](../evidence/m1/exhaustive-small/summary.json): 1,099 distinct
labelled graphs with n=1..5, h=2,3; 2,198 graph/h cases, 36,968 global queries,
4,140 restricted queries and all 4,140 chain pairs checked.
[Seeded](../evidence/m1/seeded/summary.json): seed 20260917, 100 unique graph/h
cases on 96 graphs with n=6..8; 1,338 global and 149 restricted queries.
All cases include original and relabeled/re-sorted reference prefixes.
These counts exclude additional unit/CLI calls and are not production mincuts
or solver telemetry. [Fixture manifest](../evidence/m1/fixture_manifest.json)
and each campaign's cases.jsonl retain graphs, h, seeds and exact expected ranks.

The prior review witness file was absent. A new recorded seven-vertex graph has
principal breakpoints 13/6 and 2, with 2 absent from every nonempty induced density.
Its [provenance](../reference/fixtures/outer_breakpoint.json) does not claim to
recover the unavailable historical fixture. No proof/spec/decision was changed.

No production backend, solver, real fixed-width fallback, sanitizer campaign,
baseline or benchmark was implemented/tested. The complete M3 seeded/higher-h
release tiers remain unfulfilled. These finite checks support reference
implementation validation; they do not prove O01-O03 or the mathematical theorem.

## Executed M2 exact-primitives evidence (2026-09-22)

The owner committed M1 as `1a4829a9348dae299ae074717928909598b11af6` before M2.
The dated M1 delivery paragraph above describes its former uncommitted state;
O01's reference implementation now has the required commit. M2 was delivered
uncommitted and then committed by the owner as
`0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6` before M3. Its [source hashes](../evidence/m2/source_hashes.json)
and [changed files](../evidence/m2/files_changed.json) retain delivery provenance;
the formal M2 commit gate is now met. No theorem claim follows.

| Task / obligations | Delivered symbols | Executed evidence |
|---|---|---|
| P02.1 / O01 support | Graph, VertexSet, Membership, normalize_graph, parse_graph/parse_set, canonical_graph, sha256 | T01 exact IDs/isolate/loop-only preservation; components; strict rejection; canonical hashes versus hashlib |
| P02.2 / O01,O06 support | MaterializedCliques, count, incidence, degree | T04 full tuples/incidences and every induced count for all declared cases; h>=2 including h>n |
| P02.3 / O11 | BigInt, Fraction, checked_add/sub/mul, scaled_objective | T05 near-limit overflow checks, exact signed comparison and real automatic BigInt flow |
| P03.1 / O06 | aggregate_footprints | T06 all tested subsets; 10,842 exhaustive nested-bound pairs across n<=4 at h=2,3; crossing/singleton/repeated footprints |
| P03.2 / O06,O11 | Dinic<UInt128>, Dinic<BigInt>, max_flow, reachable | T07 135 independently enumerated tiny cut/backend runs, reverse edges/cancellation, >64/128-bit values, 20,000-node stack-safe path |
| P03.3 / O05 | RestrictedRequest, CertifiedGlobalRequest, full_graph_request, largest_restricted, global_F | T08 separate scope; private full-graph construction; owner checks; empty/equality/zero |
| P03.4 / O03,O06 support | closure execute and L=N+1 capacity construction | T09 compares complete largest sets, including tied unions, across exact reference parameters; no solver recursion |
| P03.5 / O09 partial | run_cli, oracle_json, atomic_write, QueryStats, query_stats_json | CLI canonical fields/statuses, atomic writes/input aliases and I/O failure regression; per-query counters independently recomputed |

Executed [commands/environment/logs](../evidence/m2/final/commands.json) and
[post-I/O-fix builds/CTest](../evidence/m2/io-final/commands.json): four profiles
build and pass 5/5 CTest each, standalone pytest 74 passed, BUILD_TESTING=OFF
Release builds and executes the six-vertex bridged-triangle oracle. Final CTest
includes 1,458 primitive assertions, 135 tiny cut/backend runs, 56 CLI invocations,
28-case oracle smoke, and the unchanged independent reference suite.

Both Debug and ASan/UBSan run the full M2 campaigns:
- Exhaustive-small: 2,198 graph/h cases / 1,099 graphs; 40,591 oracle requests;
  all 4,140 independent-chain endpoint pairs; 152,506 footprint identities.
- Seeded: seed 20260922, 1,000 unique graph/h cases / 870 graphs, n=6..8;
  12,000 requests (4,000 global, 8,000 explicitly restricted), 200 cases per family.
- Higher-h: 72 graph/h cases / 67 graphs; 1,053 requests, including h=4,5 and h>n.
- Smoke: 28 graph/h cases / 24 graphs; 537 requests.

Tiers overlap and backend repetitions are not extra distinct graphs/requests.
Each query uses auto and forced BigInt, and forced UInt128 when safe or bypassed.
The two main tiers alone execute 3,198 automatic BigInt flows per build, separately
from forced-BigInt diagnostics. Every tier's probe stderr is empty; no oracle
mismatch or sanitizer diagnostic occurred. Detailed queries/results and inputs
are retained in [fixture/campaign manifest](../evidence/m2/fixture_manifest.json).

Full oracle tiers ran before the isolated directory-input I/O fix; mathematical
primitive and campaign code did not change. The fix and version-pin check were
then built/tested on all profiles, including oracle smoke. Original failed I/O
checks and the passing regression are retained, not overwritten. See the
[M2 report](../evidence/m2/REPORT.md) for precise sequencing and limits.

P02.1–P03.5 were complete at M2 delivery. At that time all M3+ tasks, chain/core certificates,
solver timing/hash/fixed-k output, end-to-end solver verification, baselines,
benchmarks, extended campaigns and TSan were unrun/unimplemented at M2 delivery. The oracle
failure minimizer's mismatch path was not triggered by this successful campaign.
Papers, accepted decisions, theory contracts and all M1 reference bytes remain
unchanged. No external baseline technique was used (D012).


## Executed M3 solver/correctness evidence (2026-09-29)

M3 is based on the owner's M2 commit `0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6`.
P04.1–P04.4, P05.1–P05.3 and P06.1 have executed evidence; P13.1's review and local freeze are
complete with one resolved engineering finding (R01, moved certificate payload).
M3/P13.1 complete: local annotated tag `v0.1.0-m3-correctness` freezes the tested implementation.
Implementation commit: `23a5b3415cf3ae053e55a01b219ca074ffe6fd67`.

[Report](../evidence/m3/REPORT.md) maps every task to actual symbols, commands,
environment, graph/seed records and limits. [Acceptance command manifest](../evidence/m3/accepted/commands.json)
contains 35 successful commands after the R01 fix; each log is hashed.
Four profiles build and pass 9/9 CTest each; standalone pytest reports 74 passed.
The production-only Release target builds without test/probe/Python dependencies
and executes a separately definition-checked CLI solve.

Both Debug and ASan/UBSan execute the same complete M3 release tiers:
- Exhaustive-small: 2,198 graph/h cases / 1,099 labelled graphs n=1..5;
  4,140 independent chain pairs, 37,825 explicit oracle requests, 38,480 solver
  runs (including auto/forced-BigInt repeats), 14,844 distinct fixed-k prefix checks.
- Seeded: seed 20260929, 1,000 distinct graph/h cases / 860 graphs n=6..8;
  200 per family, 16,610 explicit oracle requests, 19,992 solver runs,
  7,956 fixed-k prefix checks, 20 isolate and 20 disjoint-union cases.
- Higher-h: 64 graph/h cases / 60 graphs; 985 explicit oracle requests,
  1,168 solver runs and 456 prefix checks; includes h=4,5 and h>n.
- Smoke: 30 named/generated graph/h cases, every prefix, 30 isolate and 30
  disjoint-union cases; retained split/tie/non-emitting terminal traces.

Every base graph is also relabeled with order-reversing arbitrary-size original
IDs; complete truth is transformed and re-sorted before testing its prefixes.
Each full run checks 2r-1 against an independently constructed chain and verifies
logical/mincut counters separately. Both builds also rerun the complete M2 oracle
release tiers, preserving actual automatic arbitrary-precision execution.
[Fixture manifest](../evidence/m3/fixture_manifest.json) retains per-tier counts,
seeds, inputs, output/trace streams and their hashes. Seven Debug/sanitizer pairs
have byte-identical case files and decompressed result streams.

[Review](../evidence/m3/REVIEW.md) records exact code refinement and the production
call path without a candidate verifier. [Preservation](../evidence/m3/preservation_final.json)
confirms unchanged papers, accepted decisions/theory contracts and M1 reference.
No new proof/spec conflict or unresolved implementation finding remains in the
executed scope. The review was a separate pass by the implementing assistant,
not independent human sign-off. Finite test agreement does not prove the theorem.
O10/T17 and every M4/M5 task stay open. O12 evidence covers M3 definition checking
and manifest/timing separation, not baseline agreement or benchmark conclusions.
Extended n<=12 campaigns, GCC/Linux, OS OOM pressure and TSan remain unrun.
