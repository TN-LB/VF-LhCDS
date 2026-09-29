# Claim-to-Code-to-Test Evidence

Revision 2026-09-09. Proof obligations and their arguments live in
`THEORY_TO_CODE_AUDIT.md`; this file is the single implementation evidence ledger.
A code symbol, test command, evidence path and commit are needed before marking
`implementation-tested`. Passing tests do not prove a theorem.

| Obligation | Exact source | Planned owner / symbol | Tests | Evidence / commit | Status |
|---|---|---|---|---|---|
| O01 Definition-level truth | Defs. 1.1-1.3 | reference: direct_compact, direct_maximal_compact, direct_lhcds | T01,T02 | [M1 reference execution](../evidence/m1/REPORT.md); `1a4829a9348dae299ae074717928909598b11af6` | implementation-tested (independent reference scope) |
| O02 Hierarchy/leaves | 1.8-1.10 | validation/reference_campaign.py: check_case | T02; reference hierarchy diagnostics; production T11,T14 pending | [M1 finite reference diagnostics](../evidence/m1/REPORT.md); reference commit `1a4829a`; production pending | planned (formal acceptance pending) |
| O03 Largest F / independent chain | 1.11-1.14 | reference: exhaustive_F, cardinality_line_chain | T03; M2 T09 executed; solver T10 pending | [M1](../evidence/m1/REPORT.md), reference commit `1a4829a`; [M2 oracle evidence](../evidence/m2/REPORT.md), new commit pending | planned (remaining production scope / commit gate) |
| O04 Exact separator | 1.15; Eq. 11-12 | solver: visit_interval | T06,T10 | not run | planned |
| O05 Restricted/global boundary | 1.19 proof + audit A | ClosureOracle::largest_restricted, full_graph_request, global_F | T08,T09 | [M2 executed](../evidence/m2/REPORT.md); source hashes, new commit pending | planned (formal commit gate; M2 tests passed) |
| O06 Exact network / largest ties | Eq. 15; 1.19 | aggregate_footprints; oracle execute; Dinic<Capacity> | T06,T07,T09 | [M2 executed](../evidence/m2/REPORT.md); source hashes, new commit pending | planned (formal commit gate; M2 tests passed) |
| O07 Terminal extraction | 1.16 | solver: extract_terminal | T11,T17 | not run | planned |
| O08 Fixed-k order / verification-free | 1.17; top-k convention | solver: emit_fixed_k | T12,T15,T16 | not run | planned |
| O09 Query / network bounds | 1.18; 1.20 | QueryStats; ClosureOracle::largest_restricted | standalone/network counters executed; full-recursion T13 pending | [M2 measured network/counter checks](../evidence/m2/REPORT.md) | planned (solver query bound pending) |
| O10 Safe core search bounds | 1.21-1.22 | clique: peel_core; oracle: certified_core_bounds | T17 | not run | planned |
| O11 Exact numeric refinement | 1.19-1.20; D005 | Fraction; checked_add/sub/mul; ClosureOracle::largest_restricted; Dinic | T05,T07 | [M2 executed real auto fallback](../evidence/m2/REPORT.md); source hashes, new commit pending | planned (formal commit gate; M2 tests passed) |
| O12 Evidence scope / validation | Def. 1.3 + audit F | external validation / experiment harness | T02,T14; shared smoke | not run | planned |

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
O01's reference implementation now has the required commit. M2 remains a new
uncommitted working tree on that base, identified by [source hashes](../evidence/m2/source_hashes.json)
and [changed files](../evidence/m2/files_changed.json). Consequently the formal
`implementation-tested` table label for new M2 implementation is withheld pending
its commit; this does not mean its tests were unrun. No theorem claim follows.

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

P02.1–P03.5 are complete at M2 scope. All M3+ tasks, chain/core certificates,
solver timing/hash/fixed-k output, end-to-end solver verification, baselines,
benchmarks, extended campaigns and TSan remain unrun/unimplemented. The oracle
failure minimizer's mismatch path was not triggered by this successful campaign.
Papers, accepted decisions, theory contracts and all M1 reference bytes remain
unchanged. No external baseline technique was used (D012).
