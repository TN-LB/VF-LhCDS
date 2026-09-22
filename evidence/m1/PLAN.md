# M1 execution scope fixed before tests

P01.1-P01.5 only. Reference implementation uses Python standard library, exact
integers/Fraction, explicit deletion subsets and proper supersets, and an
independent cardinality-line envelope. No production code or external baseline
is imported. No changes to papers/decisions/theory are planned.

Named tests: T01 normalization/IDs/isolation/zero-clique components; T02 bridged
triangles and multi-vertex maximality; T03 exact envelope samples and an outer
breakpoint absent from all induced densities. Also reference-only largest ties,
restricted/global boundaries, complete-truth relabeling, k=0 rejection, and CLI
serialization/error/size-guard tests. No production T04-T17 gate is closed.

Declared finite reference tier: all 1,099 labelled simple graphs with 1<=n<=5,
h=2,3 (2,198 graph/h cases). Check direct truth, all reference prefixes through
q+2, independent chain, sampled parametric maximal components, and every pair
of chain endpoints against exhaustive F (diagnostics only, no recursive solver).
Higher-h named K4/K5 and overlapping-clique fixtures cover h=4,5 and h>n.
Seeded supplement: seed 20260917, 100 unique graph/h cases, 6<=n<=8, h in
{2,3,4,5,n+1}; five deterministic generator families (random, planted clique,
bridged cliques, tied disjoint cliques, disconnected). The full M3 1,000-case /
10,000-query campaign is deferred, not silently replaced by this M1 tier.

The prior review witness file is absent. Search deterministically for a seven-
vertex replacement using seed 20260917, h=2 then h=3 per sampled graph, at most
10,000 sampled graphs. Save its full graph and provenance, and test the claimed
property exhaustively. This is fixture construction, not an experiment selection
rule. Do not claim it reproduces the unavailable historical witness.

Default n<=12 guard is enforced before exponential allocation/enumeration;
an explicit local max_vertices override is available. Ordinary tests do not run
large overridden truth enumeration. CLI smoke and existing CTest integration
will be run. Save any failing graph/seed/configuration before local diagnosis;
counterexamples to the proof/spec stop the affected path. Record actual coverage,
commands, logs, hashes and unrun work before marking tasks complete.
