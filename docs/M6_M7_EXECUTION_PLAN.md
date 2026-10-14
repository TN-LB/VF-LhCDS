# M6 and M7 implementation and formal experiments

Revision: 2026-10-14. D043 authorizes an eight-graph formal evaluation and a
separate experimental milestone within **four weeks of additional work**, excluding
thesis writing. This plan schedules data/tool implementation in M6 and the unified
formal campaign in M7. Both milestones are **planned, not executed**.

M0–M5 keep their historical completion status. All earlier local measurements,
including the D040/D041 batches named `final-*`, are development/preliminary
evidence relative to M7. Their raw records, failures and reports remain unchanged.
They must not enter M7 performance tables, speedup summaries, repeat counts or
formal ablations. Existing correctness evidence and verified input artifacts may
be reused with provenance; **every formal timing must be measured anew**.

## Scope and four week budget

| Stage | Budget | Deliverable |
|---|---|---|
| M6 data and experiment tooling | Weeks 1–2 | Eight pinned inputs, Linux environment/resource support, tested result separation, common builds and a reviewable frozen campaign package |
| M7 unified formal experiments | Week 3 and first part of week 4 | Fresh main comparison and bounded ablations on one recorded machine; complete outcome ledger and reproducible aggregation |
| Repair and reproduction reserve | Remainder of week 4 | Correctness repair if needed, explicitly versioned remeasurement, hash verification and table regeneration |

The four weeks cover M6 and M7 together, including setup, implementation, testing
and execution. Thesis chapters, theoretical discussion, literature analysis and
writing are not milestones. No new solver optimization is selected by this plan;
D039 remains in force. Interval-local clique worklists and other algorithm ideas
remain unscheduled candidates, rather than an extra prerequisite or an additional
four-week allowance. Adding one later requires replacing budgeted work explicitly.
DCLDS stays deferred under D029; no new baseline or parallel solver is required.
IPPV's known zero-density omissions, unidentified upstream license and unaudited
floating bounds remain disclosed under the existing baseline audit. D027's local
use authorization does not authorize source redistribution. The eight-graph scope
does not imply that IPPV has gained full-domain correctness.

## Selected eight graphs

