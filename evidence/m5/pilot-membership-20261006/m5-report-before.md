# M5 partial execution status — 2026-10-02

**Latest execution, 2026-10-06:** [CA-CondMat paired diagnostic](condmat-pair-20261006/REPORT.md).
Both programs return five structurally checked sets. Ranks 1–4 are identical;
rank 5 differs only at the density-22 cutoff, so tie-aware agreement passes.
VF membership takes 38.525397500 s; seven-patch IPPV takes 2.723666167 s. All four
native/validator exits are zero. This is one pair; repeated experiments and M5
remain incomplete. Production and historical evidence are unchanged.

**Previous execution, 2026-10-06:** [CA-CondMat membership diagnostic](condmat-membership-20261006/REPORT.md).
The existing membership mode completes h=3,k=5 in 38.997086249 s, returning five
structurally checked sets after 304 queries/mincuts. Native and validator exits
are zero. This single diagnostic uses unchanged production code; no repeated
speedup or paired comparison is claimed. The 60-second completion issue is
resolved for this mode/case; wider experiments and M5 remain incomplete.

**Previous execution, 2026-10-05:** [D032 CA-CondMat phase diagnosis](condmat-phase-20261005/REPORT.md).
The separate adjacency probe passes both builds and two tiny output/query-counter
checks plus independent definition validation. CA-CondMat parsing and indexing
finish in 0.042061041 and 0.1166765 s. The run completes 137 queries/mincuts before
the unchanged 60-second guard interrupts solving, with no accepted output.
Each completed query scans all 173,361 triangles. Internal operation costs are
not isolated. All production/library pins and the historical fixed-pilot record
are preserved. An existing-membership-mode diagnostic is prepared only; no
post-timeout real run, production optimization or broad M5 completion follows.

**Previous execution, 2026-10-05:** [D031 repaired-baseline pilot](pilot-fixed-20261005/REPORT.md).
The same approved 48-call grid is frozen with seven-patch IPPV. All 24 CA-GrQc
runs and separate validators complete; 12/12 pairs match with cutoff ties
allowed (6/12 strictly). Every completed three-repeat cell has stable output.
The first CA-CondMat VF call, h=3,k=5, hits the 60-second limit. The driver exits
1 after 25 calls and retains 23 unrun entries. Time/RSS summaries and the
timeout are saved separately from the historical pilot. The timeout's phase is
unknown; no post-stop native call, algorithm change, build or test-suite rerun
is performed. P12.1 and M5 remain incomplete.

**Previous execution, 2026-10-05:** [discrepancy diagnosed and fixed](ippv/disagreement-20261005/REPORT.md).
Independent all-deletion checks and an exact global flow/cut certificate establish
that VF's disputed density-56/13 set is correct. IPPV-B07 truncates fractional
verification capacities; patch 0006 preserves them by checked exact scaling.
Patch 0007 repairs an additional PAVA vector-size violation. Both final builds
pass the new all-superset regression and original k=20 comparison; 123 pytest
checks pass and prior baseline coverage is retained. The known zero-density
omission remains. The stopped pilot and old binaries are preserved; benchmark
execution is not resumed and no new performance conclusion is made.

**Previous execution, 2026-10-05:** [D030 approved pilot, stopped](pilot-20261005/REPORT.md).
The owner approved the exact 48-call proposal. Twenty native calls and their
20 external validators complete; nine of ten pairs pass tie-aware agreement.
CA-GrQc h=3,k=20, repeat 0 disagrees: VF returns a density-56/13 set absent from
IPPV above their shared 10/3 cutoff. The driver stops with exit 1 and retains
28 unrun calls, including all CA-CondMat runs. Raw outputs, the original
reproducer and all-cell aggregates are saved. Cause remains unresolved; no
algorithm repair, rerun, minimization or broader performance conclusion follows.

**Previous execution, 2026-10-05:** [fresh paired smoke and preparation](paired-smoke-20261005/REPORT.md).
Both pinned builds complete CA-GrQc h=3,k=5 with five structurally checked sets,
strict output agreement and identical semantic hashes. IPPV takes 0.176496415 s
and VF adjacency/basic 1.202863333 s in this one pair. This completes P11.3's shared
smoke gate, without a repeated-performance conclusion. External stop-on-failure
control is tested; combined pytest passes 123 checks. The [48-call repeated pilot](campaign-proposal-20261005/PROPOSAL.md)
is fully specified as a draft and remains unrun pending owner decision. No new
production algorithm, build, theorem change or DCLDS work is included.

**Previous execution, 2026-10-03:** [authorized enumeration extension](enumeration-20261003/REPORT.md).
Adjacency extension is implemented behind an explicit selector, with combinations
still the default. Three profiles pass 14/14 CTest; 115 pytest checks and 14
differential campaigns pass. All 1,392,496 saved response records agree with their
pre-change counterparts except measured reduction time. CA-GrQc h=3,k=5 now
completes in 0.767723375 s and returns five structurally checked sets strictly
matching the historical IPPV run. The bounded repair is complete; final benchmark
policy and a fresh paired campaign are pending. No formal speedup is claimed.

**Previous execution, 2026-10-03:** [approved phase diagnostic](phase-diagnostic-20261003/REPORT.md).
The separate probe builds and passes both tiny output/definition checks. On the
same CA-GrQc h=3,k=5 input, parsing takes 0.0038615 s and the index constructor
has not returned at the 60-second guard; solve is not reached. The production
algorithm, binary and library are unchanged. An enumeration-preservation/change
plan is prepared but unimplemented; work stops at the measured blocker.

