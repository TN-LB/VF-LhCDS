# P13.1 code/evidence correctness review

Scope: exact unoptimized M3, after M1/M2 integration and before any M4 work.
This is a separate review pass by the implementing assistant, not independent
human sign-off. It checks the unchanged manuscript/specification against actual
code and executed evidence. It is not a new mathematical audit or theorem proof.

## Findings

**R01 — resolved, medium severity: moved certificate payload could invalidate its promise.**
An ordinary C++ move of `CertifiedGlobalRequest` moved its bound vectors but left
the original owner pointer usable. Reusing that object for a global zero query
could return empty. The old type had no invalid-state check or documented move
restriction. The new chain values needed the same invariant protection.

Reproducer: `token_move_reproducer.cpp`. The recorded original execution
(`token-move-before.json`) exits 1 with transferred size=2, original size=0.
The fix makes certificate payload, chain sets/counts and interval endpoints const:
assignment is disabled and moving copies the immutable payload, preserving source
validity. `tests/m3_solver.cpp:certificates` exercises moved certificates, points
and intervals, as well as static nonconstructibility/nonassignability and foreign
owner rejection. The same standalone reproducer then exits 0, both sizes=2
(`token-move-after.json`). All acceptance builds and campaigns use the fixed types.

No open correctness finding, new proof/spec conflict, silent numeric overflow or
solver/reference mismatch remains in the executed scope. This assertion is
conditioned on the listed finite coverage and reviewed call paths, not all inputs.

## Refinement and call-path checks

| Obligation | Code inspected / reason | Executed evidence |
|---|---|---|
| O01 | Unchanged `Reference`, direct maximality over every proper superset; declared Graph universe and exact original IDs | M1 pytest; M2 primitive/CLI campaigns; complete M3 families including zeros |
| O02 | `solve` uses ordinary components and anti-adjacency to all of X; no invented boundary-clique exclusion | Bridged triangles, K4/pendant, full-family direct comparisons |
| O03 | Chain tokens arise only from proved extremes or actual certified global F; independent expected chain is the cardinality-line envelope | T10 all independent endpoint pairs, outer-breakpoint witness; M2 largest-set tests |
| O04 | `ChainInterval::lambda`, `separator_request`, `separate` preserve original endpoint counts/bounds and assert strict progress | Every recorded separator/trace checks exact lambda, original counts, global F and consecutive-pair terminality |
| O05 | Private immutable certificate payload; sealed same-owner chain points; arbitrary CLI X/Y still restricted | Type/owner/move tests and retained M2 T08 cases |
| O06 | Existing footprint and generic Dinic construction unchanged; boundary footprints, L=N+1, exact finite infinity retained | Full M2 oracle regression tiers and tiny-cut tests under both capacity types |
| O07 | `solve`: terminal iff Z==original Y; original G[Y minus X]; retain components only if no edge reaches any X vertex | T11 traces explicitly include a rejected pendant increment and non-emitting terminal |
| O08 | Explicit stack pushes right then left; layer sorting uses original-ID-equivalent vectors; stop immediately at k | Every prefix through q+2, transformed/re-ranked complete truth, no eager right-query unit trace |
| O09 | One logical event at original interval entry; actual cuts accumulated separately, zero-query fields null | Every full run compared with independent 2r-1; per-query totals and zero cases |
| O10 | Core reduction and core-origin certificates absent; CLI accepts only core off | Deferred to M4/T17; no implementation-tested claim |
| O11 | M2 exact fractions/counts/preflight and genuine cpp_int flow retained; counters also use exact integers | Numeric-limit unit tests, real >128-bit automatic global queries, auto/BigInt solver agreement, sanitizers |
| O12 | Complete output checked against definitions, not only density/connectivity; validation outside measured child process | External runner success/error manifests; frozen cases/results/command/source hashes; experimental shared smoke deferred |

Reviewed production path:
`run_cli -> solve -> ClosureOracle::separate -> separator_request -> global_F ->
largest_restricted -> aggregate_footprints -> Dinic<Capacity>`, followed by ordinary
component/edge extraction and exact serialization. The count of an emitted set
is used to populate its record, not to accept/reject its maximality. No production
target imports, starts or links the Python reference/validation code. The only
Python discovery in CMake is inside BUILD_TESTING. The production-only build
omits every probe/test and executes solve successfully.

Errors preserve available work counters and never return a successful semantic
hash. Output files are committed only after complete successful serialization.
Resource/OOM tests are explicit injection/index-domain tests, not an OS pressure
campaign. Cancellation is cooperative at safe boundaries; no immediate interrupt
inside clique enumeration or a flow call is promised.

## Freeze gate and limits

Acceptance evidence is `accepted/commands.json`, its per-command stdout/stderr,
source snapshot and per-tier cases/results summaries. The earlier `final/` run is
retained as pre-R01 evidence, not substituted for acceptance of the fix. The
freeze operation must verify command exits, source hashes, protected papers and
reference bytes, and a clean diff check before creating the local annotated tag.

No optimization, external baseline, benchmark parameter choice, speedup or
scalability assertion enters this review. Extended n<=12 campaigns, GCC/Linux,
TSan/parallel code, OS OOM stress and baseline agreement are outside executed scope.
