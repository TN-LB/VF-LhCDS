# Claim-to-Code-to-Test Evidence

Revision 2026-09-09. Proof obligations and their arguments live in
`THEORY_TO_CODE_AUDIT.md`; this file is the single implementation evidence ledger.
A code symbol, test command, evidence path and commit are needed before marking
`implementation-tested`. Passing tests do not prove a theorem.

| Obligation | Exact source | Planned owner / symbol | Tests | Evidence / commit | Status |
|---|---|---|---|---|---|
| O01 Definition-level truth | Defs. 1.1-1.3 | reference: direct_compact, direct_maximal_compact, direct_lhcds | T01,T02 | [M1 reference execution](../evidence/m1/REPORT.md); implementation commit pending | planned (formal acceptance pending) |
| O02 Hierarchy/leaves | 1.8-1.10 | validation/reference_campaign.py: check_case | T02; reference hierarchy diagnostics; production T11,T14 pending | [M1 finite reference diagnostics](../evidence/m1/REPORT.md); implementation commit pending | planned (formal acceptance pending) |
| O03 Largest F / independent chain | 1.11-1.14 | reference: exhaustive_F, cardinality_line_chain | T03; production T09,T10 pending | [M1 reference execution](../evidence/m1/REPORT.md); implementation commit pending | planned (formal acceptance pending) |
| O04 Exact separator | 1.15; Eq. 11-12 | solver: visit_interval | T06,T10 | not run | planned |
| O05 Restricted/global boundary | 1.19 proof + audit A | oracle: largest_restricted, global_F | T08,T09 | not run | planned |
| O06 Exact network / largest ties | Eq. 15; 1.19 | oracle: footprints, build_closure; flow: Dinic<Capacity> | T06,T07,T09 | not run | planned |
| O07 Terminal extraction | 1.16 | solver: extract_terminal | T11,T17 | not run | planned |
| O08 Fixed-k order / verification-free | 1.17; top-k convention | solver: emit_fixed_k | T12,T15,T16 | not run | planned |
| O09 Query / network bounds | 1.18; 1.20 | telemetry: interval_queries, mincut_calls | T13 | not run | planned |
| O10 Safe core search bounds | 1.21-1.22 | clique: peel_core; oracle: certified_core_bounds | T17 | not run | planned |
| O11 Exact numeric refinement | 1.19-1.20; D005 | exact: Fraction, capacity_dispatch | T05,T07 | not run | planned |
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
