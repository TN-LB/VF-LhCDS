# Shared VF-LhCDS / IPPV evidence tools

These tools are external to both algorithms. DCLDS work remains deferred by D029.
The historical D040/D041 evaluation is complete at D042's bounded scope.
D045 now schedules [M6–M8](../docs/M6_M8_EXECUTION_PLAN.md): cost instrumentation,
interval-local clique/count reuse and fresh formal evaluation. All earlier local
measurements remain preliminary and excluded from M8. Preserve
[historical results](../evidence/m5/REPORT.md) and
[reproduction instructions](../docs/M5_REPRODUCTION.md).

The tools below describe the implemented M5 behavior. M6's separate
[`final_profile`](final_profile/README.md) now implements source-pinned diagnostic/
control builds, work accounting and reports, accepted at `de25116`
([evidence](../evidence/m6/final-profile-20261014/REPORT.md)). M7 work modes and their local matched-source diagnostic refresh are
[validated](../evidence/m7/interval-20261015/REPORT.md). Linux enforcement, final-host/source alignment, shared
baseline smoke and formal M8 campaign gates remain planned.
The old `fine_profile` pins precede the count optimization and must not be relabeled
as final-source diagnostics. M8 requires matching final diagnostic/control builds.

`build_vf.py` builds an unchanged Release solver with recorded source/compiler/
binary hashes. `prepare_input.py` converts an explicit-n edge list, preserving the
complete declared vertex universe and recording loops/duplicates and checksums.
`validate.py` checks exact canonical records and separates structural checks from
tiny all-superset definition truth. `run.py` freezes configuration and seeded
within-block algorithm order before launching children, retains every outcome,
and writes immutable per-run outputs/manifests with a final campaign checksum list.

```sh
.venv/bin/python experiments/build_vf.py --build build-m5-release --evidence evidence/m5/new-build --cmake .venv/bin/cmake
.venv/bin/python experiments/prepare_input.py --source .deps/baselines/ippv/dataset/CA-GrQc.txt --evidence evidence/m5/new-normalized-input
.venv/bin/python -m pytest experiments/test_harness.py baselines/ippv/test_adapter.py reference/tests -q
.venv/bin/python experiments/run.py --config CONFIG.json --evidence NEW_DIRECTORY
```

All run directories must be new. Example configurations and actual outcomes are
in [the executed report](../evidence/m5/harness-20261003/REPORT.md). A `draft` config
cannot run. `diagnostic` records local validation/smoke work; `approved_campaign`
must only be used after the owner has approved and recorded final settings. The
scope string is an execution safeguard, not proof of human approval.

For the owner's stop-at-blocker workflow, pass `--stop-on-failure`. The runner
records `execution-policy.json` before launch, stops on the first unsuccessful
run or a tie-aware disagreement at the end of a completed comparison block, and
writes `stopped.json` with the reason and every planned but unrun entry. Existing
raw logs and failed outcomes remain in the checksum inventory. Different valid
cutoff ties alone do not stop execution. Without this flag the existing run-all
policy remains available. A changed input/binary pin or invalid configuration
raises immediately; the stopped-run ledger covers recorded run/comparison
failures, not rejected preflight inputs. There is no automatic retry or resume.

For a frozen campaign that should continue after native timeouts, add
`--continue-on-timeout` together with `--stop-on-failure`. Each timeout remains
an unsuccessful, censored measurement with no accepted output or retry. The
remaining fixed schedule runs normally; validation failures, errors and substantive
pair disagreements still stop. Both switches are saved before any native child.
The driver still exits 1 if any native call timed out, even when all planned calls
were attempted. This is D035's execution policy; historical policies are unchanged.

For equivalent VF-mode ablations, also pass `--require-strict-agreement`.
Canonical records must match exactly, including cutoff tie selection. This flag
is recorded before execution, makes any completed-pair difference unsuccessful,
and combines with `--stop-on-failure` to stop on that difference. Without it,
the cross-algorithm cutoff-tie policy remains unchanged. D036 uses this stricter
contract for core off/on; it changes no solver semantics or resource limit.

