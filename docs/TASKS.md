# Task Tracker

Revision: 2026-09-29. `[ ]` means implementation evidence is still outstanding.
Document review and `review/math_sanity.py` do not complete these tasks.
Each task must link its command/log/seed evidence before being checked off.

## M0 - Freeze contracts and bootstrap (prompt 00)

- [x] P00.1 Preserve the four proof/reference files and record SHA-256 snapshots; retain D005 and D012. [Evidence](../evidence/m0/REPORT.md): owner confirmed no earlier snapshot existed; initial snapshot now recorded, all four match HEAD and pass before/after SHA-256 verification. D006 also unchanged.
- [x] P00.2 Review `THEORY_TO_CODE_AUDIT.md` obligations O01-O12 and revised decisions; flag only genuinely new semantic choices. [Evidence](../evidence/m0/REPORT.md): no new conflict; no theory/decision changes or second audit.
- [x] P00.3 Create C++17/CMake and independent Python layouts; warnings, CTest, pytest, sanitizer targets. [Executed commands/logs](../evidence/m0/checks/commands.json): Debug, ASan+UBSan, Release, RelWithDebInfo build and pass 3/3 CTest each; standalone pytest 1 passed.
- [x] P00.4 Freeze canonical input/output contracts, error statuses, fixed-k order, and minimal timing/counter definitions. [Frozen contract](INTERFACE_CONTRACT.md), [scope/evidence](../evidence/m0/REPORT.md); future algorithm behavior is documented, not implemented.

Gate: contracts are explicit and the skeleton commands actually run. No solver code yet.
M0 gate met on 2026-09-09. Later milestone statuses are recorded below.

## M1 - Independent exhaustive truth (prompt 01; needs M0)

- [x] P01.1 Combination clique enumeration, ordinary connectivity, `mu_h`, deletion loss, exact compactness. [M1 tests/evidence](../evidence/m1/REPORT.md): T01 and independent induced-combination counts across the declared reference tier.
- [x] P01.2 Direct LhCDS maximality over ALL proper supersets; test multi-vertex-extension witness T02. [Evidence](../evidence/m1/REPORT.md): bridged triangles plus definition/parametric component and hierarchy-leaf comparisons.
- [x] P01.3 Exhaustive largest `F_h(lambda)` including empty maximizers and zero lambda. [Evidence](../evidence/m1/REPORT.md): union-of-all-ties, signed exact objective, empty/equality/zero and explicitly restricted results.
- [x] P01.4 Independent cardinality-line chain; exact intersections/midpoints; outer-density witness T03. [Saved witness](../reference/fixtures/outer_breakpoint.json), [evidence](../evidence/m1/REPORT.md); prior review fixture was absent, so this is a documented new reconstruction.
- [x] P01.5 Canonical fixtures/generators and hard size guard; no imports from production. [Reference usage](../reference/README.md), [fixtures/seeds](../evidence/m1/fixture_manifest.json), [CLI/pytest logs](../evidence/m1/final/commands.json); default n<=12, explicit local override.

Gate: T01-T03 fixtures and the declared truth tier pass; no claim of production correctness.
M1 gate met on 2026-09-17: 74 pytest tests; 2,198 exhaustive-small graph/h cases
(1,099 distinct graphs), plus 100 seeded graph/h cases (96 distinct graphs).
This is reference-only evidence. Later milestone execution is recorded below.

## M2 - Exact primitives (prompts 02, 03; needs M0 and M1 for integration)

