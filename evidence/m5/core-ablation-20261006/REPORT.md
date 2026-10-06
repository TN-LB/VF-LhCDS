# VF core off/on ablation — 2026-10-06

**48/48 calls recorded:** {'completed': 30, 'timeout': 18}; 30 separate structural validators pass. 15 complete pairs have identical canonical outputs; 9 blocks cannot be compared. Unrun: 0. Driver exit: 1.

The same VF Release binary uses adjacency enumeration and membership footprint scanning; only core off/safe changes. CA-GrQc (5,242 vertices, 14,484 edges) and CA-CondMat (23,133 vertices, 93,439 edges), h=3, k={5,10,15,20}, three repeats, seed 20261003. Apple M1/16 GiB, macOS 15.7.7, AppleClang 17, Python 3.12.2; serial one-worker execution, randomized order within blocks, 60-second native/separate-validator guards, no memory cap, uncontrolled cache, no warm-ups/retries. IPPV is not rerun.

| Graph | k | Core off: median s / status | Core safe: median s / status | Safe / off time | Strict pairs |
|---|---:|---:|---:|---:|---:|
| ca-grqc | 5 | 0.316864 | 0.313924 | 0.991 | 3/3 |
| ca-grqc | 10 | 0.887300 | 0.890939 | 1.004 | 3/3 |
| ca-grqc | 15 | 1.684735 | 1.689759 | 1.003 | 3/3 |
| ca-grqc | 20 | 2.686251 | 2.690686 | 1.002 | 3/3 |
| ca-condmat | 5 | 38.475664 | 39.717360 | 1.032 | 3/3 |
| ca-condmat | 10 | 3 timeout | 3 timeout | unavailable | 0/3 |
| ca-condmat | 15 | 3 timeout | 3 timeout | unavailable | 0/3 |
| ca-condmat | 20 | 3 timeout | 3 timeout | unavailable | 0/3 |

Across 5 completed paired settings, safe-core median wall changes range from -0.93% to +3.23%; peak-RSS median changes range from -11.91% to -4.18%. [Exact ratios](performance-summary.json).

Ratios above 1 mean core safe is slower. Small differences in these three-repeat samples are not evidence of a stable general speedup. Medians require all three scheduled runs to complete; ratios additionally require all three strict pairs. Timeouts remain censored. [All raw times/ranges/RSS](aggregate/TABLE.md). Native time includes core computation and all solver work; external validation is separate. Historical timings are not pooled.

| Completed case | Queries | Sum of oracle sizes: off → safe | Sum of network nodes: off → safe | Median core time s |
|---|---:|---:|---:|---:|
| ca-grqc-h3-k5 | 13 | 6529 → 1719 | 200807 → 186274 | 0.003043 |
| ca-grqc-h3-k10 | 72 | 7807 → 2933 | 227835 → 212905 | 0.015330 |
| ca-grqc-h3-k15 | 112 | 15930 → 7524 | 254918 → 233876 | 0.023416 |
| ca-grqc-h3-k20 | 154 | 17796 → 9376 | 263059 → 241982 | 0.030589 |
| ca-condmat-h3-k5 | 304 | 48622 → 31870 | 794541 → 715040 | 0.969507 |

Core time is already inside solve/native time. Summed query sizes are workload counters, not peak live memory; network shrinkage alone does not establish a runtime benefit or an O(k) bound. Internal counting/footprint/network-build/flow times are not individually measured. Completed pairs retain identical footprint scan visits: the materialized backend still scans all stored cliques per query, and core does not change the separate endpoint-counting path. This limits what network shrinkage alone can explain. [Per-run telemetry](aggregate/telemetry.json) and [paired counter checks](core-pair-details.json).

Completed outputs have stable hashes in 10 cells. All 24 completed CA-GrQc outputs also match the prior membership campaign. The earlier CA-CondMat timeout campaign and single-run completions remain separate; changing wall time across campaigns cannot be attributed to core without this paired control.

Only the external runner/test interface changes: `execute(require_strict_agreement=True)` enforces identical cutoff selection for equivalent modes. **137 pytest checks pass**. The saved-evidence verifier passes and all seven aggregates regenerate identically. Production code/binary, papers, reference and historical evidence remain unchanged.

Evidence: [config](config.json), [pins](preflight.json), [schedule](schedule.json), [environment](environment.json), [commands](commands.json), [raw campaign](campaign/summary.json), [verification](verification.json), [regeneration](regeneration.json), [changed files](files_changed.json).

P12.1/O10/O12 gain local core-ablation evidence; P14.1/P15.1 gain scoped review/regeneration evidence. M5 remains open. Unrun: wider h/grid experiments, new phase instrumentation/optimization, fresh IPPV comparison, C++ rebuild/CTest/sanitizers, clean-machine release and DCLDS work. Structural checks and mode agreement do not prove real-graph maximality or the theorem.
