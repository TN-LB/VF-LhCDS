# M2 execution scope declared before implementation/testing

P02.1-P02.3 and P03.1-P03.5 only. Preserve papers, accepted decisions, theory,
and the committed independent M1 reference. No solver recursion, core reduction,
parallel backend, baseline, optimization or final experiment configuration.

Implementation: exact original IDs/counts/fractions with Boost.Multiprecision
cpp_int, checked native unsigned __int128 flow, one generic iterative-stack
Dinic, one deterministic materialized clique/incidence backend, aggregated
footprints, largest_restricted and a certified full-graph global_F. Full-graph
certificates have no public arbitrary-bound constructor; chain/core certificate
creation remains in M3/M4 orchestration. No enum or subset check certifies
arbitrary bounds. Minimal oracle/inspect CLI; solve stays unavailable.

Tests named before implementation: T01 graph/ID/checksum/set domains; T04 cliques,
all-subset counts/incidences; T05 exact fraction/signed objective/checked limits
and genuinely executed automatic >128-bit fallback; T06 all-subset footprint
identity; T07 independent tiny-cut flow/residual tests on both capacity types;
T08 restricted/global empty/equality/zero cases; T09 exact largest set/ties.

Finite campaign fixed now: all n=1..5 labelled graphs at h=2,3 (1,099 graphs /
2,198 graph-h cases), querying independent cardinality-line samples and all
principal-chain endpoint pairs. On all n<=4 graph/h cases also enumerate every
nested X,Y and every S subseteq Y\X for the footprint identity. Seeded tier:
seed 20260922; 1,000 distinct graph/h cases from the existing M1 five-family
generator (n=6..8, within the planned n<=10 limit), at least 10 queries per case
including global, arbitrary restricted and >128-bit rational queries. All these
queries are tested in auto and forced arbitrary-precision modes; checked-128 is
compared where safe. This does not implement or close M3 fixed-k/end-to-end tests.
Include existing named h=4,5 and h>n fixtures. Save every case/query, seed, result,
failure and original/minimized reproducer; do not silently omit failed cases.

Debug CTest/pytest plus ASan+UBSan build/tests and the oracle differential tiers
run before acceptance. Release and RelWithDebInfo are build profiles, not speed
claims. No benchmark dataset/resource/thread/timeout decisions are made here.
Guard graph-size/index allocations with explicit resource failures; exact
preflight must select actual multiprecision before fixed-width construction.
