# D031 repaired-baseline pilot — 2026-10-05

**Stopped at the approved timeout boundary.** Of 48 planned native calls, 25 ran: 24 CA-GrQc calls completed and one VF CA-CondMat call timed out. All 24 external validators passed; all 12 completed pairs agree with cutoff ties allowed. The remaining 23 native calls were not launched. This is partial P11.2/P12.1/O12 evidence, not M5 completion.

## Frozen scope and environment

The owner requested “好的。现在继续跑实验” after the IPPV-B07/B08 repair report. [Approval](approval.json), [config](config.json), [schedule](schedule.json), [preflight](preflight.json), [environment](environment.json) and [launch pins](launch.json) were saved before native execution. D031 records a fresh full schedule using the repaired seven-patch baseline, preserving the historical stopped five-patch campaign. Only the config name and IPPV label/executable/hash differ from D030. No old/new timings are pooled.

- Local CA-GrQc: 5,242 declared vertices / 14,484 normalized edges; graph SHA-256 `85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32`.
- Local CA-CondMat: 23,133 declared vertices / 93,439 normalized edges; graph SHA-256 `5e48ff6e02d4015364788f606f59adb4dafcc4dbdc92ce33a209a4eeb50c8adb`.
- Both inputs: h=3, k={5,10,15,20}; three repetitions each; seed 20261003; same shuffled within-block order as D030.
- One worker, serial native/validation children, 60 seconds per child, no imposed memory cap, uncontrolled filesystem cache, no additional warm-ups.
- VF: adjacency enumeration, core reduction off, sorted footprint scan; Release binary SHA-256 `8a8252e31156a75899aa758ba1e357953d1dfee9914287d9970c5f67b921b4f8`.
- IPPV: author commit `f61881d4752170c03585e4281f0c49d7ef14aa1e` plus seven disclosed patches; iterations=10, p=0; Release binary SHA-256 `573d24e3bb189f3cacd86e2f7ee50441eb6c927e5ce60c5654f372485abf3879`.
- Same Apple M1, 16 GiB, eight physical/logical cores, macOS 15.7.7 arm64; Python 3.12.2. Existing build provenance records AppleClang 17.0.0.17000603. Root HEAD `56229397903813d3509ecb45b178bbde823e357b` with the pre-existing M5 working-tree changes, pinned by content; no commit or build in this continuation.

## Actual results

Campaign driver exit: **1**, wall time **177.552329835 s**, including validation/evidence I/O. This is distinct from native algorithm timing. [Completion](completion.json), [totals](aggregate/totals.json), [full raw runs](aggregate/runs.json), [all 16 planned cells](aggregate/TABLE.md), [unrun ledger](campaign/stopped.json).

- 24 completed native calls, all exit 0; 24 subsequent external validators, all exit 0 and structurally passing.
- 12/12 tie-aware matches: 6 strict at k=5,10 and 6 allowed cutoff-tie differences at k=15,20. Each of the eight completed algorithm/case cells has one stable semantic hash across three repetitions.
- 1 timeout: VF on CA-CondMat h=3,k=5, repeat 0. No native OOM, other error or output disagreement occurred in the executed subset.
- 23 unrun calls: the other 23 CA-CondMat schedule entries, including every IPPV call on that graph.

CA-GrQc medians from three repetitions (seconds):

| k | VF native end-to-end | IPPV native end-to-end | VF post-load | VF solver after indexing |
|---:|---:|---:|---:|---:|
| 5 | 1.191481 | 0.176961 | 1.176148 | 1.167067 |
| 10 | 5.316309 | 0.198185 | 5.298348 | 5.287575 |
| 15 | 10.452431 | 0.254021 | 10.432339 | 10.423466 |
| 20 | 18.082301 | 0.317450 | 18.066890 | 18.058157 |

