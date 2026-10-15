# M7 interval-local clique propagation and exact count reuse

Accepted 2026-10-15 for P17.1–P17.7, after executed implementation, preservation,
independent correctness, lifetime/numeric and observation checks. This is finite
development evidence, not a proof of the manuscript or a formal M8 benchmark.
Implementation checkpoint: pending local commit; the starting commit was `046c553`.

## Implementation and mathematical boundary

[The unchanged semantic specification](../../../docs/ALGORITHM_SPEC.md) and
[M7 preservation argument](../../../docs/M7_INTERVAL_CLIQUES_PLAN.md) govern this
refinement. Root IDs represent every materialized h-clique. A proper certified Z
partitions C(X,Y) by C subseteq Z into disjoint child ranges. Crossing-Z cliques
stay right and later contribute C minus Z. Exact mu(Z)=mu(X)+left-size is computed
before constructing the immutable ChainPoint. Temporary core exclusion never
removes inherited IDs. No public ID list supplies a global certificate.

- P17.1/O04–O06/O09–O11: written set/count/footprint identities, original-core
  preservation, ownership preconditions and O(M(D+1)) tuple/ID-visit bounds.
  Logarithmic depth requires a separate balance condition and is not claimed.
- P17.2: `IntervalTraversal` owns one root ID vector and private DFS frames;
  `CliqueRange::partition` visits each active ID once and swaps only within its
  half-open range. No parent-sized copied clique lists or eagerly executed right
  oracle. `next` cannot be reused after an exception.
- P17.3–P17.5: `aggregate_impl`, `ClosureOracle::global_impl/local_footprints/
  separate_impl`, and `solve` retain the existing exact network, safe-core
  certificate, original endpoints/lambda, left-first traversal and extraction.
  `global` remains the default; `interval-scan` isolates local scanning and
  partitioning; `interval-reuse` additionally eliminates proper-separator count
  scans. Emitted components and standalone queries retain their count paths.
- P17.6/O08/O09/O11/O12: solve-only `--clique-work` with strict option errors,
  explicit mode/depth/range/partition/reuse/capacity counters, source-pinned M6
  events and `local_cliques` report joins. Canonical solutions/hashes are unchanged.
- P17.7: actual outcomes, fixture/seed manifests, source pins, work/storage
  examples and reproducible commands below. M8 final host/data/resource/variant
  decisions and shared baseline smoke remain outstanding.

Changed production files: `include/vflhcds/solver/traversal.hpp`,
`src/solver/traversal.cpp`, oracle header/implementation, solver header/implementation,
query telemetry header/implementation, CLI dispatch and root CMake. Tests add
`m7_interval.cpp`, `m7_cli.py`, the test-only probe's work configuration and
`validation/m7_campaign.py`; `scripts/run_m7_checks.py` records acceptance.
The final-profile generator, observer, pin/verifier, validator and report tests
are updated. Supporting interface, architecture, build, task and traceability
records link here. See `checks.json` for preserved-path checks: papers, independent
reference, exact/flow implementation, materialized enumeration/counting and core
implementation, baselines, old fine profiler and all M5/M6 evidence are unchanged.
D012/D029 remain respected; no new baseline acquisition or technique import.

## Executed validation

[Commands and exit codes](acceptance/commands.json),
[start-of-run environment](acceptance/environment.json),
[fixture/seed inventory](fixture_manifest.json) and [verified summary](checks.json)
are machine-readable. The command runner stops at the first nonzero exit; all
30 scheduled commands completed successfully. T21/T22 native tests
in each Debug/ASan build checked 140,576 nested combinations with 1,850,979
assertions: every labelled graph n<=4 at h=2/3, all X subseteq Z subseteq Y and
intermediate upper bounds, both enumerators/count predicates/footprint predicates,
and named h=4/5 cases. They independently enumerate tuples by vertex subsets.

T23 uses the existing independent M3/M4 direct-definition/all-proper-superset
truth and cardinality-line-envelope chain. All k prefixes through q+2, original
and relabeled ties, isolates, disjoint components, h>n, core off/safe, both
footprint modes and auto/forced-big policies are checked. Debug uses sorted counts;
ASan uses membership counts. Both enumerators/count modes also run through named
CLI and all-subset tests. Table entries count solve operations in persistent native
probes, not that many independent process launches or distinct graphs.

| Build | Tier | Base graph/h cases | Variants | Three-mode solve executions |
|---|---|---:|---:|---:|
| debug | exhaustive-small | 2,198 | 4,396 | 461,760 |
| debug | higher-h | 64 | 128 | 14,016 |
| debug | seeded | 1,000 | 2,040 | 239,904 |
| debug | smoke | 31 | 124 | 14,928 |
| sanitize | exhaustive-small | 2,198 | 4,396 | 461,760 |
| sanitize | higher-h | 64 | 128 | 14,016 |
| sanitize | seeded | 1,000 | 2,040 | 239,904 |
| sanitize | smoke | 31 | 124 | 14,928 |

