# M6 current-source observation tooling acceptance

Completed 2026-10-15 Australia/Sydney. The directory date is its start date.
Scope: P16.1–P16.6, T18–T20 and the M6 portion of T27; O09/O11/O12, with retained
O01/O08 numeric/output checks. This is development tooling acceptance, not M8
performance evidence, a theorem proof, or final optimized-source profiling.

## Delivered implementation

[`experiments/final_profile`](../../../experiments/final_profile/README.md) adds:

- `instrument.generate`: production hash pins, unique insertion/replacement
  anchors and reversible edits. All production/manuscript files remain unchanged.
- `fp::Scope`, `CleanupBegin/End`, `QueryScope`, `OracleEnd`, `Session`: monotonic
  exclusive timing, actual named-object cleanup, partial events, immutable original
  endpoints and traversal identities, internal rank snapshots and separate JSONL.
- Distinct count-site and footprint tuple/vertex work, post-core H/W histograms,
  original-bound versus core rejection, actual core loop work, network sums/maxima,
  depth/frontier and non-output layers. No reinterpretation of `cliques_scanned`.
- `cost_associations`, `core_cost`, `early_stop`, `overhead`: deterministic reports,
  strict/prefix checks, executed suffix work and explicit unavailable-data labels.
- `verify_build`, `validate.check_events`, native boundary tests and lossless
  archive/report regeneration. Instrumentation is absent from the control library.

The diagnostic is built from the production source at `35961a6` and the exact
observer/generator contents in each configuration's `source_manifest`. Pins cover
29 production inputs and 14 tooling inputs. Both build identities confirm matching
compiler/options for all 13 library translation units and no observer symbols in
the control library. This source is the validated pre-M7 solver, not a claim that
M7 has been implemented.

## Executed checks

| Accepted evidence | Release | Debug + ASan/UBSan |
|---|---:|---:|
| CTest tests passed | 7/7 | 7/7 |
| Scheduled CLI calls (control + diagnostic) | 224/224 completed | 224/224 completed |
| Independent definition/observer/trace cases | 112 | 112 |
| Separate native control trace-adapter calls | 112 | 112 |
| Observed separator queries checked | 246 | 246 |
| Maximum visited depth | 2 | 2 |
| Non-output terminal layer occurrences | 16 | 16 |
| Strict off/safe report pairs | 56 | 56 |
| Executed full-suffix report pairs | 56 | 56 |

The accepted directories are **[`accepted-release-v3`](accepted-release-v3/checks.json)**
and **[`accepted-sanitize-v3`](accepted-sanitize-v3/checks.json)**. Each freezes 28
named/family/seeded graph/h fixtures, core off/safe, k=1/all and both executables
before execution. Eight random fixtures use seed 20261014; others have explicit
generation parameters. Named coverage includes zero cliques, h>n, ordinary bridges,
tied outputs, non-output layers, core restoration/cascades, repeated footprints,
clique concentration, equal-density regions and multiple nested density layers.
The same independently enumerated graph/h truth is used for all modes.

All outputs match the independent direct definition. Separators match exhaustive
global F; terminal adjacency is checked against the independently constructed
cardinality-line envelope. The uninstrumented TraceSink adapter's semantic query
trace matches the diagnostic. Count/footprint visits and histograms are calculated
independently from reference cliques; arc identities, root-zero parent/depth,
full 2r−1 queries and exact fixed-k incurred-work/full-prefix reconciliation pass.

The seven CTest entries include seven Python artifact-contract tests, a fake-clock
test, native partial-coverage tests and existing primitive/core suites against both
libraries. Actual arbitrary-precision max-flow executes, including automatic
fallback; forced-uint128 rejection and ordinary exact arithmetic limits are retained.
The standalone [Release](boundaries-release/checks.json) and
[sanitizer](boundaries-sanitize/checks.json) boundary captures preserve deliberate
SIGKILL, controlled cancellation and real automatic fallback. The first two are
expected test outcomes, not censored benchmark runs or sanitizer failures.

