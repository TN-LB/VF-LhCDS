# M5 status — 2026-10-06

M5 remains **in progress**. The latest [core off/on ablation](core-ablation-20261006/REPORT.md)
executes 48 VF calls: two graphs, h=3, k={5,10,15,20}, three repetitions,
seed 20261003, the same adjacency/membership Release binary and 60-second guards.

| Scope | Result |
|---|---|
| CA-GrQc, all four k values | Both modes complete; 12/12 strict paired matches |
| CA-CondMat, k=5 | Both modes complete; 3/3 strict paired matches |
| CA-CondMat, k=10/15/20 | Both modes time out in all 18 calls |

All 30 completed outputs pass separate structural checks and are stable across
repetitions. Core does not resolve the large-k timeout boundary. Across the five
completed settings, safe-core median time changes range from **-0.93% to +3.23%**;
peak-RSS medians decrease **4.18%-11.91%**. These are three-repeat local observations,
not a general speedup or memory guarantee. [Full time/RSS table](core-ablation-20261006/aggregate/TABLE.md).

Core shrinks oracle/network sizes but retains the same query counts and footprint
scan visits. Its measured overhead is included in solve/native time. The five
complete settings have identical canonical outputs with the switch off/on.
Finer counting, footprint, network-build and flow times remain unmeasured.

137 Python tests pass. Evidence checks verify 365 raw inventory entries; seven
aggregate artifacts regenerate identically. The campaign driver exits 1 for
retained timeouts; aggregation, verification and regeneration exit 0. This turn
changes only the external comparison policy, tests, documentation and evidence.
Production code/binary, papers, reference and historical records are unchanged.

The earlier [VF/IPPV pilot](pilot-membership-20261006/REPORT.md) remains separate:
IPPV was faster in its four completed CA-GrQc settings, and VF timed out in all
12 CA-CondMat runs. IPPV is not rerun in this ablation. The new off-mode CA-CondMat
k=5 completion cannot be attributed to core; cross-campaign timing variation is
unresolved and measurements are not pooled. IPPV's known zero-density omission
still limits full-domain comparison. DCLDS remains deferred.

P11.3's smoke gate is complete. Broader h/grid experiments, finer phase profiling,
remaining baseline/final-comparison scope, clean-machine smoke and a reproducibility
release remain unfinished. C++ builds/CTest/sanitizers are not rerun this turn.
Structural checks and output agreement do not prove maximality or the theorem.

[Latest results, commands and environment](core-ablation-20261006/REPORT.md) ·
[Changed-file manifest](core-ablation-20261006/files_changed.json) ·
[Core preservation argument](../../docs/M4_IMPLEMENTATION.md)
