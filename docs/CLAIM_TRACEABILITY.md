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
| O07 Terminal extraction | 1.16 | solve; Graph::induced_components; Membership | T11; M4 T17 evidence below, new commit pending | [M3 named traces](../evidence/m3/accepted/build-smoke/named_traces.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O08 Fixed-k order / verification-free | 1.17; top-k convention | solve; solution_json; reviewed production call path | T12,T15,T16 | [M3](../evidence/m3/REPORT.md), [review](../evidence/m3/REVIEW.md); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O09 Query / network bounds | 1.18; 1.20 | SolveStats::record; solve; QueryStats; largest_restricted | T13; per-query network counts | [M3 independent 2r-1 checks](../evidence/m3/fixture_manifest.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67` | implementation-tested (finite M3 scope) |
| O10 Safe core search bounds | 1.21-1.22 | peel_core; ClosureOracle::global_F/restricted_impl; OracleOptions; unchanged solve endpoints | T17; independent core truth and all-mode prefixes | [M4 executed evidence](../evidence/m4/REPORT.md), [argument](M4_IMPLEMENTATION.md); working tree on `5802d5a`, new commit pending | planned (M4 tests passed; formal commit gate pending) |
| O11 Exact numeric refinement | 1.19-1.20; D005 | Fraction; checked_add/sub/mul; largest_restricted; Dinic | T05,T07,T16 | [M2](../evidence/m2/REPORT.md); `0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6`; [M3 real auto fallback regression](../evidence/m3/fixture_manifest.json) | implementation-tested (finite numeric scope) |
| O12 Evidence scope / validation | Def. 1.3 + audit F | Campaign.variant/inspect_trace; run_solver.main; experiments.run.execute | T02,T14,T15; scoped M5 shared smoke | [M3 manifests](../evidence/m3/fixture_manifest.json), [separate validation](../evidence/m3/accepted/cli-definition-run/manifest.json); `23a5b3415cf3ae053e55a01b219ca074ffe6fd67`; [M5 paired smoke](../evidence/m5/paired-smoke-20261005/REPORT.md) | implementation-tested (finite M3 scope); structural/agreement evidence on one M5 real case |

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
At M3 delivery O10/T17 and every M4/M5 task were open. O12 evidence covers M3 definition checking
and manifest/timing separation, not baseline agreement or benchmark conclusions.
Extended n<=12 campaigns, GCC/Linux, OS OOM pressure and TSan remain unrun.


## Executed M4 core and single footprint optimization (2026-09-29)

P07.1-P07.3 and P08.1 are complete at implementation/test scope. This is an
uncommitted working tree on `5802d5a2a04cae35eaf708aba65f638abf642c8f`;
[source snapshot](../evidence/m4/accepted/environment.json) and
[changed-file hashes](../evidence/m4/files_changed.json) identify actual tested code.
The table's formal implementation-tested state for new O10/M4 code is withheld
until an implementation commit exists. Existing M1/M2/M3 commits and tests are
not retroactively relabelled. M4 requests no additional tag; M3's tag is preserved.

| Task / obligations | Actual symbols | Evidence |
|---|---|---|
| P07.1 / O10 | peel_core; CoreStats | Independent all-subset union definition, exact updates, zero/huge thresholds, h-clique versus ordinary degree; T17 |
| P07.2 / O04,O05,O07,O10 | global_F, restricted_impl, OracleOptions; solve passes options without changing its traversal | Original/reduced sizes, exact ceil(lambda), audit-C non-chain core and restored pendant; all certified sets/traces/prefixes |
| P07.3 / O09,O10,O12 | core query counters and reduction timing; m4_campaign.ModesProbe, check_query; m4_profile | [Preservation argument](M4_IMPLEMENTATION.md), four-mode equality, 36 saved local timing/RSS processes |
| P08.1 / O06,O11 | aggregate_footprints(FootprintMode::Membership), CLI --footprint-scan | Pre-edit M3 measurement/selection; independent exact footprint records and full core/scan mode corpus; auto/BigInt and boundary/fallback checks |

[Acceptance](../evidence/m4/accepted/commands.json): all 36 commands exit 0;
four profiles build and pass 12/12 CTest each, including 30 new C++ checks and
40 M4 CLI invocations; standalone pytest 74 passed. Production-only Release also
builds and executes safe+membership with external definition validation.

Each of Debug and ASan/UBSan runs:
- Exhaustive-small: 2,198 base graph/h cases / 1,099 graphs, 22,054 definition-core
  requests, 42,164 footprint-bound pairs, 153,920 solver executions across modes
  and capacity repetitions; 14,844 distinct fixed-k prefix requests.
- Seeded: seed 20260929, 1,000 distinct graph/h cases / 860 graphs, 8,492 core
  requests, 10,200 footprint-bound pairs, 79,968 solver executions and 7,956
  fixed-k prefix requests, with all original/relabelled and declared extra variants.
- Higher-h: 64 base cases / 60 graphs, 430 core requests, 1,184 footprint pairs,
  4,672 solver executions and 456 prefix requests.
- Smoke: 31 base cases / 27 graphs including audit C, 589 core requests,
  1,642 footprint pairs and 4,976 solver executions.

Counts are per build and include stated repetitions, not extra distinct graphs;
tiers overlap. Full M2 oracle regression tiers also pass in both builds.
[Fixture manifest](../evidence/m4/fixture_manifest.json) retains actual counts,
seeds and every graph/mode response. [Integrity/comparisons](../evidence/m4/verification.json)
checks source/log hashes, seven Debug/sanitizer response pairs (excluding measured
core time), and reproduction of the three saved M3 baseline corpora with modes off.

The local profile workload was frozen before production edits. Its three synthetic
fixtures justify testing one footprint-scanning change; they do not establish
universal speed/memory improvement or select M5 benchmark parameters. Core and
membership modes remain explicit, default off/sorted. No additional backend,
parallel code or external technique was introduced. [Report](../evidence/m4/REPORT.md)
retains all measurements, two corrected development-only errors and remaining limits.
No new proof/spec conflict or solver/reference mismatch remains in the executed
scope. Independent finite agreement supports implementation validation, not a theorem.

## M5 partial baseline evidence (2026-10-02)

P09.1 remains incomplete. IPPV author commit
`f61881d4752170c03585e4281f0c49d7ef14aa1e` was acquired under owner decision D027.
The original build failed on missing `omp.h`; the separately owner-approved
[single-header-removal patch](../baselines/ippv/patches/0001-remove-unused-openmp-header.patch)
then [built successfully, exit 0](../evidence/m5/ippv/compat-20261002/commands.json).
Source/binary/patch/log hashes and the subsequent source-inspected uninitialized
member blocker are in [IPPV-B02](../evidence/m5/ippv/compat-20261002/stop.json).

This is provenance and build evidence only. There are no baseline runtime,
definition-checked output, cross-implementation agreement or performance results.
O12's experimental smoke remains unrun; no obligation status or M5 completion
checkbox is promoted by this build. The proposed implementation/reference is
unchanged and all 53 M4 accepted source hashes still match.

### Subsequent IPPV execution under D028 (2026-10-02)

The [current report](../evidence/m5/ippv/reproduction-20261002/REPORT.md) supersedes
the preceding build-only status while preserving those historical failures.
P09.1 now has three pinned source patches, reproducible Release and sanitizer
builds, a native-process adapter and separate external validation. The 17 adapter
tests plus 74 unchanged reference tests pass. Six tiny native runs pass exhaustive
definition checks; one real-data native run returns 20 structurally checked sets.
The latter does not establish maximality, completeness or comparative performance.

Three additional native runs fail zero-density completeness, including Release
and sanitizer executions of the one-vertex minimum reproducer. These are recorded
as mismatches, not hidden or converted into passes by the adapter. Source defects
IPPV-B02/B03 are repaired; output-domain finding IPPV-B04 remains unresolved for
full-domain comparison. This provides scoped baseline evidence relevant to O12,
not completion of O12's shared experimental smoke, P09.1, or M5. No theorem claim,
obligation status or M5 checkbox is promoted. The proposed implementation and
independent reference remain unchanged.

### DCLDS preflight boundary (2026-10-02)

P09b.1 has a [D012 content/version snapshot](../evidence/m5/dclds/preflight-20261002/freeze.json)
and public repository commit/tree metadata only. The unidentified-license decision
is [pending](../evidence/m5/dclds/preflight-20261002/stop.json). No source build,
runtime/semantic result, detailed comparison, historical-priority proof or technique
import is claimed. O12 and M5 completion statuses remain unchanged.

### D029 scope and additional IPPV diagnostics (2026-10-02)

D029 defers further DCLDS reading/integration while independent work continues;
P09b.1 stays incomplete. No new DCLDS evidence or historical-priority claim is made.

P09.1/O12 have additional [executed diagnostics](../evidence/m5/ippv/coverage-20261002/REPORT.md):
IPPV `onepass` h=2 and `Graph::connected_components` boundary defects are repaired
under D028. `check_toys.fixtures,classify,main` retains fixed input hashes and all
outcomes. The final 48 native runs across h=2,3,4,5 and two profiles yield 32
definition passes and 16 preserved zero-density mismatches. The real h=3 smoke
returns 20 structurally checked sets with the same canonical bytes as before.
All five patches replay to the 17 locked source hashes; eight configure/build
commands exit 0. No finite test, obligation completion, shared benchmark smoke or
M5 performance conclusion is implied. Core solver/reference code remains unchanged.

### Shared experiment harness diagnostics (2026-10-03)

P11.1-P11.3/O12 have new [scoped evidence](../evidence/m5/harness-20261003/REPORT.md).
`experiments.validate.parse_records,validate,compare` distinguish canonical exact
records, structural checks, independent all-superset definition truth, and
cross-implementation agreement. `run.load_config,schedule,run_vf,execute` retain
input/binary pins, predeclared shuffled blocks, native versus validation process
resources, failure statuses and checksums. `prepare_input.prepare` preserves the
declared vertex universe; `build_vf.main` records the unchanged Release build.

112 pytest cases pass (21 harness, 17 IPPV adapter, 74 reference). Twelve tiny
native runs yield ten definition-checked completions and two preserved known
IPPV omissions. Four eligible paired comparisons agree under tie-aware rules;
two of those differ under strict cutoff-tie selection. Repeated semantic hashes
are stable. The shared real smoke yields five structurally checked IPPV sets and
a VF basic timeout at 60 seconds, so no output agreement or speedup is claimed
on that real case. No mathematical obligation, final experimental gate, or M5
checkbox is promoted. All four papers and 53 accepted M4 source hashes remain
unchanged; DCLDS stays deferred under D029.

### Approved existing-mode diagnostic (2026-10-03)

P11.2/P11.3/O12 gain [four additional recorded native outcomes](../evidence/m5/m4-mode-diagnostic-20261003/REPORT.md).
The owner-approved draft was executed with the same CA-GrQc h=3,k=5 input,
Release binary, 60-second guard, one worker and frozen seed 20261003. Core-only,
both, membership-only and basic all time out with empty stdout/stderr; no
external validator runs and all six output comparisons remain unavailable.
Integrity checks pass for the raw outcomes/checksums, 53 accepted M4 source
hashes and four paper hashes. Builds and test suites were not rerun.

Static source inspection records exhaustive index construction over
C(5242,3)=23,993,367,880 candidate triples before M4 query options take effect.
This is a code observation and next-diagnosis hypothesis, not measured phase
attribution, a semantic counterexample or a performance conclusion. The
phase-diagnosis proposal remains unrun. No obligation or M5 checkbox is promoted;
DCLDS remains deferred and no proposed-algorithm implementation is changed.

### Bounded phase diagnostic (2026-10-03)

P11.2/P11.3/O12 have [measured phase-boundary evidence](../evidence/m5/phase-diagnostic-20261003/REPORT.md).
The separate `vflhcds_phase_probe` target links the unchanged Release library;
`mark/main` flush parse/index/solve/serialize boundaries without changing the
production CLI or algorithm. Configure/build succeed. Both T-PHASE-01 fixtures
produce eight ordered markers, byte-identical production output and passing
independent definition checks (four native calls and two later validators).

The single CA-GrQc h=3,k=5 diagnostic parses in 0.0038615 s, enters index
construction, then hits the declared 60-second guard without reaching solve.
This establishes the immediate incomplete phase for this instrumented call,
not a completed runtime, output-equivalence result on the real graph, theorem
claim or retrospective trace for prior failures. Integrity checks preserve all
53 accepted M4 source hashes, four papers and the original executable/library.
The adjacency-extension plan includes an enumeration-order/incidence preservation
argument and regression gates, but no production optimization is implemented or
accepted. Full suites are unrun this turn; no task/obligation status is promoted.

### Authorized adjacency enumeration (2026-10-03)

P02.2/T04 preservation, O06/O11 and P11.2/P11.3/O12 gain
[executed evidence](../evidence/m5/enumeration-20261003/REPORT.md).
`MaterializedCliques::enumerate_adjacency` uses sorted common-neighbor extension
and an explicit stack; shared `append` preserves tuple/incidence order. The old
combination enumeration remains the default/control. CLI and external harness
record the optional selector without changing canonical records/hashes or query
counter meanings. No flow, oracle or solver-recursion implementation is changed.

Debug, Release and ASan/UBSan each pass 14/14 CTest. Combined pytest passes 115
checks. Fourteen Debug/sanitizer campaigns retain the original fixture/seed
corpora and compare both representations before querying the new index against
independent reference truth. All 1,392,496 saved new responses match pre-change
M4 responses, excluding only `core_reduction_seconds`. Numeric limits and actual
arbitrary-precision fallback execute; the paper/reference hashes remain unchanged.

The single predeclared CA-GrQc h=3,k=5 diagnostic completes in 0.767723375 s,
enumerates 48,260 cliques, and returns five externally structurally checked sets.
These strictly match the saved IPPV outputs on the same graph. This is structural
and cross-implementation evidence, not exhaustive maximality/completeness truth
on that graph or a theorem proof. Historical timeouts remain censored failures;
no formal speedup or paired performance comparison is inferred. The bounded
enumeration repair is complete; M5 and final experiment gates remain open.

### Fresh paired smoke and campaign preparation (2026-10-05)

P11.3/O12 gain [fresh paired evidence](../evidence/m5/paired-smoke-20261005/REPORT.md)
at the existing CA-GrQc h=3,k=5 settings: one repetition, seed 20261003, one worker,
60-second guard, no imposed memory cap, uncontrolled cache. Both native processes
and their later external validators exit zero. Each returns five structurally
checked sets; ordered outputs and semantic hashes match strictly. IPPV native
wall time is 0.17649641539901495 s and VF adjacency/basic is 1.2028633328154683 s.
One paired repetition does not establish performance stability or a speedup.
It does complete the scoped shared smoke gate P11.3. Exact maximality/completeness
on this real input remains uncertified; no mathematical obligation is promoted
to a theorem proof.

`experiments.run.execute` gains optional `stop_on_failure`; its CLI flag records
the execution policy and retains the failure plus all pending schedule entries.
Injected failure/comparison tests cover timeout, error, OOM, semantic mismatch,
driver exception, genuine pair disagreement, valid cutoff ties and the retained
run-all policy. Combined harness/adapter/reference pytest passes 123 checks.
Production sources/binaries, four papers, reference and patched IPPV sources
remain unchanged. No build or sanitizer campaign is rerun for this external-only
change. The exact pre-edit runner used for the smoke is separately snapshotted.

CA-CondMat is normalized with every declared vertex retained. Its inclusion in
the [two-input, 48-call proposal](../evidence/m5/campaign-proposal-20261005/PROPOSAL.md)
is pending owner approval; the draft has no benchmark results. P11.1/P11.2/P12.1,
broader baseline/release work and M5 remain open. DCLDS stays deferred under D029.

### Approved pilot stopped at output disagreement (2026-10-05)

D030 records explicit owner approval before the limited paired campaign. P11.2,
P12.1 and O12 gain [executed pilot evidence](../evidence/m5/pilot-20261005/REPORT.md):
20 native runs and 20 later external validators exit zero and pass structural
checks. Of ten pairs, six are strict matches, three more allow cutoff ties at
k=15, and one fails tie-aware agreement at CA-GrQc h=3,k=20, repeat 0. The overall
driver exits 1 as required by its frozen stop policy; 28 scheduled calls remain
unrun. No timeout, OOM or native crash occurs in the executed subset.

The observed discrepancy is substantive under the recorded comparator: VF's
rank-18 set has 13 vertices and 56 triangles, density 56/13, and is absent from
IPPV's output above their common 10/3 cutoff. Both sides' structural validity
does not establish full compactness/maximality or establish which implementation
is responsible. A copied original graph, exact outputs, commands, hashes and
seed are retained; root-cause analysis, minimization and a new native run are
not performed after this stop. This is an unresolved cross-implementation
disagreement, not an established counterexample to the theorem.

`evidence/m5/pilot-20261005/summarize.py` derives raw-run and all-planned-cell
tables from immutable manifests. Completed triples at k=5,10,15 have native
time/RSS median/min/max; mismatching k=20 keeps its single raw pair and no
three-repeat comparison summary. Every pending case remains visible. The script
does not launch either algorithm. All pinned algorithm/harness sources, binaries,
reference files and papers remain unchanged. No build, test-suite or sanitizer
campaign is rerun. No full M5 task or mathematical claim is promoted; the approved
pilot is incomplete and performance conclusions remain limited by this stop.

### Disputed-set certificate and external baseline repairs (2026-10-05)

P09.1/O01/O12 gain [executed diagnosis and regression evidence](../evidence/m5/ippv/disagreement-20261005/REPORT.md).
The 13-vertex candidate from VF has density/compactness 56/13 by every-deletion
enumeration. Independently generated integer flow allocations match a cut of
537086985 at theta=293607/68159 on the original 5,242-vertex graph. The certified
global optimum has 692 vertices and the candidate is exactly one ordinary
connected component. Supermodularity plus strict theta<56/13 forces every
56/13-compact set into that optimum, excluding any connected proper compact
superset of the candidate. This certifies the disputed finite-instance set and
establishes the old IPPV omission; it is neither a general theorem proof nor a
definition-checked label for the entire original top-20 output.

External baseline patches 0006/0007 repair truncated rational verifier capacities
and a shrunken PAVA workspace. A PAVA-only sanitizer control still reproduces
the omission, isolating the numeric cause. A saved synthetic 13-vertex regression
checks every proper superset and is one-edit irreducible under the recorded
predicate after 31 deterministic attempts. Exact scaling/range tests and
native regression pass in Release and ASan/UBSan/bounds-check profiles. Both
fixed original replays pass tie-aware comparison; legitimate cutoff ties remain.
The 48-case baseline corpus retains 32 definition passes and 16 known zero-density
omissions, and 123 pytest checks pass. Production VF sources/binary, reference,
papers and existing decisions remain unchanged; no verifier enters the VF path.
The new certificate code is external diagnostic evidence only. No full M5 gate
or benchmark result is inferred and the stopped campaign is not resumed.

### Repaired-baseline pilot: CA-GrQc complete, CA-CondMat timeout (2026-10-05)

D031 authorizes a fresh campaign using seven-patch IPPV and the unchanged D030
graph/grid/resource/seed/repetition settings. P11.2/P12.1/O12 gain
[new executed evidence](../evidence/m5/pilot-fixed-20261005/REPORT.md): 25 native
calls, comprising 24 completed CA-GrQc runs and one CA-CondMat VF timeout.
All 24 separate validators exit zero and pass structural checks. All 12 pairs
match under the accepted cutoff-tie rule; six match strictly (k=5,10), and six
have only allowed cutoff differences (k=15,20). Each algorithm/case has the same
semantic hash across its three completed repetitions. This supports repeated
cross-implementation agreement, not maximality/completeness of the real graphs
or a mathematical theorem proof.

Eight completed algorithm/case cells have three-repeat native time/RSS
median/min/max, excluding external validation. IPPV is faster in these observed
CA-GrQc settings; this is not a general-h, all-mode, all-dataset or SOTA conclusion.
VF at CA-CondMat h=3,k=5, repeat 0 reaches the 60-second timeout (observed process
wall 60.009898708 s, peak RSS 144261120 bytes, timeout termination signal 9).
Empty stdout/stderr provide no phase diagnosis or valid completed output.
The driver exits 1; 23 scheduled native calls remain unrun, including every IPPV
CA-CondMat call. The timeout is retained and excluded from successful-run medians;
all 16 planned cells remain visible.

The evidence-only aggregation and verification scripts pass, rechecking all
263 raw inventory entries, 261 historical-pilot files, source/binary/data pins,
all saved comparisons and aggregate medians. No algorithm/harness source, paper,
reference or historical pilot is changed. There is no post-stop native call,
retry, build, test-suite rerun, sanitizer campaign or new DCLDS work. P12.1 and
M5 remain incomplete; the next affected path is the unresolved VF timeout.

### CA-CondMat solving-stage diagnosis (2026-10-05)

D032/P11.2/P12.1/O12 gain [instrumented boundary evidence](../evidence/m5/condmat-phase-20261005/REPORT.md).
The separate probe links the preserved adjacency Release library, explicitly
selects adjacency/basic semantics and uses the existing completed-query callback.
Both configure/build commands exit zero. T-PHASE-ADJ passes on two fixtures:
canonical output and all query counters equal production, and independent
all-superset definition validation passes (four tiny native children, two
subsequent external validators). Production, reference and proof sources are
unchanged; the instrumentation does not enter the solver or semantic hash.

The single real call at CA-CondMat h=3,k=5 times out after 60.009140917 s. Parsing
takes 0.042061041 s and adjacency indexing 0.1166765 s; solve begins at elapsed
0.158885875 s. Before termination 137 sequential query-end markers report 137
actual mincuts, all using uint128, and 23,750,457 footprint clique visits. The
last completed query ends at elapsed 59.242462667 s. There is no solve-end or
serialization marker and stdout is empty. This establishes incomplete solving,
not an index-construction blocker or a completed result.

Inter-query gaps combine traversal/counting, footprint work, network construction,
flow and instrumentation; they are not isolated operation timers. Static source
inspection identifies repeated full-clique scans and sorted includes checks in
aggregate_footprints and MaterializedCliques::count as plausible avoidable work,
without claiming a measured percentage or excluding flow cost. An existing M4
membership-mode diagnostic is prepared, not executed. The evidence verifier
passes for 43 raw inventory entries, all source/library/binary pins and all
313 historical fixed-pilot files. No production change, new mathematical
conflict, post-timeout native call, full regression or M5 completion is claimed.

### CA-CondMat membership mode completes (2026-10-06)

P11.2/P12.1/O12 gain a [single completed diagnostic](../evidence/m5/condmat-membership-20261006/REPORT.md):
CA-CondMat h=3,k=5, core off, adjacency enumeration and existing membership
footprint scanning complete in 38.997086249 s, peak RSS 158580736 bytes. Five
outputs pass the separate exact structural validator; native/validator exits are
zero. All 304 queries use uint128; their first 137 counter records match the
prior sorted-mode trace. This is counter-prefix agreement, with no complete
real-case off/on output comparison or IPPV pair. A host-label preflight mismatch
is retained; a fresh matching hardware/profile check precedes the sole native
call. No production change, repeated speedup estimate, definition-level real-graph
truth, theorem proof or full M5 completion follows. Source/paper/historical
evidence pins and the saved run pass verification; no build/test suite is rerun.

### CA-CondMat paired output agreement (2026-10-06)

P11.1/P11.2/P12.1/O12 gain [one fresh paired diagnostic](../evidence/m5/condmat-pair-20261006/REPORT.md).
VF membership and seven-patch IPPV return five structurally checked sets each;
both native calls and separate validators exit zero. Ranks 1–4 are identical;
the differing rank-5 sets have exact density 22. Tie-aware comparison passes,
strict comparison is false, and VF's output equals its prior saved diagnostic.
Native wall times are 38.525397500 s and 2.723666167 s respectively. This is
single-case agreement and timing evidence, without a repeated speedup estimate,
real-graph definition truth or theorem proof. No production/harness change or
test-suite rerun occurs; all historical records remain intact. Wider repeated
experiments and M5 remain open.

### Complete membership pilot schedule (2026-10-06)

P11.1/P11.2/P12.1/O12 gain a [48-call repeated campaign](../evidence/m5/pilot-membership-20261006/REPORT.md)
with unchanged graph/binary pins, h=3, k={5,10,15,20}, three repeats and seed
20261003. The frozen runner policy continues native timeouts without retry while
retaining stops for other failures and substantive disagreements. Ten added
control-path cases plus prior harness/adapter/reference checks pass (133 total).
No algorithm, theorem, independent reference or historical evidence changes.

All 48 calls are attempted: 36 complete with passing separate structural
validators, and 12 VF CA-CondMat runs time out. All 12 complete CA-GrQc pairs
match with cutoff ties allowed, six strictly; all 24 CA-GrQc outputs also equal
the earlier repaired-baseline campaign. The 12 CA-CondMat blocks are not compared.
Completed outputs have stable hashes in all 12 completed cells. Earlier one-shot
CA-CondMat completion is not repeated under the same 60-second limit; no cause
of timing variation is established. No theorem proof or real-graph maximality
claim follows from these checks.

P14.1 gains a scoped review of timing/validation separation and negative/mixed
outcomes; P15.1 gains byte-identical local regeneration of seven aggregates from
461 checked raw inventory entries. Three-repeat medians require all scheduled
runs of that algorithm/case to complete, and comparison availability is separate.
Timeouts are retained, not substituted into completion-time medians. Source,
binary, paper and historical evidence pins pass the saved-evidence verifier.
The driver exits 1 because timeouts remain unsuccessful outcomes; aggregation,
verification and regeneration exit 0. Wider experiments, clean-machine release,
C++ rebuild/CTest/sanitizer reruns and DCLDS work are unrun; M5 remains incomplete.

### Core off/on repeated ablation (2026-10-06)

P12.1/O10/O12 gain [48 frozen core-ablation calls](../evidence/m5/core-ablation-20261006/REPORT.md)
using the same pinned adjacency/membership Release binary, two graphs, h=3,
k={5,10,15,20}, three repetitions, seed 20261003 and 60-second guards. Only the
core selector changes. The external runner gains explicit strict agreement for
equivalent modes; four added policy checks plus prior tests pass (137 total).
Production/theory/reference code and historical evidence remain unchanged.

All 30 completed outputs pass external structural validation; all 15 complete
pairs match exact canonical records. All 18 CA-CondMat k=10/15/20 runs time out,
with no remaining unrun calls. Completed outputs are stable across repetitions;
24 CA-GrQc outputs match the previous membership pilot and six CA-CondMat k=5
outputs match the saved paired diagnostic. Paired counters retain the same query
count, original interval sizes and footprint scan visits; oracle sizes and
network node/arc counts do not increase. These observations support the existing
O10 argument on this workload, not a new proof or real-graph maximality claim.

Across the five complete settings, safe-core median native time changes range
from -0.93% to +3.23%, and peak-RSS medians decrease 4.18%-11.91%. Core's measured
cost is already included in solve/native time. Finer counting/footprint/network/
flow timing remains unavailable, and three-repeat differences are not generalized.
P14.1 gains this scoped review; no fresh IPPV comparison or historical timing
pooling occurs. P15.1 gains byte-identical regeneration of seven aggregates from
365 checked raw inventory entries. Driver exit 1 retains timeouts; aggregation,
verification and regeneration exit 0. Wider experiments, clean-machine release,
C++ rebuild/CTest/sanitizers and DCLDS work remain unrun. M5 stays incomplete.

## M5 fine phase diagnostic — 2026-10-07

P12.1/O12 gain [D037 phase evidence](../evidence/m5/fine-profile-20261007/REPORT.md)
from hash-checked generated source copies. `vf_profile::Scope` records exclusive
monotonic wall times; the added lines do not alter production expressions,
ordering or counters. Deterministic timer tests cover nesting, phase changes,
snapshots and exception unwinding. Production, reference and all four papers
remain unchanged; this is instrumentation validation, not a new theorem claim.

Release and ASan/UBSan builds succeed; each diagnostic CTest passes 1/1. The
reference/harness/adapter/instrumentation pytest run passes 141 tests. Six tiny
native runs pass independent definition validation; four diagnostic/control
comparisons preserve exact output and full counters. The real-graph schedule
executes all four calls: the GrQc pair completes with strict output/counter
agreement and separate structural checks; both CondMat calls time out at 60 s.

The 289-query CondMat prefix records 57.092156 s of clique counting within
59.650414 s accounted solve time; max-flow is 0.947874 s. Every prefix counter
matches all three earlier matching 304-query core-off runs. This establishes a
measured partial-run counting bottleneck, not complete CondMat output agreement,
a future optimization's speedup, or a new VF/IPPV comparison. GrQc's complete
profile has 32.03% counting, 23.34% footprints, 22.39% network construction and
16.66% max-flow. Its single diagnostic/control time ratio 1.0416 does not isolate
or generalize instrumentation overhead.

P14.1 gains this scoped interpretation of complete versus censored timing.
P15.1 gains byte-identical aggregate regeneration and verification of 18 raw
native/validator process records and 5,243 unchanged historical evidence files.
Eight native calls complete, two time out, none remain unrun. No production
optimization, full C++ correctness/numeric-fallback campaign, clean-machine run,
new baseline comparison or DCLDS work is added; M5 remains incomplete.

## M5 exact count optimization — 2026-10-07

P12.1/O01/O04/O08/O11/O12 gain [D038 executed evidence](../evidence/m5/counting-20261007/REPORT.md).
`CliqueCounting::Membership` changes only the clique-in-set predicate inside
`MaterializedCliques::count`; the immutable tuples and BigInt accumulation stay
unchanged. Sorted counting remains the default and explicit control. The
[preservation argument](COUNTING_IMPLEMENTATION.md) covers equal integer counts,
chain parameters, ranked outputs and counter semantics; it is separate from tests.

T04-COUNT checks all subsets, unrelated repeated sets, invalid sets/modes, huge h,
isolates, both enumerators and a real automatic big-integer flow. T04-COUNT-CLI
checks 217 calls per build across count/enumeration/core/footprint choices, output
scopes, defaults and argument errors. Debug, Release and ASan/UBSan each pass
16/16 CTest. Python passes 144 checks. The existing M2/M4 corpus runs through
membership-counting probes in all 14 Debug/sanitizer campaigns; every campaign
exercises automatic fallback. Every case manifest and all 1,392,496 saved responses
match the earlier sorted-count corpus, excluding only `core_reduction_seconds`.

The same new Release binary executes twelve predeclared count-mode calls on two
graphs at h=3,k=5, three repeats, with prior serial/60-second/resource policies.
All twelve complete and pass separate structural validation; all six strict pairs
match. Completed outputs and full counters match within each case and all three
earlier corresponding core-off runs. There is no historical timing pooling.
Sorted/member medians: GrQc 0.349554/0.250145 s (1.40x), CondMat
38.791546/1.709334 s (22.69x). One GrQc pair is slower with membership. These
measurements include marker allocation/initialization and support only this local
count-mode comparison, not a new VF/IPPV result or general performance guarantee.

P14.1 gains that scoped interpretation. P15.1 gains nine byte-identically
regenerated aggregates from 113 checked raw campaign inventory entries. Papers,
reference, old binaries and historical evidence remain unchanged. No theorem is
proved by finite agreement; final benchmark settings, broader experiments and
clean-machine/release work remain open. DCLDS remains deferred; M5 is incomplete.

## M5 scope/readiness preparation — 2026-10-08

P11.2/P14.1 gain a [concrete proposed scope and remaining-gate map](M5_COMPLETION_PLAN.md),
with [executed preparation checks](../evidence/m5/final-scope-20261008/REPORT.md).
D039 closes development optimization; D040 is only a proposal. The review pack
checks two graph and two executable pins, 40 production-source hashes, seven
baseline patch hashes, the four paper hashes and 113 prior raw inventory entries.
Both supported-schema drafts are rejected for execution and pass separate read-only
schema/pin checks; deterministic schedule counts are 240 main, 60 core and 60 stop.
The stop specification is explicitly not supported by the current runner.

Existing harness tests pass 49/49. A preparation-time hardware/load/VM/power
snapshot and successful read-only hardware/swap retry are recorded, without
changing system settings. This is not continuous monitoring or a controlled-load
benchmark. No production/reference/experimental-harness source changes, native
solver/baseline runs, C++ builds, sanitizer campaigns or new mathematical evidence
are added. O12's reporting scope is clarified, not newly proved or algorithmically
validated. Full-mode/prefix and per-block observation support, final configuration,
all 360 proposed native calls and release work remain unrun. No M5 task is newly
completed; DCLDS remains deferred.

## D040 execution readiness — 2026-10-08

P11.1/P11.2/P12.1 gain [external-harness readiness](../evidence/m5/final-evaluation-20261008/REPORT.md).
The selected five-repeat scope has three executable configs with unchanged
draft graph/binary pins and schedule order. `validate_comparison` rejects mixed
binary/feature prefix comparisons; `compare_prefix` requires the exact ranked
fixed-k prefix, including exhaustion/zero-density tails. Full external validation
uses explicit all scope. Read-only block observations are excluded from native
timing; power changes, missing required power observations and interruption retain
completed records and an explicit unrun ledger. No load-based filtering exists.

Final reference/adapter/harness pytest passes 164 tests. Six tiny VF calls and
definition validators pass; three strict prefix comparisons pass. These exercise
O09/O12 contracts without modifying or reproving the solver. Production/reference/
baseline algorithm sources and papers stay unchanged. C++/sanitizer rebuilds,
the 360 native measurements and release work are not completed by readiness.

## D040 evidence and IPPV-B09 repair — 2026-10-08

[P11.1/P11.2 execution](../evidence/m5/final-evaluation-20261008/REPORT.md) freezes
configuration before measurement and keeps validation levels/time boundaries
separate. Of 360 planned native calls, 302 execute and pass separate structural
checks. The main suite stops after 182 at a genuine h=4,k=15 disagreement; 58
stay unrun. Core completes 30 strict pairs and B-stop completes 30 strict prefix
pairs. Main has 90/91 tie-aware matches (35 strict). Counters and timings remain
observations, not theorem evidence or a real-graph completeness certificate.

The [B09 exact witness and regression](../evidence/m5/ippv/equality-20261008/REPORT.md)
disprove one IPPV candidate's maximality via a connected 21-compact proper
superset. This corroborates VF's exclusion of that set without certifying all
original top-15 outputs. An independent 13-vertex full-superset reference confirms
the smaller equality-bridge failure. Patch 0008 fixes two baseline verification
boundaries; both build profiles pass the named new/old regressions and original
repair replay, retaining 16 known zero-density failures in the 48-run corpus.
No proof, reference or production VF change occurs. P09.1 remains limited by the
known full-domain gap. D041 uses fresh paired measurements for the repaired
version; all old main timings and failed/unrun records remain separate.

P14.1/P15.1 gain scoped interpretation, 6 aggregation tests, verification of
3,309 raw inventory entries and byte-identical regeneration of 22 artifacts.
Broad final conclusions and clean-machine release remain unfinished.

## D041 selected-scope conclusion and local rebuild — 2026-10-08

P12.1/O12 gain [240 repaired-main records](../evidence/m5/final-main-repaired-20261008/REPORT.md):
240 structural checks, 120/120 tie-aware pairs, 40 strict pairs, no failed/censored/
unrun D041 calls. D040's 120 VF-only ablation records remain valid; its stopped
182-call seven-patch main and 58 unrun calls remain separate. Every final setting
has five repeats; prior-version and development timings are not pooled.

P14.1's selected-scope review is complete. VF's wall median is lower in 11/24
settings, IPPV's in 13/24; VF RSS medians are lower in 10/24. Observed load/swap,
full ranges, CPU time, native IPPV verification and output-tie differences stay
visible. These descriptive results do not establish a universal speed/memory
advantage, real-graph maximality/completeness, SOTA or a new mathematical claim.
The main raw inventory verifies 2,765 entries and all 12 derived artifacts
regenerate byte-identically, without native algorithm reruns.

P15.1 gains [fresh local builds and smoke](../evidence/m5/reproduction-20261008/REPORT.md):
23 commands exit 0, 16/16 CTest and 164 pytest pass; all eight IPPV patches apply
to a fresh pinned local checkout before its Release build. Three baseline fixtures
and the VF triangle/isolate full-output fixture pass independent definition checks.
Rebuilt VF and IPPV executables match their measured hashes on this host. The
initial wrapper-path failure and its source/log are preserved; no build began in
that attempt. This is same-host reuse of installed dependencies, not a clean-machine
run or a repeated sanitizer/differential acceptance campaign. All four paper
hashes match and production/reference remain unchanged. P09.1/P10.1/P12.1/P15.1
broader gates remain open; DCLDS is deferred and M5 is not marked complete.

## Fresh Ubuntu software-environment reproduction — 2026-10-08

P15.1/O12 gain [executed Linux evidence](../evidence/m5/clean-env-20261008/REPORT.md):
fresh Ubuntu 24.04.5 arm64 userspace/dependency installation, GCC 13.3 strict
Release builds of VF and pinned eight-patch IPPV, 23 successful smoke commands,
16/16 CTest, 164 pytest and four separate definition checks. All four fixture
outputs equal the macOS outputs; 26 aggregate/review artifacts regenerate
byte-identically. This is shared-kernel OrbStack on the same Mac, not independent
hardware or repeated performance measurements. Finite agreement is implementation
evidence, not proof or real-graph completeness.

`scripts/reproduce_release.py::main` preserves the virtualenv interpreter path;
`tests/m2_probe.cpp::main` and `tests/m3_probe.cpp::main` split adjacent statements
to satisfy GCC's existing warnings. No production/reference/theory change occurs.
The failed interpreter/build attempts and their source hashes remain preserved.
The two modified probes rebuild under AppleClang and pass 3/3 affected smoke tests.
Read-only integrity checks verify 6,074 historical raw entries, four papers,
40 production hashes, 112 unchanged source/test/fixture files and whitespace-only
changes in the two probes. Original broad M5 gates remain open pending explicit
scope closure; no new sanitizer/full differential campaign or DCLDS work is claimed.

## Bounded M5 closure — 2026-10-09

D042 closes the explicitly bounded M5 stage using the existing D040/D041 and
fresh Ubuntu evidence above. The [current acceptance checklist](TASKS.md) covers
P09.1/P11.3 in the selected baseline scope, P11.1/P11.2, the executed P12.1 grid,
P14.1's restricted conclusions and P15.1's local package/clean-userspace reproduction.
The original broader checklist remains visible with unperformed coverage and
stronger release levels deferred or limited. IPPV zero-density/license limitations
and D029's DCLDS deferral remain unchanged.

This closure changes documentation/status only. No new algorithm, experiment,
fixture, seed, build/test result or mathematical obligation is introduced.
Prior counts remain 360 final native calls, 120 main tie-aware matches, 30 core
matches, 30 early-stop prefix matches, and 26 identically regenerated artifacts.
Failed/censored historical evidence remains separate. Finite agreement does not
prove the theorem, certify real-graph completeness or establish universal speedup.
