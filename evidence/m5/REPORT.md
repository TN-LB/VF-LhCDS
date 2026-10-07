# M5 status — 2026-10-08

M5 remains in progress. The [D040 five-repeat batch](final-evaluation-20261008/REPORT.md)
executes 302 of 360 native calls. The main comparison stops on an IPPV correctness
error after 182 calls, retaining 58 unrun; both 60-call VF ablations complete, with
30/30 strict core pairs and 30/30 strict early-stop prefix pairs. Native calls and
separate structural validators all complete, but one IPPV candidate fails maximality.

The [B09 repair](ippv/equality-20261008/REPORT.md) corrects two equal-density
verification boundaries. An exact original-graph witness and independent small
all-superset truth identify the error. Release and ASan/UBSan checks pass the new
and previous regressions and both original-case replays; the known zero-density
gap remains. Production VF, reference and papers are unchanged.

D041 now repeats only the affected main comparison: 240 fresh paired calls with
the eight-patch baseline, the same five repetitions/grid/resources and fresh VF
controls. The completed VF-only ablations remain valid; old/new baseline timings
are not pooled. No further performance optimization is planned.

P11.1/P11.2 evidence-level and configuration gates are met for the selected scope.
P12.1/final conclusions/release remain open. The first batch's 3,309 raw inventory
entries verify and its 22 aggregates regenerate identically; 164 harness/reference/
adapter checks and six aggregation checks pass. Tests are implementation evidence,
not theorem proofs. [Current plan](../../docs/M5_COMPLETION_PLAN.md).
