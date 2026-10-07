# D040 local evaluation — 2026-10-08

**302 of 360 native calls executed; the seven-patch IPPV comparison stopped on
one substantive output error.** No native timeout/crash occurred. The two VF-only
ablations completed, and their results remain valid within this measured scope.
The [IPPV-B09 repair](../ippv/equality-20261008/REPORT.md) is separately validated;
D041 repeats the affected main suite with fresh eight-patch measurements.

| Suite | Native completed / planned | Separate structural passes | Required pair matches | Unrun |
|---|---:|---:|---:|---:|
| Main, seven-patch IPPV | 182 / 240 | 182 | 90 / 91 tie-aware (35 strict) | 58 |
| Core off/safe | 60 / 60 | 60 | 30 / 30 strict | 0 |
| Fixed k=5/full chain | 60 / 60 | 60 | 30 / 30 strict prefix | 0 |

The main disagreement is CA-CondMat h=4,k=15, repeat 0. The IPPV density-21 K10
has a connected proper 21-compact superset, so it is not an LhCDS. The
[exact witness](diagnosis/nonmaximality-certificate.json) certifies that failure.
It also demonstrates why a structural pass does not certify maximality.
All older measurements, the failed pair and every unrun call remain immutable;
none is substituted into the repaired-version campaign.

## VF ablations

| Graph, h | Core off / safe median seconds (k=20) | Fixed k=5 / all median seconds |
|---|---:|---:|
| GrQc, 3 | 0.34622 / 0.34921 | 0.23610 / 0.43209 |
| GrQc, 4 | 2.22701 / 2.22899 | 1.87219 / 2.57004 |
| GrQc, 5 | 14.66772 / 14.32210 | 12.75380 / 16.08393 |
| CondMat, 3 | 3.00433 / 4.51620 | 1.58434 / 3.66893 |
| CondMat, 4 | 5.03218 / 6.60441 | 1.97240 / 6.28513 |
| CondMat, 5 | 8.74468 / 10.19351 | 3.87056 / 10.32678 |

Five scheduled repetitions form each median; full min/max, native CPU times,
peak RSS and all raw measurements are in [core aggregates](aggregate/core/TABLE.md)
and [early-stop aggregates](aggregate/stop/TABLE.md). Core does not provide a
consistent time improvement here. Fixed k=5 finishes sooner than full-chain
execution in all six cells; its outputs match the full prefix exactly. This is
not a claim of O(k) queries, streaming latency or general performance guarantees.
[Historical main measurements](aggregate/main/TABLE.md) are retained, not a final
comparison against the repaired baseline.

## Verification and reproducibility

- Existing harness/reference/adapter readiness: **164 pytest passes**, six tiny
  definition checks and three strict prefix pairs. No production VF change.
- Aggregation failure/censoring/comparator tests: **6 passed**. The synthetic
  stopped-fixture metadata was corrected to include its seed during test development.
- All **3,309** raw campaign inventory entries verify; **22** aggregate artifacts
  regenerate byte-for-byte without native algorithm reruns.
- Driver exits: main **1** for disagreement, core **0**, stop **0**; aggregation
  and regeneration exit **0**. No new C++/sanitizer build was needed for the harness.
  The separate baseline repair has its own build and native validation records.

Commands actually executed (full arguments and logs in linked records):

```sh
.venv/bin/python evidence/m5/final-evaluation-20261008/prepare.py
.venv/bin/python evidence/m5/final-evaluation-20261008/run_batch.py
.venv/bin/python evidence/m5/final-evaluation-20261008/postprocess.py
.venv/bin/python evidence/m5/final-evaluation-20261008/certify_disagreement.py
```

[Launch and commands](launch.json) · [pins](preflight.json) ·
[readiness](readiness/completion.json) · [final tests](readiness/final-tests.json) ·
[postprocessing](postprocess/commands.json) · [regeneration](regeneration.json).
Machine: Apple M1, 16 GiB, eight logical CPUs, macOS 15.7.7 arm64, Python 3.12.2;
pinned AppleClang 17 Release builds. Inputs are the two existing normalized
artifacts; h={3,4,5}, main k={5,10,15,20}, seed 20261003, five repeats, one worker,
serial calls, 60-second native/separate-validator guards, uncapped memory,
uncontrolled cache, no warmups/retries. Exact fixture/config hashes are retained.
Before/after block power/load/VM/swap observations are in each campaign. They
are not continuous monitoring, host reservation or temperature/frequency data.
No power-condition stop occurred. Validation and observation probes are outside
native time; IPPV's own verification remains inside its time.

Changed harness symbols: `run_vf`, `execute`, `validate_comparison`, `validate`,
`compare_prefix`, and the read-only environment helpers; new tests and evidence
reuse the existing runner/aggregator. Tasks P11.1/P11.2/P12.1/P14.1/P15.1; O09/O12
scope discipline. Papers/reference/VF algorithms and original binaries are
unchanged. Finite tests/agreements are not a theorem proof. The 58 old main calls
are unrun; a new complete version-pinned main suite replaces no historical record.
Final performance conclusions and clean-machine/release gates remain open;
DCLDS remains deferred, and zero-density IPPV omissions remain recorded.
