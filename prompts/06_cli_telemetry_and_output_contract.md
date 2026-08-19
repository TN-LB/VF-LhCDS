# Prompt 06 — CLI, Telemetry, and Canonical Output Contract

## Goal

Create a stable interface for experiments without changing the validated solver semantics.

## Context to read

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/REPRODUCIBILITY.md`
- current solver and tests

## Deliverables

1. Production CLI with explicit arguments for input, format, `h`, `k`, output path, trace level, timeout-cooperation flag, reduction mode, and flow backend.
2. Canonical machine-readable output, preferably JSON Lines plus one run-summary JSON, containing:
   - schema version;
   - graph fingerprint and normalized counts;
   - solver commit/build ID;
   - exact result rank, density numerator/denominator, clique count, size, sorted original IDs, result hash;
   - oracle-call count and terminal-layer count;
   - phase timing and peak internal counters;
   - completion/timeout/OOM/error status.
3. A separate human-readable summary mode.
4. Deterministic output independent of hash-table iteration, thread count (while single-threaded), or input edge order.
5. Output validator that checks exact densities, vertex validity, ordering, duplicates, disjointness, and optional equality to a reference result.
6. CLI integration tests and schema examples.
7. Update `docs/REPRODUCIBILITY.md` with exact build and run commands.

## Boundaries

- Do not mix logging text into machine-readable stdout.
- Do not make wall-clock telemetry part of semantic output hashes.
- Do not introduce default approximations.
- Do not silently normalize invalid inputs; report all transformations.
- Do not expose baseline-specific options in the proposed solver CLI.

## Verification

Run the same graph several times with permuted edge order and verify byte-identical semantic outputs. Validate all existing regression cases through the new CLI and output validator.