Total: **1,461,216 mode solve operations**. The seeded
tier uses 20260929; the full per-case metadata, exact expected outputs and observed
outputs/traces are retained in `cases.jsonl`, `results.jsonl.gz` and
`mode_results.jsonl.gz`. Debug/ASan fixture bytes agree. Both builds pass 18/18
CTest entries, including 594 M7 CLI invocations per build and the unchanged 74
independent reference tests. RelWithDebInfo build/CTest is recorded separately
in `logs/relwithdebinfo-*` and `supplemental-checks.json`.

T24 includes the original core pendant recovery witness and crossing-triangle
singleton residual. T25 covers invalid/missing/duplicate/out-of-range IDs, foreign
index ownership, noncopyable traversal, early stop, cancellation, trace exceptions
and exhausted traversal. Existing primitives test numeric limits, forced-uint128
rejection and real automatic arbitrary-precision flow on suitable standalone
requests. Tiny separators also run forced exact backends; no fabricated enormous
chain count or forced-big run is described as automatic fallback. ASan/UBSan found
no failure in the executed scope. No parallel solver or TSan claim is made.

## Final local diagnostic/control acceptance

Release and Debug ASan/UBSan each pass 7/7 observer CTest entries (including eight
Python contract tests), 31 production-source pins, 14 matched library translation
units and absence of observer symbols in the control archive. The final build
manifests in each `profile-*/configuration.json` pin the actual observer tooling;
`environment.json` is the earlier start-of-run snapshot. Production sources are
fixed across the whole accepted correctness campaign. Reporting refinements
made before final diagnostic configuration are covered by those final manifests.

Each build completes 672 CLI calls on 28 fixtures, three work modes, core off/safe,
k=1/all and diagnostic/control roles, plus 336 independent native control-trace
calls. Across builds: **1,344 CLI calls and
672 trace calls**. All completed; zero timeout/OOM/error
and no missing scheduled row. Seed 20261014 defines eight diagnostic fixtures.
Independent checks cover outputs, exhaustive F, envelope adjacency, local/global
scan visits, partition membership visits, exact count reuse, footprint histograms,
network identities, depth and exact fixed-k prefix work. Report regeneration from
lossless hash-checked raw archives agrees. `core`, `early_stop`, `local_cliques` and
observer-overhead joins require the appropriate semantic equality. IPPV pairs
remain unavailable in this development-only bundle.

Phases add root ID setup, partition and count reuse. Both scan savings and
partition overhead remain visible. Capacity/peak inventories are not subtracted
as additive suffix work. Initial-cost reporting includes the root worklist setup;
older M6 streams use their original index boundary. Old M6 Release and sanitizer
reports still regenerate byte-identically with the updated report builder.

## Observed work/storage example, not a timing conclusion

`nested_density_layers_4`, h=2, core off, full traversal has ten materialized
cliques. The final Release diagnostic records:

| Mode | Footprint tuple visits | Partition ID visits | Count tuple visits | Reused separator counts | Extra ID payload bytes |
|---|---:|---:|---:|---:|---:|
| global | 60 | 0 | 70 | 0 | 0 |
| interval-scan | 30 | 20 | 70 | 0 | 80 |
| interval-reuse | 30 | 20 | 40 | 3 | 80 |

These are different recorded work categories, not equal-cost operations. Full
examples with actual reserved capacities, pending-frame peaks and paired control
process peak RSS are in `checks.json`. ID payload bytes exclude vector/allocator
metadata, endpoints and other owners. Global core work, enumeration and emitted
counts remain. The root flow network is unchanged in core-off mode. This does
not establish real-graph speedup or lower total peak RSS.

## Environment, preservation and reproduction

Local macOS arm64; exact platform/Python in `acceptance/environment.json`, compiler
and CMake in command logs, compile flags in each build identity. AppleClang 17,
C++17, Boost 1.86.0, CMake 4.4.3 and Python 3.12.2 were used. Validation has no
host/cache isolation or performance claim. The acceptance driver runs its native
checks sequentially; earlier preflight/build work can overlap. Diagnostic native
guard is 30 seconds, memory uncapped, one repeat, 5 ms process polling; these are
development limits, not D046 approval. Actual time/RSS is retained, never repaired.

```sh
.venv/bin/python scripts/run_m7_checks.py evidence/m7/new-acceptance
.venv/bin/python evidence/m7/interval-20261015/summarize.py
.venv/bin/python experiments/final_profile/reports.py evidence/m7/interval-20261015/acceptance/profile-release/bundle.json --output /tmp/m7-report.json
cmp /tmp/m7-report.json evidence/m7/interval-20261015/acceptance/profile-release/reports.json
.venv/bin/python scripts/verify_papers.py
```

Initial Debug smoke/17-test checks and the eight-fixture diagnostic preflight are
retained outside `acceptance/`, with their original hashes and logs. The preflight
predates final initial-cost/report refinements and is not pooled into final counts.
There was no algorithm/output mismatch requiring a counterexample repair. Deliberate
negative tests, cancellation and native partial-stream SIGKILL are contract tests,
not excluded benchmark failures. No real graph, baseline or formal M8 campaign ran.
M8 still needs input acquisition/provenance, Linux enforcement, exact final machine
and schedule decisions, shared baseline smoke and fresh formal measurements.
