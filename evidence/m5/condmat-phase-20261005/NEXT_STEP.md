# Prepared next diagnostic: existing M4 membership mode

Status: proposal only; no new native call is executed. The owner-directed stop
at the incomplete D032 solving path is retained. This is a concrete local
diagnostic, not an amendment to D030/D031's formal timing campaign.

## Observation and hypothesis

CA-CondMat parsing and adjacency indexing finish in 0.158854 s from main entry.
The 60-second run finishes 137 oracle queries; every query scans all 173,361
triangles. Late queries can have only 12–40 network nodes but roughly 0.4 s gaps.
Those gaps include work outside max flow and are not isolated flow timers.

The sorted footprint scan calls includes/set_difference using original query
bounds for every clique. The accepted M4 membership path marks X/Y once, then
checks each clique vertex directly; its exact footprint-preservation argument
and previously executed equivalence evidence are in docs/M4_IMPLEMENTATION.md
and evidence/m4. MaterializedCliques::count still uses a full sorted scan even
in membership mode. This may limit improvement; completing within 60 seconds is
not assumed, and no production change is proposed before measuring the switch.

## Recommended concrete scope

Use [draft-membership-config.json](draft-membership-config.json): the same pinned
VF Release binary and normalized CA-CondMat artifact, h=3,k=5, adjacency
enumeration, core off, existing footprint membership mode, automatic exact
capacities. One native call, one worker, 60-second guard, no memory cap,
uncontrolled cache, no warm-up/retry. Seed remains 20261003; a single algorithm
needs no random ordering. No IPPV call or new parameter grid is included.

Freeze a separate executable diagnostic configuration before launch (the current
scope=draft is rejected by the shared runner). Preserve both prior campaigns.
Use unchanged experiments/run.py with --stop-on-failure. If the child completes,
run its separate exact structural validator at the same 60-second limit. A
completed real basic output is unavailable, so do not claim real-case off/on
agreement from this one run. Existing M4 preservation evidence is the reason
this switch is eligible to test; real structural checks do not establish
maximality/completeness.

Retain timeout/error/validation failure and stop after this one planned call.
If it completes, review what was learned before proposing any fresh paired or
expanded campaign. No successful measurement is substituted into the historical
basic-mode timing cells. Phase diagnostics and benchmark timings remain distinct.

## Alternatives and consequences

- Recommended: measure the already implemented membership switch under the same
  60-second guard. Minimal implementation risk; its benefit on this graph is
  still unknown and endpoint counting remains unchanged.
- More detailed inner-operation instrumentation: distinguishes footprint,
  endpoint counting, network construction and flow. Requires a separate traced
  build/validation plan and another bounded run.
- Increase the timeout: may produce a basic output, but adds resource cost and
  does not identify avoidable work; do not silently revise the campaign budget.

Production optimization, a new flow algorithm, caching, default changes,
parallel execution and DCLDS techniques are outside this proposal.
