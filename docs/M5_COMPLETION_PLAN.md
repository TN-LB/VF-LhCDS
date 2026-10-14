# M5 completion scope — 2026-10-09

Subsequent direction (2026-10-14, D043): [M6/M7](M6_M7_EXECUTION_PLAN.md) now cover
eight-graph preparation and a new unified formal campaign. Every M5 measurement
below is historical local/preliminary evidence relative to M7 and is excluded
from its formal results, including ablations. M5's bounded completion and raw
records remain intact. New data/tool work does not reopen D039's solver
optimization cycle or D029's DCLDS deferral.

M0–M4 and **bounded M5 are complete** at their recorded gates. D042 closes the
selected evaluation, conclusion review, table regeneration, local rebuild and
fresh Ubuntu software-environment reproduction. Original broader coverage and
stronger release levels remain explicitly deferred or limited below. D039 still
ends the development optimization cycle. This file records the completed scope;
earlier campaign records remain historical.

## Completed work and scope boundaries

| Work package | Status | Evidence / next deliverable |
|---|---|---|
| One targeted count optimization | Complete | [D038 report](../evidence/m5/counting-20261007/REPORT.md); implementation commit `0315c5d` |
| Freeze evaluation scope and prepare execution | Complete | Five repetitions; [accepted configs and readiness](../evidence/m5/final-evaluation-20261008/REPORT.md); environment recorded at each launch |
| Execute and aggregate the frozen suite | Complete for selected local scope | [D041 main](../evidence/m5/final-main-repaired-20261008/REPORT.md): 240 runs, 120 tie-aware matches; retained VF ablations: 120 runs, 60 required matches. Stopped D040 main remains separate |
| Review conclusions and reproduce release | Complete at D042's bounded gate | [P15.1 Linux reproduction](../evidence/m5/clean-env-20261008/REPORT.md): new dependency installation/builds, 16 CTest, 164 pytest, four definition fixtures and 26 identical derived artifacts; shared kernel/physical host disclosed |

D038's existing evidence is 16/16 CTest in each of Debug, Release and ASan/UBSan,
144 pytest passes, 14 differential campaigns and 1,392,496 matching saved responses.
Its 12 count-mode measurements complete with six strict paired matches. These
are prior results, not checks rerun by this planning update. They do not prove
the theorem or establish a new VF/IPPV speedup.

P11.3 shared smoke is complete. P09.1 retains IPPV's zero-density coverage gap;
P09b.1 remains deferred under D029. P11.1/P11.2 now have executed level/timing
separation and configuration-freeze evidence. P14.1 is complete for the selected
claims. P10.1/P12.1/P15.1's broader portions are deferred under D042, not falsely
completed. No further local optimization or automatic benchmark cycle is planned.

## Stop adding performance optimizations

Keep the solver/reference/papers and existing CLI defaults unchanged. Freeze the
tested production source at `0315c5d`; the candidate Release binary is the existing
`build-m5-counting-release/vflhcds`, matched by source and executable hashes.
The proposed measured VF mode is adjacency enumeration, membership footprints,
membership counting, exact automatic capacity dispatch and core off. Core safe
is an ablation, not a mode selected after seeing final results. IPPV remains the
separately patched baseline with iterations=10 and native p=0: D040 records seven
patches; the independently validated B09 repair produces eight for D041.

Do not start another optimization/profile/parameter-search cycle because results
are slow, mixed or negative. Routine preparation is limited to existing-harness
support for the planned full-output prefix comparison, environment observations,
validation, aggregation and release instructions. No new profiling framework or
algorithm dependency is required.

A correctness failure still requires diagnosis and regression validation. Keep
the failed version's records, pin any repaired version separately and prerecord
which affected measurements must be repeated. Never pool different executable
versions or silently substitute a repaired result. D028 still governs routine
IPPV defect repairs; a new problem/output-policy conflict stops its affected path.

## Final local evaluation — D040, five repetitions selected

