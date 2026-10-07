# Final local evaluation — 2026-10-08

Status: **ready for the frozen 360-call batch; measurements not yet started**.
Main/core/stop configs preserve the reviewed graph/binary pins and deterministic
schedules: 240 + 60 + 60 calls, five repeats, seed 20261003, 60-second native and
separate-validator guards, one worker, serial calls, uncapped memory, uncontrolled
cache. There are no warmups, adaptive repeats or retries.

Readiness: the final Python checks pass **164 tests in 6.53s**. Six native VF
calls on three named fixture/settings pass six independent definition validators;
all three fixed/full pairs match strictly at the required prefix. They cover
cutoff, exhaustion and zero-density h>n behavior. [Fixtures/results](readiness/completion.json),
[final tests and source hashes](readiness/final-tests.json).

Changed symbols: `experiments.run.validate_comparison`/`run_vf`/`execute`,
`experiments.validate.validate`/`compare_prefix`/`main`, and read-only
`experiments.environment.snapshot`/`power_state`/`power_change`. Production,
reference and IPPV executable sources/binaries are unchanged. No C++ build,
CTest or sanitizer campaign is rerun for these external-harness changes.

The runner records full output explicitly, enforces identical fixed/full modes,
compares exact prefixes, observes load/VM/swap/power outside native time and
retains stopped/unrun ledgers for power changes and interruption. Tests cover
ties, exhausted output, missing zero-density tails, native/external timing scope,
wrong comparison configurations, timeout retention and interruption/power stops.

Commands executed:

```sh
.venv/bin/python -m pytest experiments/test_harness.py -q
.venv/bin/python evidence/m5/final-evaluation-20261008/prepare.py
.venv/bin/python -m pytest experiments/test_harness.py reference/tests baselines/ippv/test_adapter.py -q
```

The first run passes 70 tests; preparation passes 161 plus the six tiny calls;
the final run adds interruption cases and passes 164. Exact command arrays and
stdout/stderr are saved in `readiness/pytest`, `readiness/driver`, and
`readiness/final-pytest`. Tiny runner source pins are in its campaign environment;
the final tests pin the updated source. Environment: Python 3.12.2 on the current
macOS arm64 host; actual measurement hardware/power conditions will be rechecked
by `run_batch.py` before launch.

Task scope: P11.1/P11.2/P12.1 preparation, O09/O12 interface/evidence discipline.
Finite checks do not prove mathematical correctness. Real-graph outputs will
receive structural checks/agreement, not definition completeness certification.
The original drafts and previous timings remain unchanged and separate. M5
remains open for actual execution, conclusions and release reproduction.
