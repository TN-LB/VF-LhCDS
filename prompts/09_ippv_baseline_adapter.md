# Prompt 09 — IPPV Baseline Provenance, Build, and Adapter

## Goal

Integrate the public IPPV implementation as an external, pinned, minimally modified exact arbitrary-h baseline.

## Context to read

- `AGENTS.md`
- `docs/BASELINE_AUDIT.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/REPRODUCIBILITY.md`
- `papers/2408.14022v1.md`

## Deliverables

1. Complete the IPPV row in `docs/BASELINE_AUDIT.md`:
   - repository identity and provenance;
   - commit hash and retrieval date;
   - license status;
   - supported `h`, `k`, graph assumptions, exactness;
   - build toolchain and dependencies;
   - input/output format;
   - default parameters and any paper-vs-code discrepancies.
2. Add IPPV under `baselines/` as a submodule or reproducible fetch script pinned to a commit. Do not vendor an unpinned moving branch.
3. Build it unmodified first and preserve the original executable.
4. Add an external wrapper under `tools/baseline_adapters/` that:
   - consumes the common normalized graph;
   - writes the baseline's required input;
   - invokes the baseline with explicit `h` and `k`;
   - captures stdout/stderr, exit code, wall time, peak RSS, timeout/OOM;
   - parses results into the common schema without changing their meaning.
5. Store any unavoidable patch as a separate patch file with rationale. Do not mix it into proposed-solver code.
6. Validate IPPV outputs against the exhaustive oracle on tiny graphs and against VF-LhCDS on a small shared corpus. Classify every mismatch before benchmarking.
7. Record exact commands in `docs/REPRODUCIBILITY.md`.

## Boundaries

- If the license is absent or incompatible, do not copy or redistribute source; document the limitation and use a local external checkout.
- Do not reimplement IPPV and label it as the authors' baseline.
- Do not tune IPPV using information unavailable to VF-LhCDS.
- Do not compare different normalized graphs.
- Do not hide failed/unknown output parsing.

## Verification

Report commit, license, build command, smoke test, tiny-graph exactness results, output parser tests, and any paper/code deviations. If network access is unavailable, prepare the scripts and audit checklist, then state exactly what remains unverified.
