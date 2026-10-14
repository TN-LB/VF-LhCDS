# AGENTS.md - VF-LhCDS Repository Instructions

## Mission and source priority

Implement and evaluate the exact verification-free top-k algorithm in
`papers/veri_free_lhcds_v3_1_submit.md`. Mathematical correctness, implementation
validation and empirical performance are separate claims. Never trade the first
for the third, and never call finite test agreement a proof.

Priority: unchanged proof manuscript; explicit decisions in `docs/DECISIONS.md`;
`docs/ALGORITHM_SPEC.md` plus its audited clarifications; implementation/evidence
plans. Other papers specify baselines and related work, not replacement semantics.
Do not edit any of the four files under `papers/` without a separate requested
manuscript revision. Preserve D012's independent-development/freeze boundary.

## Decision boundary

Carry out theorem-forced clarifications and the routine implementation choices
already specified in this revised plan without repeatedly asking the owner.
Do not reopen accepted D005 (real arbitrary-precision fallback), D006 (set order)
or D012 (independent parallel work) as unresolved questions.

Request a decision before a new choice changes the problem definition, output
policy, theorem assumptions, licensing/use of external techniques, or final
experimental fairness/conclusions. Record alternatives, consequences and a
recommended default; block only that affected path. Final dataset/resource/thread/
timeout choices must be recorded before a benchmark campaign, not silently chosen
after results. A plan-review default is not a claim of prior owner confirmation.

If a proof/specification conflict or counterexample appears, document it and stop
that local path. Do not silently fix the manuscript or hide the failure in output
validation. Independent unaffected work may continue.

## Core mathematical contracts

- Nonempty finite simple undirected graph; fixed h>=2; induced subgraphs; preserve all declared vertices.
- Exact clique counts, rational densities and capacities; no floating semantic decisions.
- Oracle largest-set ties are cardinality-based; ranked output ties use the accepted original-ID lexicographic order.
- Separate largest restricted optimum from global F; global equality requires certified containment.
- A standalone global query may return empty; strict X<F progress is specific to separator queries.
- ChainInterval endpoints stay immutable; core reduction changes only Y_oracle, never lambda or recursion endpoints.
- Use left-first traversal; terminal comparison is Z==original Y.
- Extract ordinary connected components of original G[Y\X]; emit only those with no edge to all of X.
- Only emitted components have the terminal layer density; no candidate verifier in the solver path.
- Fixed-k means min(k,q); k=0 is invalid; preserve zero-density/isolate solutions.
- A complete basic recursion has 2r-1 logical queries, not necessarily that many mincuts; no O(k) claim follows.

## Required minimal implementation

Independent Python direct-definition/exhaustive-F/line-envelope reference; C++17
and CMake; one materialized clique backend; aggregated footprints; one generic
exact Dinic algorithm with checked 128-bit and actual automatic arbitrary-precision
execution; one fixed-k solver; minimal CLI and evidence telemetry.

Streaming, extra flow algorithms, tie-inclusive output, component scheduling and
parallel execution are deferred. Do not make them prerequisites for the first
correctness release or add their dependencies merely for future convenience.

## Workflow and tests

Use milestone/task IDs in `docs/TASKS.md` and proof obligations in
`docs/THEORY_TO_CODE_AUDIT.md`. Name the test, implement the smallest correct
behavior, run relevant deterministic/differential tests, then optimize only after
M3. Every semantic optimization needs a written argument, preconditions, a switch,
and output-equivalence evidence. Timings and backend trace fields are excluded
from canonical semantic hashes.

Reference code may not call production code. Check every proper superset for
reference maximality. Construct the expected chain independently of recursive
separation. Relabel complete truth and re-sort before comparing fixed-k ties.
Save failing seeds and original/minimized reproducers. Test ASan/UBSan, exact
numeric limits and real fallback. TSan is required before parallel code is enabled.

`review/math_sanity.py` is plan-review evidence only, not a completed production
reference, flow backend, sanitizer campaign or benchmark.

## Local commits

Owner direction (2026-10-06): after meaningful progress and the relevant checks,
create a focused local Git commit without asking for confirmation again. Include
task-related code, documentation and evidence; leave unrelated edits untouched.
Report the commit ID and any remaining limitations. Do not push unless the owner
explicitly requests it. A commit is a progress checkpoint, not a declaration that
a milestone is complete; preserve failed/censored experimental evidence.

## External methods and experiments

Pin baseline commits and record licenses, patches, supported h, output semantics
and timing. DCLDS and IPPV are primary general-h targets; specialized baselines are
stratified. Do not copy DCLDS techniques into the proposed algorithm without the
separate approval required by D012, even if a license permits copying.

Current owner direction (2026-10-02, D029): defer further DCLDS reading, acquisition,
code/theory comparison and integration. Continue the independently planned
VF-LhCDS/IPPV work; DCLDS is not a prerequisite for this current execution stage.
Preserve its existing snapshots and historical records; do not mark P09b.1 complete.

Current owner direction (2026-10-14, D045): the selected follow-up plan is
`docs/M6_M8_EXECUTION_PLAN.md`: M6 cost diagnostics, M7 interval-local
clique propagation/count reuse, and M8 unified formal experiments. This supersedes
D039's optimization stop only for that increment. Preserve the original interval
clique set across query-local core filtering. Rebuild diagnostic/control binaries
against final optimized source. Earlier local timings remain preliminary and are
excluded from M8; final resource/data/variant settings still require freezing.
Completion follows delivered implementation, validation and reproducible evidence.

Use common normalized graphs. Distinguish definition-checked, structural-checked
and cross-implementation-agreement evidence. Density/connectivity checks do not
prove LhCDS maximality. Keep external validation outside algorithm timing; include
any native baseline candidate verification in that baseline's algorithm time.
Record all completed, timeout, OOM and error runs; no post-hoc favorable selection.

## Completion report

Report changed files, code symbols, task/obligation IDs, commands, environment,
fixture/seed manifest, actual results and evidence locations, plus remaining
limitations. Update tasks and traceability only for executed work. Never mark a
test or build complete merely because its command is documented.
