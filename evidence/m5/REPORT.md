# M5 status — 2026-10-07

M5 remains **in progress**. The [targeted count optimization](counting-20261007/REPORT.md)
is implemented and validated. `--clique-count membership` uses exact vertex
membership checks to count induced cliques; the original sorted mode remains
the default and control. This addresses the counting cost identified by the
[previous profile](fine-profile-20261007/REPORT.md).

| Case (h=3,k=5) | Sorted median [min,max] s | Membership median [min,max] s | Median ratio sorted/member |
|---|---:|---:|---:|
| ca-grqc-h3-k5 | 0.349554 [0.342789, 0.533862] | 0.250145 [0.230998, 0.597547] | 1.40x |
| ca-condmat-h3-k5 | 38.791546 [38.556403, 39.562047] | 1.709334 [1.634339, 1.716649] | 22.69x |

All 12 planned native calls were attempted:
{'completed': 12}, 0 unrun;
6/6 pairs match strictly.
All completed outputs pass separate structural validation and retain identical
query counters. This is a local three-repeat comparison of count modes, with no
new IPPV run or historical timing pooling. Larger-k/general-h benefits are untested.

Debug, Release and ASan/UBSan each pass 16/16 CTest; 144 pytest tests and 14
independent-reference campaigns pass. All 1,392,496 saved responses match the
earlier corpus after excluding only measured core time. Production optimization
changes no mathematical semantics; papers/reference and historical records remain
unchanged. Finite tests do not prove the theorem.

The next work package is to freeze the final experiment scope: datasets/h/k,
resource limits, applicable baseline comparisons and IPPV's known zero-density
coverage limitation. Then execute that suite and finish conclusion/reproduction
checks. This count change does not complete P12.1 or M5; no further optimization
loop is launched. DCLDS remains deferred.

Earlier [core ablation](core-ablation-20261006/REPORT.md) and
[VF/IPPV pilot](pilot-membership-20261006/REPORT.md) remain separate historical
results. No new claim that VF is faster than IPPV follows from this turn.

[Latest report and commands](counting-20261007/REPORT.md) ·
[Changed files](counting-20261007/files_changed.json) ·
[Preservation argument](../../docs/COUNTING_IMPLEMENTATION.md)
