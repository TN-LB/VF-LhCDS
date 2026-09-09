# M0 interface contract, version 1 (P00.4)

This freezes serialization and engineering boundaries under the unchanged
`ALGORITHM_SPEC.md`, D005/D006/D012 and audit O01-O12. It adds no mathematical
choice, backend, experiment parameter or theorem claim. Future implementation
must satisfy this contract; examples below are specification fixtures, not
algorithm-generated results. Mathematical/API preconditions remain in the
existing specification and architecture; they are not re-audited here.

## 1. Implementation boundary

M0 implements only `vflhcds --help` (also `help`), `print-build-info`, dispatch and
failure records. Each diagnostic takes no additional arguments. No arguments,
unknown commands and extra diagnostic arguments return `invalid_argument`.
`solve`, `oracle` and `inspect-graph` are reserved: M0 returns `not_implemented`
before reading inputs, validating their options, or opening output files. Thus
M0 does not pretend to validate k, graphs, fractions or solver results. All request
validation and mathematical behavior specified below are work for M1-M3.

M1 reference modules import only Python standard-library/reference code. External
process differential tests belong in `tests/` or `validation/`, never inside a
reference mathematical implementation. Reference counts/fractions use Python
integers and `fractions.Fraction`; the existing n<=12 default guard remains an
M1 implementation requirement.

The reserved C++ modules mirror `ARCHITECTURE.md`: `core`, `io`, `clique`, `flow`,
`oracle`, `solver`, `telemetry`, `cli`. No graph, number, certificate, clique,
network or interval implementation is supplied in M0. In particular a public
enum must not manufacture a global-containment certificate. M2 implements the
restricted/global interfaces and internal certificate construction as already
specified; M3 owns immutable principal-chain endpoints.

## 2. Canonical graph and original IDs (O01; D006/D017)

Version 1 uses an explicit vertex list and this plain-text grammar:

```text
vflhcds-graph 1
n <vertex_count>
v <original_id>                 # exactly n vertex records
...
m <edge_count>
e <original_id> <original_id>    # exactly m undirected edge records
...
```

The explanatory comments above are not file content. Counts are nonnegative
decimal integers, n>=1. IDs are signed decimal integers with numeric total order;
zero is `0`, no `+`, leading zeros or `-0`. IDs have no semantic machine-word
bound; implementations parse/compare them exactly or report a resource failure.
Text labels require offline conversion to unique integer IDs and a retained
reversible mapping. Version 1 does not accept text labels directly.

All unsigned decimal fields use `0` or a nonzero leading digit followed by digits;
no signs, exponent notation or leading zeros. The canonical byte form is ASCII,
one space between tokens, one LF after every
record including the last, no blank lines or comments. Vertex records are in
strictly increasing numeric ID order. Each edge has u<v, endpoints declared,
and edges are in lexicographic numeric (u,v) order. All counts must match records.
Self-loops, duplicate IDs, duplicate edges (including reversed duplicates),
undeclared endpoints, n=0, malformed integers, unknown versions and trailing
records are `invalid_graph`. Readers accept ASCII whitespace variation,
unsorted vertex/edge records and reversed edge orientation, then canonicalize.
Duplicate edges are
detected after orientation. Counts/record sections still have the stated order.

Internal IDs are 0..n-1 in sorted original-ID order; both directions of the map
must be retained. Never infer V from edge endpoints or remove isolates. `h>n`
is valid. Original IDs are restored in every public vertex set. A raw converter
is separate: capture the entire declared universe first, remove loops and
duplicate undirected edges deterministically, and record their counts. It must
neither invent undeclared isolates nor lose vertices occurring only in loops.
The canonical reader rejects loops/duplicates rather than silently normalizing
raw data. No converter or reader is implemented in M0 (P02.1 remains open).

`graph_sha256` is the SHA-256 of the canonical bytes above, including the declared
IDs and isolates. It excludes input record order and whitespace variation after
normalization. The graph hash does not include h. No hash replaces full set
equality. Resource exhaustion must not truncate an ID, count, set or graph.

## 3. Requests and ordering (O03/O05/O08)

The implemented CLI will accept:

```text
vflhcds solve --graph G --h H (--k K | --all) [--core-reduction off] [--output P]
vflhcds oracle --graph G --h H --lambda A/B [--x X --y Y] [--output P]
vflhcds inspect-graph --graph G
```

