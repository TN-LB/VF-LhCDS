# Reproducibility Specification

Revision: 2026-09-09. Commands are targets until their actual execution logs exist.
The plan-review evidence under `review/` is not a production release.

Current formal evaluation target (2026-10-14, D043) is
[M7 after M6 preparation](M6_M7_EXECUTION_PLAN.md). Formal aggregates must accept
only an explicit allowlist of freshly measured M7 campaign IDs and their pinned
inputs/binaries/configurations. Reject every M5/M6 timing row, including the old
`final-*` batches. Earlier input artifacts and correctness fixtures may be reused
with hashes/provenance; old timing samples and repeat counts may not. M7 raw
hash verification and table regeneration are P17.3/P17.4, both still planned.

For the executed bounded M5 scope, use [M5 reproduction instructions](M5_REPRODUCTION.md).
Its fresh local rebuild and subsequent fresh Ubuntu userspace reproduction are
reported separately; the latter uses OrbStack on the same Mac. This does not
claim independent-machine performance replication or completion of all original
release gates. D042 closes the documented bounded stage; broader levels below
remain separate.

## 1. Reproduction levels

### Level 1 — correctness smoke

A clean machine can build the project, run a tiny exhaustive case, run the production solver, and verify identical output.

### Level 2 — baseline smoke

A clean machine can build each included baseline, run one shared small dataset, normalize output, and pass the tie-aware validator.

### Level 3 — paper tables

Given dataset files and the documented hardware class, scripts regenerate the raw manifests and aggregate tables/plots used in the paper.

## 2. Environment capture

Every run manifest records:

- UTC timestamp;
- repository commit and dirty-tree status;
- submodule/baseline commits;
- compiler path and full version;
- compile flags and build type;
- OS/kernel;
- CPU model, sockets, cores, and enabled thread count;
- total memory;
- hostname or anonymized machine ID;
- relevant environment variables;
- command line and working directory;
- timeout and memory limits;
- dataset checksum;
- random seed;
- feature switches.

Provide `vflhcds print-build-info` and a script that dumps system information.

## 3. Dataset manifest

For each dataset, record:

```text
name:
source_name:
source_version_or_download_date:
license_or_terms:
raw_checksum:
normalization_command:
normalized_checksum:
original_vertices:
original_edges:
removed_self_loops:
removed_duplicate_edges:
normalized_vertices:
normalized_edges:
isolated_vertex_policy:
notes:
```

Do not rely only on dataset display names; several repositories distribute variants with different edge counts.

## 4. Build commands

Document and test commands similar to:

```text
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
ctest --test-dir build --output-on-failure
```

For final experiments, store the exact compiler flags emitted by the build system. Avoid hidden local configuration.

## 5. Result directory contract

```text
results/
  raw/
    <experiment_id>/
      manifest.json
      stdout.txt
      stderr.txt
      time.txt
      proposed_output.jsonl
      canonical_output.jsonl
      oracle_stats.jsonl
      validation.json
  aggregate/
    runs.parquet-or-csv
    summary.csv
    tables/
    figures/
  logs/
```

Raw run directories are immutable after completion. If parsing or aggregation changes, regenerate only the aggregate layer.

## 6. Experiment manifest fields

At minimum:

```text
experiment_id
algorithm
algorithm_commit
baseline_patch_hash
configuration_name
dataset_name
dataset_checksum
h
k
repeat
seed
threads
timeout_seconds
memory_limit_bytes
command
start_time
end_time
exit_code
status
wall_seconds
user_seconds
system_seconds
peak_rss_kb
output_count
ordered_output_hash
validation_status
validation_evidence_level
external_validation_seconds
external_validation_peak_rss_kb
timing_scope
postload_seconds_or_unavailable
postindex_seconds_or_unavailable
logical_interval_queries
mincut_calls
capacity_backend
capacity_bit_length
```

For VF-LhCDS, also include all internal metrics named in `EXPERIMENT_PLAN.md`.

## 7. Determinism

The solver should be deterministic for fixed graph, `h`, `k`, and configuration. Sources of nondeterminism must be eliminated or explicitly seeded:

- hash-table iteration must not determine result order;
- parallel clique enumeration must merge in canonical order;
- equal min-cut outcomes must be resolved by the mathematical perturbation, not traversal accident;
- output components are sorted by the fixed subset order.

Run a determinism test that repeats the same case several times and compares canonical semantic output. Compare traces only after removing timing and backend-specific fields, and only for the same trace contract.

## 8. Release checklist

- source archive or public repository tag;
- `AGENTS.md` and all design documents;
- dependency and license list;
- build container or environment specification when possible;
- dataset preparation scripts and checksums;
- baseline commit/patch records;
- correctness fixture corpus;
- smoke commands;
- experiment configs;
- raw manifests for reported results or an archival location;
- aggregation and plotting scripts;
- final tables generated without manual edits.

## 9. Proof/design snapshot and scope

Before detailed DCLDS comparison, retain the supplied proof/design snapshot and
SHA-256 manifest under a recorded version. The revision preserves all `papers/`
files byte-for-byte and records their hashes; this is a content snapshot, not
independent evidence of historical priority. The archive contains no claim that
baseline commits/licenses/builds, production code, or final experiments were run.

A release's complete evidence needs reference and production commands, sanitizer
logs, exact-backend fallback tests, pinned baseline records, dataset checksums and
immutable run manifests. Review-only mathematical evidence is labelled separately.
