# M8 unified formal real-graph evaluation

Status: planned under D045; P18.1–P18.8. D043 selects eight real graphs and excludes
earlier local timings from formal results. D046 proposes the matrix below; prepare
exact artifacts, host, limits and schedules before the remaining execution decision.
A draft configuration must not launch a campaign.

## Input and environment preparation

Use all eight graphs in [the execution plan](M6_M8_EXECUTION_PLAN.md): CA-GrQc,
CA-CondMat, soc-hamsterster, fb-pages-politician, fb-pages-company,
web-webbase-2001, Amazon and Email-Enron. Freeze one source/normalized manifest
per graph: retrieval URL/version/date, use terms, raw checksum, declared vertex
universe, original-ID mapping, normalization command/hash, loops/duplicates removed,
normalized checksum and measured n/m. Preserve every declared vertex, including
isolates and vertices appearing only in loops. Map text IDs reversibly and record
any source's inability to declare absent vertices.

Feed both algorithms the same normalized graph with lossless format conversion.
No implicit largest-component filtering, sampling or graph-specific preprocessing.
Check all eight identities before freeze; do not replace graphs after observing
performance. Verify existing GrQc/CondMat provenance but rerun all measurements.
Paper statistics alone do not identify source bytes.

| Setting | D046 proposed configuration |
|---|---|
| Host | One reserved Linux machine, preferably Ubuntu 24.04 LTS with 64 GiB RAM; record CPU model/allocation, physical host and virtualization |
| Build | Same installed compiler/toolchain for VF variants and IPPV where supported; documented Release flags, C++17/native unsigned 128-bit support, Boost 1.86.0; Python/test dependencies pinned |
| VF main | Final accepted M7 interval-reuse; adjacency enumeration, membership footprints/counting, core off, automatic exact capacity backend |
| IPPV | Pinned author commit plus disclosed accepted patches; iterations=10, p=0; not a claim of reproducing every paper setting |
| Execution | One algorithmic worker; serial native processes; seed 20261003; randomized within-block variant order saved before launch |
| Guards | 300 seconds per native process and separately per external validation phase; identical enforced 48 GiB per-process-group cap on the proposed host, no swap for those groups |
| Cache/repeats | Uncontrolled filesystem cache; no warmup calls, adaptive repeats or favorable retries; five repeats for primary/ablation suites, three diagnostic/control pairs per diagnostic cell |
| Timing | Native launch through output, including loading/enumeration and baseline internal verification; common offline normalization and external validation excluded and reported separately |

No host is allocated yet. Record different common limits before launch if needed.
Current `run.py` rejects memory caps; current `environment.py` uses macOS probes
and AC-power checks. P18.2 implements and tests Linux capture, CPU allocation and
actual process-group enforcement without assuming a server has a battery sensor.
Unavailable temperature/frequency stay unavailable. `wait4` RSS is measurement,
not enforcement; environment sampling runs outside native timing.

Test bounded memory stress, timeout/process-group cleanup and kernel/controller
evidence for confirmed OOM. An unexplained SIGKILL is not OOM. Guard conversion
and external validation as one separately recorded phase; no expensive unchecked
validation work may fall outside that budget. Preserve baseline outputs intact.

## Formal matrix

Every row is newly executed on the same frozen host. Coincident configurations
across suites receive their own preregistered repeats; do not pool them afterward
or substitute M5/M6/M7 records.

| Suite | Graph/h/k scope | Variants and repetitions | Native calls |
|---|---|---|---:|
| Main | Eight graphs; h={3,4,5}; k={5,10,15,20} | Final uninstrumented VF versus IPPV; five repeats | 960 |
| B-local | Eight graphs; h={3,4,5}; k={5,20} | Uninstrumented global, interval-scan, interval-reuse; core off; five repeats | 720 |
| B-core | Eight graphs; h={3,4,5}; k=20 | Uninstrumented interval-reuse, core off versus safe; five repeats | 240 |
| B-stop | Eight graphs; h={3,4,5}; k=5 versus all | Uninstrumented interval-reuse, core off; five repeats | 240 |
| D-final | GrQc, CondMat, Amazon, Enron; h={3,4,5}; eight configurations below | Final-source diagnostic and matching uninstrumented control; three paired repeats | 576 |

Primary/ablation suites total **2,160** native calls; D-final adds **576**, yielding
**2,736** proposed calls, plus separately guarded validators where applicable.
This is a workload count, not a runtime prediction or executed evidence. P18.3
generates and validates the counts from frozen schedules.

D-final's eight configurations for each graph/h are:

1. global, core off, k=5;
2. interval-scan, core off, k=5;
3. interval-reuse, core off, k=5;
4. global, core off, k=20;
5. interval-scan, core off, k=20;
6. interval-reuse, core off, k=20;
7. interval-reuse, core safe, k=20;
8. interval-reuse, core off, all.

This preselected diagnostic subset covers collaboration, co-purchase and communication
inputs with different clique/work patterns; it does not establish phase coverage on
all eight graphs. All eight receive main/local/core/stop comparisons. Matrix changes
must be recorded before measurement, not selected to support a preferred result.

