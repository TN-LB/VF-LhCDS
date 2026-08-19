# Baseline Audit and Integration Checklist

Audit date for this template: 2026-08-19. Re-run the audit before final experiments.

## 1. Why audit before coding adapters

A fair comparison requires more than compiling a repository. Each baseline must be checked for:

- exact problem definition;
- supported motif/clique size;
- top-k and tie semantics;
- graph normalization assumptions;
- correctness guarantees;
- code version and license;
- default parameters and hidden preprocessing;
- output completeness and parseability;
- thread usage;
- timing scope.

Do not reimplement a baseline from pseudocode unless public code is unavailable and the paper clearly specifies enough detail. A reimplementation must be labeled separately from author code.

## 2. Candidate matrix

### IPPV — `Elssky/IPPV`

**Role:** primary published exact baseline for general `h`.

**Paper behavior:** iterative propose-prune-and-verify using h-clique compact-number bounds, candidate decomposition, self-densest testing, and basic/fast flow verification.

**Public code observations:**

- C++/CMake project;
- executable examples use graph, `h`, iteration count `t`, `k`, pattern `p`, and verification mode;
- README lists 15 datasets and experiments for `h in {3,4,5}` and `k in {5,10,15,20}`;
- input begins with `n m`, followed by 0-based edges.

**Audit tasks:**

- pin commit and license;
- determine exact flag for fast verification and default iteration count;
- confirm whether timing includes clique enumeration and input loading;
- verify output lists complete vertex sets and exact densities;
- check whether vertex IDs must be contiguous and whether duplicate edges are tolerated;
- reproduce one README command before writing the wrapper.

### LDS-Opt / LDS-DC — 2023 ICDE

**Role:** `h=2` verification-free hierarchy baseline and specialization check.

**Support:** edge-density LDS only, equivalent to L2CDS.

**Audit tasks:**

- locate author code and license;
- if unavailable, contact authors or document a paper-based reimplementation;
- preserve largest-maximizer and top-k ordering semantics;
- validate on tiny `h=2` instances against the common truth program.

Do not use LDS-Opt as an arbitrary-h baseline.

### LDScvx — `chenhao-ma/LDScvx`

**Role:** strong exact convex-programming baseline for `h=2`.

**Public code observations:**

- C++/CMake repository;
- example command accepts graph path and `k`;
- README reports default/reproduction settings for `k` values and memory measurement;
- code appears to target edge-based LDS.

**Audit tasks:**

- pin commit and license;
- confirm output format and whether all top-k vertex sets are exposed;
- confirm Frank-Wolfe iteration default and verification behavior;
- separate preprocessing, optimization, and verification time if possible;
- validate against definition-level L2CDS truth.

### LTDScvx

**Role:** strong exact convex-programming baseline for `h=3`.

**Support:** triangle density only, equivalent to L3CDS.

**Audit tasks:**

- locate public author code corresponding to the journal paper;
- determine whether it is in a separate branch/repository or available on request;
- pin its Frank-Wolfe iteration setting and triangle enumeration backend;
- validate output against definition-level L3CDS truth.

Do not infer that the edge-only `LDScvx` repository implements LTDScvx without inspection.

### LDSflow and LTDSflow

**Role:** classical exact flow baselines for `h=2` and `h=3`.

**Audit tasks:**

- obtain author source where licensing allows;
- identify any core pruning and flow library;
- confirm candidate and verification time scope;
- use mainly on graph sizes where they complete under the preregistered timeout.

### Public DCLDS repository — `s01bvral/DCLDS`

**Status:** mandatory provenance/overlap investigation.

Its README claims a divide-and-conquer algorithm for LhCDS, supports clique and other patterns, emits LhCDS and density-decomposition layers, and uses a 15-dataset suite closely overlapping IPPV.

Before using or citing it, determine:

1. Is it your own or a collaborator's repository?
2. What paper, preprint, submission, or technical report does it implement?
3. What is its commit history and license?
4. Is its mathematical algorithm the same as, derived from, or independent of `veri_free_lhcds_v3_1_submit.md`?
5. Does it use the same exact max-closure residual-footprint oracle, or another density decomposition?
6. Are its results independently validated?
7. If independent, is it the most direct current baseline and related-work item?

Do not copy code or claim novelty until these questions are resolved.

## 3. Audit record template

Create one section or YAML/JSON record per baseline with:

```text
name:
problem_definition:
exact_or_approximate:
supported_h:
top_k_semantics:
tie_semantics:
repository_identifier:
commit:
license:
build_environment:
compiler_and_flags:
thread_count:
input_format:
preprocessing:
parameters_and_defaults:
output_format:
timing_scope:
peak_memory_method:
patches:
known_failures:
validation_cases:
status: pending | buildable | validated | excluded
exclusion_reason:
```

## 4. Wrapper architecture

Keep each author code in a separate directory or submodule:

```text
baselines/
  ippv/
  ldscvx/
  ltdscvx/
  ldsopt/
  ldsflow/
  ltdsflow/
  dclds_audit/
  patches/
```

Write wrappers under `tools/baseline_adapters/` that:

1. convert the canonical normalized graph to baseline input;
2. run the baseline with explicit parameters;
3. capture command, environment, stdout, stderr, exit status, wall time, and RSS;
4. parse outputs into canonical result JSONL;
5. recompute every reported clique count and density using the independent validator;
6. run strict or tie-aware comparison.

The wrapper must not silently repair invalid output. It should mark validation failure and preserve the raw files.

## 5. Patching rules

Allowed minimal patches:

- build compatibility;
- file paths and CLI output location;
- deterministic printing of already-computed result sets;
- disabling hardcoded dataset assumptions;
- fixing a confirmed bug with a separate upstream-style patch and regression test.

Not allowed under the original baseline name:

- replacing its core algorithm;
- adding proposed-method optimizations;
- changing approximation/exactness behavior;
- changing tie semantics without a separate label;
- excluding expensive stages from timing while including them for VF-LhCDS.

Every patch is stored as a diff and described in the experiment manifest.

## 6. Baseline acceptance gate

A baseline enters the main comparison only after:

- commit and license are recorded;
- build is reproducible;
- at least one toy and one real dataset run succeeds;
- output passes independent validation;
- supported `h` and exactness are clear;
- timing and memory scope are documented;
- required patches are reviewed.