- [x] P02.1 Preserve declared vertices; canonical graph and reversible original-ID mapping. [M2 evidence](../evidence/m2/REPORT.md): T01 strict reader/normalizer, exact IDs, ordinary components and canonical checksum.
- [x] P02.2 One deterministic materialized h-clique/incidence backend; differential enumeration T04. [M2 evidence](../evidence/m2/REPORT.md): T04 tuples/incidence/all-subset counts agree in exhaustive-small, seeded and higher-h tiers.
- [x] P02.3 Exact fractions/counts and checked 128-bit operations; arbitrary-precision path end to end, T05. [M2 evidence](../evidence/m2/REPORT.md): T05 checked boundaries, signed objectives and actual automatic cpp_int flow execution.
- [x] P03.1 Aggregate residual footprints; all-subset identity T06. [M2 evidence](../evidence/m2/REPORT.md): T06 includes all nested bounds for n<=4 and every subset for each tested bound pair; boundary/singleton/repeated footprints.
- [x] P03.2 Generic exact Dinic with 128-bit and arbitrary-precision instantiations; residual-cut tests T07. [M2 evidence](../evidence/m2/REPORT.md): T07 135 tiny cut/backend runs, residual/cancellation tests and a 20,000-node explicit-stack path.
- [x] P03.3 Restricted-closure API plus certified-global wrapper; empty/equality/zero cases T08. [M2 evidence](../evidence/m2/REPORT.md): T08 private full-graph certificate factory; arbitrary bounds remain restricted; empty/equality/zero cases pass.
- [x] P03.4 Preserve `L=N+1` cardinality tie term; exact largest-set differential campaign T09. [M2 evidence](../evidence/m2/REPORT.md): T09 exact largest sets agree for 40,591 exhaustive-small and 12,000 seeded requests, plus named/higher-h tests.
- [x] P03.5 Minimal standalone oracle reproducer and logical-query/mincut counters. [M2 evidence](../evidence/m2/REPORT.md): 56 CLI invocations per final profile pass; counters distinguish shortcuts, actual cuts and executed numeric backends.

Gate: true global comparisons only use certified bounds; fallback runs rather than merely reporting overflow.
M2 gate met on 2026-09-22 at P02.1–P03.5 scope. Debug, ASan+UBSan, Release and
RelWithDebInfo each pass 5/5 CTest; independent pytest remains 74 passed. Both Debug
and sanitizer oracle campaigns pass. Full-graph certificates are implemented;
Chain/core certificate construction belongs to M3/M4. The owner subsequently
committed M2 as `0a4aef801fa91b38f7643b0b8c8f5683a58dbcd6`; its source/command
manifests remain in the M2 evidence directory. M3 execution follows below.

## M3 - Solver and correctness freeze (prompts 04-06, 13; needs M1+M2)

- [x] P04.1 Immutable principal-chain endpoints and exact outer lambda; separator invariant T10. [Evidence](../evidence/m3/REPORT.md): sealed same-owner points, all 4,140 exhaustive-small chain pairs, move-validity regression.
- [x] P04.2 Left-first traversal, original-endpoint terminal test, ordinary-edge leaf extraction T11. [Named traces](../evidence/m3/accepted/build-smoke/named_traces.json): K4/pendant non-emitting layer, bridged triangles and outer breakpoint.
- [x] P04.3 Fixed-k lexicographic ordering and stop; reject k=0; support k>q and full mode, T12. [Evidence](../evidence/m3/REPORT.md): every k=1..q+2 versus direct truth, huge IDs/k and no eager right query.
- [x] P04.4 Full run counts: exactly `2r-1` logical interval queries; mincut count reported separately T13. [Campaign manifests](../evidence/m3/fixture_manifest.json): independent chain and every complete trace/counter checked.
- [x] P05.1 Exhaustive/seeded differential tiers, saved failures and deterministic minimizer T14. [Evidence](../evidence/m3/REPORT.md): both Debug and ASan/UBSan complete release tiers; reducer tested with a labeled synthetic faulty candidate; no solver mismatch occurred to reduce.
- [x] P05.2 Tie-aware relabeling, isolates, disjoint-union and input-order properties T15. [Evidence](../evidence/m3/REPORT.md): complete truth relabeled/re-sorted, all prefixes; named and first 20 seeded isolate/disjoint cases; CLI input reorder.
- [x] P05.3 ASan/UBSan and numeric boundary suite; no candidate verifier in solver call path T16. [Review](../evidence/m3/REVIEW.md), [actual commands](../evidence/m3/accepted/commands.json): 9/9 CTest in four profiles, real arbitrary-precision regression, production-only build.
- [x] P06.1 Minimal canonical CLI/JSON output, timing boundaries, manifests, stable semantic hash. [Contract implementation](M3_IMPLEMENTATION.md), [production CLI run](../evidence/m3/accepted/cli-definition-run/manifest.json): 31 direct + 2 runner CLI checks per profile; external validation separately timed.
- [x] P13.1 Record code symbols + test evidence in traceability and tag the unoptimized correctness release. [Review](../evidence/m3/REVIEW.md) completed with R01 resolved; local annotated freeze recorded below.