Native time measures process launch through wait4 completion; native IPPV candidate verification is included. External structural validation, normalization and adapter work are outside that interval. VF phase timing is reported separately from native process time. IPPV prints CPU-time phases, which are not substituted for comparable wall-time phases; those wall phase fields remain unavailable. Per-run native user/system time, peak RSS, separate validator time/RSS and VF phases are retained in runs.json. The all-cell table supplies native time/RSS median/min/max. No per-rank latency was measured.

IPPV is faster than this VF basic configuration in all four observed CA-GrQc cells. These measurements do not establish performance on CA-CondMat, other h, optimized modes or other datasets. Output agreement and structural validity do not certify full LhCDS maximality/completeness on either real graph, and finite agreement is not a mathematical proof. The previous independent certificate concerns the disputed single set only.

## Timeout and retained failure

[Native process record](campaign/runs/0012-0/process.json): wall **60.009898708 s**, user **59.121100 s**, system **0.435166 s**, peak RSS **144261120 bytes**. The timeout guard terminates the child with signal 9 (recorded exit -9); this is a known timeout, not an inferred OOM. Both stdout and stderr are empty. No validator runs for this incomplete call and no phase timings are available.

The original normalized graph is retained in [the run directory](campaign/runs/0012-0/graph.txt); command, input hash, seed, versions and status are also linked from [stop context](aggregate/stop-context.json). A timeout alone does not identify parsing, clique indexing, flow or recursion as the cause. No phase diagnosis, minimization, retry, increased timeout, new mode or post-stop native call was performed. The censored timeout remains visible and does not enter successful-run medians.

## Commands and verification

[Commands and exit codes](commands.json) contain the executed preparation, environment, launch, aggregation and verification entry points. The native driver command was:

```sh
.venv/bin/python experiments/run.py --config evidence/m5/pilot-fixed-20261005/config.json --evidence evidence/m5/pilot-fixed-20261005/campaign --stop-on-failure
```

Every actual native and validator command is saved in campaign/runs/*/process.json and its validation/process.json. Driver stdout/stderr, preflight logs, aggregation logs and verification logs are retained here. The four sysctl commands all exit 0; preflight, environment, evidence aggregation and verification each exit 0. The campaign and its wrapper correctly exit 1 at the timeout.

[Verification](verification.json) rechecks 263 raw inventory entries, all 261 historical-pilot files, four paper hashes, 23 reference files, 40 VF source pins, 18 IPPV source pins, seven patches, 13 harness-source pins and snapshots, two binary/provenance pins and both inputs. It recomputes all 12 comparisons and semantic hashes from saved records, verifies serial validation outside native timing, all 16 aggregate cells/medians, and the absence of directories for 23 unrun calls. All checks pass.

No configure/build, CTest, pytest, sanitizer or numeric-regression suite was rerun in this continuation because algorithm and harness sources were not changed. Prior repair/build/test evidence remains historical.

## Changes, symbols and remaining work

Added this evidence directory: approved config/version/environment pins, schedule, copied harness sources, raw process outputs/manifests, all-cell aggregates, stop ledger, verification and reports. Updated docs/DECISIONS.md (D031), docs/TASKS.md, docs/CLAIM_TRACEABILITY.md, experiments/README.md and evidence/m5/REPORT.md. [files_changed.json](files_changed.json) gives the complete turn-specific inventory.

No production, reference, adapter or runner symbol changed. Evidence-only prepare.py, environment.py and launch.py freeze/check/execute the schedule; summarize.summarize and verify.verify read and check saved evidence. Existing experiments.run.execute and its opt-in stop policy are used unchanged.

The affected experiment path remains blocked by the CA-CondMat VF timeout. A separately bounded phase diagnosis is the recommended next step; no new budget or diagnostic run is claimed approved/executed here. The 23 pending schedule entries, wider h/dataset scope, ablations, rank latency, full-domain IPPV issues (including known zero-density omissions), broader baseline audit and clean-machine package remain unfinished. DCLDS remains deferred under D029; no paper/theory changes or new semantic conflict are asserted.
