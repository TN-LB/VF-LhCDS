# CA-CondMat membership diagnostic — 2026-10-06

**Completed within 60 seconds: five outputs, structural validation passed.**
The existing M4 membership footprint mode was used with adjacency enumeration,
core off and automatic exact capacities. Production code and defaults are unchanged.

| Measurement | Result |
|---|---:|
| Native process wall time | 38.997086249 s |
| Solver after indexing | 38.875202292 s |
| Native peak RSS | 158580736 bytes |
| Queries / mincuts | 304 / 304 |
| Materialized triangles / footprint visits | 173361 / 52701744 |
| Separate validation | Passed, exit 0, 0.406393332 s |

Input: CA-CondMat, 23,133 vertices / 93,439 edges; h=3,k=5. One run, one worker,
60-second native/validator limits, no memory cap, uncontrolled cache, seed 20261003.
[Config](config.json) pins input and executable hashes. Environment: Apple M1,
16 GiB, macOS 15.7.7 arm64, Python 3.12.2; existing AppleClang 17 Release build.
A host-label mismatch stopped the initial preflight before any native call;
fresh hardware/profile checks matched the prior settings. Both attempts are saved.

The native process, external validator and driver exit 0. Exact counts, density,
connectivity, ordering and completion metadata pass. The first 137 query-counter
records match the prior sorted-mode trace. This is one diagnostic measurement;
full off/on output agreement, real-graph maximality and a stable speedup are not
established. The historical basic timeout remains recorded separately.

[Raw results](campaign/runs/0000-0/manifest.json), [output](campaign/runs/0000-0/canonical_output.jsonl),
[verification](verification.json), [environment](environment.json) and
[actual commands/exit codes](commands.json) retain the evidence. The run command was:

```sh
.venv/bin/python experiments/run.py --config evidence/m5/condmat-membership-20261006/config.json --evidence evidence/m5/condmat-membership-20261006/campaign --stop-on-failure
```

P11.2/P12.1/O12 gain this completed-case evidence; M5 remains open. Added diagnostic
config, execution/verification scripts and logs; updated decisions, tasks,
traceability and experiment summaries. No production symbol changed. The saved
evidence verifier and diff check pass; no build, CTest, pytest or sanitizer rerun.
[File inventory](files_changed.json) distinguishes these edits from prior work.

Next: [one fresh VF/IPPV pair](next-pair-draft.json) on this same case, one run per
algorithm, same 60-second limits and existing pinned binaries. It remains a draft.
The 23 pending historical pilot calls, repeated comparisons and broader experiments
are unrun; the completion limit is resolved only for the observed mode/case.
