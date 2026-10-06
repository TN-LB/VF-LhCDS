# Membership / IPPV repeated pilot — 2026-10-06

Recorded **48/48 native calls**: {'completed': 36, 'timeout': 12}. 36 separate structural validators pass; 0 calls remain unrun. Completed pairs: 12 tie-aware matches, 6 strict matches, 0 substantive disagreements. 12 blocks have no complete comparison.

Scope: CA-GrQc (5,242 vertices / 14,484 edges) and CA-CondMat (23,133 / 93,439), h=3, k={5,10,15,20}, three repetitions, seed 20261003. VF uses adjacency/membership/core-off; IPPV uses seven patches, iterations=10,p=0. Apple M1, 16 GiB, macOS 15.7.7, AppleClang 17 Release, Python 3.12.2; one worker, serial seeded order, 60-second native and separate validator guards, uncapped memory, uncontrolled cache, no warm-ups or retries.

| Graph | k | VF median seconds / outcome | IPPV median seconds / outcome | Tie-aware pairs |
|---|---:|---:|---:|---:|
| ca-grqc | 5 | 0.516958 (3/3 complete) | 0.178408 (3/3 complete) | 3/3 |
| ca-grqc | 10 | 1.449934 (3/3 complete) | 0.199315 (3/3 complete) | 3/3 |
| ca-grqc | 15 | 2.809717 (3/3 complete) | 0.254034 (3/3 complete) | 3/3 |
| ca-grqc | 20 | 4.404297 (3/3 complete) | 0.280171 (3/3 complete) | 3/3 |
| ca-condmat | 5 | 3 timeout | 4.219049 (3/3 complete) | 0/3 |
| ca-condmat | 10 | 3 timeout | 7.222165 (3/3 complete) | 0/3 |
| ca-condmat | 15 | 3 timeout | 8.484404 (3/3 complete) | 0/3 |
| ca-condmat | 20 | 3 timeout | 8.618505 (3/3 complete) | 0/3 |

Medians use all three scheduled successful runs of one algorithm/case. Timeouts are censored, never substituted as completion times. IPPV timings beside VF timeouts do not imply output agreement. Native timing includes each program’s own work, including IPPV candidate verification; separate external validation is excluded. [All raw timings, ranges and RSS](aggregate/TABLE.md).

All 12 cells with completed outputs have stable semantic hashes. The 24 completed CA-GrQc outputs also exactly match the earlier repaired-baseline campaign; historical timings are kept separate. CA-CondMat’s earlier single k=5 VF completion in 38.525397500 seconds is not a guarantee of repeat completion under 60 seconds. This campaign does not isolate the cause of timing variation.

Changes: `experiments.run.execute` adds explicit timeout continuation while retaining stops for other failures and substantive disagreement. Ten new control-path tests plus the existing suite pass: **133 passed**. Algorithm sources, binaries, four papers, independent reference and historical evidence remain unchanged. Saved-evidence verification passes; aggregation regenerates 7 identical artifacts without solver reruns. Driver exit: 1 (non-success outcomes remain visible).

Evidence: [config](config.json), [schedule](schedule.json), [source/data pins](preflight.json), [environment](environment.json), [native launch](launch.json), [completion](completion.json), [pytest command/result](pytest-command.json), [check commands](postprocess-commands.json), [verification](verification.json), [regeneration](regeneration.json), [changed files](files_changed.json). Raw logs/manifests are under `campaign/runs/`.

P11.1/P11.2/P12.1/O12 gain scoped evidence; P14.1/P15.1 gain local review and table-regeneration evidence only. M5 remains open: no broader h/grid campaign, controlled ablations, clean-machine smoke, release package or DCLDS work. C++ builds/CTest/sanitizers were not rerun. Structural checks and cross-implementation agreement do not establish real-graph maximality or prove the theorem; IPPV’s known zero-density omission remains.
