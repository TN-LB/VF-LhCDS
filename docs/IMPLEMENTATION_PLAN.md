# VF-LhCDS Implementation and Evaluation Plan

## 1. Target result

Produce a research-grade implementation of the exact, verification-free, top-k LhCDS algorithm whose correctness follows the principal-chain and closure-oracle theory in `veri_free_lhcds_v3_1_submit.md`.

A successful project must establish all three claims separately:

1. **Semantic correctness:** outputs match the formal LhCDS definition on exhaustive small instances.
2. **Algorithmic correctness:** the closure oracle and divide-and-conquer implementation match their theorem-level specifications.
3. **Empirical performance:** under a preregistered, fair protocol, the implementation is faster and/or more memory efficient than applicable exact baselines.

The third claim is not assumed in advance.

## 2. Key implementation hypothesis

The proposed solver has the following path:

```text
G, h, k
  -> graph normalization
  -> h-clique enumeration/index
  -> exact interval query F_h(lambda) by max-weight closure/min-cut
  -> left-first principal-chain divide and conquer
  -> terminal layer component extraction
  -> deterministic top-k output
```

Unlike IPPV and convex-programming candidates, the main algorithm does not propose a candidate and then verify it. Its expensive primitive is the exact parametric maximizer oracle. Therefore, the engineering question is whether fewer or better-structured oracle calls offset clique enumeration and closure-network costs.

## 3. Phase plan and acceptance gates

### Phase 0 — Semantic freeze and repository bootstrap

**Deliverables**

- repository layout, build skeleton, formatting and test entry points;
- `docs/DECISIONS.md` with all known ambiguities;
- theorem-to-module map in `docs/CLAIM_TRACEABILITY.md`;
- baseline provenance table with repository identifiers and intended commit pins.

**Gate**

No production algorithm code is merged until definitions, tie behavior, output order, graph preprocessing, and exact arithmetic policy are explicit.

**Prompt**

`prompts/00_theory_audit_and_repo_bootstrap.md`

### Phase 1 — Independent exhaustive reference implementation

**Deliverables**

- Python graph normalizer and combination-based h-clique enumerator;
- exhaustive `mu_h(S)`, deletion loss, compactness, maximality, and LhCDS checker;
- exhaustive `F_h(lambda)` with largest-maximizer tie behavior;
- deterministic random graph generator and serialized truth fixtures.

**Gate**

Hand-checked examples and randomly generated tiny graphs produce stable truth files. The reference path must not call production code.

**Prompt**

`prompts/01_exhaustive_reference_oracle.md`

### Phase 2 — Production graph and clique foundation

**Deliverables**

- C++ normalized graph representation;
- degeneracy-oriented fixed-h clique enumeration;
- materialized clique index backend and a streaming/query-local backend interface;
- exact fraction utilities and checked integer helpers;
- unit tests against the Python fixtures.

**Gate**

For every test graph and selected subset, C++ and Python agree on graph normalization, clique tuples, clique degrees, and `mu_h`.

**Prompt**

`prompts/02_graph_and_clique_infrastructure.md`

### Phase 3 — Exact closure oracle for `F_h(lambda)`

**Deliverables**

- residual-footprint aggregator for an interval `X subseteq F_h(lambda) subseteq Y`;
- exact closure-network constructor;
- max-flow/min-cut backend;
- source-side extraction and oracle telemetry;
- exhaustive differential tests against all subsets on tiny graphs.

**Gate**

Across the fixed corpus and a large randomized campaign, the oracle returns exactly the inclusion-wise largest exhaustive maximizer for every tested rational lambda and interval. Tie-heavy fixtures are mandatory.

**Prompt**

`prompts/03_exact_closure_oracle.md`

### Phase 4 — Principal-chain divide-and-conquer top-k solver

**Deliverables**

- exact outer density `d_h(Y,X)`;
- left-first recursive or equivalent stack traversal;
- terminal layer extraction using connected components of `G[Y\X]` and anti-adjacency to `X`;
- deterministic output order and early stop at `k`;
- optional tie-inclusive output mode kept separate from default fixed-cardinality mode.

**Gate**

Full C++ results match the exhaustive LhCDS checker for all generated tiny instances and all tested `k` values, including `k=1`, `k=q`, and `k>q`.

**Prompt**

`prompts/04_divide_and_conquer_solver.md`

### Phase 5 — Correctness campaign and release candidate 0

**Deliverables**

- thousands of seeded random differential cases;
- property and metamorphic tests;
- automatic failure reduction and reproducer storage;
- sanitizer builds and overflow tests;
- first frozen correctness corpus.

**Gate**

