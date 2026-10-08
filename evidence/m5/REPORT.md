# M5 completed bounded evaluation — 2026-10-09

**M5 is complete for the two-graph, five-repeat evaluation and documented
software-environment reproduction scope.** Broader study/release work remains
separately identified below.

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

The subsequent [fresh Ubuntu reproduction](clean-env-20261008/REPORT.md) installs
new Linux dependencies and passes both Release builds, **16/16 CTest**, **164 pytest**,
four definition fixtures and **26 byte-identical regenerated artifacts**. A venv
interpreter-path defect and two GCC test-formatting warnings were repaired; failed
attempts are preserved. The environment uses OrbStack on the same Mac, with no
independent-hardware performance rerun. Production and measured binaries are unchanged.

The selected-scope conclusion review and reproduction package are complete.
Broader baseline/data coverage and stronger replication/publication levels are
deferred. IPPV's zero-density gap, unidentified upstream license and unavailable
rank/detailed-phase metrics remain explicit; DCLDS stays deferred. No universal
speedup, real-graph completeness or theorem proof follows from these finite checks.
No further optimization or automatic measurement cycle is planned.
[Completed scope and limits](../../docs/M5_COMPLETION_PLAN.md) ·
[Reproduction instructions](../../docs/M5_REPRODUCTION.md).
