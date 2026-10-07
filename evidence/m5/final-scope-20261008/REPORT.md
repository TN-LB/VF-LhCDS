# M5 scope preparation — 2026-10-08

**Planning/readiness evidence only; no final benchmark launched.** The
[completion plan](../../../docs/M5_COMPLETION_PLAN.md) closes development
optimization, records current progress and proposes one coordinated local batch.
M5 and its unfulfilled gates remain open.

## Prepared scope

- Existing GrQc/CondMat artifacts; VF at `0315c5d` production source and the
  seven-patch IPPV build; all input/executable/source pins are in [plan.json](plan.json).
- Main: h={3,4,5}, k={5,10,15,20}, five repeats, 240 native calls.
- Core off/safe at k=20: 60 calls. Fixed k=5/full-chain: 60 calls, with strict
  prefix comparison. Total 360, plus at most 360 external validators.
- Proposed serial one-worker, 60-second native/separate-validator guards,
  uncapped memory, uncontrolled cache and seed 20261003. Guard sums are 6 hours
  native plus at most 6 hours validation, not a runtime prediction or total deadline.
- All configs remain drafts. Full-mode/prefix and per-block observation support
  are missing from the current runner; this pack is not launch-ready.

## Executed checks

| Check | Actual result |
|---|---|
| `prepare.py` | Exit 0; two graph/binary pins, 40 production-source hashes, seven patches and four paper hashes match |
| Historical count campaign | 113 raw inventory entries match recorded hashes |
| Main/core drafts | Both reject launch; read-only copies pass existing schema and pin validation |
| Schedule | Reproducible seed; complete mode pairs; 240 + 60 + 60 calls |
| Existing harness pytest | **49 passed in 4.74s**, exit 0 |
| Native VF/IPPV measurements | **0** |

Commands actually executed:

```sh
.venv/bin/python evidence/m5/final-scope-20261008/prepare.py
.venv/bin/python -m pytest experiments/test_harness.py -q
```

[Preparation command/logs](prepare-command.json), [checks](checks.json),
[pytest command/logs](pytest-command.json), [environment observations](environment.json)
and [read-only metadata retry](hardware-retry.json) contain raw results.
Environment probe command arrays are recorded in those JSON files. The initial
sandbox denied four sysctl reads; the later read-only retry succeeded for all four.

Hardware: Apple M1, 16 GiB, eight logical CPUs; macOS 15.7.7 arm64, Python 3.12.2.
The retained VF provenance records AppleClang 17 Release. No compiler was rerun.
Snapshot: AC power, low-power mode off, load averages about 2.18/2.09/1.95 and
6,082.19 MiB allocated swap. A one-time swap allocation does not demonstrate
active paging or explain prior timing variance. Temperature/frequency unavailable;
no power settings or other applications changed.

## Changes and limits

Changed documentation: `M5_COMPLETION_PLAN`, `EXPERIMENT_PLAN`,
`IMPLEMENTATION_PLAN`, `DECISIONS`, `TASKS`, `CLAIM_TRACEABILITY`, and the current
M5 status report. Added this review pack and its one-time preparation script;
reused `experiments.run.load_config`/`schedule`. No production/reference/harness
symbols changed. Task scope: P11.2/P14.1 preparation; O12 evidence discipline.
Fixture manifest: two exact graph hashes in plan.json; proposed schedule seed
20261003. Harness tests use their existing deterministic/fault-injection fixtures.

No new theory conflict was identified by preparation; no new theory audit was
performed. Final scope/resources remain undecided. No solver build/CTest/sanitizer
rerun, final measurements/validators, full-mode harness implementation, final
aggregation, clean-machine reproduction, specialized baseline or DCLDS work ran.
The known IPPV zero-density gap remains. No performance/theorem conclusion or
new M5 completion checkbox follows from these checks.