No mismatch, sanitizer failure, undefined behavior, or silent overflow remains. The release candidate is tagged before performance optimization.

**Prompt**

`prompts/05_differential_test_campaign.md`

### Phase 6 — Instrumentation and safe optimization

Implement optimizations one at a time, each behind a switch and each validated against the frozen corpus.

Recommended order:

1. query and `mu_h` cache;
2. global materialized clique/incidence index;
3. safe high-density h-clique-core restriction;
4. residual-footprint aggregation improvements;
5. singleton-footprint folding and other proven network reductions;
6. flow object allocation reuse or alternative exact flow backend;
7. component-wise interval processing;
8. parallel clique enumeration, only if determinism is preserved;
9. any LDS-Opt-inspired seeding only after a separate safety proof or explicit non-core heuristic mode.

**Gate**

Each optimization has an ablation switch, regression evidence, and telemetry showing where it helps or hurts.

**Prompts**

- `prompts/06_cli_telemetry_and_output_contract.md`
- `prompts/07_safe_clique_core_reduction.md`
- `prompts/08_profile_guided_optimization.md`

### Phase 7 — Baseline integration

**Deliverables**

- unmodified or minimally patched builds of applicable baselines;
- adapters that normalize input and parse output into one canonical schema;
- commit, license, compiler, flags, and patch records;
- exact-output cross-check on shared feasible instances.

**Required baseline strata**

| h | Exact baselines to target | Notes |
|---|---|---|
| 2 | IPPV, LDS-Opt, LDScvx, LDSflow | LDS-specific methods are valid here |
| 3 | IPPV, LTDScvx, LTDSflow | Triangle density equals 3-clique density |
| 4,5 | IPPV and any verified arbitrary-h exact implementation | Do not include h=2/3-only methods as general baselines |

The public `s01bvral/DCLDS` repository requires immediate provenance and overlap review.

**Prompts**

- `prompts/09_ippv_baseline_adapter.md`
- `prompts/10_h2_h3_baseline_adapters.md`

### Phase 8 — Experiments, analysis, and reproducibility release

**Deliverables**

- smoke, correctness, main performance, scalability, and ablation suites;
- raw immutable run manifests and logs;
- aggregation scripts with timeout and OOM handling;
- result tables/plots generated from raw data;
- release artifact with build and reproduction instructions.

**Gate**

Every reported number is traceable to a run manifest, command, log, code commit, dataset checksum, and aggregation script version.

**Prompts**

- `prompts/11_experiment_harness.md`
- `prompts/12_ablation_and_scalability.md`
- `prompts/13_correctness_review.md`
- `prompts/14_performance_review.md`
- `prompts/15_reproducibility_release.md`

## 4. Branch and worktree strategy

Do Phase 0 in the main checkout. After interfaces are frozen, parallel worktrees can be used for:

- `ref-truth`: Python exhaustive reference and generators;
- `closure-oracle`: exact flow and oracle;
- `baseline-adapters`: external builds and parsers;
- `experiment-harness`: run manifests and aggregation.

Do not develop two independent versions of the same mathematical primitive in parallel and merge by intuition. One implementation must be designated authoritative and differential tests must mediate integration.

## 5. Principal risks and mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Clique explosion | `|Psi_h|` can dominate memory and time | Two clique backends, telemetry, h-clique core, streaming fallback |
| Closure network size | One node per unique footprint may still approach clique count | Aggregate identical footprints, fold safe special cases, measure `P` |
| Tie errors | Wrong min-cut tie handling changes `F_h(lambda)` and the whole chain | Exact `+1` cardinality perturbation, dedicated tie fixtures |
| Integer overflow | Capacity scaling multiplies counts, numerator, denominator, and `N+1` | checked `__int128`, overflow tests, fail closed |
| Small-k latency | Worst-case oracle-call bound is not output-sensitive | measure time-to-result, investigate safe high-density reductions |
| Baseline mismatch | Different preprocessing or top-k tie semantics invalidates comparison | canonical input/output adapter and tie-aware validator |
| Directly overlapping work | Public DCLDS repository may affect novelty and baseline choice | provenance audit before implementation claims |
| Shared-bug testing | Reference and production code could accidentally share logic | independent combination enumeration and exhaustive definitions |

## 6. Definition of done

The implementation is ready for paper-level experiments only when:

- all semantic decisions are documented;
- exhaustive and production outputs agree on the frozen corpus;
- the closure oracle independently passes exhaustive tests;
- all optimizations can be disabled and do not alter outputs;
- baseline commits and licenses are pinned;
- the experiment harness captures full provenance;
- a clean machine can reproduce at least one correctness case and one benchmark case from the release instructions.
