# Prompt 99 — Minimize and Diagnose a Correctness Failure

## Goal

Convert one failing test, seed, output mismatch, crash, or overflow into the smallest reproducible case and identify the violated invariant before changing production logic.

## Inputs to provide

- failing command or test name;
- seed/shard, if randomized;
- input graph artifact;
- `h`, `k`, lambda/interval when relevant;
- expected and actual outputs;
- build mode and commit.

## Procedure

1. Reproduce the failure unchanged.
2. Capture a self-contained failure bundle.
3. Classify the first divergent layer:
   - normalization;
   - clique enumeration/count;
   - exact arithmetic;
   - footprint construction;
   - min-cut/closure extraction;
   - recursion/terminal extraction;
   - output ordering/serialization;
   - reduction;
   - baseline adapter.
4. Use the independent Python oracle wherever tractable.
5. Minimize by attempting, in deterministic order:
   - remove irrelevant isolated vertices;
   - remove vertices;
   - remove edges;
   - reduce `k`;
   - reduce `h` only if the same bug remains;
   - simplify lambda/interval.
6. State the earliest violated invariant and the exact source theorem/spec section.
7. Add the minimized case as a regression test before applying a fix.
8. Make the smallest justified fix.
9. Run the targeted test, related component tests, then the full required regression tier.

## Boundaries

- Do not weaken or delete the failing assertion.
- Do not change expected output without proving the prior expectation was wrong.
- Do not add floating tolerance.
- Do not fix a downstream symptom when an upstream invariant first fails.
- Do not discard the original failure bundle after minimization.

## Completion report

Include original reproducer, minimized reproducer, root cause, violated invariant, code change, new regression test, commands run, and residual risk.
