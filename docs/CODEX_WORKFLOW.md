# Codex Workflow for VF-LhCDS

Revision 2026-09-09. Start with `AGENTS.md`, then the active milestone and task IDs.
Use `ALGORITHM_SPEC.md` for behavior, `THEORY_TO_CODE_AUDIT.md` for arguments,
`CORRECTNESS_TEST_PLAN.md` for test contracts and `CLAIM_TRACEABILITY.md` for evidence.

## 1. Small, checkable work units

Each request specifies one task or coherent task group, prerequisites, source
obligation, observable behavior, forbidden changes and verification command.
Do not implement an entire paper in a single unbounded request. Do not reopen
settled decisions or silently choose new consequential experiment parameters.

## 2. Order and parallel work

M0 contracts first. M1 truth and M2's standalone flow work can proceed independently;
M2 oracle integration needs reference fixtures and graph/clique infrastructure.
M3 needs M1+M2. Complete a correctness review and freeze before M4 optimization.
M5 baseline metadata/build/harness work may run in parallel once its input/output
contracts are stable; it does not block M3. DCLDS detail review respects D012.

Streaming, alternate flow algorithms, tie-inclusive mode and parallel enumeration
are optional and do not appear as missing core-release requirements.

## 3. Completion report

```text
task_id / obligation_id / prerequisites
files and code symbols changed
commands, environment, fixture manifest or seeds
actual test results and evidence paths
mathematical refinement argument, if behavior changed
performance observations only if measured
remaining limitations and unrun work
```

Mark tasks complete only when their evidence exists. Leave the implementation
ledger planned after documentation-only changes. A reviewer script using exhaustive
F is not evidence that production max flow or automatic fallback works.

## 4. Reviews

Correctness review: oracle scope, tie rules, boundary cliques, immutable chain
endpoints, original-graph extraction, exact arithmetic/fallback, independent
reference, relabeling ties and zero-density behavior. Never hide a solver bug with
a candidate-verification fallback.

Performance review: actual hotspots, enumeration/network memory, core cost,
cache hit rate, timing boundaries and dataset selection. Do not mix an unproved
semantic optimization into performance cleanup. Release review checks evidence
levels, baseline inclusion/exclusions, run provenance and clean reproduction.
