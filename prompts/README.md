# Prompt Index - VF-LhCDS

Revision 2026-09-09. Use the task IDs and gates in `docs/IMPLEMENTATION_PLAN.md`
and `docs/TASKS.md`. Filenames are retained where possible; numbering is not a
requirement to execute all optional work. Every task uses the centralized proof
obligations, test IDs and decision log rather than duplicating specifications.

| Milestone | Prompts | Scope / dependency |
|---|---|---|
| M0 | 00_theory_audit_and_repo_bootstrap.md | Contracts and skeleton only |
| M1 | 01_exhaustive_reference_oracle.md | Independent truth and independent chain |
| M2 | 02_graph_and_clique_infrastructure.md; 03_exact_closure_oracle.md | One clique backend, exact restricted/global oracle, real numeric fallback |
| M3 | 04_divide_and_conquer_solver.md; 05_differential_test_campaign.md; 06_cli_telemetry_and_output_contract.md; 13_correctness_review.md | Fixed-k solver, evidence and unoptimized correctness freeze |
| M4 optional | 07_safe_clique_core_reduction.md; 08_profile_guided_optimization.md | Query-local safe core; one measured optimization at a time |
| M5 | 09_ippv_baseline_adapter.md; 09b_dclds_baseline_adapter.md; 10_h2_h3_baseline_adapters.md as applicable; 11_experiment_harness.md; 12_ablation_and_scalability.md; 14_performance_review.md; 15_reproducibility_release.md | Validated claim-scoped comparison and release |
| Failure path | 99_minimize_a_failure.md | Preserve a counterexample and diagnose the first violated obligation |

M1 and standalone M2 flow work may proceed in parallel after M0; oracle integration
needs M1 fixtures and graph/clique infrastructure. M3 needs M1+M2. M4 needs M3.
Baseline/harness work can proceed independently after contracts are stable and
must preserve D012's snapshot boundary. It does not block the M3 release.

Streaming, alternative flow algorithms, parallelism and tie-inclusive mode are
backlog, not mandatory prompt milestones. DCLDS is a primary baseline task;
its independence is already recorded and must not be re-asked.

Suggested task request:

```text
Read AGENTS.md and the contract files named in the selected prompt.
Execute task <ID> using prompts/<filename>.
Preserve the proof sources and accepted decisions.
Report actual commands, code/test evidence, seeds and unrun work.
```