Gate: no known semantic mismatch or silent overflow in the executed scope; no streaming/tie-inclusive/baseline requirement.
Implementation/test gate passed 2026-09-29: all 35 acceptance commands exit 0,
2,198 exhaustive-small + 1,000 seeded + 64 higher-h base graph/h cases per build
(tiers overlap), 74 unchanged reference tests. M3/P13.1 complete: local annotated tag `v0.1.0-m3-correctness` freezes the tested implementation.
Implementation commit: `23a5b3415cf3ae053e55a01b219ca074ffe6fd67`. [Report](../evidence/m3/REPORT.md).
At M3 delivery M4/M5 remained open; finite agreement is implementation evidence,
not a theorem proof. Executed M4 work follows below.

## M4 - Optional optimization (prompts 07, 08; needs M3)

- [x] P07.1 Exact clique-core peeling; one update per invalidated clique. [M4 evidence](../evidence/m4/REPORT.md): independent all-subset core truth, cascades and exact incidence/update counters in Debug and ASan/UBSan.
- [x] P07.2 Query-local `Y_oracle` only; original lambda, endpoints and extraction graph unchanged, T17. [Actual audit-C trace](../evidence/m4/core_witness.json): root non-chain core, lower-threshold pendant recovery and original-Y terminal extraction.
- [x] P07.3 Written containment argument + off/on equality + separate reduction-cost measurements. [Argument](M4_IMPLEMENTATION.md), [four-mode campaigns and local time/RSS](../evidence/m4/REPORT.md): core defaults off; exact threshold/work/time measured separately.
- [x] P08.1 Profile first; select ONE justified optimization and provide equivalence argument, switch and regression. [Pre-edit measurement/selection](../evidence/m4/profile-selection.json): membership footprint scan, explicit switch, all-corpus equality and 36 local post-change profile runs; sorted remains default.

M4 implementation/test gate met on 2026-09-29: 36/36 acceptance commands exit 0;
Debug, ASan/UBSan, Release and RelWithDebInfo pass 12/12 CTest each; pytest 74 passed.
Both Debug and sanitizer run 2,198 exhaustive-small, 1,000 seeded, 64 higher-h and
31 smoke base graph/h cases through all four core/footprint mode combinations.
M3 frozen sources/evidence/tag and M1 reference remain preserved. Changes are
uncommitted on `5802d5a`; source hashes identify the tested working tree, and the
formal new-code traceability commit gate remains pending. No new tag is required
by M4. Local synthetic diagnostics do not complete any M5 benchmark task.

Backlog, not the initial release gate: streaming, singleton folding, alternative flow algorithms,
oracle-result caches, component scheduling, parallel enumeration, tie-inclusive output.

## M5 - Baselines, experiments and release (prompts 09, 09b, 10-12, 14-15)

Current execution scope: D029 defers further DCLDS reading/integration at the
owner's request. Continue independent VF-LhCDS/IPPV validation and experiment
preparation. The earlier DCLDS license stop no longer blocks this scope; P09b.1
stays deferred and incomplete, and no full-competitor/SOTA claim follows.

