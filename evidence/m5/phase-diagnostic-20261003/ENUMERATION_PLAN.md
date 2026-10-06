# Proposed materialized-enumeration repair — not implemented

This plan follows the measured index-construction timeout in
[the phase report](REPORT.md). It is an implementation preservation argument and
test plan, not a new theory audit, manuscript revision or claim that tests passed.
The currently authorized phase diagnosis and preparation of this plan are done;
production changes have not started.

## Proposed change and independence

Retain one materialized tuple/incidence backend. Add a selectable way to build
exactly that same representation by extending a clique prefix using its common
neighbors, instead of visiting every h-subset of V. Derive the procedure directly
from the clique definition and the repository's sorted adjacency lists; no IPPV
or DCLDS algorithm code/technique is being imported. Preserve D012/D029.

Keep the current combination enumerator as the explicit off/control path and
initial default. Proposed implementation selector:
`--clique-enumeration combinations|adjacency`; no automatic heuristic selection.
This switch selects an equivalent computation, not a new h/k/output policy or
final experimental parameter choice. Do not change a benchmark default silently.

For a strictly increasing prefix P, maintain the sorted candidates C of vertices
larger than the last prefix member and adjacent to every member of P. Initially
P is empty and C is all vertices. Visit v in C in increasing order. Descend with
P followed by v and candidates equal to the suffix after v intersected with
N(v). Emit at prefix size h. If too few candidates remain to reach h, stop that
branch. Use an explicit depth-first stack so valid large h does not create a
new recursive C++ call-stack limit. No degeneracy reordering, parallel traversal,
streaming storage, caching, core pruning or h-specific external backend is added.

## Preconditions and preservation argument

- Existing `Graph` gives a finite simple graph, distinct internal IDs in increasing
  original-ID order, and sorted adjacency lists. Preserve all declared vertices.
- Induction on P: it is a clique; C consists exactly of vertices extending it to
  a clique. Intersecting its suffix with N(v) establishes this invariant for P+v.
- Soundness: each emitted h-tuple is a clique. Completeness: for any clique with
  sorted vertices v1,...,vh, vi always belongs to the candidates along its unique
  prefix path. Cardinality pruning cannot remove this path. Strictly increasing
  prefixes prevent duplicate output.
- Increasing sibling traversal and depth-first extension emit fixed-size tuples
  in the same lexicographic order as the old combination scan with noncliques
  removed. Thus clique IDs, each vertex's incidence-ID sequence, degrees and
  every induced clique count are unchanged, not merely the multiset of tuples.
- Retain h>=2 checks and the h>|V| early return before converting to machine-size
  storage. Preserve zero-clique graphs, isolates, exact counts and resource-error
  behavior. Integer arithmetic and all downstream flow/tie/recursion logic stay
  unchanged. Preserve original chain endpoints and original-graph extraction.
- Both builders append through the same materialization routine. The stored
  tuple/incidence equality implies identical footprint records and multiplicities
  for every valid query. With unchanged exact oracle and solver code, output
  semantics and semantic hashes are preserved. Timing/implementation-mode metadata
  remain outside canonical hashes.

This argument concerns the new enumeration mechanism only. It does not prove the
full mathematical theorem or promise a particular performance improvement.

## Expected file/interface changes

`include/vflhcds/clique/materialized.hpp` and `src/clique/materialized.cpp`: mode
selector plus one new traversal inside the existing backend; keep legacy builder.
`src/cli/dispatch.cpp`: validate/pass the selector for solve and oracle and update
help. Probe adapters under `tests/` and campaign drivers under `validation/`:
exercise both selectors against independent expected truth and each other.
`experiments/run.py`: accept/record the explicit selector, preserving legacy
configuration meaning. Interface/architecture/build documentation: explain the
selector and keep one materialized backend. No proof paper or reference algorithm
change is needed. Change this list only for a demonstrated implementation need.

## Required verification before acceptance

1. Name new T04 equivalence checks before implementation. Compare complete ordered
   tuples, exact incidence IDs, degrees, degree sum and all induced-subset counts
   against the unchanged Python combination reference and old builder. Include
   complete/edgeless/disconnected graphs, isolates, original-ID relabeling, h=2,
   h=3, higher h and h>|V|, using the existing frozen fixture/seed manifests.
2. Reuse M2/M3/M4 exhaustive-small, seeded, higher-h and smoke corpora. Check
   downstream footprints/global/restricted answers, all fixed-k prefixes and all
   existing core/footprint modes (T06-T17). Compare semantic hashes, excluding
   only documented timing/backend metadata. Keep failing seeds and reproducers.
3. Run applicable CTest/pytest and Debug/Release/ASan+UBSan builds. Check numeric
   limits and real arbitrary-precision fallback on the existing corpus. No TSan
   claim or new parallel execution is involved.
4. Freeze a new diagnostic configuration before running the optimized path on
   exactly the same CA-GrQc graph, h=3,k=5, one worker and 60-second guard. Reuse
   all old failures as censored controls; do not replace them or calculate a
   speedup from a timeout. Validate any completed output externally and label
   structural versus cross-implementation agreement separately.
5. If another phase becomes the next blocker, preserve that outcome and stop at
   the owner's boundary. No final benchmark policy, scalability claim, new flow
   algorithm or further optimization is bundled with this repair.

Alternative: keep the exhaustive enumerator and change the resource/dataset
policy before a formal campaign. That leaves the identified enumeration cost
unchanged. Recommended next action is the single equivalent enumeration change,
retaining the old path and executing its verification gates. This is still a
proposal awaiting the owner's continuation decision, not completed work.
