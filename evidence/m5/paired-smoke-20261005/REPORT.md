# M5 fresh paired smoke and campaign preparation — 2026-10-05

The same-settings shared smoke now completes for both pinned algorithms and
passes strict output comparison. **P11.3 is complete in this scoped smoke sense;
M5 is not complete.** The next repeated campaign is prepared as a draft and has
not run. Work stops before the new experiment-scope/resource decision.

The owner authorized continuation after the adjacency-enumeration repair. This
turn repeats the existing real smoke configuration and prepares the next step;
it does not treat that continuation as approval of a new benchmark grid. D029
continues to defer DCLDS. No paper, theory contract or production solver changes.

## Actual paired outcome

One block, CA-GrQc h=3,k=5, seed 20261003, one repetition, one algorithmic worker,
serial execution, 60-second native guard, no imposed memory cap, uncontrolled
cache. Seeded order was IPPV then VF. Both were launched afresh; this comparison
does not combine a new VF run with historical IPPV output.

| Algorithm | Native exit | Native wall seconds | Native peak RSS bytes | External validation seconds | Outputs |
|---|---:|---:|---:|---:|---:|
| IPPV, five patches, iterations=10/p=0 | 0 | 0.17649641539901495 | 31,948,800 | 0.15163874998688698 | 5 |
| VF adjacency/basic, core off, sorted footprints | 0 | 1.2028633328154683 | 46,071,808 | 0.1581342499703169 | 5 |

Both external validators also exited zero. Both outputs are structural-checked;
canonical output files are byte-identical, and strict/tie-aware comparison passes.
Their shared semantic hash is
`c33ccb405e263ae7fcf10f60585c8441dbc821bbc1f7958ba4dd828ac0cf797f`.
Completeness/maximality on this real graph is **not certified**. One pair does not
establish performance stability, a speedup, general-h superiority or a theorem.
These raw times are reported including the unfavorable VF result in this pair.

Native process time includes each algorithm's I/O, enumeration, native candidate
verification where present, and serialization. External validation starts later
and is separately recorded. No baseline-native verification time is subtracted.

## Current code change and tests

`experiments.run.execute(..., stop_on_failure=False)` and the CLI's optional
`--stop-on-failure` implement the owner's stop-at-blocker workflow. The runner
freezes `execution-policy.json` before launch. With the flag, the first recorded
unsuccessful run stops further calls; a tie-aware disagreement stops after that
comparison block. `stopped.json` preserves the cause and the complete pending
schedule. All recorded raw outputs/failures remain checksummed. Different valid
cutoff ties alone do not stop execution. The default run-all policy is retained.
Invalid configuration or changed input/binary pins raise before the affected
launch; the failure ledger does not claim to cover rejected preflight requests.
There is no automatic retry or resume.

`experiments/test_harness.py` adds eight tests: five injected failure statuses
(timeout, error, OOM, semantic mismatch and driver exception), run-all behavior,
pair disagreement, and valid cutoff-tie continuation. These are deterministic
runner-control tests, not actual OOM/numerical stress or new mathematical checks.
The final tie fixture has two disjoint triangles at h=2,k=1; either component is
an eligible tied result. Each stopped fixture retains all five/four unrun entries
of its six-entry schedule and verifies the saved inventory.

The combined harness/adapter/independent-reference suite ran twice:

- Initial run: **123 passed in 4.95 s**, exit 0; driver wall 5.363310583867133 s.
- Final run after strengthening the valid-tie fixture: **123 passed in 4.54 s**,
  exit 0; driver wall 4.869613625109196 s. This is the delivered source version.

Final breakdown is 32 harness + 17 adapter + 74 unchanged reference tests.
No production build, CTest, ASan/UBSan, or broad differential campaign is rerun
this turn: the production sources/binaries are unchanged, and their previously
executed gates are in [the enumeration report](../enumeration-20261003/REPORT.md).

The paired smoke preceded the external stop-control edit. Its exact Python files
are preserved in `source-before/`; the delivered tested Python files are saved
in `stop-control-final-tests/source/`. The new flag is exercised by tests, not
retrospectively claimed as part of the earlier smoke invocation.

## Prepared next step, not executed

CA-CondMat normalization retains all 23,133 declared vertices and 93,439 edges;
no loops or duplicate edges are removed. Raw SHA-256 is
`0521b9a50d7606a8990a3621a2a6a2a908b3473ca50507b287b2e6cc2e46717d`;
normalized SHA-256 is
`5e48ff6e02d4015364788f606f59adb4dafcc4dbdc92ce33a209a4eeb50c8adb`.
CA-GrQc reuses the existing common normalized artifact, preserving its 5,242
vertices, 14,484 edges and hash recorded in the config.

