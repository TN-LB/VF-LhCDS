# Prompt 00 — Theory Audit and Repository Bootstrap

## Goal

把论文中的数学对象映射成明确的软件接口，建立可编译、可测试的仓库骨架；本阶段不实现生产算法。

## Context to read

- `AGENTS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/ALGORITHM_SPEC.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `papers/veri_free_lhcds_v3_1_submit.md`
- `papers/2023-icde-lds.md`
- `papers/2408.14022v1.md`
- `papers/2504.10937v1.md`

Source priority is defined in `AGENTS.md`. The new theory manuscript is authoritative.

## Deliverables

1. Create `docs/THEORY_TO_CODE_AUDIT.md` containing a table with:
   - mathematical object/theorem;
   - exact source section or theorem number;
   - software component;
   - preconditions;
   - postconditions/invariants;
   - planned unit or differential test;
   - unresolved ambiguity, if any.
2. Audit and explicitly record at least:
   - graph normalization semantics;
   - `mu_h`, `d_h`, deletion loss, compactness, LhCDS;
   - exact rational representation;
   - largest-maximizer semantics of `F_h(lambda)`;
   - residual footprint aggregation;
   - closure capacities and source-side extraction;
   - left-first recursion and terminal layer extraction;
   - deterministic tie order and top-k stopping;
   - `k > q`, `lambda = 0`, no h-clique, disconnected graph, isolated vertices;
   - safe clique-core reduction assumptions.
3. Append every unresolved semantic choice to `docs/DECISIONS.md`. Do not invent an answer.
4. Create the repository directories described in `docs/ARCHITECTURE.md`.
5. Add a minimal CMake project with:
   - one placeholder library target;
   - one placeholder CLI target;
   - one smoke-test target under CTest;
   - warnings enabled and deterministic build options.
6. Add a minimal Python package/test layout under `reference/` without implementing algorithms.
7. Update `docs/TASKS.md` and `docs/CLAIM_TRACEABILITY.md` with phase-0 entries.

## Boundaries

- Do not implement clique enumeration, max-flow, `F_h`, or the top-k solver.
- Do not import code from any baseline.
- Do not replace exact fractions with floating point.
- Do not resolve manuscript ambiguities from general graph knowledge.
- Do not edit the four files under `papers/`.
- Keep dependencies minimal; do not add a package solely for future convenience.

## Verification

Run and report:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j2
ctest --test-dir build --output-on-failure
python -m pytest reference/tests -q
```

Also verify that every theorem-dependent planned component has an entry in `docs/THEORY_TO_CODE_AUDIT.md`.

## Completion report

Use the repository completion-report format. Include a dedicated section listing decisions that require owner approval before implementation.