Exactly one of `--k` and `--all` is required for solve; there is no implicit k.
H and K are exact positive decimal integers with H>=2, K>=1. `--k 0`, negative,
fractional, floating, missing/duplicate/unknown options and both modes together
are `invalid_argument`. No undocumented MAX_H or numeric truncation is allowed.
Unsupported capacity diagnostics/core-on/tie-inclusive/parallel options are
rejected, not silently enabled. Core defaults to off; capacity dispatch in M2
defaults to true auto (checked 128-bit plus actual arbitrary precision, D005).

Solve emits exactly the first min(k,q) LhCDSes, or all q with `--all`. Compare
density fractions exactly, decreasing; equal densities compare sorted original-ID
vectors lexicographically (proper prefix first). Never use lexicographic ties
for the oracle's cardinality-based largest optimum. A kth-density tie does not
expand fixed-k output. k>q is successful exhaustion. Preserve zero-density and
isolate solutions. No solver-side candidate verifier may decide emissions.

Oracle lambda accepts A/B with arbitrary-size decimal A>=0 and B>0; reduce it
exactly before use, including 0/1. X and Y are paths to set files: the first line
is `vflhcds-set 1`, followed by `n <count>` and that many `v <original_id>` records
with the same ID/whitespace/order rules. Empty sets have count 0. IDs must be
declared in G and unique; X subseteq Y. Invalid sets/lambda are `invalid_argument`;
file access failures are `io_error`. Both bounds or neither must be supplied.
No bounds means a certified full-graph global query; arbitrary CLI bounds always
mean restricted. Empty/equal-X results are valid outside separator queries.

Validate command syntax/domains before graph access, then graph, then bound
membership/nesting. Do not pre-create/truncate the output while validating.
--output defaults to stdout; `--output -` explicitly selects stdout. It must
not name an input file (including an alias/symlink to it); reject as
`invalid_argument`. No runtime can claim a successful unimplemented operation.

## 4. JSON and completion protocol

Result output is UTF-8 JSON Lines with LF endings; no status or human text is
mixed into it. A solve record has exactly these keys, in this order for canonical
serialization (the order of keys is not a mathematical property):

```json
{"rank":1,"h":3,"vertex_count":3,"clique_count":"1","density_num":"1","density_den":"3","vertices":[1,4,9]}
```

Ranks are consecutive from 1, vertex_count equals array length, and vertices are
distinct sorted original IDs. Counts and fraction components are exact decimal
strings; density is nonnegative, reduced, positive denominator (zero is 0/1).
Density equals clique_count/vertex_count. Rank, h, vertex_count and vertex IDs
are JSON integer tokens (no exponents); consumers must parse them exactly, not
through IEEE-754. No bounded-ID conversion or floating density is canonical.
Unbounded integers are constrained only by available resources.

An oracle emits one record, even for the empty set, with these ordered keys:
`scope` (`global` or `restricted`), `h`, `lambda_num`, `lambda_den`, `vertex_count`,
`clique_count`, `vertices`. Fractions/counts are strings as above. It has no rank
or density (density of the empty set is undefined). `inspect-graph` emits one
record with `graph_sha256`, `vertex_count`, `edge_count`, `vertices` in that order;
it performs no clique enumeration or solver work.

For each algorithm/inspection invocation, stderr ends with exactly one JSON
status record and no human diagnostics. Its minimum fields, in order, are
`schema_version` (1), `status`, `complete`, `output_count`, `semantic_sha256`.
Failure messages may later be added as a JSON `message` string. In M0, failure
output_count=0 and semantic_sha256=null; no timing/counter measurements exist.

| Status | Exit | Meaning |
|---|---:|---|
| completed | 0 | Requested operation finished; complete=true, including k>q exhaustion |
| invalid_argument | 2 | CLI/request domain error |
| invalid_graph | 3 | Readable graph violates the graph contract |
| io_error | 4 | Input access or result/status write/flush/commit failure |
| resource_limit | 5 | An explicit resource limit was reached; no alternate answer |
| oom | 6 | Allocation failure; status output is best effort |
| incomplete | 7 | Controlled cancellation or other unfinished execution |
| not_implemented | 8 | Known command has no implementation |
| internal_error | 9 | Unexpected exception or invariant failure |

Only completed has complete=true. For fixed-k, this means the requested prefix
is complete, not necessarily that the full family/chain was traversed. Future
solve status additionally includes `termination`: `k_reached` when the limit
stopped traversal, or `exhausted` when traversal ended; do not infer q from a
stopped prefix. Successful oracle and inspection use `exhausted`.

