# M5 bounded four-mode diagnostic — 2026-10-03

The owner approved the previously prepared four-mode diagnostic with "好的".
All four native invocations ran once on the same input and existing executable;
all timed out at the predeclared 60-second guard. P11.2/P11.3 have additional
diagnostic evidence, but neither task nor M5 is complete. There is no completed
output comparison, speedup conclusion or new mathematical correctness claim.

## Authorization and frozen configuration

[Authorization](authorization.json) links the unchanged prior draft and records
its checksum. The new [configuration](config.json) changes only `name` and
`scope`; the historical draft and previous failure evidence remain unchanged.
The diagnostic uses one worker, one repetition per mode, seed 20261003, no
imposed memory cap and uncontrolled cache. The 60-second guard applies to each
native process and any subsequent external validator, as in the approved draft.
No final experiment resource/dataset policy is approved by this local run.

Fixture: normalized CA-GrQc, 5,242 declared vertices, 14,484 edges, h=3, k=5.
The exact normalized graph SHA-256 is
`85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32`.
Its existing [normalization manifest](../harness-20261003/data/ca-grqc/normalization.json)
is reused; no new dataset was acquired or selected.

The prewritten [schedule](campaign/schedule.json) is core-only, both,
membership-only, basic. All modes use `build-m5-release/vflhcds`, SHA-256
`4858481c0f86dcdb942149e0fb137c20a5d3fa12a01ffa4d2e4d2c62be8227e0`.
The binary was not rebuilt. Its [provenance](vflhcds.provenance.json) records
M4 HEAD `56229397903813d3509ecb45b178bbde823e357b`, Apple Clang 17.0.0.17000603,
C++17 Release, strict warnings and sanitizers off. This is the existing dirty
M5 working tree, not a new committed release.

## Executed commands and outcomes

From the repository root:

```sh
.venv/bin/python experiments/run.py --config evidence/m5/m4-mode-diagnostic-20261003/config.json --evidence evidence/m5/m4-mode-diagnostic-20261003/campaign
.venv/bin/python evidence/m5/m4-mode-diagnostic-20261003/verify_evidence.py
git diff --check
```

The [runner command record](command.json) reports exit **1**, total driver wall
time **240.30401662457734 s**. That exit preserves unsuccessful runs; it is not a
driver exception. [Driver stderr](driver.stderr) is empty. Each native command,
working directory, UTC start/end, actual exit/signal and wait4 resources are in
the corresponding `process.json` below.

| Execution order / mode | Core / footprint | Result | Observed wall seconds | Peak RSS bytes | Run evidence |
|---|---|---|---:|---:|---|
| 1. Core only | safe / sorted | timeout | 60.005234 | 7,340,032 | [manifest](campaign/runs/0000-1/manifest.json) |
| 2. Both | safe / membership | timeout | 60.006619 | 5,996,544 | [manifest](campaign/runs/0000-3/manifest.json) |
| 3. Membership only | off / membership | timeout | 60.002428 | 6,602,752 | [manifest](campaign/runs/0000-2/manifest.json) |
| 4. Basic | off / sorted | timeout | 60.006234 | 5,259,264 | [manifest](campaign/runs/0000-0/manifest.json) |

All four processes were killed by the declared timeout guard (native exit -9,
SIGKILL), not classified as OOM. All stdout/stderr files are zero bytes. There
are no completed semantic hashes, phase timings or counters. External validation
did not run. All six pairs are explicitly `not_compared` in the
[summary](campaign/summary.json). Observed wall times and peak RSS are measurements
of truncated runs, not completed runtimes or full-run memory requirements. The
results neither rank the modes nor invalidate earlier small-corpus equivalence.

The integrity verifier exits **0**; its [result](verification.json) checks exact
configuration changes, seeded order, all four outcomes, all six comparison
records, input/executable pins, raw inventory and checksums, runner/adapter source
snapshots, the 53 accepted M4 source hashes and four paper hashes. `git diff
--check` also exits **0**. These are evidence-integrity checks, not algorithm
correctness tests or a mathematical proof.

## New static observation and current stop

Read-only inspection of `MaterializedCliques::MaterializedCliques` found that it
visits every size-h vertex subset. On this input, a full h=3 index construction
visits C(5242,3) = **23,993,367,880** candidate triples, checking adjacency for
each candidate until accepted or rejected. `run_cli` constructs this index
before the two M4 switches can affect oracle execution. The exact source hashes
and calculation are recorded in [static-observation.json](static-observation.json).

This identifies a priority hypothesis, not a measured bottleneck. The timed-out
processes emitted no phase boundary, so their stopping phase is still unknown.
The recommended [next step](NEXT_STEP.md) is a separate bounded phase diagnostic
on the same graph and 60-second guard, before changing enumeration or increasing
the runtime budget. It has not been run. Expansion stops under the owner's
instruction to stop at blockers/decisions; the four-run authorization is fully
executed. No proof/specification conflict or counterexample has been produced.

## Environment, files and remaining work

Current platform/Python/environment are recorded in [environment.json](environment.json)
and [campaign/environment.json](campaign/environment.json): macOS 15.7.7 arm64,
Python 3.12.2. The same-host hardware metadata already obtained earlier on
2026-10-03 is preserved in [hardware-retry.json](hardware-retry.json): Apple M1,
8 physical/logical cores, 17,179,869,184 bytes RAM. Hardware was not queried again.

No production, reference, baseline, harness or build symbol changed. Existing
`experiments.run.load_config,schedule,run_vf,execute` and `process.capture` were
executed. The only new executable code is this evidence's `verify_evidence.main`.
Changes comprise this evidence directory and evidence-only notes in
`docs/TASKS.md`, `docs/CLAIM_TRACEABILITY.md`, and `evidence/m5/REPORT.md`.
[The file manifest](files_changed.json) lists these turn-specific paths and hashes;
it does not relabel the larger preexisting M5 working tree as new work.

No CMake build, CTest, pytest suite, sanitizer suite, IPPV rerun, DCLDS work,
phase-timing probe, enumeration repair, full benchmark, enlarged timeout or
clean-host release reproduction was run this turn. Earlier 112-test success is
historical evidence, not a new test run. D029/D012 and accepted mathematical
contracts remain unchanged. P11.1-P11.3/O12 statuses are not promoted by these
four censored diagnostic observations.
