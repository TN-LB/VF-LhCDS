# Fresh local reproduction — 2026-10-08

**The local rebuild and correctness smoke pass. This is not a clean-machine run.**
The [checked plan](checked/plan.json) records the environment, source pins and all
commands before execution; [23 command records](checked/commands.json) exit 0.

- VF: new Release directory, strict warnings, membership-count test probes;
  **16/16 CTest pass in 13.25 s**, including oracle/solver/mode smoke and actual
  numeric fallback tests. [CTest log](checked/commands/vf-ctest/stdout.txt).
- Independent reference, harness and adapter: **164 pytest pass in 13.02 s**.
  [Python log](checked/commands/python-tests/stdout.txt).
- IPPV: fresh local clone at the pinned author commit, all eight patches applied
  in order, every patched-source/patch hash checked, new Release build succeeds.
  Fractional-bridge, equal-density-bridge and ordinary bridged-triangle fixtures
  pass independent definition checks. No zero-density output extension is made.
- VF adjacency/membership/membership/core-off on triangle plus isolate at h=3,
  explicit full output, matches independent truth including the zero-density
  isolate. [Definition evidence](checked/vf-definition/manifest.json).
- All four paper hashes match. Production/reference code is unchanged. The newly
  built VF and IPPV hashes equal the measured D041 hashes on this host; this is
  one observed local result, not a cross-platform bit-reproducibility guarantee.

Environment: existing Apple M1/macOS 15.7.7 arm64 host, AppleClang 17.0.0
(`clang-1700.6.3.2`), Python 3.12.2, CMake 4.4.3, pytest 8.4.2, Boost 1.86.0.
The clone uses existing local Git objects; Python/Boost/OS/compiler are reused.
No dependency acquisition, performance campaign or concurrent benchmark occurs.
The selected performance runs finished before any build started.

The first wrapper attempt in [accepted/](accepted/) exits 1 before building:
its paper-check child exits 2 because a relative script path is resolved from a
log directory. The failed driver and log remain intact. The corrected driver
resolves executables/input paths and writes a new [checked/](checked/) directory;
no original evidence is overwritten. This is a wrapper correction, not an
algorithm or experiment-configuration change.

Executed entry point:
`run.py --build build-m5-reproduction-fixed-20261008 --evidence evidence/m5/reproduction-20261008/checked`.
[Completion and executable hashes](checked/completion.json),
[baseline build flags/logs](checked/ippv-build/commands.json),
[VF emitted compile flags](checked/vf-compile-commands.json),
[reproduction instructions](../../../docs/M5_REPRODUCTION.md).
`run.py::main` orchestrates existing builders/tests; no new algorithm is added.
The final [integrity command](integrity-command/process.json) exits 0:
**6,074 inventory entries** across both main versions and both ablations verify;
**114 production/reference/test/fixture files** remain unchanged from the measured
commit. [Hashes, fixture manifest and checks](integrity.json). `verify.py::main`
performs read-only comparisons and launches no native algorithm.
[Changed-file index](file_changes.json); documentation updates cover current
tasks/traceability, the M5 plan, build/reproduction instructions and reports.
Main-suite aggregation uses `postprocess.py::main` and `review.py::main` in the
D041 evidence directory; the shared algorithm/harness implementations are unchanged.

P15.1/O12 gain this local reproduction evidence; P15.1 stays open for a genuine
clean-machine run. Full sanitizer/exhaustive/seeded tiers are not rerun here;
their existing D038/B09 evidence remains separate. TSan/parallel code, DCLDS,
broader data/baseline coverage and unavailable rank/detailed-phase metrics remain
unrun. Finite smoke agreement does not prove the mathematical theorem.
