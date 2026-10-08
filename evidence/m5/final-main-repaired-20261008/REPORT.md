# Five-repeat repaired main comparison — 2026-10-08

**240/240 native runs and 240/240 separate structural validators complete.**
All **120 paired comparisons pass the cutoff-tie rule**: 40 are strictly equal,
80 differ only within the permitted cutoff tie. There are no timeouts, OOMs,
errors, substantive disagreements or unrun calls. The driver exits 0 after
1,379.073511 s. Structural checks and agreement do not certify real-graph
maximality/completeness.

Together with D040's completed 60-call core and 60-call early-stop suites, this
finishes the selected **360-run local evaluation**. The earlier seven-patch main
is retained separately: 182 executed calls, one failed comparison and 58 unrun.
Across both attempts, 542 benchmark native calls were actually executed. No old
baseline timings or development trials enter the final 360-run summaries.

## Observed performance

All 24 graph/h/k settings have five complete, agreeing pairs. VF has the lower
wall-time median in **11/24**, IPPV in **13/24**. These are descriptive counts,
not significance tests. The geometric mean of IPPV/VF median wall time across
all 24 settings is **0.9381**; this small aggregate difference does not establish
a stable overall winner on this shared host.

| Graph / h | Observed wall-time medians across k=5/10/15/20 |
|---|---|
| CA-GrQc / 3 | IPPV lower at all four k; VF 0.260–0.347 s, IPPV 0.117–0.192 s |
| CA-GrQc / 4 | IPPV lower at all four k; VF 1.953–2.330 s, IPPV 1.205–1.245 s |
| CA-GrQc / 5 | IPPV lower at all four k; VF 13.235–14.952 s, IPPV 10.163–10.360 s |
| CA-CondMat / 3 | VF lower at all four k; IPPV/VF median ratio 1.900–2.091 |
| CA-CondMat / 4 | IPPV lower at k=5; VF lower at k=10/15/20, ratios 1.194–1.358 |
| CA-CondMat / 5 | VF lower at all four k; ratios 1.297–1.735 |

[Every wall/CPU/RSS median and paired ratio](review/TABLE.md),
[all min/max, outcomes and raw repeats](aggregate/main/TABLE.md).
VF has lower RSS medians in 10/24 settings; memory superiority is not universal.
The largest observed VF network is the GrQc h=5 root: 2,220,744 forward nodes
and 13,298,242 forward arcs, with 2,215,500 materialized cliques. Its roughly
1.85–1.94 GiB RSS medians exceed those on the larger-vertex CondMat graph. These
are [observed counters](aggregate/main/telemetry.json), not a new scalability law
or an isolated final-version flow-time breakdown. Query count is not O(k).

The retained [core ablation](../final-evaluation-20261008/aggregate/core/TABLE.md)
passes 30/30 strict pairs: safe core has lower RSS medians in all six cells but
higher runtime medians in five. CondMat overhead is about 17–50%; tiny GrQc
differences are not a stable speed claim. The retained
[early-stop ablation](../final-evaluation-20261008/aggregate/stop/TABLE.md)
passes 30/30 strict prefix pairs; k=5 has lower process-time medians in all six
cells. This compares completion times, not per-rank streaming latency.

## Environment, fairness and reproduction

Apple M1, 16 GiB, eight logical CPUs, macOS 15.7.7 arm64; AppleClang 17.0.0,
Python 3.12.2. VF remains production commit `0315c5d`, adjacency enumeration,
membership footprints/counts, core off. IPPV is the pinned author commit plus
eight disclosed patches, iterations=10, p=0. Input/grid/binary hashes, five
repeats, seed 20261003 and randomized within-pair ordering are frozen in
[config](main/config.json), [schedule](main/schedule.json) and [preflight](preflight.json).
One worker, serial calls, 60-second native and separate-validator limits,
uncapped memory, uncontrolled cache; no warmup, retry or adaptive repetition.
Native IPPV candidate verification remains timed; external checking is excluded.

All 240 before/after-block observations report AC power and the same settings.
The [environment summary](review/environment.json) records one-minute load
2.286–14.694 and system swap use 5,989.56–6,109.56 reported M. The host was not
reserved or idle; swap use alone does not establish active swapping during a run.
Temperature/frequency are unavailable. Every sample is retained. Five-repeat
max/min wall ratios reach 1.386 for VF and 1.284 for IPPV; small differences should
not be generalized across hardware or loads.

Executed commands and logs: [native launch](launch.json),
[completion](main/completion.json), [all native/validator records](main/campaign/runs/),
[postprocessing commands](postprocess/commands.json).
`postprocess.py` reuses the tested D040 `summarize` function; `review.py` derives
paired ratios and environment ranges from the same records. **2,765 raw inventory
entries verify; seven aggregate and five review artifacts regenerate byte-identically.**
[Regeneration](regeneration.json), [local reproduction package](../../../docs/M5_REPRODUCTION.md).

P12.1/O12 gain completed selected-scope measurements; P14.1 gains this review;
P15.1 gains raw verification and table regeneration. Papers, reference, solver and
measured executables are unchanged. No new blocking conflict occurred.
IPPV's known zero-density gap, unidentified license and unaudited floating bounds
remain. DCLDS stays deferred. Clean-machine reproduction, broader baseline/data
coverage and unavailable rank/detailed-phase metrics remain open; M5 is not
declared complete and no further optimization cycle is started.