The selected scope uses the two already normalized IPPV-bundled artifacts,
selected by local availability. It extends h coverage without new data acquisition.
It is a bounded local evaluation, not the full candidate dataset pool or a broad
specialization/SOTA comparison. D040 now records the selected five-repeat scope.
The original review-pack drafts remain immutable; executable configs and actual
readiness/results are stored separately in [final evaluation evidence](../evidence/m5/final-evaluation-20261008/).

| Setting | Selected value |
|---|---|
| Graphs | CA-GrQc: n=5,242, m=14,484; CA-CondMat: n=23,133, m=93,439; exact hashes in review pack |
| Main comparison | VF versus IPPV (D040 seven patches, D041 eight); h={3,4,5}, k={5,10,15,20} |
| B-core | Same VF binary, core off versus safe; both graphs, h={3,4,5}, k=20 |
| B-stop | Same VF mode, k=5 versus explicit full-chain `--all`; both graphs, h={3,4,5}; compare the first min(5,q) records strictly |
| Repetitions | Exactly five per setting and mode, fixed before results; no warmup calls, adaptive extra repeats or retries |
| Machine | Current Apple M1 / 16 GiB / macOS host and pinned Release builds; recheck actual environment before launch |
| Concurrency | One algorithmic worker; serial native and validator calls; no concurrent builds or agent benchmark jobs |
| Guards | 60 seconds per native child, separate 60 seconds per external validator; no imposed memory cap |
| Cache / seed | Uncontrolled filesystem cache; seed 20261003; randomized mode order within each repeat block |
| Order | Main, B-core, B-stop; graph order GrQc then CondMat; ascending h/k and repeat order; schedule saved before launch |
| Failure handling | Continue native timeouts, retain censoring; stop affected suite on other errors, validation failure or substantive disagreement; record every unrun entry |

There are **240 main + 60 B-core + 60 B-stop = 360 native calls**, plus at most
360 separate validators. Native guard sum is **6 hours**, with at most another
6 hours of validator guards. These are conservative guard sums, not expected
duration or a strict total deadline; setup and wrapper overhead are additional.
Timeouts may prevent a complete ablation, especially full-chain execution. Do not
extend limits or drop cases after observing that outcome. Uncapped memory can
cause system pressure; the current runner does not enforce a safe physical-RAM cap.

Five fixed repeats make the spread more visible than the pilot's three; they do
not eliminate load/thermal bias or justify small differences as significant.
The earlier three-repeat and dedicated-host alternatives remain in the immutable
review pack. Neither is selected for this batch.

## Environment and measurement protocol

Before launch, record actual hardware/OS/compiler, executable/source pins, power
source and available power-mode settings, system load, VM statistics and swap.
Use AC power with one unchanged recorded power mode. The operator must arrange
the quiet working period; no program is killed and no system setting is changed
automatically. Single-worker execution does not reserve the host.

Record lightweight load/VM/swap/power observations before and after each paired
block, outside native timing. These are observations, not continuous monitoring
or proof of an idle host. Record unsupported/denied probes as unavailable;
temperature and CPU frequency remain unavailable unless actually measured.
Power-mode/source changes or an external interruption stop before the next block;
retain the current block and all unrun entries. High load alone does not trigger
post-hoc deletion, reruns or a newly chosen numeric exclusion threshold. Disclose
the observations and withhold fine-grained speed claims when spread is large.

Reuse native wait4 wall/user/system time and peak RSS; add no clocks inside the
solver. External validation and environment probes stay outside native timing;
IPPV's own candidate verification stays inside it. Report five-repeat medians
and min/max only for complete five-run cells, all raw outcomes for other cells,
and paired ratios only for common completed/validated comparable cases. Include
coverage counts next to any speedup summary; do not replace timeouts with runtimes.
No earlier pilot/profiler timing is pooled into this batch.

## Comparability, exclusions and claim limits

- Preserve every declared vertex and zero-density solution. Never repair IPPV
  output by synthesis, filter VF, lower k or remove an unfavorable case.
- Keep IPPV's known zero-density omission and unidentified upstream license
  explicit. Existing local use is unchanged; no external redistribution is part
  of this plan. A newly observed discrepancy remains a failed comparison pending
  diagnosis, not an automatic assertion that the omission explains it.
