# Proposed next diagnostic — not executed

The first shared CA-GrQc smoke completed only for IPPV. VF basic mode hit the
predeclared 60-second guard. No completed runtime, output agreement, speedup, OOM
or algorithmic counterexample is inferred for that VF run.

Recommended next action: diagnose using the four already implemented M4 modes,
with the same normalized CA-GrQc input, h=3,k=5 and the same 60-second native and
external-validation guard. Run each once, serially, with a frozen seeded order:

| Mode | Core | Footprint scan |
|---|---|---|
| Basic | off | sorted |
| Core only | safe | sorted |
| Membership only | off | membership |
| Both | safe | membership |

[Draft configuration](proposed-diagnostic.json) pins the existing Release binary
and exact graph checksum. It is marked `draft` and cannot execute as-is. This
would add four native diagnostic runs (at most 240 seconds of native budget,
plus setup/external validation), retain all failures, and change no algorithm
code. One worker, no memory cap, uncontrolled cache, seed 20261003. It is not a
final benchmark or a post-hoc replacement for the saved timeout.

Alternative: first choose the final experiment dataset/resource/time budget and
scope. No such settings have been assumed accepted. The original instruction to
stop at a blocker/decision is respected here; IPPV routine-fix authorization D028
does not settle the VF performance-diagnosis/resource choice. DCLDS stays deferred.
