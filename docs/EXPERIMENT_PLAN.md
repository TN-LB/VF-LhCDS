# Experimental Evaluation Plan

## 1. Research questions

### RQ1 — Exactness

Does VF-LhCDS return the same exact top-k LhCDSes as the definition-level reference on tiny graphs and as other exact algorithms on shared feasible instances?

### RQ2 — Overall efficiency

How do runtime, peak memory, and time-to-first/top-k result compare with applicable exact baselines for each value of `h`?

### RQ3 — Where is time spent?

How much cost comes from clique enumeration, footprint aggregation, network construction, max flow, recursion, core reduction, and output extraction?

### RQ4 — Which optimizations matter?

What are the individual and combined effects of clique indexing, h-clique-core reduction, footprint aggregation/reduction, caching, flow backend, and early stopping?

### RQ5 — Scalability and sensitivity

How does performance change with graph size, clique count, `h`, `k`, graph density, number of principal-chain layers, and number of unique residual footprints?

## 2. Algorithm comparison matrix

| Algorithm | Exact | Verification-free | Supported comparison | Intended role |
|---|---:|---:|---|---|
| VF-LhCDS | yes | yes | `h>=2` | proposed method |
| IPPV | yes | no | general `h` | primary direct published baseline |
| LDS-Opt | yes | yes | `h=2` | hierarchy-based specialization |
| LDScvx | yes | no | `h=2` | convex-programming LDS baseline |
| LDSflow | yes | no | `h=2` | classical flow baseline |
| LTDScvx | yes | no | `h=3` | convex-programming triangle baseline |
| LTDSflow | yes | no | `h=3` | classical triangle-flow baseline |
| Greedy/KClist++ variant | no | not applicable | quality/runtime only | heuristic reference, never exact SOTA |
| DCLDS public repository | to audit | claims D&C | appears general | provenance and overlap must be resolved |

Do not aggregate speedups across incomparable `h` values or across exact and heuristic methods without separate labels.

## 3. Dataset program

### Tier A — correctness and diagnostics

- hand-built toy graphs;
- all nonisomorphic graphs up to a feasible small `n`, if tooling permits;
- seeded synthetic families from `CORRECTNESS_TEST_PLAN.md`.

Purpose: exact validation, tie behavior, oracle traces, failure minimization.

### Tier B — IPPV-overlap benchmark set

Use the same normalized versions of the 15 public graphs listed by IPPV where available:

- soc-hamsterster;
- CA-GrQc;
- fb-pages-politician;
- fb-pages-company;
- web-webbase-2001;
- CA-CondMat;
- soc-epinions;
- Email-Enron;
- loc-gowalla;
- DBLP;
- Amazon;
- soc-youtube;
- soc-lastfm;
- soc-flixster;
- soc-wiki-talk.

This tier is the main general-`h` comparison because IPPV reports `h=3,4,5` on overlapping datasets.

### Tier C — larger h=2/h=3 specialization set

For comparisons with LDScvx/LTDScvx, use the public subset of their 13 datasets that can be obtained and normalized unambiguously. Private datasets are excluded unless legally available.

Purpose: test whether VF-LhCDS remains competitive against highly optimized special-case methods on large edge/triangle instances.

### Tier D — controlled scalability

Generate induced or edge-sampled graphs at fixed fractions, but keep the sampling procedure and seed identical across algorithms. Also include synthetic planted structures that vary:

- `n` and `m`;
- total h-cliques;
- degeneracy;
- number of dense regions;
- number of equal-density regions;
- boundary-clique intensity.

## 4. Parameters

### h values

- main: `h in {2,3,4,5}`;
- optional larger `h` only on datasets whose clique count is tractable and with explicit selection criteria.

### k values

Use a preregistered grid such as:

```text
k in {1, 5, 10, 20, 50, 100, all}
```

For datasets with fewer than `k` LhCDSes, record the actual output count and completion status. Do not treat early exhaustion as a failure.

For reproduction of IPPV plots, also support its reported grid `k in {5,10,15,20}`.

### Threads

Default fairness experiment: one algorithmic worker thread. If a baseline is inherently parallel, report that separately and add a matched-thread experiment when possible.

### Timeout

Set timeout before running the main suite. Suggested protocol:

- short smoke timeout for CI and command validation;
- fixed final timeout up to the scale used by the target baseline paper when resources permit;
- record timeout as censored, not as the timeout value pretending to be a completed runtime.

## 5. Canonical preprocessing

Create one normalized binary/text graph artifact per dataset and feed the same artifact to every wrapper.

Normalization:

1. parse original IDs;
2. treat edges as undirected;
3. remove self-loops;
4. collapse parallel/reversed duplicates;
5. remove or preserve isolated vertices according to a documented project decision;
6. remap to contiguous 0-based IDs;
7. sort canonical edges;
8. compute checksum and statistics.