- Main pairs use the existing cutoff-tie-aware rule and also report strict
  equality. B-core requires strict entire-output equality. B-stop requires strict
  prefix equality; different full/fixed output hashes are expected.
- Real graphs receive structural checks and cross-implementation agreement only;
  tiny independent definition truth remains separate. Agreement does not certify
  maximality or completeness on the real graphs.
- DCLDS remains deferred. No h=2 experiment or specialization comparison is in
  this proposal. Record P10.1 exclusions explicitly; make only VF-versus-IPPV
  claims on tested h=3/4/5 cases, no h=3 SOTA or specialization-competitiveness claim.
- Two graphs do not establish general scalability. No synthetic/fraction grid is
  introduced. Broader dataset/scalability claims remain outside this scope.
- RQ3's detailed phase evidence belongs to the older profiled version; do not
  label it a breakdown of the final optimized binary. Use available final native
  phases/counters and mark missing phase times unavailable. Per-rank streaming
  latency is currently unavailable; fixed-k process time is not that metric.

This bounded scope can yield a final local evaluation with negative results.
It does not silently complete every original M5 gate: broader baseline coverage,
unavailable metrics and the full-domain IPPV gap remain separately identified.
The subsequent fresh Ubuntu installation supplies clean software-environment
evidence; shared-kernel/hardware limits and unrerun raw measurements remain explicit.

## Preparation and execution checklist

1. Review D040's scope/resources and claim exclusions. Verify draft input/binary
   pins and counts without launching algorithms; record current readiness gaps.
2. Reuse the existing runner. Add only full-mode validation/prefix comparison and
   observation records needed above; test those failure paths and tiny fixtures.
   Implemented and tested: 164 pytest checks, six tiny definition checks and three
   strict prefix pairs pass. Production sources and binaries stay unchanged.
3. Freeze the accepted config, actual environment, runner/source hashes and whole
   schedule before any measured call. Drafts cannot launch; readiness checks are
   not performance measurements. Recheck pins at launch.
4. Run the fixed batch, aggregate from immutable records, review conclusions and
   regenerate the tables. No favorable selection or new optimization in this step.
5. Prepare the reproduction package using the same pins, run a fresh build/smoke,
   and state whether the environment is a fresh local directory or a genuinely
   clean machine. The former does not satisfy a claim about the latter. Review
   each remaining M5 gate individually before changing task checkboxes.

## Final scope closure

**D042 completes the bounded M5 stage.** The fresh Ubuntu reproduction is complete;
no new mathematical conflict or unresolved build/test failure remains. The following
limits stay explicit and do not become completed experiments through scope closure.

| Item | Evidence now available | Remaining boundary |
|---|---|---|
| P09.1 IPPV | Pinned source, eight disclosed patches, native/validation timing audit, shared real-graph results and tiny definition checks | Known zero-density omissions and unidentified upstream license remain; no output synthesis or source redistribution |
| P10.1 specialization | No h=2 benchmark or h=3 SOTA/specialization claim in selected scope | No specialty-baseline implementation/comparison |
| P12.1 measurements | Two graphs, h=3/4/5, k=5/10/15/20, five repeats, runtime/RSS, core and early-stop ablations | No broad scalability grid, per-rank latency or final detailed flow-phase timing |
| P15.1 reproduction | Fresh Ubuntu dependencies and Release builds; 16 CTest, 164 pytest, four definition fixtures; 26 identical regenerated artifacts | Same physical Mac/shared OrbStack kernel; no raw benchmark replication on independent hardware, no published archive/tag |
| P09b.1 DCLDS | Existing records retained | Deferred under D029; no new reading/integration |

Use only the tested VF-versus-IPPV claims and recorded clean-userspace reproduction
level. Keep negative results, coverage gaps and all failed/censored evidence.
The original broader tasks remain labelled deferred or limited, not completed.
There is no new experiment grid, algorithm change, public release or automatic
next milestone. Any later broader campaign needs a separate scope/resource plan;
DCLDS remains deferred unless separately changed. Independent hardware is a
possible stronger check, not a prerequisite added to this bounded completion.
