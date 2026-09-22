# Independent exact reference (M1 / P01.1-P01.5)

Python >=3.10, standard library at runtime and pytest for tests. No C++ binary,
extension, production import, flow code, external baseline or production build
is used. Activate the M0 environment if needed: `. .venv/bin/activate`.

`graph.py` preserves an explicitly declared integer-ID universe and reversible
bit-position mapping. `normalize_graph` removes raw loops/duplicate undirected
edges with counts; the canonical reader in `io.py` rejects them. Both retain
isolates. `Graph` stores sorted original IDs and ordinary adjacency; empty graphs,
duplicate declarations and undeclared endpoints are errors. Empty sets are valid
oracle sets, are not connected/compact, and have undefined density/compactness.
Disconnected nonempty sets have compactness zero per Definition 1.2.

`direct.py` combination-enumerates cliques, caches induced counts for one graph/h,
and checks the definitions using all deletion subsets and all proper supersets.
It uses Python integers/Fraction exclusively for semantic decisions. `Reference`
rejects n>12 before exponential allocation; `max_vertices=N` (CLI
`--max-vertices N`) is an explicit local override, never an implicit relaxation.
This guard does not promise every n=12 workload will be fast. h>n is valid and
produces zero cliques. Numeric IDs, h, k and thresholds have no machine-word cap;
interpreter decimal-conversion/resource limits produce explicit failure.

`parametric.py` enumerates all feasible subsets, including empty, maximizes the
signed scaled objective, unions all ties and checks the union is optimal.
`exhaustive_F` means full-graph global; `exhaustive_restricted` always labels its
result restricted, including equal bounds and full bounds. Arbitrary bounds
are never promoted to a containment certificate.

The principal chain is generated independently: cardinality maxima M_j, all
nonnegative line intersections, zero, sentinel mu(V)+1 and exact midpoints.
Only after the chain sets are found are outer breakpoints reported. Neither
direct LhCDS enumeration nor principal-chain generation uses separator recursion.

Python example (with `reference` on the import path):

```python
from fractions import Fraction
from vflhcds_reference.graph import normalize_graph
from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.parametric import exhaustive_F, cardinality_line_chain

graph = normalize_graph([1, 4, 9, 20], [(1, 4), (1, 9), (4, 9)]).graph
ref = Reference(graph, h=3)
truth = [graph.ids(mask) for mask in direct_lhcds(ref)]
largest = graph.ids(exhaustive_F(ref, Fraction(1, 3)).largest)
chain = cardinality_line_chain(ref)
```

## CLI and serialization

From the repository root:

```sh
PYTHONPATH=reference python -m vflhcds_reference truth --graph reference/fixtures/bridged_triangles.graph --h 3 --all
PYTHONPATH=reference python -m vflhcds_reference truth --graph reference/fixtures/triangle_and_isolate.graph --h 3 --k 1
PYTHONPATH=reference python -m vflhcds_reference oracle --graph reference/fixtures/triangle_and_isolate.graph --h 3 --lambda 1/3
PYTHONPATH=reference python -m vflhcds_reference chain --graph reference/fixtures/triangle_and_isolate.graph --h 3
```

Canonical graph/set syntax is the frozen M0 format in
`docs/INTERFACE_CONTRACT.md`. `oracle --x PATH --y PATH` explicitly requests
restricted maximization; neither bound means global. `truth` requires exactly
one of `--all` or `--k K`, K>=1. Duplicate/unknown options and floating inputs
are errors. `--seed S` records input-generation provenance only; it does not
change the algorithm. Hand fixtures use null seed; seeded cases carry actual
generator seeds and metadata. `--output PATH` is optional (default stdout).

This reference CLI emits **one JSON envelope line**, not the production CLI's
result stream. The envelope carries schema_version=1, kind (`reference_truth`,
`reference_oracle`, `reference_chain`), canonical graph hash, original graph,
h, seed and the requested results. Truth contains ordered `results` records
using the frozen rank/count/exact-density/vertex fields. Oracle includes scope,
lambda, bounds, signed objective_scaled (denominator is lambda_den), all tied
maximizers and the largest set. Chain includes exact breakpoints, cardinality
maxima, intersections, sentinel and samples. Zero is 0/1; no floating density
enters output ordering. JSON integer IDs must be parsed exactly by consumers.

A separate stderr status record reports completed/invalid_argument/invalid_graph/
io_error/resource_limit/oom/incomplete/internal_error with exit codes 0/2/3/4/5/6/7/9.
output_count counts complete envelope lines (normally one); semantic_sha256 is
null, since M3 production output hashing is not implemented here. Help is a
diagnostic and prints no algorithm status. Input syntax/domain errors are checked
before graph access. A sibling temporary file is replaced after successful
serialization; earlier validation/computation/write failures preserve existing
output. Input/output aliases (including hard links/symlinks) are rejected.
Consumers require successful exit and completed status; no partial output is an
exact completed result. CLI tracebacks are not mixed into its result JSON.

## Fixtures and executed coverage

`fixtures/named_truth.json` contains 11 hand-specified cases with exact ranked
expectations. `outer_breakpoint.json` is a seven-vertex T03 witness found with
seed 20260917; its breakpoints are 13/6 and 2, and no induced subset has density 2.
The historical `review/math_sanity_results.json` was absent; this is explicitly
a new reconstruction, not that unavailable historical fixture. Its generating
script is `scripts/find_reference_outer_witness.py`.

`generators.py` supplies all labelled n<=5 graphs and deterministic seeded tiny
families. `validation/reference_campaign.py` checks direct maximal compact sets
against parametric components, hierarchy leaves against direct truth, chain
coverage on a second grid derived from deletion compactness, all chain pairs,
and complete-truth relabeling followed by re-sorting/prefix selection. It writes
every completed case and retains original/minimized failures if any. The failure
reducer keeps the same check ID and h while deleting edges/vertices; it is not
the future production P05.1 differential failure harness.

```sh
python -m pytest reference/tests -q
PYTHONPATH=reference python validation/reference_campaign.py --tier exhaustive-small --output-dir /tmp/m1-exhaustive-new
PYTHONPATH=reference python validation/reference_campaign.py --tier seeded --output-dir /tmp/m1-seeded-new
```

Campaign output directories must not exist, so a rerun cannot silently overwrite
evidence. The declared M1 scope is in `evidence/m1/PLAN.md`; actual commands,
coverage and limitations are in `evidence/m1/REPORT.md`. Finite reference checks
are not a proof or production correctness claim. M2/M3 numeric/flow/solver tests,
full release seeded tier and production sanitizer campaign remain future work.
