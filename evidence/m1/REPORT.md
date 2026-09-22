# M1 completion record — 2026-09-17

Scope: P01.1-P01.5, independent Python reference only. Base commit:
`a779112bcfe6ff6360876ecb44ec46c49777ff85`. This delivery is uncommitted; the
file/hash manifest identifies it without inventing an implementation commit.
M0 evidence was retained unchanged. No new theory/specification conflict was
found and no M2+ task is marked complete. Finite tests do not prove the theorem.

## Task status and implemented symbols

| Task | Status | Implementation / evidence |
|---|---|---|
| P01.1 | Complete | `graph.Graph`, `normalize_graph`, ordinary components/connectivity; `direct.combination_cliques`, `Reference.mu_h`, `density`, `deletion_loss`, `direct_compact`, `compactness`. T01 plus independent induced-combination counting in both reference campaigns. |
| P01.2 | Complete | `direct_maximal_compact` examines every proper extension; `direct_lhcds` evaluates the direct definition and ranks exact densities/original IDs. T02's single-vertex extensions all fail while the full bridged two-triangle set succeeds. |
| P01.3 | Complete | `parametric.exhaustive_F` and `exhaustive_restricted` enumerate all feasible subsets, use signed exact scaled values, union all maximizers, and check the union's optimality. Empty/zero/equal bounds and restricted labels tested. |
| P01.4 | Complete | `cardinality_line_chain` uses cardinality maxima, all nonnegative line intersections, rational midpoints, zero and sentinel mu(V)+1. No recursion. T03 and a second coverage grid based on direct deletion compactness pass. |
| P01.5 | Complete | Canonical graph/set input, exact records, reference CLI, 11 hand truth fixtures, saved outer-breakpoint witness, deterministic exhaustive/seeded generators, default n<=12 guard before exponential work, explicit local override and import isolation tests. |

O01-O03 have executed reference evidence; O05/O08 have supporting reference-only
boundary/ranking diagnostics. No production obligation is accepted from this
work. The main ledger requires an implementation commit before the formal
`implementation-tested` label, so that label is withheld pending a commit rather
than falsely claiming these tests were unrun.

## Exact executed results

| Check | Actual result | Artifact |
|---|---|---|
| Final pytest | 74 passed, 0 failed, no skips/xfails, 1.26 s | `final/01.stdout`, `final/pytest.xml` |
| Existing CTest integration | 3/3 passed, 0 failed, 1.43 s; reference test invokes the same pytest suite | `final/09.stdout` |
| Standalone reference CLI | 6 successful invocations (truth full/prefix, global tie/empty, restricted zero, chain); invalid k=0 returned expected exit 2 with no result | `final/02.*` through `final/08.*` |
| Exhaustive-small reference | All 1,099 labelled simple graphs, n=1..5, h=2,3: 2,198 unique graph/h cases passed | `exhaustive-small/summary.json`, `cases.jsonl`, `exhaustive-small.log` |
| Seeded reference | 100 unique graph/h cases on 96 distinct graphs, n=6..8, fixed seed 20260917; all passed | `seeded/summary.json`, `cases.jsonl`, `seeded.log` |
| Paper preservation | All four SHA-256 hashes match M0 snapshot | `final/10.stdout`, `preservation_final.json` |
| Patch formatting | `git diff --check` exit 0 | `final/11.stdout`, `final/11.stderr` |

The campaign counts are **primary input cases**, not counts of queries or of
isomorphism classes. Each primary case also checks a deterministic relabeling,
then re-sorts complete truth before prefix comparison. The two campaigns have
disjoint n ranges, together covering 1,195 distinct primary labelled graphs
and 2,298 distinct primary graph/h cases. The unit tests' named/invalid cases
and CLI calls are separate; no unsupported all-tests unique-graph total is claimed.

Exhaustive-small made 36,968 global and 4,140 restricted reference queries and
checked every one of its 4,140 chain endpoint pairs. Seeded made 1,338 global and
149 restricted queries and checked all 149 chain pairs. Across both, 15,610
original/relabelled prefix checks passed (all k=1..q+2). These are reference
function executions, not production logical_interval_queries or mincut_calls.

Every campaign case compares cached counts with a separate per-induced-subset
combination count using original-ID edges. It compares global-F components with
direct maximal compact sets, hierarchy leaves with direct LhCDSes, envelope
coverage with a second grid from direct compactness, and certified reference
interval queries with full-graph queries. None of these diagnostics constructs
or invokes the production divide-and-conquer solver, closure network or flow.

## Commands and environment

Runtime: Python 3.12.2, pytest 8.4.2, macOS 15.7.7 / Darwin arm64. The existing
repository-local `.venv` was used; no packages were installed. Runtime imports
are Python standard library/reference only. CTest uses the existing M0 build;
no C++ configure/build or new sanitizer campaign was needed or run in M1.

