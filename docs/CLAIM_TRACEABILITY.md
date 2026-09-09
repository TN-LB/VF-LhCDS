# Claim-to-Code-to-Test Evidence

Revision 2026-09-09. Proof obligations and their arguments live in
`THEORY_TO_CODE_AUDIT.md`; this file is the single implementation evidence ledger.
A code symbol, test command, evidence path and commit are needed before marking
`implementation-tested`. Passing tests do not prove a theorem.

| Obligation | Exact source | Planned owner / symbol | Tests | Evidence / commit | Status |
|---|---|---|---|---|---|
| O01 Definition-level truth | Defs. 1.1-1.3 | reference: direct_compact, direct_lhcds | T01,T02 | not run | planned |
| O02 Hierarchy/leaves | 1.8-1.10 | reference hierarchy diagnostics | T02,T11,T14 | not run | planned |
| O03 Largest F / independent chain | 1.11-1.14 | reference: exhaustive_F, cardinality_line_chain | T03,T09,T10 | not run | planned |
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