Every configuration explicitly supplies seed, repeats, timeout, thread count,
memory policy, cache policy, binary/graph checksums, algorithm feature switches,
and h/k/validation scope. This version supports one algorithmic worker, no imposed
memory cap, and uncontrolled cache; other policies are rejected, not ignored.
IPPV iterations are explicit. No dataset/grid/timeout/repeat defaults are invented.
VF `options` also accepts optional `enumeration`: `combinations` or `adjacency`.
Omission keeps the historic combinations behavior and emits no new CLI option,
so old pinned binaries remain usable. Explicit modes are saved in the frozen
configuration and actual native command; neither changes semantic hashes.
Optional `counting` accepts `sorted` or `membership` and emits `--clique-count`
only when explicitly present. Omission retains the old sorted-count behavior
and compatibility with earlier binaries. Use strict agreement for count-mode
comparisons; the switch changes inclusion checks, not output semantics.
Optional VF `output` is `fixed` (default) or `all`; the latter passes explicit
`--all` to both native solver and external validator. Case `k` stays the target
prefix length. Full-output configs require `--require-prefix-agreement`, exactly
two VF modes with identical binary/options except output scope, and no simultaneous
whole-output strict flag. The comparator checks `fixed == full[:k]`, including
exhaustion and the accepted tie order. It does not compare their full hashes or
claim real-graph completeness from agreement. Manifest k is null for the full run;
summary `output_scope` records which task was executed.

`--environment-baseline PATH` enables D040's before/after block observations via
`environment.py`. Save an AC-power snapshot before launch and reuse it across all
three suites. Power-source/settings changes or missing required power evidence
stop subsequent calls and retain an unrun ledger; unavailable VM/swap probes are
recorded without fabrication. Load never triggers filtering or retries. Probes
run outside native timing; they are not continuous monitoring or host reservation.
The default without this flag preserves the historical runner behavior.
CLI SIGINT/SIGTERM requests retain the current guarded run and stop before the
next child; completed records and every unrun call remain in the ledger. These
signals do not initiate retries or accept partial output.
Checksums pin both binaries, VF source provenance and the current IPPV source lock.

Process time and peak RSS come from the native child's `wait4` record. Validation
runs as a separate later process with its own resource record. IPPV's enumeration,
candidate verification and serialization stay timed. VF's native phase/counter
telemetry is retained; unavailable IPPV wall phases and per-rank latencies are
null. No signal is guessed to be OOM; only VF's explicit documented exit-6/status
pair receives that label. Crashes, timeouts, partial/malformed outputs, wrong
semantic hashes and validation failures remain unsuccessful results.

The cross-implementation comparator preserves selected sets, checks counts,
cutoff density and all strictly higher-density sets, and permits different valid
cutoff ties. Its label is agreement evidence; it never upgrades structural checks
to a maximality/completeness proof. Failed runs are recorded and not compared as
successful outputs. No speedup aggregation or favorable-case filtering is done.

Current limitations: full resource-profile integration, final configuration,
numerical/broad baseline coverage, performance aggregation, rank latency, full
experiments and clean-host release reproduction remain unfinished. Hardware is
recorded in the evidence's `system.json`/`hardware-retry.json`; it is not yet embedded
in every per-run manifest. The first shared real smoke timed out in the basic VF
mode at 60 seconds. The later [phase diagnostic](../evidence/m5/phase-diagnostic-20261003/REPORT.md)
builds a separate target linked to the unchanged Release library and confirms
that indexing has not finished when the 60-second guard fires; solve is not
reached. See [phase_probe](phase_probe/README.md) for this diagnostic's distinct
stderr contract and scope. The subsequent enumeration extension and its executed
checks are recorded separately under `evidence/m5/enumeration-20261003`.
The fresh [paired real smoke](../evidence/m5/paired-smoke-20261005/REPORT.md)
completes for both algorithms with strict output agreement. D030 subsequently
approves the first repeated pilot via a separate config, preserving the
[non-executable draft](../evidence/m5/campaign-proposal-20261005/PROPOSAL.md).
The [executed pilot](../evidence/m5/pilot-20261005/REPORT.md) stops after 20 of
48 planned native calls at a tie-aware output disagreement. Its evidence-only
aggregation script reads immutable manifests; remaining runs and diagnosis are
unrun, and neither algorithm is silently repaired or retried.
The subsequent [authorized diagnosis](../evidence/m5/ippv/disagreement-20261005/REPORT.md)
certifies the disputed VF set and repairs IPPV capacity truncation and PAVA bounds
with patches 0006/0007. The corrected baseline uses `build-ippv-fixed-*`; the old
pilot's pinned binaries/configuration remain historical. Original-case correctness
replays pass tie-aware comparison, but no benchmark campaign has resumed or mixed
old/new baseline measurements.

