# M3 scope and finite campaign, declared before implementation

Base: owner's M2 commit 0a4aef8. Implement P04.1–P04.4, P05.1–P05.3,
P06.1 and correctness review/freeze P13.1. Preserve papers, decisions, theory
contracts and independent M1 reference. No M4 optimization/core or baseline work.

Name tests first: T10 sealed principal-chain endpoints, exact separators and
progress; T11 ordinary components/anti-adjacency/non-emitting layers; T12 every
fixed-k prefix and exact ID tie order; T13 2r-1 logical entries versus actual cuts;
T14 independent exhaustive truth/failure retention and deterministic reduction;
T15 complete-truth relabel/re-sort, disjoint unions, isolates and input order;
T16 strict warnings, ASan/UBSan, numeric fallback, semantic hashes, no candidate
verifier in the solver path. Retain M1/M2 tests and actual fallback regression.

Implementation: heap-backed left-first interval stack; immutable certified chain
points and interval bounds with stored endpoint counts; root [empty,V] and points
obtained by genuine certified global calls; no public arbitrary-set certificate.
Original endpoints determine lambda/terminal comparison. Exact terminal results
are sorted within their density layer and emitted until k or exhaustion. Expose
solve --k/--all, exact result records, semantic hash, per-query/event counters and
postload/postindex timing. External runner records process end-to-end time apart
from independent validation. No new benchmark budgets/parameters/dependencies.

Finite acceptance tiers in both Debug and ASan+UBSan: smoke existing named fixtures
plus K4/pendant, disjoint ties and explicit zero cases; all 1,099 labelled graphs
n=1..5 at h=2,3 (2,198 graph/h cases), all k=1..q+2, --all and all independently
constructed chain endpoint pairs; 1,000 unique seeded graph/h cases from the M1
five-family generator, n=6..8, seed 20260929, all prefixes and at least 10,000 oracle
requests; named h=4,5/h>n plus the matching higher-h seeded subset. Auto and forced
BigInt solver modes must agree; shared-domain UInt128 is exercised by M2 tests and
auto traces. Every base case is relabeled with an order-reversing large-ID map and
full truth is re-sorted before prefix comparisons. Isolate/disjoint-union properties
run on named fixtures and the first 20 seeded cases within the reference size guard.
Save graphs, exact requests/truth/outputs/traces, actual counts, failing originals
before reduction, and minimized reproducers. Exercise reducer separately with an
explicit synthetic faulty candidate; never count it as a solver failure or proof.

Four CMake profiles and production-only build; CTest, pytest, full finite solver
campaigns and M2 oracle campaigns where interfaces changed. Review executed logs
and actual call paths before marking tasks or freezing a local correctness tag.
No theoretical proof, scalability, speedup or cross-platform claim from testing.
