# M5 status — 2026-10-07

M5 remains **in progress**. The latest [fine phase diagnostic](fine-profile-20261007/REPORT.md)
locates a counting bottleneck on CA-CondMat: its recorded 289-query prefix spends
**57.09 s of 59.65 s** in `MaterializedCliques::count`, versus **0.95 s** in max-flow.
These are partial-run measurements; both fresh production and diagnostic calls
reach the unchanged 60-second limit. Complete CondMat output/profile comparison
is unavailable, and no production optimization has been made yet.

The fresh CA-GrQc pair completes with identical output and counters. Counting,
footprint aggregation, network construction and flow take 32.03%, 23.34%, 22.39%
and 16.66% of its complete diagnostic solve time. One instrumented/control pair
does not establish stable overhead or performance differences.

The counting path still tests each clique against a sorted vertex set; membership
footprint scanning optimizes a separate path. Applying exact membership checks
to counting is the next candidate, subject to a preservation argument, switch,
strict output-equivalence tests and a fresh bounded performance comparison.

This diagnostic executes all ten fixed native calls: eight complete, two timeout,
none unrun. Six tiny definition checks, two real structural checks and five
complete diagnostic/control output/counter comparisons pass. CondMat's 289-query
prefix matches all three earlier matching core-off runs; historical times are
not reused. Strict-warning Release and ASan/UBSan builds pass one diagnostic
CTest each; **141 pytest tests pass**. The aggregate regenerates identically;
18 raw process records and 5,243 historical evidence files verify. Production,
reference, the four papers and historical measurements remain unchanged.

Earlier evidence remains separate:

- [Core ablation](core-ablation-20261006/REPORT.md): 48 calls, 30 complete and 18
  timeout; all 15 complete pairs strictly agree. Safe-core time changes are mixed
  (-0.93% to +3.23% medians), with smaller observed peak-RSS medians. It does not
  resolve larger-k timeouts.
- [VF/IPPV pilot](pilot-membership-20261006/REPORT.md): IPPV is faster in the four
  completed GrQc settings; VF times out in all 12 CondMat calls. No new IPPV run
  or pooled timing comparison is added. Runtime variation across campaigns is
  unresolved; IPPV's zero-density omission still limits full-domain comparison.

Broader h/grid experiments, complete CondMat profiling, remaining baseline/final-
comparison scope, full production correctness reruns for future optimizations,
clean-machine smoke and the reproducibility release remain open. DCLDS stays
deferred. Structural checks and finite agreement do not prove maximality or the
mathematical theorem.

[Latest commands, environment and limitations](fine-profile-20261007/REPORT.md) ·
[Changed files](fine-profile-20261007/files_changed.json) ·
[Timer boundaries and preservation argument](../../experiments/fine_profile/README.md)
