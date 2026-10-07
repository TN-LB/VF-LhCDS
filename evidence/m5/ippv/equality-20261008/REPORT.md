# IPPV-B09: equal-density verification boundary — 2026-10-08

**The disputed IPPV set is nonmaximal; VF correctly excludes it.** Patch 0008
repairs two verifier boundary comparisons. Release and ASan/UBSan builds pass
the new independent regression, previous regressions and original-case checks.
This establishes the recorded repair scope, not full-domain baseline correctness.

## Exact original-graph witness

D040 stops at CA-CondMat h=4,k=15, repeat 0. IPPV emits a K10 of density 21
that VF omits above the common density-14 cutoff. It is connected by edge
`(1748,18841)` to a disjoint K10, also of density 21. Their induced union has
20 vertices, 91 edges and 420 four-cliques, with no crossing four-clique.

Deleting a vertices from the first K10 and b from the second loses
`420 - C(10-a,4) - C(10-b,4)` cliques, at least `21*(a+b)` for every a,b=0..10.
The checker verifies the original graph edges, all 4,845 possible four-tuples
and all 121 deletion-cardinality classes. Thus the connected proper superset
is 21-compact, disproving the candidate's required maximality. This is an exact
finite-instance witness, not full original top-15 truth or a theorem proof.

[Witness graph and certificate](../../final-evaluation-20261008/diagnosis/) ·
[Standalone checker](../../final-evaluation-20261008/certify_disagreement.py).

## Cause and minimal repair

`Graph::verify_LhCDS_small` used `rho_gu[w] - DELTA >= g` and
`rho_l[w] + DELTA <= g` to discover ordinary-edge neighbors. Even exact bounds
equal to g fail these tests. This can omit an equal-density extension not reached
through an h-clique. The verifier then accepts a candidate without considering
that connected compact superset.

Patch [0008](../../../../baselines/ippv/patches/0008-include-equal-density-verification-neighbors.patch)
uses `rho_gu[w] + DELTA >= g` and `rho_l[w] <= g + DELTA`: equality stays in the
verification search, and the existing tolerance admits near-boundary uncertainty
conservatively. The same existing exact network checks the expanded search.
No new parameter, VF technique, flow backend, epsilon value or synthesized output
is added. Other floating bounds and legacy verifier code remain audit limitations.

The deterministic 13-vertex fixture is a K5 followed by two K4s, joined by ordinary
bridges, with h=3,k=3. The unchanged exhaustive reference checks every proper
superset under the existing explicit local size-13 diagnostic guard and returns
only the K5 (density 2). Old IPPV additionally emits the last K4 (density 1);
VF and both repaired builds return just the K5. This is a small regression,
not a claim of globally minimal reduction of the original graph.

## Executed verification

- Release and ASan/UBSan/bounds-check builds succeed in new `build-ippv-equality-*`
  directories. Old seven-patch binaries remain untouched.
- New equality regression: **2/2 independent definition checks pass**.
- Prior fractional-capacity regression: **2/2 definition checks pass**.
- Existing h=2..5 corpus: **48/48 native runs**, 32 definition passes and the
  same 16 known zero-density omissions. Its expected exit 1 preserves those failures.
- Original h=4,k=15: **2/2 structural checks and tie-aware comparisons pass**;
  the invalid K10 disappears in both profiles. Strict equality remains false only
  at the allowed density-14 cutoff. Native stderr is empty in the repaired replay
  and named regressions; there are no sanitizer diagnostics.
- Adapter/reference pytest: actual output in [checks/pytest/stdout.txt](checks/pytest/stdout.txt).

Commands and outcomes are saved in [checks/commands.json](checks/commands.json),
with full per-command process/stdout/stderr records. Build commands/flags are in
`build-release/commands.json` and `build-sanitize/commands.json`. The executed driver:

```sh
.venv/bin/python evidence/m5/ippv/equality-20261008/checks.py
```

This runs `check_equality.py`, `check_fractional.py`, `check_toys.py`, the independent
certificate and reference/adapter pytest, followed by one original-case correctness
replay per profile. Each native/validator uses the existing 60-second guard.
No baseline benchmark timings are inferred from these diagnostic calls.

Changed files/symbols: `source-lock.json`, patch 0008 (only the two comparisons),
`fixtures/equal-density-bridge.graph`, `check_equality.py`, and repair evidence.
Environment: Apple M1, macOS arm64, AppleClang 17, Boost 1.86.0, Python 3.12.2;
deterministic fixtures, no random seed. Task P09.1; O12 evidence separation.
VF/reference/papers are unchanged. Zero-density/full-domain limits, broader
baseline auditing and clean-machine reproduction remain open. Fresh main
measurements must use the eight-patch binary consistently; earlier timings stay
historical and the two VF-only ablations remain unaffected.