Every run manifest includes the normalized dataset checksum. Baseline-specific conversion must be lossless and separately checksummed.

## 6. Output equivalence and tie handling

Exact algorithms may use different tie conventions. Compare outputs with two validators:

### Strict validator

Used when both algorithms implement the same deterministic subset order. Requires identical ranked sets.

### Tie-aware validator

For a requested `k`:

- all outputs with density strictly greater than the kth density must match;
- every returned set must be a valid LhCDS with the reported density;
- differences among valid sets tied at the kth density are allowed if the baseline does not expose a compatible total order;
- the count and tie policy are recorded.

Never call two outputs inconsistent solely because they select different members of the kth-density tie layer.

## 7. Metrics

### Primary

- end-to-end wall-clock time;
- solver-only wall-clock time after input loading;
- peak resident set size;
- completed/timeout/OOM/error status;
- latency to ranks 1, 5, 10, 20, and final `k`.

### Proposed-solver internal

- h-clique enumeration/index time and memory;
- total h-cliques;
- oracle call count;
- terminal/internal interval count;
- maximum recursion depth;
- cliques scanned per oracle;
- unique residual footprints per oracle;
- closure nodes and arcs;
- network-build time;
- max-flow time;
- h-clique-core time and vertices/cliques removed;
- cache hits/misses;
- result validation time.

### Output integrity

- output count;
- each exact density;
- each vertex-set hash;
- combined ordered-output hash.

## 8. Run protocol

1. Pin code and baseline commits.
2. Build all algorithms with documented compilers and release flags.
3. Validate every wrapper on toy instances.
4. Randomize algorithm run order within each `(dataset,h,k,repeat)` block.
5. Run at least three measured repetitions for feasible cases; use more when variance is high.
6. Record one immutable manifest and full stdout/stderr per run.
7. Use `/usr/bin/time -v` or an equivalent wrapper for wall time and peak RSS.
8. Do not reuse a partially written result after timeout.
9. Validate output before accepting the run as successful.
10. Aggregate from manifests, never from manually transcribed numbers.

State whether filesystem cache is warm or uncontrolled. Randomized run order reduces systematic cache bias.

## 9. Statistical reporting

For completed repeated runs, report:

- median;
- interquartile range or min/max when repeats are few;
- geometric-mean speedup over common completed instances;
- number of wins, ties, losses;
- timeout/OOM counts.

For censored cases, use explicit timeout markers and performance profiles rather than substituting timeout values into ordinary means.

Do not report only the best run.

## 10. Main tables and figures

### Table A — correctness agreement

Per algorithm and comparison stratum: cases checked, strict matches, tie-aware matches, mismatches, timeouts.

### Table B — dataset characteristics

`n`, `m`, degeneracy, h-clique counts for each tested `h`, normalized checksum.

### Figure 1 — runtime by dataset

Separate panels for `h=2`, `h=3`, and `h in {4,5}`.

### Figure 2 — runtime versus k

Use representative sparse, dense, low-clique, and high-clique datasets.

### Figure 3 — peak memory

Show both absolute memory and memory normalized by h-clique count where informative.

### Figure 4 — time breakdown

Enumeration, footprint, flow build, max flow, other.

### Figure 5 — oracle/network structure

Runtime versus number of scanned cliques and unique footprints; show whether footprint aggregation is effective.

### Figure 6 — scalability

Runtime/memory versus graph fraction and clique count.

### Figure 7 — cactus or performance profile

Include timeouts fairly across the full benchmark set.

## 11. Ablation matrix

Use named configurations:

- `B0`: simplest exact solver, streaming or uncached reference production mode;
- `B1`: materialized clique index;
- `B2`: aggregated residual footprints;
- `B3`: safe h-clique-core reduction;
- `B4`: `mu_h` and oracle caching;
- `B5`: safe closure-network reductions;
- `B6`: alternative exact flow backend;
- `B7`: full optimized solver;
- `B8`: full-chain enumeration versus top-k early stop.

Each ablation reports both output hash equality and performance. A faster but semantically different configuration is not an optimization; it is a different algorithm and must be labeled accordingly.

## 12. Claim discipline

Allowed claims must match evidence:

- “Exact” only after definition-level differential validation and proof traceability.
- “Verification-free” refers to the algorithmic structure, not the absence of all internal assertions or output validation.
- “Faster than IPPV” only on the exact common dataset/`h`/`k` domain tested.
- “State of the art” only after the baseline audit includes the current direct competitors, including the DCLDS overlap check.
- “Scalable” must state the largest completed graph, h-clique count, memory, hardware, and timeout policy.

Negative or mixed results should be reported. In particular, the exact closure network may be disadvantaged when unique footprint count is close to total clique count; that outcome is scientifically informative.