File results are written to a sibling temporary file and committed only after
successful computation/serialization/flush; pre-existing output is preserved on
failure. Stdout can contain partial lines on failure; it is usable as completed
output only with exit 0 and a completed status record. output_count counts fully
serialized result records, not necessarily committed file records. Failures have
semantic_sha256=null. A kill/crash/missing status is incomplete even if result
bytes exist. An external runner records timeout as `timeout` and an OS-proven
OOM as `oom`, retaining the actual native exit/signal; the executable does not
invent timeout budgets, synthesize an exit code after a kill, or infer OOM from
every SIGKILL. Exit status and final I/O success are required along with JSON.

The successful solve semantic hash is SHA-256 of: one compact JSON header line
`{"schema_version":1,"graph_sha256":"<hash>","h":H}`, then the canonical result
lines above. Every line ends with LF; no spaces appear outside strings. It covers
graph identity, h, ordered sets, counts and exact densities. Requested k/mode,
backend, traces, timing and validation labels are excluded: requests yielding the
same prefix have the same hash. Different prefixes must be compared as prefixes,
not whole-file hashes. Oracle/inspection semantic_sha256 is null in version 1;
oracle differential checks compare exact fields plus graph/bounds directly.
Hash generation and successful result writers are deferred to M3/P06.1.

## 5. Timing and counters (O09/O11/O12; D013/D025)

Use monotonic wall durations, in seconds, for telemetry only. `T_e2e` is measured
by the external runner from process launch to successful process completion
after result serialization/flush (includes I/O, enumeration, algorithm and
output). `T_postload` starts after the normalized graph and reversible map are
loaded; `T_core` starts after the initial clique/incidence index is ready. Both
end after result serialization/flush. These nested scopes are not added together.
Post-index scope is diagnostic until matching baseline scopes are audited.
Build-info/help/stub runs do not publish algorithm timing measurements.

Offline raw normalization and subsequent external validation have separate time
and RSS. Native baseline candidate verification remains inside algorithm time.
Unavailable/not-instrumented fields are null or absent, never fabricated zero.
Future status may attach `timing` and `counters` objects; per-query telemetry is
separate from canonical result lines/hashes. No experimental limits, threads,
datasets, parameter grids, seeds or repeats are chosen by this contract.

| Counter / trace | Precise event or scope |
|---|---|
| logical_interval_queries | Increment once on entry to each original ChainInterval query, including zero lambda and queries needing no cut; standalone oracle calls do not increment it |
| mincut_calls | Increment at entry to each actual positive-network max-flow execution; not at oracle dispatch or graph construction; retries count actual executions |
| original_interval_size | Per query, cardinality of original Y minus X |
| oracle_interval_size | Per query, cardinality of Y_oracle minus X; same in basic M3 |
| cliques_scanned | Per query, number of materialized clique records inspected for footprints, including records rejected by bound checks; repeated inspections count again; initial enumeration separate |
| unique_footprints | Per query, number P of distinct nonempty aggregated footprints before network construction; zero is measured only if the aggregation ran on an empty family |
| forward_nodes | Per constructed network, N+P+2 including source/sink |
| forward_arcs | Per constructed network, N+P+sum of footprint sizes; excludes residual reverse arcs |
| residual_arcs | Per constructed network, twice forward_arcs for the paired residual representation; not a theorem network-size counter |
| capacity_bit_length | Per constructed network, bit length of the maximum initial forward capacity, including exact finite infinity; not machine type width or a float estimate |
| capacity_backend | Per actual flow execution, `uint128` or `arbitrary_precision`; configured `auto` is a policy, never evidence that a backend executed |

For zero/equal-bound oracle shortcuts, network/footprint/backend fields are null
when that stage was bypassed; actual mincut_calls is 0. Queries that fail keep
their attempted-work counters and failure status. Counter integers must not wrap.
Network size/bit length are per execution, not additive run totals; summed run
totals are defined only for event counts (logical queries, mincuts, clique scans).
Optional cache counters appear only once a cache exists. For complete unmodified
recursion only, logical queries equal 2r-1; this is neither a mincut-count identity
nor an O(k) bound. M0 measures none of these algorithm counters.

Validation labels distinguish definition-checked, structural-checked and
cross-implementation agreement. Completion is not a maximality certificate, and
finite tests are not a theorem proof. No production obligation is closed by M0.