- [ ] P09.1 IPPV: pin commit/license; build; audit output, parameters, preprocessing and timing.
  2026-10-01: [preflight evidence](../evidence/m5/preflight-20261001.json) confirms
  committed M4 source hashes and unchanged papers. IPPV metadata reports no
  identified license (`license: null`); authorization remains unverified.
  Stopped all further M5 work at the owner's requested decision boundary;
  no source build, adapter or experiment has run. See [options](BASELINE_AUDIT.md#m5-preflight-stop-2026-10-01).
  Subsequent owner decision D027 permits proceeding with IPPV use. Source is now
  pinned to `f61881d4752170c03585e4281f0c49d7ef14aa1e`; configuration passed,
  but the unmodified author build failed on missing `omp.h` under AppleClang.
  [Current stop/evidence](../evidence/m5/ippv/stop.json): stopped before patches,
  dependency installation, runtime validation or adapters; P09.1 remains open.
  2026-10-02: owner-approved patch 0001 removes the unused OpenMP include;
  [rebuild passed, exit 0](../evidence/m5/ippv/compat-20261002/commands.json).
  Runtime preparation then found an uninitialized `hc_num` read in the author
  constructor. [Current blocker IPPV-B02](../evidence/m5/ippv/compat-20261002/stop.json)
  is source-inspected, not a reproduced runtime failure. Stopped before applying
  a second fix or running the program; P09.1 and all M5 completion gates remain open.
  Subsequent D028 authorizes automatic IPPV reproduction fixes. Three hashed
  patches now build and run; the [current report](../evidence/m5/ippv/reproduction-20261002/REPORT.md)
  records 91 pytest passes, six tiny definition-check passes, one real structural
  pass (20 outputs), and three preserved zero-density completeness mismatches,
  including both builds on the one-vertex minimum reproducer. Source defects
  IPPV-B02/B03 are repaired. Full-domain comparison remains unresolved; no baseline
  output extension, experiment exclusion or M5 completion is implied.
  After D029: [h=2..5 diagnostics](../evidence/m5/ippv/coverage-20261002/REPORT.md)
  reproduce and repair missing h=2 enumeration (IPPV-B05, including ASan heap
  overflow) and skipped single-edge component extraction (IPPV-B06). The five-patch
  builds complete 48 tiny native runs: 32 definition passes and 16 preserved known
  zero-density mismatches. A repeated real smoke has 20 structurally checked
  outputs identical to the earlier three-patch run. Broad correctness/experiment
  gates remain open; this is not a performance comparison.
  2026-10-05: [D030 discrepancy repair](../evidence/m5/ippv/disagreement-20261005/REPORT.md)
  independently certifies VF's disputed set and repairs IPPV-B07 fractional
  capacity truncation plus IPPV-B08 PAVA workspace bounds. Seven-patch Release
  and sanitizer builds pass the new 13-vertex all-superset regression and the
  original k=20 tie-aware comparison. Numeric boundary tests pass in both
  profiles; 123 pytest checks pass. The 48-case h=2..5 corpus retains the same
  32 definition passes and 16 known zero-density omissions. The routine repair
  is complete, but the baseline's full-domain gate remains open.
- [ ] P09b.1 DCLDS: preserve D012 freeze boundary; add explicit primary-baseline adapter/audit; no technique import.
  **Deferred by owner, D029 (2026-10-02).** Do not continue reading/acquiring or
  integrating DCLDS until the owner resumes that work. The records below are
  historical; no licensing/use approval is being requested at this stage.
  2026-10-02: [pre-comparison snapshot](../evidence/m5/dclds/preflight-20261002/freeze.json)
  records 98 file hashes and the committed M4/M3 versions. Public metadata pins
  `60093e582bc584815ab824c3e8b94efdef138200`; GitHub reports `license: null`, and
  the complete 16-file inventory has no license/notice-named path. Source-file
  notices and separate permission are unverified. [Decision stop](../evidence/m5/dclds/preflight-20261002/stop.json)
  precedes source acquisition/build, detailed comparison or adaptation. Existing
  D027/D028 apply specifically to IPPV; no DCLDS use authorization is invented.
- [ ] P10.1 Audit only specialization baselines relevant to intended h=2/h=3 claims; record unavailable/excluded methods.
- [ ] P11.1 Separate definition-checked, structural-checked and cross-implementation-agreement evidence.
  2026-10-03: [shared harness evidence](../evidence/m5/harness-20261003/REPORT.md)
  implements separate validation processes, canonical exact-output checks, strict/
  tie-aware comparison, random within-block order, and preserved native failures.
  21 harness + 17 adapter + 74 reference tests pass (112 total). Shared tiny checks
  retain 10 completed outputs and two known IPPV zero-density mismatches across
  12 native runs; repeat hashes are stable. Full campaign metadata integration
  and final experiment scope remain unfinished.
- [ ] P11.2 Freeze graph checksums, parameter grid, timeout/memory/thread policy and phase timing in config.
  Local diagnostic configurations were frozen before execution; they are not
  final benchmark settings. CA-GrQc normalization preserves 5,242 declared vertices
  and 14,484 edges. Hardware/read failures, successful metadata retry, compiler
  commands, binary pins and raw evidence are saved. No final configuration is approved.
  2026-10-05 update: D030 approves the [limited 48-call pilot](../evidence/m5/pilot-20261005/approval.json).
  Its machine, graph/binary/source pins, h/k grid, three repetitions, seed, order,
  timing/resource and stop policies were recorded before launch. The original
  draft remains immutable. The broader final configuration remains open.
  D031 authorizes a [fresh seven-patch IPPV rerun](../evidence/m5/pilot-fixed-20261005/REPORT.md)
  with the same 48-call grid, resource limits, repetitions and seed. All pins and
  the unchanged machine profile were checked before launch; its baseline version
  and measurements are separate from D030's historical five-patch campaign.
- [x] P11.3 Run a shared validated smoke configuration before the full suite.
  The shared CA-GrQc h=3,k=5 smoke runs both algorithms: IPPV returns five
  structurally checked outputs; VF basic mode times out at the predeclared
  60-second guard. At that stage no completed cross-implementation comparison existed for this
  real case. The owner then approved the [four-mode diagnostic](../evidence/m5/m4-mode-diagnostic-20261003/REPORT.md):
  core-only, both, membership-only and basic each ran once with the same graph,
  binary and 60-second guard; all four timed out with no complete outputs.
  All six comparisons remain unavailable. The initial diagnostic choice is now
  executed. The owner then approved the [bounded phase diagnostic](../evidence/m5/phase-diagnostic-20261003/REPORT.md):
  its separate Release target builds, both tiny instrumented fixtures match
  production and independent definition truth, and CA-GrQc finishes parsing in
  0.0038615 s but remains inside index construction at the 60-second timeout;
  solve is not reached. The [enumeration-preservation/change plan](../evidence/m5/phase-diagnostic-20261003/ENUMERATION_PLAN.md)
  was subsequently approved and [implemented/validated](../evidence/m5/enumeration-20261003/REPORT.md):
  adjacency extension preserves ordered materialized tuples/incidence, with the
  original combinations default retained. Debug/Release/ASan+UBSan each pass
  14/14 CTest; 115 pytest checks and 14 differential campaigns pass. All 1,392,496
  saved response records match their pre-change counterparts excluding measured
  core-reduction time. The same CA-GrQc h=3,k=5/60-second diagnostic now completes
  in 0.767723375 s, with five structurally checked outputs strictly matching the
  historical IPPV run. The enumeration blocker is resolved for this case; final
  benchmark/resource policy and a fresh paired campaign remain unfinished.
  No mode speedup, new semantic conflict or final setting is inferred.
  2026-10-05: [fresh paired smoke](../evidence/m5/paired-smoke-20261005/REPORT.md)
  now runs both pinned builds at the same CA-GrQc h=3,k=5 settings. Both return
  five structurally checked sets, with identical ordered outputs and semantic
  hashes. Native and external-validator exits are all zero. This completes the
  scoped shared smoke gate, not definition-level truth on this graph or M5.
  The external runner adds an opt-in stop-on-failure policy and an explicit unrun
  ledger. The [first repeated-campaign proposal](../evidence/m5/campaign-proposal-20261005/PROPOSAL.md)
  pins two local inputs and 48 planned native calls, but is a non-executable draft
  pending owner decision; P11.2 and P12.1 remain open.
- [ ] P12.1 Runtime/RSS/time-to-result, k/h sensitivity and enabled-feature ablations; retain failed/censored runs.
  2026-10-05: the [D030 pilot](../evidence/m5/pilot-20261005/REPORT.md) executes
  20 of 48 planned native calls plus 20 separate validators, all with native exit 0
  and passing structural checks. Six comparisons match strictly; three additional
  comparisons at k=15 match under the accepted cutoff-tie rule. CA-GrQc h=3,k=20,
  repeat 0 fails tie-aware agreement: VF returns a density-56/13 set absent from
  IPPV's output above their common 10/3 cutoff. The driver exits 1 and stops;
  all 28 pending calls remain unrun, including every CA-CondMat call. Saved raw
  evidence and a copied original reproducer retain the discrepancy without
  assigning fault. Aggregates include every planned cell; diagnosis, repairs,
  retries, minimization, remaining repetitions and wider experiments are unrun.
  Subsequent owner-authorized diagnosis identifies and repairs the baseline
  defects [IPPV-B07/B08](../evidence/m5/ippv/disagreement-20261005/REPORT.md), with
  independent correctness evidence for the disputed set. The saved 20-call pilot
  remains unchanged. Its remaining 28 calls are not resumed or silently switched
  to the new seven-patch binary; a new version-pinned campaign is still unrun.
  Subsequent D031 continuation: the [fresh campaign](../evidence/m5/pilot-fixed-20261005/REPORT.md)
  records 25 native calls: 24 CA-GrQc successes plus one VF timeout at CA-CondMat
  h=3,k=5, repeat 0. All 24 external validators pass; all 12 completed pairs match
  under the cutoff-tie rule (six strictly), and all completed triples have stable
  per-algorithm semantic hashes. Three-repeat time/RSS summaries cover each of
  CA-GrQc's four k values. The first CA-CondMat call hits the frozen 60-second
  limit; the driver exits 1 and retains 23 unrun calls. No retry, timeout increase,
  phase diagnosis or new algorithm change follows the stop. The timeout's phase
  is unknown; wider h sensitivity, ablations and full M5 gates remain open.
  D032 [phase diagnosis](../evidence/m5/condmat-phase-20261005/REPORT.md) locates
  that timeout in solving: parsing 0.042061041 s, adjacency indexing 0.1166765 s,
  then 137 completed queries/mincuts before the same 60-second guard. Each saved
  query scans all 173,361 triangles (23,750,457 footprint scan visits in total).
  Two diagnostic-only configure/build commands pass; two tiny fixtures match
  production output/query counters and independent definition truth. The
  instrumented real run times out, with no accepted output. These markers do not
  isolate footprint, endpoint counting and flow costs. Production/library and
  the 313-file fixed-pilot record remain unchanged. A one-call existing-membership
  mode diagnostic is [prepared only](../evidence/m5/condmat-phase-20261005/NEXT_STEP.md);
  no further real call, production optimization or campaign continuation follows.
  2026-10-06: [membership-mode diagnostic](../evidence/m5/condmat-membership-20261006/REPORT.md)
  completes CA-CondMat h=3,k=5 in 38.997086249 s with five structurally checked
  outputs; native/validator/driver exits are zero. The unchanged Release binary
  performs 304 queries/mincuts. Its first 137 query-counter records match the
  previous sorted trace. This single diagnostic resolves the 60-second completion
  issue for this mode/case; pairing, repetitions and the broader campaign remain
  unrun. Production/defaults and historical timing cells are unchanged.
  The subsequent [fresh CA-CondMat pair](../evidence/m5/condmat-pair-20261006/REPORT.md)
  completes both native calls and external validators (all exit 0). VF membership
  takes 38.525397500 s; seven-patch IPPV takes 2.723666167 s. Ranks 1–4 match
  exactly; rank 5 differs only at their common density-22 cutoff, so tie-aware
  agreement passes. VF output also equals the prior membership diagnostic.
  This completes the two-call diagnostic, not a repeated comparison or P12.1.
  D035 [membership pilot](../evidence/m5/pilot-membership-20261006/REPORT.md)
  now executes all 48 scheduled calls: 36 completed with separate passing
  structural validators, and 12 VF CA-CondMat timeouts at the unchanged 60-second
  guard. No calls remain unrun. All 12 completed CA-GrQc pairs pass tie-aware
  comparison (six strictly); the 12 CA-CondMat blocks remain uncomparable.
  Completed outputs are stable within each cell, and all 24 CA-GrQc outputs
  equal the prior repaired-baseline campaign's outputs. Time/RSS tables cover
  every planned cell and retain censored runs. This repeated campaign does not
  reproduce the earlier single CA-CondMat k=5 VF completion under 60 seconds;
  the cause of timing variation is unmeasured. The external runner's tested
  timeout-continuation policy preserves other failure/disagreement stops;
  133 pytest checks pass. Production, reference, papers and historical records
  are unchanged. P12.1 and M5 remain open for broader h/grid and ablation work.
  D036 [core off/on ablation](../evidence/m5/core-ablation-20261006/REPORT.md)
  executes all 48 calls on the same graph/h/k/repeat/resource grid, changing only
  the existing core selector in the same adjacency/membership binary. All 30
  completed outputs pass separate structural validation; all 15 complete pairs
  match strictly, including cutoff selection. Both modes time out in all 18
  CA-CondMat k=10/15/20 calls. No calls remain unrun. Across five complete settings,
  safe-core median time changes range from -0.93% to +3.23%, and peak-RSS medians
  decrease 4.18%-11.91%. Core cost is included in native/solve time; query counts
  and footprint scan visits stay equal while oracle/network sizes shrink.
  These three-repeat observations do not establish a general speedup. Strict
  ablation comparison is now an explicit runner policy; 137 pytest checks pass.
  Production, papers and historical evidence remain unchanged. Broader h/grid,
  phase profiling and remaining M5 gates stay open.
  D037 [fine phase diagnostic](../evidence/m5/fine-profile-20261007/REPORT.md)
  executes two tiny fixtures in production/Release/ASan+UBSan, then one fresh
  production/diagnostic pair on each graph at h=3,k=5. Eight calls complete and
  two CondMat calls time out; none remain unrun. All six tiny definition checks,
  both GrQc structural checks and five complete diagnostic/control output/counter
  comparisons pass. The CondMat 289-query prefix spends 57.092156 s of 59.650414 s
  in clique counting; its counters match all three earlier 304-query core-off
  runs. Complete CondMat output/profile equivalence remains unavailable. Separate
  strict-warning Release and ASan+UBSan builds pass one diagnostic CTest each;
  141 pytest checks pass. Source copies contain observation-only timer insertions;
  production and papers remain unchanged. This profiles a counting bottleneck,
  without implementing its optimization or completing P12.1/M5.
- [ ] P14.1 Review conclusions against available direct baselines and validation/timing scope.
  2026-10-06: [local pilot review](../evidence/m5/pilot-membership-20261006/REPORT.md)
  checks pins, serial execution and separate validation boundaries. IPPV has
  lower median native time in all four completed CA-GrQc cells; CA-CondMat has
  no complete VF comparison in this campaign. No historical timing pooling,
  maximality inference, broad speedup/SOTA conclusion or complete review gate.
  The subsequent core-ablation review finds no resolution of the larger-k
  timeout boundary, with smaller observed peak-RSS medians and mixed small time
  differences. The off control also completes CA-CondMat k=5 in this new campaign;
  cross-campaign timing variation is not attributable to core. IPPV is not rerun,
  and no new relative-performance conclusion combines the two campaigns.
  D037 distinguishes complete GrQc times from the censored CondMat query prefix;
  neither one-pair overhead nor historical query-counter agreement establishes
  a general speedup or complete CondMat correctness/performance result.
- [ ] P15.1 Regenerate results from immutable manifests; clean-machine smoke; reproducibility package.
  2026-10-06: [local regeneration](../evidence/m5/pilot-membership-20261006/regeneration.json)
  reproduces all seven aggregate artifacts byte-for-byte from 461 verified raw
  inventory entries, with no solver rerun. Clean-machine smoke and the full
  reproducibility release remain unrun.
  D036 also verifies 365 raw inventory entries and regenerates all seven core-
  ablation aggregate artifacts identically, without solver reruns. The clean-
  machine and full-release gates remain open.
  D037 regenerates its diagnostic aggregate identically, checks 18 raw native/
  validator process records and preserves 5,243 historical evidence files. No
  clean-machine run or full reproducibility release is added.

Gate: traceable evidence, not a predetermined speedup or SOTA outcome.
