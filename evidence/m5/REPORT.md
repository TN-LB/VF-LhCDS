# M5 status — 2026-10-08

The selected five-repeat local evaluation is complete: **360 native runs**,
comprising 240 repaired VF/IPPV main calls plus 60 core and 60 early-stop calls.
All complete with separate structural checks. Main has **120/120 tie-aware
matches** (40 strict); core has **30/30 strict matches**; early stop has
**30/30 strict prefix matches**. No timeout/OOM/error occurs in this final set.
[Final main results and all timing/RSS ranges](final-main-repaired-20261008/REPORT.md).

VF has lower wall-time medians in **11/24** settings, IPPV in **13/24**.
IPPV is faster on every tested GrQc setting; VF is faster on CondMat except
h=4,k=5. RSS outcomes are mixed. Safe core lowers RSS medians but usually adds
runtime; fixed-k early stop lowers completion-time medians in all six cells.
These shared-host observations support no universal speedup or SOTA claim.

The [stopped seven-patch main](final-evaluation-20261008/REPORT.md) remains separate:
182 calls, one genuine IPPV maximality failure, 58 unrun. The
[B09 repair](ippv/equality-20261008/REPORT.md) and fresh eight-patch measurements
preserve all old records; timings are never pooled across baseline versions.
Across both benchmark attempts, 542 native calls were executed.

All final tables regenerate identically. [Fresh local reproduction](reproduction-20261008/REPORT.md)
passes new VF/IPPV builds, **16/16 CTest**, **164 pytest**, and four additional
independent definition fixtures. Both rebuilt binaries match measured hashes.
The initial wrapper-path failure is retained. Papers/reference/solver stay unchanged.

**M5 remains open.** The selected-scope P14.1 review is complete; P15.1 still
needs a clean-machine run. Broader baseline/data coverage, IPPV's zero-density
gap and unavailable rank/detailed-phase metrics remain explicit; DCLDS stays
deferred. No further optimization or automatic measurement cycle is planned.
[Current plan](../../docs/M5_COMPLETION_PLAN.md) ·
[Reproduction instructions](../../docs/M5_REPRODUCTION.md).
