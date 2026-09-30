# M4 implementation review

Scope: P07.1-P07.3 / O10,T17 and one P08.1 optimization; M3 remains frozen.
This is the implementing assistant's separate code/evidence review, not independent
human sign-off, a new theory audit, or a theorem proof.

## Code refinement

- `peel_core` initializes the full original graph each call. The queue includes
  each vertex at most once. A live-clique flag allows precisely one invalidation;
  only active vertices are decremented, with an explicit zero-underflow assertion.
  Degrees are bounded by real materialized incidence sizes; exact thresholds and
  BigInt telemetry never narrow to a machine threshold. Threshold zero returns V.
- `global_F` derives a smaller local request only from an immutable same-owner
  parent certificate. It computes ceil(lambda) exactly, intersects the full core
  with original Y, and preserves original X and lambda. Containment comes from
  Lemma 1.22 plus the parent; the subset assertion is not a substitute proof.
  `largest_restricted` has no core option, so arbitrary bounds are not mislabelled.
- `ChainPoint`/`ChainInterval` remain immutable. The solver changes only which
  equivalent oracle mode it requests; its original-Y terminal comparison, child
  bounds, left-first order and original ordinary graph extraction are unchanged.
- The membership footprint path checks the same inclusion and set difference as
  the sorted path, then uses the same ordered weight map and exact network. No
  singleton folding, new clique backend, cache or alternative flow was added.
- Original/reduced interval counts remain distinct. Core counters describe full
  original-graph peeling, while their difference describes query-bound savings.
  Core timing is nested; bypass fields are null. Canonical output is unchanged.
- The production path still calls no candidate verifier. The M1 reference is
  unchanged; all-subset core truth is confined to the external M4 harness.

The complete preservation arguments and preconditions are in
docs/M4_IMPLEMENTATION.md; they are separate from finite execution evidence.

## Development findings

No new proof/specification conflict or production/reference counterexample was
found during the initial code review and Debug runs. Two routine development
errors were corrected with their original logs retained:

1. `dev-build.log`: strict -Wshadow rejected a test-probe local name. It was
   renamed; no warning was suppressed (`dev-build-2.log`).
2. `dev-ctest.log`: the newly added audit-C Python fixture listed its final two
   edges out of canonical order. The independent Graph constructor rejected it
   before that case was queried. Sorting the fixture edges fixed its construction;
   the persistent `dev-smoke/` run then passed. This was not a solver mismatch or
   mathematical counterexample. The other 10 CTest tests had passed in that run.

The acceptance driver is run after these corrections. Final results and remaining
limits must be read from REPORT.md and accepted/commands.json, not inferred from
this review text. Original failing logs are not overwritten with successful runs.

## Evidence/claim boundaries

All implementation modes are compared on the unchanged M3 corpus plus the
audit-C witness. Independent core truth unions every induced set satisfying the
degree threshold; it does not run the peeling algorithm. Footprint records are
constructed independently from reference cliques. T17 covers lower thresholds,
zero bypass, empty cores, h>n, cascades, exact large rationals and real fallback.

Profiling used a frozen local workload before edits. Separately measured footprint
and solve times are diagnostic estimates and cannot be added as exact phase
totals. Post-change core time is part of solver time; whole-process RSS includes
index and driver work. Small noisy local workloads support no universal speedup,
scalability or competitor claim. Defaults stay off/sorted. No M5 configuration,
external technique, dependency or parallel implementation was introduced.

M4 does not request another correctness tag. Changes remain reviewable and
uncommitted; formal implementation-tested ledger labels requiring a new commit
are withheld for new M4 code even after the executed test gates pass.
