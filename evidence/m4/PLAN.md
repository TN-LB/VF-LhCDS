# M4 declared work and gates

Start from clean M3 evidence commit 5802d5a and correctness tag
v0.1.0-m3-correctness. User requires stopping the whole task on a blocking
condition, new theory conflict or consequential decision; do not bypass it.

P07.1-P07.3 / O10,T17: deterministic current h-clique-degree queue peeling,
invalidate each clique once, update remaining vertices only. For a certified
positive query restrict only its search upper bound to the original bound
intersected with the ceil(lambda) clique core of the ORIGINAL graph. Zero bypasses.
Recompute from the full index per query; no cross-threshold cache. Preserve
original chain endpoints, lambda, terminal test and ordinary extraction graph.
Default core off; explicit safe mode. Write the preservation argument before code.

Named tests first: audit-C K4 disjoint triangle+pendant (non-chain root core and
lower-density pendant retention); cascades and one invalidation per clique;
h=3 ordinary degrees are not clique degrees; zero/empty/huge exact thresholds;
decreasing thresholds recover removed vertices; foreign/moved certificates;
all subset definition cores; exact global and separator sets; all fixed-k prefixes,
full output/hashes/traces across modes, relabeling, boundary cliques and fallback.

P08.1: frozen local profile_workload.json before production edits. Measure the
M3 baseline before selecting ONE extra bottleneck fix. No baseline techniques,
parallelism, new dependency, heuristic or experimental conclusion. Record the
selected argument, switch, full corpus equality, overhead and actual time/RSS.
The diagnostic workload is not the still-unfrozen M5 benchmark configuration.

Acceptance: strict-warning Debug/ASan+UBSan/Release/RelWithDebInfo builds and
CTest; unchanged 74 reference tests; all M3 exhaustive-small/seeded/higher-h/smoke
cases reused, same truth and prefixes, both numeric policies, core off/safe and
the selected optimization off/on. Independent core and certified oracle tests,
retained M2 regressions where affected. Save original failures and logs before
fixes/reduction. Stop if a new proof/spec conflict or blocker appears.

Keep papers, decisions, theory/audit, independent reference and M3 evidence/tag
unchanged. Update tasks/traceability only for actual evidence. M4 needs no new
Git tag; leave reviewable working-tree changes unless a commit is requested.
