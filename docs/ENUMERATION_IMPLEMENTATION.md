# Materialized clique enumeration choices

Scope: the M5 index-construction blocker and authorized preservation plan in
`evidence/m5/phase-diagnostic-20261003/ENUMERATION_PLAN.md`. Evidence belongs in
`evidence/m5/enumeration-20261003`. This argument does not replace the manuscript,
audit or independent mathematical reference, and is not a claim of unrun tests.

The backend still materializes every h-clique and its vertex-incidence entries.
`CliqueEnumeration::Combinations` remains the constructor and CLI default.
`CliqueEnumeration::Adjacency` selects the new explicit-stack traversal. Both
append through `MaterializedCliques::append`; storage, original vertex universe,
clique IDs and downstream APIs are unchanged. No external method is imported.

## State invariant and exact preservation

For an increasing clique prefix P, a stack frame owns sorted common-neighbor
candidates larger than the last prefix vertex, and the next candidate position.
The initial frame contains all graph vertices with an empty prefix. A chosen
vertex v extends P; intersecting the remaining candidate suffix with sorted N(v)
produces exactly the vertices that extend P+v. A branch with fewer candidates
than unfilled positions cannot contain an h-clique. On backtracking, the parent
retains its next position and the child prefix vertex is removed once.

The constructor rejects h<2 and unknown enumeration values, and returns an empty
clique family for h>|V| before converting h to size_t. Thus h is exact and has no
new fixed limit. Each loop starts with |P|<h and next<=candidate count, so the
remaining-size subtractions are nonnegative. A size-h prefix is appended and
popped immediately. The explicit stack avoids a new native call-stack bound.

Every emitted tuple is an h-clique by the prefix invariant. Conversely, the
sorted vertices of any h-clique define one unique path, and its remaining members
are always present in the successive common-neighbor candidates. No cardinality
prune removes that path. Increasing siblings and depth-first traversal order all
size-h leaves lexicographically. This is exactly the old combination order after
discarding noncliques. Both builders therefore produce identical tuple sequences,
incidence-ID sequences, clique degrees and induced-subset counts.

Since the graph and materialized representation are unchanged, all subsequent
footprint keys/multiplicities, capacities, residual decisions, chain endpoints,
ordinary components, density/ID ordering and fixed-k prefixes see the same inputs.
No oracle, flow, recursion, extraction or serializer implementation is modified.
The output schema, canonical semantic hash and clique/query counter meanings are
unchanged. The argument proves preservation of this enumeration transformation;
finite implementation tests do not prove the full mathematical theorem.

## Cost and controls

Adjacency mode avoids descending prefixes that cannot form a clique, but still
materializes the entire family. Candidate intersections and stack-owned buffers
add work and temporary memory; there is no universal speed/memory guarantee.
Dense graphs can still contain combinatorially many cliques. No degeneracy order,
parallel code, streaming backend, cache, new flow algorithm or heuristic is added.

`solve` and `oracle` accept `--clique-enumeration combinations|adjacency`.
The existing core and footprint switches remain independent and retain their
defaults. The external experiment runner accepts optional VF `enumeration` in
`options`; omitted means the historic combinations path and sends no new CLI flag,
preserving compatibility with previously pinned binaries. New diagnostic configs
must record explicit feature choices. Mode selection never enters semantic hashes.

## Verification design

`tests/enumeration_equivalence.hpp` constructs both representations for each
M2/M3/M4 probe case, requires exact tuple/incidence equality, then returns adjacency
for the existing queries. These are production control comparisons, not expected
mathematical truth. Unchanged Python combination enumeration, all-superset truth
and line envelopes continue to supply that truth in the existing campaigns.

T04-ADJ/T04-EDGE check ordered tuples, exact IDs, all-subset counts, zero/h>|V|,
large original IDs, a depth-128 complete-graph path and real automatic capacity
fallback. T04-CLI compares default/control/adjacency canonical output, non-timing
status, all existing M4 modes and argument failures. T04-HARNESS checks both old
and explicit configurations and the actual native command. Full Debug/sanitizer
corpora and Release CLI tests plus comparison to saved pre-change responses are
execution gates, documented with results only after they run.