**Previous execution, 2026-10-03:** [approved four-mode diagnostic](m4-mode-diagnostic-20261003/REPORT.md).
The owner-approved four existing M4 modes each run once on CA-GrQc h=3,k=5 with
the same pinned binary and 60-second guard; all four time out, with no completed
outputs or eligible comparisons. Evidence integrity checks pass; no code change,
build or test-suite rerun. Expansion stops at the continuing runtime blocker.
A separate phase-diagnosis proposal is prepared but unrun. DCLDS stays deferred.

**Previous execution, 2026-10-03:** [shared harness report](harness-20261003/REPORT.md).
New external tools pass 112 pytest tests and preserve 12 tiny native outcomes.
The shared real CA-GrQc smoke completes for IPPV but times out for VF basic at
60 seconds. Formal experiments remain unrun; expansion pauses for the proposed
diagnosis/resource choice. DCLDS remains deferred.

**Current direction, D029:** the owner has deferred further DCLDS reading and
integration and asked to continue the independently planned VF-LhCDS/IPPV work.
The earlier DCLDS decision stop below is historical, not a current blocker for
that scope. No DCLDS use approval or completion is implied. Existing evidence and
the independent-development boundary are preserved.

## IPPV / P09.1

Routine reproduction fixes are authorized by D028. The original three disclosed patches fix
the unused OpenMP include, uninitialized clique-count member, and invalid indexed
access after clearing the selection vector. Reproducible Release and ASan/UBSan
builds succeed. A cache-safe build-script refinement preserves the tested binary
and compiler-command hashes. No new dependency was installed.

The external adapter preserves original vertex IDs and native selected sets,
records child exit/time/RSS, and validates in a separate process. Tests: 17 adapter
plus 74 unchanged reference tests pass. Six tiny native cases pass definition
checks; the author CA-CondMat example returns 20 structurally checked outputs.
Three zero-density completeness mismatches are retained, including both builds
on the smallest possible nonempty graph. Native exit success does not make those
semantic checks pass. No missing result is synthesized.

[Full IPPV report, environment, commands, symbols and fixture/run records](ippv/reproduction-20261002/REPORT.md).
[Integrity verification](ippv/reproduction-20261002/verification.json).
P09.1 is partial; no general-h, numeric-safety or comparative-performance claim.

After D029, two further patches repair h=2 enumeration and a single-edge component
boundary. The current build uses five patches. The final 48 native diagnostics
across h=2,3,4,5 have 32 definition passes and 16 preserved zero-density mismatches;
both profiles build successfully. The repeated real smoke returns the same 20
structurally checked outputs. [Latest coverage report](ippv/coverage-20261002/REPORT.md)
contains commands, environment, fixtures and failure/repair evidence.

## DCLDS / P09b.1

After the owner's "继续", a D012 snapshot preserved 98 file hashes, M4 commit
`56229397903813d3509ecb45b178bbde823e357b`, M3 correctness tag and current audit
document bytes before detailed comparison. Public metadata identifies commit
`60093e582bc584815ab824c3e8b94efdef138200`. GitHub reports no identified license;
the full 16-file inventory has no license/notice-named path. Source-file notices
and separate grants are unverified.

The new DCLDS licensing/use choice is not covered by IPPV-specific D027/D028.
The preflight originally stopped under AGENTS.md and the owner's stop-on-decision
instruction. D029 subsequently deferred the entire DCLDS reading/integration path,
so no DCLDS license decision is currently requested and this does not block the
independent scope. No DCLDS technique is imported. The [historical stop](dclds/preflight-20261002/stop.json)
is preserved without relabelling unrun work as complete.

## Scope and files

New code is confined to `baselines/ippv`: `build.py`, `process.py`, `adapter.py`,
`test_adapter.py`, `check_toys.py`, README, source lock and five patches. Updated documents are
`docs/DECISIONS.md`, `docs/TASKS.md`, `docs/BASELINE_AUDIT.md`, and
`docs/CLAIM_TRACEABILITY.md`, `docs/EXPERIMENT_PLAN.md`, and the owner-direction note
in `AGENTS.md`. Evidence files preserve successful and failed runs,
source/version pins, snapshots and logs. The [previous whole-tree manifest](harness-20261003/files_changed.json)
describes the prior uncommitted M5 working tree; the [four-mode manifest](m4-mode-diagnostic-20261003/files_changed.json)
and [phase-diagnostic manifest](phase-diagnostic-20261003/files_changed.json)
list their respective turn-specific changes without relabelling earlier work.
The [latest enumeration manifest](enumeration-20261003/files_changed.json) records
this authorized production change, tests, contracts and its evidence.
The [paired-smoke manifest](paired-smoke-20261005/files_changed.json) separates
the current external runner/test/document changes and new evidence from those
earlier production changes.
The [pilot report](pilot-20261005/REPORT.md) records this continuation's approval,
new evidence-only aggregation script and document changes, with no algorithm or
runner modification.

All four papers and the independent reference are unchanged. The latest authorized
enumeration extension changes six of the 53 original M4 source paths and adds
tests; the other 47 match. Its three CTest profiles were executed as recorded
above. DCLDS execution/adaptation, broader IPPV coverage, final
broader data/resource/h/k/repeat/cache approval, a campaign pinned to the repaired
IPPV version, wider benchmarks and release reproduction remain unrun. The limited
D030 pilot is approved but remains a stopped historical result; the discrepancy
has since been diagnosed and repaired in separate evidence. M5 remains incomplete. Finite
tests support implementation validation and do not prove a mathematical theorem.
