# Authorized enumeration change: pre-implementation test plan

Owner: "是，继续" after the concrete adjacency-extension proposal. Scope is that
one change, its correctness gates and the same CA-GrQc h=3,k=5/60-second diagnostic.
Keep combinations as the default/control; preserve the single materialized backend.
The prior preservation argument in phase-diagnostic-20261003/ENUMERATION_PLAN.md
applies. No papers, reference implementation, exact flow or solver recursion edits.

Named checks before implementation:

- T04-ADJ: exact ordered tuples/incidence IDs, all-subset counts and degree sums
  equal the combination control and independent Python reference. Exercise both
  builders in every M2/M3/M4 test-probe case, then run queries with adjacency.
- T04-EDGE: h=2, no cliques, original-ID relabeling, h>|V| including arbitrary
  precision h, high-depth complete graph, invalid h and invalid enum values.
- T04-CLI: explicit combinations equals default; adjacency has identical solve
  outputs/hashes across all four M4 modes, fixed-k/all/zero cases, global/restricted
  oracle results and invalid argument behavior.
- T04-HARNESS: optional enumeration config retains old-config meaning, records
  the actual switch in the native command, and rejects unsupported enum values.
- Retain T05-T17: existing numeric/actual fallback tests, M2 exact oracle tiers,
  M3/M4 independent chain/output truth, all four core/footprint modes, all prefixes
  and relabelings, Debug/Release and ASan/UBSan. Compare saved old M4 and new
  campaign responses excluding only measured reduction time; keep failing seeds.

Reuse unmodified frozen corpus generators and seeds (20260922/20260929). No
duplicate reference or theory audit. Test-only probes may compare two production
representations; expected mathematical truth remains the independent reference.
Run full exhaustive-small, seeded and higher-h tiers in Debug and sanitizer;
CTest and combined pytest also run. No parallel code, extra flow or baseline work.

Real diagnostic will be frozen after the new binary is built and before launch:
one explicit adjacency/basic invocation, original normalized CA-GrQc checksum,
h=3,k=5, one worker, 60-second native/validation guard, no imposed memory cap,
uncontrolled cache. Preserve old timed-out runs and compare any validated output
to the existing IPPV structural output separately from timing. If another blocker
appears, stop that path and report; no further optimization is included.