## Final diagnostic refresh and comparisons

P18.4 pins the final accepted M7 source and rebuilds diagnostic/control binaries
with matching toolchain/options. Recheck source guards, phase scopes, T18–T20,
partition/reuse counters and semantic equality after the last optimization. Old M5
or initial M6 profiles cannot supply this evidence. Primary timings use uninstrumented
code. D-final reports observer time/RSS overhead without correcting phase times
by subtracting an estimate.

Main uses the existing cutoff-tie-aware comparison and reports strict equality
separately. B-local and B-core require identical ordered sets, exact counts/densities
and semantic hashes; local/global interval traces also agree on tiny checked fixtures.
Work counters may differ. B-stop requires fixed==full[:k], including ties and
exhaustion. D-final requires diagnostic/control semantic/query-trace equality.

Keep proof, independent definition checks, structural real-output checks and
cross-implementation agreement distinct. Neither profiling nor agreement certifies
real-graph maximality/completeness. Internal rank-ready events are not public streaming.

## Result builders for the three questions

| Artifact | Required contents |
|---|---|
| Main outcomes | All graph/h/k/repeat/variant rows; native and validator statuses; wall/CPU/RSS; output identity/count and comparison |
| Work/phase joins | M, VF query/mincut counts, count/footprint/partition/core work, footprint histograms, network sums/maxima; phases joined only with matching source/options/input identities |
| Local increment | Global to interval-scan effect, then interval-scan to interval-reuse; partition/root-ID overhead, endpoint scans avoided, remaining global work |
| Core | Native peak RSS difference, core overhead and downstream phase/work differences; no assumed universal gain |
| Early stop | Exact prefix status, unavoidable initialization, visited prefix and measured skipped suffix, non-output layers/depth/frontier and cleanup/output differences |
| Observer overhead | Diagnostic/control distributions and pins, separate from VF/IPPV speedups |
| Coverage | Timeouts, confirmed OOMs, errors, validator failures and unrun entries; paired completion counts and unavailable metrics |

Use medians and repeat spread. Speedups require comparable completed valid outputs;
never use timeout thresholds as completed times or missing baseline outputs as fast
successes. Show full coverage alongside summaries restricted to completed pairs.
Do not fill missing repeats across suites. Relating clique/query/network size to
runtime is descriptive; matched ablations isolate the implemented feature, not
every difference between VF and IPPV's internal operations.

## Storage, failures and completion

P18.3 introduces explicit purpose/campaign/schema identities and allowlists.
Store formal records under `evidence/m8/<campaign-id>/`; M6/M7 are development
evidence. Separate primary/ablation and D-final diagnostic/control allowlists.
Reject preliminary rows, wrong pins, mixed versions and duplicate repeats regardless
of directory names. Retain source/configuration/schedule hashes and every raw outcome.

Continue after native timeouts and confirmed resource-limit OOMs after verified
cleanup. Unexpected errors, validator failures, substantive disagreement or resource
drift stop the affected suite and retain unrun entries. A stopped ledger is not
completion. D028 permits routine baseline correctness repairs; a changed binary
requires a new freeze and complete affected-suite rerun with fresh paired controls.
Preserve the failed attempt; do not merge versions or retune performance mid-batch.

IPPV's zero-density/domain and license limits remain explicit. Do not synthesize
its outputs or remove VF solutions. A diagnosed baseline limitation is not agreement;
record any revised continuation/acceptance scope before further affected measurements.
DCLDS remains deferred under D029.

| Task | Deliverable | Acceptance |
|---|---|---|
| P18.1 | Eight manifests and necessary source-format adapters | T01/T26 round trips, IDs/isolates, input hashes |
| P18.2 | Linux capture and guarded native/validation execution | T26 actual enforcement/cleanup/outcome tests on Linux |
| P18.3 | Purpose/allowlists, grid generator, stop policy and draft freeze package | T27 mixed-evidence rejection, schedule counts and outcome accounting |
| P18.4 | Final M7 diagnostic/control rebuild and observation acceptance | T18–T20/T25 plus baseline/shared tiny smoke; source/toolchain/options pins |
| P18.5 | Concrete resource/configuration decision and fresh Main execution | All scheduled outcomes; separate structural/agreement checks |
| P18.6 | Fresh B-local/B-core/B-stop and D-final execution | Strict/prefix/observer comparisons and censored outcomes |
| P18.7 | Automatic tables/joins for the questions and optimization effects | T27; allowlists/coverage retained and unavailable fields explicit |
| P18.8 | Raw integrity and clean-environment table regeneration with tested commands | Identical derived artifacts; environment/source/data records and limits |

Completion requires executed scope, trustworthy comparison handling and reproducible
artifacts. VF need not win and resource-censored calls need not become successes.
Unresolved mathematical/semantic conflicts block their affected path. Thesis writing,
unrelated algorithm extensions and source publication are not prerequisites.