The names below are the selected set for preparation, not a pool from which to
retain only fast or successful cases. They are all listed in
[IPPV Table 2](../papers/2408.14022v1.md) / the
[author manuscript](https://arxiv.org/html/2408.14022v1#S6.SS1).

| Dataset | Network type | Artifact preparation |
|---|---|---|
| CA-GrQc | Scientific collaboration | Verify and reuse the existing normalized artifact and original provenance; rerun all measurements |
| CA-CondMat | Scientific collaboration | Verify and reuse the existing normalized artifact and original provenance; rerun all measurements |
| soc-hamsterster | Social | Acquire, identify version and normalize in M6 |
| fb-pages-politician | Social / page links | Acquire, identify version and normalize in M6 |
| fb-pages-company | Social / page links | Acquire, identify version and normalize in M6 |
| web-webbase-2001 | Web | Identify the small version listed by IPPV; do not substitute the full crawl under the same name |
| Amazon | Product co-purchase | Identify the IPPV-listed version; distinguish other Amazon snapshots explicitly |
| Email-Enron | Email communication | Acquire, identify version and normalize in M6 |

Existing GrQc/CondMat input identities are in the
[two-graph manifest](../evidence/m5/campaign-proposal-20261005/dataset-manifest.json).
The six new raw artifacts and all eight final manifest entries still need M6
validation. Paper statistics are not measured statistics of acquired files.
An unavailable or ambiguously identified dataset is reported before freeze;
replacement needs a recorded scope decision, not silent substitution after timing.

Each entry records source URL/version/retrieval date, use terms, raw checksum,
format, declared vertex universe, reversible original-ID mapping, normalization
command/version, removed loops/duplicates, normalized checksum and measured n/m.
Normalize to one common simple undirected graph and lossless baseline format;
preserve every declared vertex, isolates and zero-density solutions. For edge-list
sources without explicit vertex declarations, record the recoverable universe
and do not invent absent vertices or silently equate it to another snapshot.
No largest-component filtering, sampling or dataset-specific pruning is implicit.

## M6 implementation and acceptance

| Task | Required implementation or artifact | Acceptance evidence |
|---|---|---|
| P16.1 | Eight-entry dataset manifest and reproducible source-format conversion using `experiments/prepare_input.py` or explicit adapters | Named normalization fixtures for headers, original IDs, reversed duplicates, loops and isolates; canonical round trips and all eight input hashes |
| P16.2 | Linux-aware `experiments/environment.py` and process resource enforcement in the shared capture path | Linux load/memory/swap and CPU allocation records; unavailable sensors remain null; tested limit enforcement, process-group cleanup and outcome classification |
| P16.3 | Explicit campaign identity and formal-result allowlist in configuration/aggregation | Reject M5/M6 measurements, diagnostic runs, wrong graph/binary pins, duplicate repeats and mixed campaign versions; report missing/censored rows without fabricating timings |
| P16.4 | Common fresh Release builds, baseline smoke and a concrete freeze package | Compiler/flags, source/binary hashes, eight datasets, full grid, resources, seed, order, comparison and stop policies saved before M7; applicable build/reference/harness/adapter checks actually pass |

P16.1/P16.3 need regression tests that detect data loss or mixed evidence; P16.2
needs real Linux integration checks, including a bounded memory stress child and
timeout cleanup. Existing `wait4` peak-RSS collection alone does not enforce a cap.
Record OOM only when supported by resource-controller/kernel evidence; an arbitrary
SIGKILL or allocation error is not automatically OOM. Apply identical native caps
to VF and IPPV; run external validators separately with their own recorded cap.

Current `run.py` accepts only one worker, uncapped memory and uncontrolled cache.
Current environment monitoring uses macOS probes and an AC-power guard, which
cannot simply be reused unchanged on a Linux server. Extend these paths while
keeping historical manifests readable; do not disable missing probes and claim
the intended policy was enforced. Do not require a battery sensor on a server.
Reserve CPU/resources and record the actual host/container/cgroup arrangement.

M6 smoke/pilot outputs live under `evidence/m6/<preparation-id>/` and are excluded
from M7. Resource feasibility checks may inform the explicit pre-freeze decision;
do not drop selected graphs because their comparative performance is unfavorable.
Small definition checks remain independent of production code. Large-graph
structural checks and cross-implementation agreement do not prove maximality.

## Formal campaign configuration to freeze after M6

These are **D044 proposed settings**, not previously confirmed machine/resource
values. Prepare the complete package before requesting the remaining resource
decision. The eight-graph scope and separation from earlier measurements are
already authorized by D043 and do not need to be asked again.

| Item | Proposed setting |
|---|---|
| Host | One reserved Linux machine, preferably Ubuntu 24.04 LTS and 64 GiB RAM; physical host/CPU allocation and virtualization recorded; no host has yet been selected |
| Software | C++17 GCC/Clang with native unsigned 128-bit support, CMake >=3.16, Boost 1.86.0; Python >=3.10 and pinned test dependencies; exact installed versions recorded |
| Algorithms | Current validated VF and pinned eight-patch IPPV; fresh builds on the same host, documented Release optimization flags |
| VF main options | adjacency enumeration, membership footprints/counting, core off, automatic exact numeric backend |
| IPPV options | iterations=10, p=0, preserving the current project configuration; do not present this as reproducing every paper setting |
| Main grid | All eight graphs × h={3,4,5} × k={5,10,15,20} × two algorithms × five repeats |
| Order | Serial, one algorithmic worker; randomized algorithm order within each pair, seed 20261003; full schedule saved before execution |
| Time limits | 300 seconds per native process and separately 300 seconds per external validator |
| Memory limits | On a 64 GiB host: 48 GiB per native process and separately per validator, with no swap available to those process groups; verify enforcement before launch |
| Cache/repeats | Uncontrolled filesystem cache, no warmup calls, no adaptive repetition or favorable retry; retain all five scheduled outcomes |
| Main comparison | Existing cutoff-tie-aware agreement; strict equality reported separately; no change to VF output semantics |
| Core ablation | GrQc and CondMat, h={3,4,5}, k=20, core off versus safe, five repeats, otherwise identical VF options; strict equality |
| Stop ablation | GrQc and CondMat, h={3,4,5}, k=5 versus all, five repeats, otherwise identical VF options; exact prefix equality |

Both ablations are newly measured on the M7 host, even though their graph names
match M5. They are explicitly two-graph implementation comparisons, not eight-graph
ablation claims. No detailed profiler or per-rank streaming latency is required;
use supported counters, native wall/CPU/RSS and separate validation metrics.

The proposed workload is **960 main + 60 core + 60 stop = 1,080 native calls**.
At 300 seconds each, native timeout allowances sum to 90 hours; at most another
90 hours cover separate validators. The combined **180 hours / 7.5 days** is a
guard allowance, not a predicted runtime, and excludes setup/aggregation/repairs.
The validator budget includes output conversion and validation in the guarded
external phase; M6 must confirm that no unguarded validation work invalidates it.
This motivates reserving uninterrupted run time in week 3 and repair time in week 4.
If only a 32 GiB host or a different execution window is available, record a revised
common cap/budget before freeze; do not silently label the 64 GiB proposal active.

## M7 execution and evidence boundary

| Task | Required result |
|---|---|
| P17.1 | Freeze the approved concrete package; run the 960-call main schedule on the recorded host; account for every planned outcome |
| P17.2 | Run both new 60-call ablations on that host with the strict/prefix comparators |
| P17.3 | Produce machine-generated raw inventories, outcome tables, paired summaries and comparison records from only the explicit M7 campaign allowlist |
| P17.4 | Verify raw hashes and regenerate tables from saved records in a clean software environment; provide executable reproduction commands |

Store new measurements under `evidence/m7/<campaign-id>/`, separately from
`evidence/m6/` and immutable `evidence/m5/`. A directory name or
`approved_campaign` string alone is not authorization or proof of provenance.
The aggregation input must list exact campaign IDs, configurations, input hashes,
binaries and schedules; broad recursive searches across `evidence/` are prohibited.
Reusing normalized graph bytes from M5 does not permit reusing M5 timing rows.

Primary timing spans native process launch through complete output, including
input/index construction and IPPV's own candidate verification. Shared offline
normalization and subsequent external validation remain outside native timing.
Show validator timeout/error separately from native completion; a quick native
run whose output was not validated is not a successful agreeing comparison.

Continue the fixed schedule after native timeouts and confirmed resource-limit
OOMs once process cleanup is verified. These are censored outcomes, not completed
times or wins. Unexpected errors, validator failures, substantive disagreement or
resource-policy drift stop the affected suite and retain all unrun entries. M6
must implement/test this policy; the old runner does not already support all of it.
Keep other independent preparation work available while a correctness issue is
diagnosed. Do not filter zero-density outputs or fill in omitted IPPV solutions.

D028 still authorizes routine baseline correctness repairs. If a pinned algorithm
changes, preserve the failed campaign, freeze new hashes and rerun the whole
affected suite with fresh paired controls under a new campaign ID. Never pool old
and repaired versions to fill missing repeats. No performance-driven retuning or
timeout extension is permitted during a frozen campaign.

M7 completion requires an accounted, executed schedule, valid comparison handling
and reproducible outputs; it does not require VF to win or every call to finish
before its resource limit. An unresolved semantic disagreement or unexplained
error blocks the affected acceptance gate. A stopped ledger alone is not a
completed campaign; timeout/OOM rows remain visible and cannot be replaced by
favorable subsets. If repairs exceed the four-week reserve, report the incomplete
scope and obtain a new scope decision instead of importing historical results.
If a discrepancy is diagnosed as a known baseline domain limitation, retain its
failure and restrict the comparison claim explicitly; do not label it agreement
or use its shorter output as a successful runtime win. Any revised continuation
or acceptance scope must be recorded before further affected measurements.

## Plan status and links

This revision changes planning documents only. P16.1–P17.4 remain unchecked in
[TASKS.md](TASKS.md); it adds no implementation-tested evidence for O01–O12.
P16.1/P16.3/P16.4 and P17.1–P17.4 primarily support O12; P16.2 also supports honest
O09 resource telemetry. Existing M0–M5 mathematical/correctness evidence is retained.
The broader candidate experiments in [EXPERIMENT_PLAN.md](EXPERIMENT_PLAN.md) are
background, not additional requirements within these four weeks.

[Planning checks](../review/m6-m7-plan-20261014/checks.json) record document links,
task states, workload arithmetic and unchanged papers/code/historical evidence;
they are not M6 implementation or M7 execution evidence.
