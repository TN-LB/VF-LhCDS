# M5 shared harness — executed 2026-10-03

Tasks P11.1-P11.3; evidence relevant to O12. The shared tooling is implemented and
tested, but the real-data smoke is incomplete: IPPV completes and VF basic reaches
the predeclared 60-second guard. Formal performance experiments have not started.
Expansion pauses under the owner's stop-on-blocker/decision instruction.
[Proposed next diagnostic](NEXT_STEP.md) is concrete, unrun and marked draft.
DCLDS remains deferred under D029; there was no new DCLDS reading or integration.

## Files and symbols

New external Python modules under `experiments/`:

- `build_vf.py:main`: configure/build unchanged Release VF, record source/compiler/
  binary provenance and actual build-info output.
- `prepare_input.py:prepare`: normalize an explicit-n edge list while preserving
  isolates and recording raw/normalized hashes and removed loops/duplicates.
- `support.py`: shared external imports, canonical hashes, file records and the
  already tested native `wait4` capture helper. No solver imports these tools.
- `validate.py:parse_records,validate,compare`: canonical integer/JSON/rational
  checks, exact counts/connectivity, independent definition truth, and separately
  labelled strict/tie-aware cross-implementation agreement.
- `run.py:load_config,schedule,run_vf,execute`: explicit configuration, source/binary/
  graph pins, seeded within-block order, immutable raw outputs, separate native/
  validation processes, preserved failure statuses, and final checksum inventory.
- `test_harness.py`: 21 tests, including malformed/partial outputs, exact IDs,
  nonmaximal sets, cutoff ties, missing zero results, normalization, shuffled order,
  blocked draft execution, native error/OOM/SIGKILL/timeout and wrong output hash.
- `README.md` and `__init__.py`: usage and package boundary.

TASKS, CLAIM_TRACEABILITY, BASELINE_AUDIT and the M5 status report record executed
work only. No IPPV source patch, proposed solver/reference change, paper revision,
dependency installation, commit, or M5 completion is included in this turn.
[Changed-file inventory](files_changed.json) covers the entire current M5 tree.

## Build and tests

The new `build-m5-release/vflhcds` is C++17 Release/O3, strict warnings, sanitizers
off, tests disabled in this production-only build. The source and compile commands
are pinned by [build provenance](build-vf-verified/provenance.json). The unchanged
IPPV executable uses the existing five-patch C++14 Release build/provenance.

Both initial and final CMake configure/build pairs exit 0: four successful build
commands in [initial logs](build-vf/commands.json) and
[verified logs](build-vf-verified/commands.json). The first Python build driver
then failed while incorrectly parsing `print-build-info` as JSON; that CLI emits
key=value text. [Driver error](build-vf/driver-error.json), original driver bytes,
build-info output and successful CMake logs are preserved. The corrected driver
retains text and exits 0; this was a tooling defect, not a compiler/solver failure.

The first combined pytest run recorded four failures and 108 passes: a 0.2-second
fault-fixture budget also killed ordinary Python startup. The runner correctly
reported timeout; the fixture budget was inappropriate for the four non-timeout
cases. They now use five seconds, while the intended timeout fixture retains 0.2.
Original test source and [failed log](pytest.stdout) remain. The corrected suite
passed 112 tests; the final run is **112 passed in 3.30 s**, exit 0:
[stdout](pytest-final.stdout), [stderr](pytest-final.stderr). Counts are 21 harness,
17 existing IPPV adapter, and 74 unchanged independent reference tests.

Core CTest and the full sanitizer/numeric campaigns were not rerun for these
external-only changes. All 53 accepted M4 source hashes and four paper hashes
match. These finite checks are implementation evidence, not a mathematical proof.

## Frozen tiny diagnostic

[Configuration](tiny-config.json) was written before execution: three existing
h=3 fixture requests (two tied cliques with k=1; ordinary-bridge cliques with k=1;
clique plus isolate with k=2), two repeats, VF basic and IPPV, seed 20261003,
one algorithmic worker, 60 seconds per native/validator child, no imposed memory
cap, uncontrolled cache, IPPV t=10,p=0. This is local validation, not accepted
final experimental settings. Exact graph/binary hashes and order are in the
configuration and [saved schedule](shared-tiny/schedule.json).

[Twelve native runs](shared-tiny/summary.json) yield:

- VF: six definition-checked completions.
- IPPV: four definition-checked completions and two retained known zero-density
  omissions. The latter are native exit 0 with `semantic_mismatch`, not passes.
- Four eligible paired comparisons agree under tie-aware rules. The two bridged
  cases also agree strictly; the two tied cases preserve different valid cutoff
  choices. The two incomplete cases are marked not compared.
- Repeated semantic hashes are stable per algorithm/case. Timing/backend metadata
  are excluded from semantic hashes.

