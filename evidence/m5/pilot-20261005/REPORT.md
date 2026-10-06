# D030 pilot — stopped at output disagreement, 2026-10-05

**Incomplete: 20 of 48 planned native calls executed; 28 unrun.** The approved
stop policy worked: CA-GrQc h=3,k=20, repeat 0 fails tie-aware output agreement,
so the driver exited 1 before any further call. All 20 native programs and all
20 separate validators exited zero; structural checks passed. The issue is
cross-implementation disagreement, not a native crash or timeout. Root cause is
unresolved, and neither implementation is assigned fault.

## Approval and frozen scope

The owner replied **“可以”** to the concrete 48-call proposal. D030 and
[approval.json](approval.json) were recorded before launch. A separate
[approved config](config.json) changes only name/scope from the immutable draft;
input hashes, binaries, h/k grid, repetitions and schedule are unchanged.

The scope is two pinned local artifacts (CA-GrQc, CA-CondMat), h=3,
k={5,10,15,20}, exactly three repeats, seed 20261003, one worker per child and
serial execution. Native and external validator each have a separate 60-second
guard. Memory is uncapped; filesystem cache is uncontrolled; no new warm-ups.
VF uses adjacency enumeration, core off, sorted footprints and the existing
exact auto-capacity backend. IPPV uses its same five patches, iterations=10,p=0.
The approved command includes `--stop-on-failure`; there are no automatic retries.

Both binary/source pins, graph pins and the current machine were verified before
launch. [Preflight](preflight.json), [environment](environment.json),
[launch](launch.json), and [schedule](schedule.json) preserve the actual settings.
The original draft and earlier evidence remain unchanged.

## Actual outcomes

| Input / k (h=3) | Recorded native calls / planned | Paired comparisons | Outcome |
|---|---:|---:|---|
| CA-GrQc / 5 | 6 / 6 | 3 | Strict matches |
| CA-GrQc / 10 | 6 / 6 | 3 | Strict matches |
| CA-GrQc / 15 | 6 / 6 | 3 | Strict differences, accepted cutoff-tie matches |
| CA-GrQc / 20 | 2 / 6 | 1 | Strict and tie-aware disagreement; stopped |
| CA-CondMat / 5,10,15,20 | 0 / 24 | 0 | Unrun |

Totals: 20 native successes, 20 successful structural validators, 10 paired
comparisons, 6 strict matches, 9 tie-aware matches, 1 tie-aware disagreement.
No timeout, explicit OOM or native error occurred among these calls. The remaining
28 entries comprise four CA-GrQc k=20 calls and all 24 CA-CondMat calls. The
driver's exit 1 and 48.2070587920025-second wall time are in
[completion.json](completion.json); no native exit was substituted for that
campaign-level failure.

The original [stopped ledger](campaign/stopped.json),
[summary](campaign/summary.json), every raw log, and all failed comparison
evidence are retained. Run status `completed` describes the native/structural
outcome; it does not silently make the failed pair successful.

## The observed discrepancy

At k=20 both algorithms return 20 sets and have an exact cutoff density of 10/3.
VF's rank-18 set has **13 vertices, 56 triangles, density 56/13 > 10/3**:

```text
729 733 774 776 1597 2298 2299 2300 2301 2302 2303 2311 2314
```

This set is absent from the saved IPPV output. It lies above the cutoff, so the
recorded difference is not explained by permission to select different tied
cutoff members. Other differing lower sets and the complete original records
are retained in [the original reproducer](aggregate/failure/reproducer.json).
The copied graph preserves the original CA-GrQc SHA-256
`85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32`.

The VF output hash is
`dbb4369598645c10a24128288a993a758e9dd11d36856c161068e6f829d3603c`;
IPPV's is
`d6eea487b4455a07b062271bacafceed6c6878e63171c80802f77316c89afe0d`.
Native times for this single failing pair are VF 10.820828041993082 s and IPPV
0.18204908352345228 s; native peak RSS is 49,086,464 and 32,964,608 bytes,
respectively. These remain raw observations, not a successful repeated comparison.

Structural checks and output differences alone do not establish which result
satisfies all deletion/subset and global maximality obligations. The cause may
only be assigned after investigation. No proof/specification conflict or theorem
counterexample is established by this observation. No diagnosis, minimization,
repair, new native execution or experiment-budget change follows this stop.
D028 permits routine IPPV reproduction repair once an IPPV defect is established;
this discrepancy has not yet been attributed to IPPV. The current explicit
stop-at-disagreement instruction is preserved.

## Saved measurements, with all planned cells retained

[Generated tables](aggregate/TABLE.md) and [all-cell records](aggregate/cells.json)
include all 16 algorithm/case cells. Each raw time/RSS is available in
[runs.json](aggregate/runs.json). The completed triple medians are:

