# Prompt 10 — h=2 and h=3 Baseline Adapters

## Goal

Integrate specialization baselines without misrepresenting their supported problem scope.

## Context to read

- `AGENTS.md`
- `docs/BASELINE_AUDIT.md`
- `docs/EXPERIMENT_PLAN.md`
- `papers/2023-icde-lds.md`
- `papers/2504.10937v1.md`
- relevant h=2/h=3 sections of `papers/2408.14022v1.md`

## Baseline matrix

- `h=2`: LDS-Opt/LDS-DC if authoritative code is obtainable, LDScvx, LDSflow.
- `h=3`: LTDScvx if authoritative code is obtainable, LTDSflow.
- Greedy or approximate CDS methods may be included only in a clearly labeled non-exact/effectiveness panel, never in the exact-runtime winner claim.

## Deliverables

For each candidate baseline:

1. Record repository/source provenance, commit, license, supported scope, exactness, build status, input/output semantics, and paper defaults in `docs/BASELINE_AUDIT.md`.
2. Prefer unmodified author code with an external adapter.
3. Pin source and dependencies.
4. Convert only the common normalized input into the baseline format.
5. Parse output into the common exact schema when the baseline exposes enough information.
6. Validate on tiny graphs for the exact supported `h`:
   - vertex sets;
   - exact density;
   - rank/tie semantics;
   - behavior when fewer than `k` answers exist.
7. Label unavailable or non-reproducible methods explicitly; never silently replace them with a home-grown implementation.
8. Keep separate build/run scripts per baseline.

## Special checks

- Confirm that LDScvx is an edge-density (`h=2`) method.
- Confirm that LTDScvx/LTDSflow are triangle (`h=3`) methods.
- Confirm that the 2023 LDS divide-and-conquer implementation is not treated as arbitrary-h.
- Audit whether public repositories include all algorithms claimed in the papers or only subsets.
- Audit output tie behavior; normalize reporting but do not alter which solutions the baseline returns.

## Boundaries

- Never include h=2/h=3-only runtime points in an `h>=4` comparison.
- Never call an approximate method exact.
- Never compare a reimplementation as the official baseline without a separate label.
- Never patch algorithm logic merely to make outputs match; investigate first.

## Verification

Produce a baseline status table with `ready`, `blocked-license`, `blocked-source`, `build-failed`, `semantic-mismatch`, or `validated`. Attach commands and tiny-graph results for every `validated` method.
