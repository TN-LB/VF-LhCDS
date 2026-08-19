# Codex Workflow for This Project

## 1. Persistent context

Place `AGENTS.md` at the repository root. Keep detailed theory-to-code material in `docs/` rather than making `AGENTS.md` excessively long. Add nested `AGENTS.md` files only when a subtree needs stricter instructions, for example:

```text
reference/AGENTS.md     # independence and exhaustive implementation rules
baselines/AGENTS.md     # no core-algorithm modification and license rules
experiments/AGENTS.md   # immutable raw logs and manifest requirements
```

## 2. Prompt pattern

Every coding request should specify:

- **Goal:** observable behavior to deliver;
- **Context:** exact source files and existing modules to inspect;
- **Deliverables:** files/interfaces/tests expected;
- **Boundaries:** mathematical semantics and files that must not change;
- **Verification:** commands and comparisons that prove completion.

Avoid prompts such as “implement the algorithm from the paper.” They leave tie handling, arithmetic, testing, and module boundaries underspecified.

## 3. Recommended interaction cycle

1. Use `/plan` for each phase or cross-module change.
2. Ask Codex to inspect the named theory and design files before editing.
3. Require the smallest relevant tests immediately after each change.
4. Review the diff and generated tests.
5. Run `/review` with custom criteria focused on proof invariants and missing tests.
6. Merge only after `TASKS.md`, `DECISIONS.md`, and `CLAIM_TRACEABILITY.md` are updated.

## 4. Worktree split

After Phase 0 interfaces are committed:

- Worktree A: exhaustive reference and random fixtures.
- Worktree B: flow and exact closure oracle.
- Worktree C: baseline builds and adapters.
- Worktree D: experiment manifest and aggregation.

Do not run production solver orchestration and oracle interface redesign in parallel branches without a shared contract commit.

## 5. Review prompts

Use two distinct reviews:

### Correctness review

Focus on:

- divergence from definitions or theorem assumptions;
- float use in exact decisions;
- largest-maximizer tie implementation;
- interval precondition violations;
- incorrect component/anti-adjacency extraction;
- overflow and signedness;
- tests that duplicate implementation logic rather than independently checking it.

### Performance review

Focus on:

- repeated clique scans;
- avoidable set copies;
- hash/map overhead for small footprint keys;
- closure-network allocation;
- max-flow bottlenecks;
- cache memory growth;
- misleading timing scope.

Do not mix performance refactoring into the correctness review unless a bug is involved.

## 6. Expected Codex completion report

Require this exact structure:

```text
Summary
Files changed
Commands run
Tests and results
Correctness argument tied to docs/CLAIM_TRACEABILITY.md
Performance observations, if measured
Open risks and decisions
```

A task is incomplete if Codex says tests were not run but does not explain why.
