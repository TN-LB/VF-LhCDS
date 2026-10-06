# First repeated VF / IPPV campaign — pending decision, 2026-10-05

**Status: draft; no campaign runs executed.** Recommended scope is a limited local
pilot. It will measure repeated runtime/RSS and output agreement for the two
already available graph artifacts. It will not complete all of M5, establish
general-h performance, or support a comprehensive SOTA claim.

## Concrete configuration to approve

| Item | Proposed value |
|---|---|
| Inputs | CA-GrQc and CA-CondMat as bundled in the pinned IPPV repository |
| Grid | h=3; k in {5,10,15,20}, the existing IPPV reproduction grid |
| Repetitions | Exactly 3 measured repetitions per case; no additional warm-up calls |
| Algorithms | Pinned VF adjacency/basic and five-patch IPPV |
| VF settings | adjacency enumeration, core off, sorted footprints, exact auto-capacity backend |
| IPPV settings | iterations=10; native p=0, matching the already used adapter |
| Machine | This Apple M1, 16 GiB RAM, macOS 15.7.7 arm64; existing Release builds |
| Concurrency | One algorithmic worker per child; all children run serially |
| Timeout | 60 seconds per native child; separate 60-second guard per external validator |
| Memory | No imposed per-process cap; record native peak RSS |
| Cache | Uncontrolled, with no cache-flush or warm-up policy introduced |
| Order | Cases in the draft file's order; shuffle algorithm order within each repeat, seed 20261003 |
| Failure policy | Stop at first unsuccessful run or completed block with tie-aware disagreement; retain failures and every unrun entry |

There are 8 cases, 24 paired blocks, **48 native calls** if all succeed. The sum of
native guards is 48 minutes; at most another 48 minutes of external-validation
guards. These are guard sums, not predicted runtime or a strict whole-campaign
deadline. Setup and wrapper work are additional. A stopped campaign is incomplete;
pending repetitions must not be relabelled as completed or silently excluded.

Files ready for review:

- [Exact draft config](draft-config.json), [seeded schedule](draft-schedule.json),
  [execution policy](execution-policy-proposal.json), [pins](pins.json).
- [Dataset manifest](dataset-manifest.json), including raw and normalized hashes,
  normalization commands, vertex preservation and duplicate/loop counts.
- [Machine](../paired-smoke-20261005/environment.json) and
  [hardware](../paired-smoke-20261005/hardware-retry.json).

The draft schema deliberately cannot launch. After approval, record the decision
and create a separate approved config with only the scope/name changed; keep this
draft immutable. Invoke the runner with `--stop-on-failure`, and freeze the
approved command, source hashes, environment and schedule before any native run.
Binary/source or graph pin mismatches must be resolved before launch, not bypassed.

## Inputs and why these cases

| Artifact | Declared vertices | Undirected edges | Normalized SHA-256 |
|---|---:|---:|---|
| CA-GrQc | 5,242 | 14,484 | `85333a05c5d752357d711748909f184f739487b1af2cb1745a7fe2a363620f32` |
| CA-CondMat | 23,133 | 93,439 | `5e48ff6e02d4015364788f606f59adb4dafcc4dbdc92ce33a209a4eeb50c8adb` |

Selection is by current local availability: these are the two graph files in the
already acquired IPPV bundle. It is not a claim that they represent the full
candidate pool. h=3 extends the already exercised smoke stratum; the k grid and
three-repetition minimum come from `docs/EXPERIMENT_PLAN.md`. No new algorithm
parameter is introduced. Other h strata and larger graphs remain future work.

The declared 0-based IDs of these bundled artifacts are preserved, including all
isolates. This does not independently establish the bundle's mapping to a separate
upstream dataset release or its original external labels. Both normalizations
remove zero loops and zero duplicates. Local IPPV use remains under D027/D028;
the existing unidentified-license record is not upgraded to a license grant.
No external redistribution or new dataset acquisition is part of this proposal.

## Evidence and reporting rules

Use complete native process wall time and native child peak RSS as primary
measurements. Common offline normalization and separate output validation are
excluded consistently. IPPV's own candidate verification remains in its native
time. Save native exit/status, all stdout/stderr, validation time/RSS, exact output
records and semantic hashes. Missing IPPV phase wall times and per-rank latency
remain null. Do not subtract phases to invent a comparable algorithm time.

Every completed pair receives structural and strict/tie-aware comparison. These
graphs exceed the exhaustive-reference guard; no definition-level completeness or
maximality certification is claimed. Different eligible cutoff ties alone do not
stop a pair. The known IPPV zero-density omission remains a recorded limitation;
do not synthesize missing outputs, lower k, or exclude a failed case after seeing
its result. Keep all previous failed/time-limited diagnostics separately visible.

Report every cell's statuses, each raw time/RSS and, for completed triples,
median and min/max. Show incomplete cells and unrun repetitions explicitly; never
replace a timeout with a completed runtime or select the best repetition. Any
comparison is scoped to these inputs/h/k/builds/machine. There is no predetermined
winner. Source patches, this modified working tree, and build flags stay disclosed.
Additional repeats, changed limits, optimizations or a wider grid require a new
recorded scope before execution. DCLDS stays deferred under D029.

## Alternatives and the required decision

1. **Recommended:** approve the limited 48-call pilot above. It tests repeatability
   and k sensitivity with the current supported local resource policy; it leaves
   broad performance and resource-isolated conclusions open.
2. Expand now to h in {2,3,4,5}, retaining the other settings: 192 native calls,
   up to 192 minutes of native guards plus 192 minutes of validation guards.
   This adds h coverage but may hit memory/time or existing baseline limitations.
3. Specify a different machine, memory limit or final timeout first. This delays
   measurement and requires implementing/validating the requested resource policy
   before the campaign. Current runner rejects unsupported policies explicitly.

Approval is needed because `AGENTS.md` requires a decision for changes to final
experimental fairness/conclusions and requires predeclared dataset/resource/
thread/timeout choices; the owner also requested stopping at decisions/blockers.
The latest permission to continue authorized preparation and the same-settings
smoke, and is not recorded as approval of this new repeated grid.