D031 then authorizes a [fresh seven-patch campaign](../evidence/m5/pilot-fixed-20261005/REPORT.md)
on the same 48-call schedule. All 24 CA-GrQc runs and validators pass, with
12/12 tie-aware pair matches. The first CA-CondMat VF call (h=3,k=5) times out
at 60 seconds; the driver exits 1 and preserves 23 unrun calls. All planned
cells, successful three-repeat time/RSS summaries and the censored timeout are
retained. No timeout extension or retry is performed. The old five-patch pilot
is unchanged, and its timings are not combined with the repaired baseline's.

The subsequent [D032 phase diagnosis](../evidence/m5/condmat-phase-20261005/REPORT.md)
links the same adjacency Release library in a separate probe build. Two tiny
output/query-counter checks and external definition validators pass. CA-CondMat
parsing/indexing finish in 0.042061041/0.1166765 s; 137 queries finish before the
60-second solve timeout. Query-end markers expose progress, without treating
inter-query gaps as isolated flow timings. No real completed output or new
benchmark measurement is inferred. An existing membership-mode diagnostic is
prepared separately; the campaigns remain stopped and unchanged.

The [2026-10-06 membership diagnostic](../evidence/m5/condmat-membership-20261006/REPORT.md)
completes the same CA-CondMat h=3,k=5 case in 38.997086249 s with five structurally
checked outputs. One native call and one external validator exit zero; existing
production and runner code are unchanged. This single-mode diagnostic is kept
separate from historical basic-mode timing cells and has no paired comparison.

The [fresh CA-CondMat pair](../evidence/m5/condmat-pair-20261006/REPORT.md) then
completes both native runs and structural validators. Ranks 1–4 agree exactly;
rank 5 has an allowed density-22 cutoff difference. VF membership takes
38.525397500 s and seven-patch IPPV 2.723666167 s in this single pair. Repeated
measurements remain separate future work; historical timing cells are preserved.

The [repeated membership pilot](../evidence/m5/pilot-membership-20261006/REPORT.md)
then attempts all 48 frozen calls using timeout continuation. It records 36
completed/structurally checked outputs and 12 VF CA-CondMat timeouts, with no
unrun calls. All 12 complete CA-GrQc pairs match under the cutoff-tie rule;
CA-CondMat pairs remain unavailable. The driver exits 1 for the censored outcomes.
133 pytest checks pass, saved evidence verifies, and seven aggregate artifacts
regenerate identically. The previous single CA-CondMat completion does not
recur within 60 seconds; its timings are not substituted for the repeated results.
Production code and historical evidence remain unchanged; broader M5 gates stay open.

The [core off/on ablation](../evidence/m5/core-ablation-20261006/REPORT.md) then
executes 48 VF calls with strict comparison and otherwise unchanged graph/grid/
resource settings. All 30 completed outputs pass structural checks, with 15/15
strict paired matches; both modes time out in all 18 CA-CondMat k=10/15/20 runs.
The runner's strict-policy tests bring combined pytest to 137 passes. Core reduces
observed query/network sizes and peak-RSS medians on completed settings, without
resolving the large-k timeout boundary; time effects are small and mixed. Raw
censoring, separate validators, included core cost and all seven reproducible
aggregates remain explicit. No production change or fresh IPPV run is included.