| CA-GrQc k | VF median native seconds | IPPV median native seconds |
|---:|---:|---:|
| 5 | 0.742125 | 0.113686 |
| 10 | 3.222808 | 0.126923 |
| 15 | 6.399029 | 0.158145 |

Min/max and native RSS are in the generated table; every completed repetition
contributes. No timeouts are substituted for completed times. k=20 retains its
single raw pair but has no three-repeat agreement summary. Unrun cells remain
visible and are never counted as success/failure or favorable exclusions.
Each observed algorithm/case repeats with one stable semantic hash. k=15's
cross-algorithm hashes differ because the selected cutoff ties differ.

These are measurements on the observed part of one limited local pilot, with
structural/agreement evidence only. They do not certify full output completeness
or maximality on these real graphs. There is no overall winner/speedup, general-h,
scalability or SOTA claim. The campaign remains stopped and incomplete.

Native timing includes process launch, graph I/O, enumeration, native candidate
verification where present, and output. Common offline normalization and later
external checks are excluded consistently. External validator time/RSS is retained
separately. Native phase counters remain in the manifests; unavailable IPPV wall
phases and per-rank latency remain null, not zero.

## Commands and checks actually executed

Working directory: `/Users/nost/Documents/VF-LhCDS`.

```sh
.venv/bin/python experiments/run.py --config evidence/m5/pilot-20261005/config.json --evidence evidence/m5/pilot-20261005/campaign --stop-on-failure
.venv/bin/python evidence/m5/pilot-20261005/summarize.py --output evidence/m5/pilot-20261005/aggregate
.venv/bin/python evidence/m5/pilot-20261005/verify.py
git diff --check
```

The campaign command exits **1**, deliberately preserving the disagreement.
Aggregation and final integrity verification exit **0**. Exact native/validator
commands and exits are recorded in their respective `process.json` files.
Read-only preflight pin/schema/environment checks also ran. `sysctl -n` queries
for CPU, memory and core counts all exit 0; the machine matches the approved
profile. No build, CTest, pytest or sanitizer campaign is executed this turn.
No production or shared-runner source changed, so the prior 123-test result is
not relabelled as a new test run.

## Files, symbols, environment and evidence scope

Changed documents: `docs/DECISIONS.md` (D030), `docs/TASKS.md`,
`docs/CLAIM_TRACEABILITY.md`, `experiments/README.md`, and `evidence/m5/REPORT.md`.
New files are confined to `evidence/m5/pilot-20261005/`: approval/configuration,
environment/pin snapshots, immutable native/validator outputs, source snapshots,
the read-only `summarize`/`verify` evidence scripts, generated aggregates and this
report. No production, reference, baseline or shared harness code is edited.
There is no commit. The broader existing M5 working tree remains uncommitted.

Machine: Apple M1, 16 GiB, 8 physical/logical CPUs, macOS 15.7.7 arm64;
Python 3.12.2. The pinned VF Release build uses AppleClang 17.0.0.17000603/C++17.
Root HEAD is `56229397903813d3509ecb45b178bbde823e357b`; IPPV remains
`f61881d4752170c03585e4281f0c49d7ef14aa1e` plus the five disclosed patches.
Binary hashes and build-command/flag provenance are preserved in preflight and
the per-run manifests. The historical `build-ippv-original` name does not denote
an unpatched binary. IPPV's unidentified-license and zero-density-omission
limitations are unchanged. DCLDS remains deferred under D029.

P11.2 has a scoped approved freeze; P12.1 and O12 gain finite, explicitly mixed
evidence. No incomplete M5 checkbox is promoted. Four papers, 40 production-source
pins, 17 patched IPPV-source pins, 23 independent-reference files and 12 harness
files remain unchanged, as do both binaries and every draft artifact. Evidence
hashes are checked before aggregation and again at final verification.

Useful records: [approval](approval.json), [launch](launch.json),
[native summary](campaign/summary.json), [stopped/unrun ledger](campaign/stopped.json),
[raw inventory](campaign/checksums.json), [aggregate command](aggregate-command.json),
[totals](aggregate/totals.json), [original reproducer](aggregate/failure/reproducer.json),
[integrity results](verification.json), [file inventory](files_changed.json).

Remaining blocker is the substantive output disagreement. The recommended next
step is a bounded investigation of the saved comparator inputs, VF extraction
and IPPV candidate/verification behavior, without resuming benchmarks or changing
semantics. That investigation has not started. Minimization, repairs, remaining
28 calls, wider h/dataset coverage, feature ablations, release reproduction and
DCLDS work are unrun. Finite tests/agreement do not prove the theorem.
