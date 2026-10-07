# Exact count optimization — 2026-10-07

One measured bottleneck change is implemented: `--clique-count membership`
uses exact vertex markers in `MaterializedCliques::count`. Sorted counting remains
the default and control. Both modes use the same immutable clique tuples and
`BigInt` accumulator. [Preservation, preconditions and costs](../../../docs/COUNTING_IMPLEMENTATION.md).

| Case (h=3,k=5) | Sorted median [min,max] s | Membership median [min,max] s | Median ratio sorted/member |
|---|---:|---:|---:|
| ca-grqc-h3-k5 | 0.349554 [0.342789, 0.533862] | 0.250145 [0.230998, 0.597547] | 1.40x |
| ca-condmat-h3-k5 | 38.791546 [38.556403, 39.562047] | 1.709334 [1.634339, 1.716649] | 22.69x |

Native results: **12/12 attempted**,
{'completed': 12}; **0 unrun**.
All 12 completed external validators pass;
6/6 pairs match strictly.
Completed outputs and full counters are identical within each graph and match
all three earlier corresponding core-off runs. Historical times are not pooled.
Time includes allocation/initialization of the new per-call marker array; external
validation is separate. These are three-repeat local measurements on two h=3,k=5
cases, not a general speedup, larger-k result or a new comparison with IPPV.
One GrQc pair is slower with membership; all measurements remain in the table.
[All times, RSS and censored outcomes](aggregate/TABLE.md).

## Validation and scope

- Debug, Release and ASan/UBSan: **16/16 CTest each**, including T04-COUNT,
  T04-COUNT-CLI (217 calls per build), numeric boundaries and real fallback.
- Python: **144 passed in 6.66s**. No production code is imported by the reference.
- **14 independent-reference campaigns pass**: existing
  M2/M4 exhaustive-small, seeded and higher-h tiers plus M4 smoke in Debug and
  ASan/UBSan. Every campaign executes automatic arbitrary-precision flow.
- **1,392,496 prior responses match**, excluding
  only core-reduction wall time. Case manifests are identical to the previous
  corpus; all fixed-k prefixes, relabelings and four core/footprint modes remain
  covered. No sanitizer diagnostics or correctness counterexample occurred.
- Papers, independent reference, historical evidence and prior binaries are
  unchanged. Finite agreement is implementation evidence, not a theorem proof.

P12.1/O01/O04/O08/O11/O12 gain this scoped result; P14.1/P15.1 gain bounded
interpretation and reproducible aggregates. This completes the targeted count
change and its limited comparison, not M5 or the final benchmark gate.

Environment: Apple M1, 16 GiB, macOS 15.7.7 arm64, AppleClang 17.0.0.17000603,
C++17, Boost 1.86.0, Python 3.12.2. Same new Release binary for both modes;
adjacency enumeration, membership footprints, core off, seed 20261003, three
repeats, randomized within-pair order, one worker/serial runs, 60-second native
and validator guards, no memory cap, uncontrolled cache, no warmups or retries.

## Changed files and executed evidence

Core changes: `materialized.hpp/.cpp` (`CliqueCounting`, constructor, `count`),
CLI dispatch/help, CMake and test-only probe selection. Added count/CLI regression
tests; extended the existing experiment runner's optional count selector. The
historical profiler's tests now use its retained source snapshot; no profiler
or baseline was added. Contracts, task/claim records and reports are updated.
[Full changed-file inventory](files_changed.json).

Executed: CMake configure/build (`-j2`) and CTest for three profiles; all 14
campaigns; the existing Release builder; paper verification; pytest; saved-record
comparison; the existing experiment runner with strict agreement and timeout
retention; aggregation and byte-identical replay with no native reruns.
[25 build/validation commands](checks/commands.json), [pytest](pytest.json),
[equivalence verifier command/log](verify-process/process.json),
[performance command](launch.json), [postprocessing commands](postprocess-commands.json),
[fixture/seed manifest](fixture-manifest.json), [binary/source pins](preflight.json),
[environment](environment.json), [raw native runs](campaign/runs),
[regeneration](regeneration.json).

No new blocking semantic conflict. Larger k, other h/datasets, final experimental
scope, any new IPPV comparison, clean-machine smoke and the release package remain
unrun. DCLDS remains deferred. No additional optimization cycle is started.
