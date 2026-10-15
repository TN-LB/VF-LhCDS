# M6 through M8 implementation and evaluation plan

Revision: 2026-10-14, D045. Completion is governed by delivered functionality,
mathematical preservation arguments, executed validation and reproducible evidence.
M0–M5 retain their recorded completion status. M6 initial-source observation tooling
is **accepted at `de25116`** ([evidence](../evidence/m6/final-profile-20261014/REPORT.md));
M7 is **implemented and validated** ([evidence](../evidence/m7/interval-20261015/REPORT.md)). M8 remains planned;
P18.4 still requires final-host alignment and shared baseline/definition smoke.
Thesis chapters and prose analysis are not repository milestones; the code and
measurements needed to support those analyses are required deliverables.

## Deliverables and dependencies

| Milestone | Required result | Acceptance tasks | Detailed specification |
|---|---|---|---|
| M6 cost diagnostics and work accounting | Current-source diagnostic/control builds, exclusive phase accounting, distinct clique-work counters and reports for the three questions below | P16.1–P16.6 | [M6 diagnostics](M6_DIAGNOSTICS_PLAN.md) |
| M7 interval-local clique propagation and reuse | Exact interval worklists, partition-based endpoint counts, global/interval controls, safe-core compatibility, written preservation and work bounds | P17.1–P17.7 | [M7 algorithm increment](M7_INTERVAL_CLIQUES_PLAN.md) |
| M8 unified formal real-graph evaluation | Eight identified inputs, common Linux environment, final-source diagnostic refresh, frozen main/ablation/diagnostic suites and reproducible artifacts | P18.1–P18.8 | [M8 experiments](M8_EXPERIMENT_PLAN.md) |

Build the M6 observer and establish its correctness on the current validated solver.
Implement M7 against the unchanged mathematical contracts, using M6 to account for
new partition/reuse costs. After M7 acceptance, M8 rebuilds and revalidates both
diagnostic and uninstrumented binaries from the **same final optimized source**.
The initial M6 build and the old M5 profiler are not substitutes for that final
refresh. Data acquisition and Linux harness preparation in P18.1/P18.2 can proceed
before M7 completes; formal measurement waits for all readiness gates.

## Questions supported by implementation

| Question | Required observable support |
|---|---|
| How does VF/IPPV performance vary with clique count, queries and network size? | Aligned dataset/h/k outcomes; total cliques; logical queries and mincuts separately; sums/maxima of network sizes; exclusive VF phase times; instrumented/control overhead |
| Why can safe core reduce memory while increasing time? | Matched core off/safe results; peeling, incidence visits and initialization; reductions in oracle vertices, footprints and arcs; downstream build/flow/cleanup time and native peak RSS |
| What work does early stopping avoid, and what initialization remains? | Exact fixed-k/full prefix checks; completed-prefix and skipped-suffix work counts; terminal/non-output layers, depth and pending intervals; common loading/enumeration/index/worklist costs and cleanup |

The implementation must support these questions without presupposing their answers.
Report negative or mixed effects. VF counters alone do not expose IPPV's internal
costs, and cross-graph associations do not establish causality.

## Selected real graphs

| Dataset | Type | Preparation requirement |
|---|---|---|
| CA-GrQc | Scientific collaboration | Verify existing raw/normalized provenance; measure anew |
| CA-CondMat | Scientific collaboration | Verify existing raw/normalized provenance; measure anew |
| soc-hamsterster | Social | Acquire, identify version, normalize |
| fb-pages-politician | Social / page links | Acquire, identify version, normalize |
| fb-pages-company | Social / page links | Acquire, identify version, normalize |
| web-webbase-2001 | Web | Identify the small IPPV-listed artifact, not an unrelated full crawl |
| Amazon | Product co-purchase | Identify the IPPV-listed snapshot; distinguish other Amazon versions |
| Email-Enron | Email communication | Acquire, identify version, normalize |

These are the eight selected names, not a pool for favorable post-result selection.
They appear in [IPPV Table 2](../papers/2408.14022v1.md). Existing two-graph hashes
are in the [input manifest](../evidence/m5/campaign-proposal-20261005/dataset-manifest.json).
Six new artifacts remain to be acquired; no paper statistic is treated as a measured
statistic of a downloaded file. Identify unavailable/ambiguous sources before
freeze and record any necessary replacement decision.

## Evidence boundaries and decisions

All earlier local timings, including M5's `final-*` batches and M6/M7 development
diagnostics, are preliminary and excluded from M8 formal results. Preserve their
raw records and failures. Verified input artifacts and correctness fixtures may be
reused with provenance; every formal timing, including ablations, is measured anew.
Formal uninstrumented comparisons and formal diagnostic/control overhead results
have separate allowlists and summaries, even though both belong to M8.

D045 explicitly authorizes the selected M6/M7 work and supersedes D039's stop only
for this increment. D043's eight-graph selection and historical-result separation
remain accepted. D044's previous execution layout is superseded by D046's proposed
M8 configuration. Concrete dataset versions, hardware, resource limits and schedule
must be prepared and frozen before launch; a proposed default is not prior approval.

Preserve D005 exact automatic arbitrary precision, D006 output ties, D012 independent
development, D017 vertex preservation and D029's DCLDS deferral. Do not edit the
four manuscripts. IPPV's existing domain/license limits remain disclosed; no
output repair/filtering, additional baseline, parallel solver or method import is
implicitly authorized. A speedup is not an implementation acceptance requirement.

## Tracking and checks

The prior unexecuted P16/P17 layout is replaced by the task meanings in
[TASKS.md](TASKS.md); its historical plan review remains a record of commit
`4c0b6aa`, not current acceptance evidence. New test contracts T18–T27 are in
[CORRECTNESS_TEST_PLAN.md](CORRECTNESS_TEST_PLAN.md). Refinement obligations are
linked in [THEORY_TO_CODE_AUDIT.md](THEORY_TO_CODE_AUDIT.md); executed results belong
in [CLAIM_TRACEABILITY.md](CLAIM_TRACEABILITY.md) only after checks actually run.

[Plan validation record](../review/m6-m8-increments-20261014/checks.json) covers
document links, task/test contracts, workload arithmetic and source preservation.
It is documentation-review evidence, not completed M6–M8 implementation or runs.