Primary commands actually executed:

```sh
PYTHONPATH=reference .venv/bin/python scripts/find_reference_outer_witness.py
PYTHONPATH=reference .venv/bin/python validation/reference_campaign.py --tier exhaustive-small --output-dir evidence/m1/exhaustive-small
PYTHONPATH=reference .venv/bin/python validation/reference_campaign.py --tier seeded --output-dir evidence/m1/seeded
. .venv/bin/activate
python scripts/run_m1_checks.py evidence/m1/final
```

The final driver executed the complete argv lists in `final/commands.json`,
including `python -m pytest reference/tests -q --junitxml=...`, the seven CLI
commands, `ctest --test-dir build --output-on-failure`,
`python scripts/verify_papers.py` and `git diff --check`. All 11 commands returned
their expected exit codes: ten exit 0, one intentional invalid-k exit 2.
Each command has separate stdout/stderr, timestamps and SHA-256 hashes.
`campaign_commands.json` records the two successful campaign commands, environment,
timestamps and log hashes. `final/environment.json` captures runtime, base commit,
dirty state and the tested reference package hashes. Development pytest logs
are retained but do not replace the final result.

## Fixtures, seeds and the missing historical witness

`fixture_manifest.json` records fixture names/checksums, seeds, actual n/h/family
histograms and hashes of the complete campaign case files. Those JSONL case files
contain original IDs, complete graph edges, h, generator metadata, exact expected
ranked records, chains, breakpoints and sampled parameters. No failures occurred;
the original/minimized-failure branch exists but was not exercised by a real
failure and does not complete P05.1.

The declared coverage was recorded in `PLAN.md` before the tests. Seeded families
are random, planted, bridged, tied and disconnected, 20 accepted cases each. Named
fixtures cover K4/K5, overlapping K_h, h>n, zero-clique ordinary components,
isolates, original-ID ties and the multi-vertex maximality witness. The named
fixture expectations are hand specified, not generated by a production solver.

`review/math_sanity_results.json` was not supplied. The new deterministic search
(seed 20260917) found a seven-vertex h=2 witness at zero-based sampled graph 92,
after 185 graph/h attempts including the witness. It has chain
empty < {0,1,2,3,5,6} < {0,1,2,3,4,5,6}, with breakpoints 13/6 and 2. The T03 test
checks all 127 nonempty induced subsets and confirms none has density 2. The full
graph and provenance are in `reference/fixtures/outer_breakpoint.json`; the
canonical graph is saved alongside it. This is a documented replacement fixture,
not a claim that the unavailable historical witness was recovered. The search
log is `witness-search.log`. No theorem text was changed to accommodate it.

## Files changed and preserved boundaries

Full paths/checksums are in `files_changed.json`; evidence checksums are in
`evidence_sha256.json`. Modified existing files:

- `reference/vflhcds_reference/direct.py`, `parametric.py`, `__init__.py`;
- `reference/tests/test_skeleton.py`, `reference/README.md`, `validation/README.md`;
- `README.md`, `docs/TASKS.md`, `docs/CLAIM_TRACEABILITY.md`.

Added package modules: `graph.py`, `io.py`, `generators.py`, `cli.py`, `__main__.py`.
Added tests: `test_direct.py`, `test_parametric.py`, `test_io.py`, `test_cli.py`,
`test_properties.py`, `test_named_fixtures.py`. Added `reference/fixtures/` data,
`validation/reference_campaign.py`, `scripts/find_reference_outer_witness.py`,
`scripts/run_m1_checks.py` and `evidence/m1/` records.

`preservation_start.json`/`preservation_final.json` show the four papers, accepted
decisions, algorithm specification, theory audit, architecture, correctness plan,
M0 interface contract, CMake and C++ implementation are unchanged. Only the task
and evidence ledger changed among the monitored docs. D005/D006/D012 remain in
force. No DCLDS or other external baseline technique/code was consulted/imported.

## Remaining limits and unrun work

No unresolved blocking conflict. M1's declared finite gate is met. This is still
an exponential tiny-graph reference, with no scalability or theorem-proof claim.
The CLI's reference envelope is documented in `reference/README.md`; it is not
a claim to implement the production CLI or production semantic output hash.

All M2+ work remains open: production graph/clique/exact-number/footprint/flow/
oracle implementation, actual checked-128 automatic arbitrary-precision fallback,
recursive solver/extraction, telemetry, optimizations, baselines and experiments.
The full M3 1,000-case / 10,000-oracle-request seeded release tier, its production
higher-h differentials, ASan/UBSan numeric/solver campaign and TSan/parallel work
were not run. M1's 100-case supplement does not replace that release tier.
No large n>12 overridden truth enumeration, alternate Python/platform or
clean-machine reproduction was run. The mathematical proof remains a separate
claim from these finite implementation checks.