The tiny campaign exits **1** because known failed semantic checks are preserved.
No missing result is inserted, failed row filtered out, or structural check
relabelled a maximality proof. Each definition run uses the independent reference
with all-proper-superset maximality.

## Shared real smoke and stop

[Normalization](data/ca-grqc/normalization.json) uses the CA-GrQc file already bundled
with the authorized pinned IPPV source. Its explicit vertex universe is preserved:
5,242 vertices and 14,484 edges, zero removed loops/duplicates. Raw SHA-256 is
`729bc8ed7cd185cdbeb77709ad232ba94291acdacb78ae94f5445dad5988b616`; canonical hash is
`85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32`.
This identifies that bundled variant; it does not invent independent upstream
dataset/license verification.

[Real config](real-config.json) was frozen before execution: h=3,k=5, one repeat,
same two algorithms, seed/thread/timeout/cache/memory policy as above. This is a
single local shared-input smoke, not a final benchmark grid. All native candidate
verification in IPPV remains in its timed process. External validation follows
in another child with independent time/RSS.

| Algorithm | Outcome | Native wall seconds | Native peak RSS bytes | Validation |
|---|---|---:|---:|---|
| IPPV, five disclosed patches | exit 0; five sets | 0.1138044596 | 32,866,304 | structural checks pass; maximality/completeness not certified |
| VF basic, core off / sorted scan | timeout; native SIGKILL (-9) | 60.0063944999 | 7,094,272 | not run; no completed output |

Raw [IPPV manifest](shared-real/runs/0000-1/manifest.json) and
[VF manifest](shared-real/runs/0000-0/manifest.json) retain all records. VF consumed
59.538271 user CPU seconds and emitted no final status; no bottleneck attribution
is established. The timeout is censored, not a 60-second completed runtime, OOM,
wrong-answer example, or denominator for a speedup. [Comparison](shared-real/summary.json)
is explicitly unavailable. The real campaign exits **1**. No timeout was silently
raised, dataset dropped, feature enabled after results, or extra run substituted.

The next-step draft proposes testing all four already implemented M4 feature
combinations on this same input under the same guard. It changes no solver code
and would retain all outcomes. It has not run. The alternative is to settle final
experimental resource/scope decisions first. Formal expansion stops here until
the owner chooses; the independent development and IPPV repair decisions remain.

## Commands, machine and integrity

Actual command/exit/log hashes: [commands.json](commands.json), build command
manifests above, every child `process.json`, and normalization's recorded argv.
The successful build command and substantive run/test commands were:

```sh
.venv/bin/python experiments/build_vf.py --build build-m5-release --evidence evidence/m5/harness-20261003/build-vf-verified --cmake .venv/bin/cmake
.venv/bin/python experiments/prepare_input.py --source .deps/baselines/ippv/dataset/CA-GrQc.txt --evidence evidence/m5/harness-20261003/data/ca-grqc
.venv/bin/python -m pytest experiments/test_harness.py baselines/ippv/test_adapter.py reference/tests -q
.venv/bin/python experiments/run.py --config evidence/m5/harness-20261003/tiny-config.json --evidence evidence/m5/harness-20261003/shared-tiny
.venv/bin/python experiments/run.py --config evidence/m5/harness-20261003/real-config.json --evidence evidence/m5/harness-20261003/shared-real
.venv/bin/python scripts/verify_papers.py
git diff --check
```

The initial build used `build-vf` evidence, and pytest ran three times as described
above. No listed draft diagnostic or final benchmark command is counted as run.

Machine: Apple M1, eight physical/logical cores reported, 17,179,869,184 bytes RAM
(16 GiB), macOS 15.7.7 arm64. Compiler AppleClang 17.0.0.17000603; CMake 4.4.3;
Python 3.12.2; existing Boost 1.86.0. Original sandboxed sysctl reads failed and
are preserved in [system.json](system.json); the authorized read-only retry
succeeded in [hardware-retry.json](hardware-retry.json). The machine identifier
is hashed. This workstation's cache/load were uncontrolled. Hardware is recorded
at report scope and is not yet embedded in each run's manifest.

[Integrity assertions](verification.json) verify raw checksums, exact source
snapshots for both campaign versions, build/source/binary pins, repeated hashes,
paper hashes and all reported result counts. `git diff --check` exits 0.
Fourteen actual algorithm invocations are retained: eleven completed/validated,
two semantic mismatches and one timeout. There are thirteen separate validators;
the timed-out VF process was not validated. Fault-injection pytest children are
separate test executions, not baseline experiment rows.

## Unrun / incomplete

P11 remains partial: the shared real comparison is incomplete and final experiment
configuration is unapproved. Full resource metadata integration, resource-cap
support beyond explicit no-cap, performance aggregation, per-rank latency,
broader baseline correctness/numeric coverage, full comparative experiments and
clean-host release reproduction remain unfinished. No speedup, SOTA, theorem,
complete M5 gate or DCLDS result is claimed.