The [reviewable proposal](../campaign-proposal-20261005/PROPOSAL.md) recommends
these two locally available inputs, h=3, k={5,10,15,20}, three repetitions, both
algorithms, and the same one-worker/60-second/no-cap/uncontrolled-cache policy.
There are 48 planned native calls. It records the alternatives, consequences,
binary/input/source pins, exact schedule and stop policy. Its scope is `draft`,
and the loader rejects it for execution. Read-only schema/pin validation succeeds;
no algorithm is launched by that validation. No final setting or owner approval
is invented. P11.1/P11.2/P12.1 remain open.

## Commands actually executed

Working directory: `/Users/nost/Documents/VF-LhCDS`.

```sh
.venv/bin/python experiments/run.py --config evidence/m5/paired-smoke-20261005/config.json --evidence evidence/m5/paired-smoke-20261005/campaign
.venv/bin/python -m pytest experiments/test_harness.py baselines/ippv/test_adapter.py reference/tests -q
.venv/bin/python experiments/prepare_input.py --source .deps/baselines/ippv/dataset/CA-CondMat.txt --evidence evidence/m5/campaign-proposal-20261005/data/ca-condmat
.venv/bin/python evidence/m5/paired-smoke-20261005/verify.py
```

The pytest command ran twice as above; all listed commands exited zero. The
paired driver took 2.118570332415402 s; input preparation took
0.5780733749270439 s. Exact child commands, arguments and exits are in each
`process.json`. Read-only environment/source inspection included git status/HEAD,
file hashes and `sysctl -n` hardware queries. Initial sandbox hardware reads
failed with exit 1/Operation not permitted; an approved read-only retry succeeded
with exit 0. Both attempts are preserved; no auto-review rejection occurred.

## Environment and preserved boundaries

macOS 15.7.7 arm64, Apple M1, 8 physical/logical CPUs, 16 GiB RAM; Python 3.12.2.
The existing VF Release build records AppleClang 17.0.0.17000603 and C++17.
Root HEAD remains `56229397903813d3509ecb45b178bbde823e357b` with the disclosed
uncommitted M5 work. This turn creates no commit or new build. IPPV remains pinned
at `f61881d4752170c03585e4281f0c49d7ef14aa1e` plus its same five disclosed patches;
the historical `build-ippv-original` directory name does not mean unpatched code.

The verification script checks 25 campaign inventory entries, all 40 production
build-source hashes, 17 patched IPPV-source hashes, 23 independent-reference
files, all four paper hashes, both binary/provenance pins, the seven pre-edit
runner snapshot files, and all 27 tested Python source files. Exactly two of the
57 source files in the preflight enumeration snapshot now differ: the external
runner and its tests. The baseline lock is unchanged. No new proof/specification
conflict is observed; finite agreement remains implementation evidence only.

## Files and evidence

Changed this turn: `experiments/run.py` (`execute`, CLI),
`experiments/test_harness.py` (fixture plus stop/tie/failure tests),
`experiments/README.md`, `docs/TASKS.md`, `docs/CLAIM_TRACEABILITY.md`, and
`evidence/m5/REPORT.md`. New evidence lives under this directory and
`evidence/m5/campaign-proposal-20261005/`. [File inventory](files_changed.json)
separates these changes from the earlier uncommitted production work.

- [Config](config.json), [preflight](preflight.json), [environment](environment.json),
  [hardware retry](hardware-retry.json), [driver command](command.json).
- [Native/validation manifests and outputs](campaign/summary.json),
  [immutable campaign inventory](campaign/checksums.json).
- [Final test command](stop-control-final-tests/command.json),
  [final test output](stop-control-final-tests/stdout.txt),
  [tested source hashes](stop-control-final-tests/source_sha256.json).
- [Integrity and scope verification](verification.json), reproducible with `verify.py`.
- [Draft plan and decision alternatives](../campaign-proposal-20261005/PROPOSAL.md).

Remaining decision: approve/change the concrete repeated pilot's scope and
resource policy before it runs, as required by AGENTS.md and the owner's stop
instruction. Existing IPPV zero-density omission and broader numeric/semantic
coverage remain limitations. New repeated measurements, aggregation/plots,
additional h strata/datasets, feature ablations, full resource-profile integration,
rank latency, clean-host release reproduction and DCLDS work are unrun. M5 is
incomplete; no performance or mathematical conclusion is manufactured to close it.