## Evidence and reproduction

- [Environment/toolchain](environment.json): macOS 15.8.1 arm64, Apple M1, 16 GiB,
  AppleClang 17.0.0, CMake 4.4.3, Python 3.12.2, pinned Boost 1.86.0. One native
  worker, 30-second development guards, uncapped memory, uncontrolled cache.
- [Release build identity](release-build-identity.json),
  [sanitizer build identity](sanitize-build-identity.json), and configure/build/
  CTest/validation logs in [`logs`](logs/).
- [Release configuration and complete fixture manifest](accepted-release-v3/configuration.json),
  [sanitizer configuration](accepted-sanitize-v3/configuration.json),
  [Release bundle](accepted-release-v3/bundle.json),
  [sanitizer bundle](accepted-sanitize-v3/bundle.json).
- [Release reports](accepted-release-v3/reports.json) and
  [sanitizer reports](accepted-sanitize-v3/reports.json). VF/IPPV pairs are explicitly
  unavailable here: no new IPPV run or internal IPPV phase attribution is claimed.
- `raw-runs.tar.gz` in each run directory retains every raw native stdout/stderr,
  process record, observer event and control-trace input/output. Every byte was
  checked before removing loose generated copies. Bundles pin archive and artifact
  hashes; the report builder reads the archive directly, without extraction.

Build/CTest/validation commands are in the
[tooling instructions](../../../experiments/final_profile/README.md). To regenerate
the accepted report without running a new process:

```sh
.venv/bin/python experiments/final_profile/reports.py evidence/m6/final-profile-20261014/accepted-release-v3/bundle.json --output /tmp/m6-release-report.json
cmp /tmp/m6-release-report.json evidence/m6/final-profile-20261014/accepted-release-v3/reports.json
```

Both accepted reports regenerate byte-identically. Final checks also verify all
four paper hashes and unchanged production/reference/baseline source trees.

## Retained earlier attempts

No attempt is substituted into the accepted v3 run totals:

- `development-release-initial`: 64 completed CLI calls and 32 checked diagnostic
  cases, before the full fixture suite and final observer additions.
- [`build-identity-initial-failure.json`](build-identity-initial-failure.json): the
  verifier initially conflated two `graph.cpp` basenames. It now uses complete
  source-relative paths. This was a verifier failure, not solver disagreement.
- `accepted-release` and `accepted-sanitize`: each has 200 completed native CLI
  calls and 100 successful independent checks, but its final report join failed.
  Two predeclared fixture families generate the same graph; the old generic suite
  ID made their joins ambiguous. Both `failure.json` files and all raw data remain.
- `accepted-release-v2` and `accepted-sanitize-v2`: each passed 200 CLI calls,
  100 diagnostic cases and report checks after fixture-qualified join keys. Their
  measured maximum depth was only one. V3 adds three multi-density fixtures and
  strengthens separator/chain validation; earlier evidence is not pooled with v3.

## Limits and handoff

P16.3's M7 partition/reuse fields are explicitly unavailable, not measured zero;
P17.6 supplies the real events when that algorithm exists. Only actual post-core
footprint histograms are measured. Library-internal temporaries/releases remain in
their enclosing operation; separately timed cleanup names the actual owners.
The final snapshot ends before writing its own final event; wait4 covers whole
process completion. Counter/timer overhead perturbs phases and is not subtracted.

RSS is whole-process, includes observer storage and is separate for each control.
The 5 ms capture poll and tiny single-repeat fixtures limit overhead ratios; these
are checks of reproducible accounting, not estimates of real-graph speedups.
No phase peak-RSS, causal IPPV attribution, logarithmic-depth claim, parallel solver
or new algorithm optimization is asserted. T27's M8 Linux resource/complete campaign
gates remain pending. After M7, P18.4 must refresh source pins, rebuild both binaries,
repeat observation equivalence and freeze the final-source experiment configuration.
