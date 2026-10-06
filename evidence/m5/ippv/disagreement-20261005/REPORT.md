# CA-GrQc disagreement: correct result, cause and repair — 2026-10-05

**The disputed VF set is correct; the old IPPV output omits a valid higher-density
LhCDS.** The finite-instance certificate and controlled replays below establish
this conclusion. Patches 0006/0007 repair the baseline defects; production VF,
the independent reference, accepted semantics and all four papers are unchanged.
This repair is complete within the recorded scope. M5 remains incomplete and
the stopped benchmark has not resumed.

## Which result is correct

The original disagreement is CA-GrQc h=3,k=20, seed 20261003, repeat 0 from D030.
Both programs return 20 sets with cutoff density 10/3. VF also returns this set
above the cutoff, which IPPV omits:

```text
729 733 774 776 1597 2298 2299 2300 2301 2302 2303 2311 2314
```

It has 13 vertices, 41 edges, 56 triangles and density **56/13**. Checking just
those counts would not establish correctness. Two independent checks go further:

1. The unchanged direct-definition reference, with an explicit local guard of
   13 vertices, checks all **8,192 deletion subsets**. Minimum deletion loss per
   deleted vertex is exactly 56/13. Thus the connected candidate is self-compact.
2. `certify_original.py` independently enumerates all **48,260 triangles** of the
   original 5,242-vertex graph and constructs an integer closure certificate at
   theta=293607/68159 < 56/13. A feasible flow and cut both have value **537086985**,
   certifying a global maximizer F of mu(S)-theta|S|. F has 692 vertices; the
   candidate is exactly one ordinary connected component of G[F].

Why this checks global maximality: any 56/13-compact set W must lie in F. If
U=W\F were nonempty, clique supermodularity and compactness would give
mu(F union W)-mu(F) >= mu(W)-mu(W intersect F) >= (56/13)|U|. Adding U would then
strictly improve the objective at theta, contradicting the certified optimum.
Every connected compact superset of the candidate therefore lies inside its
component of F, which already equals the candidate. No proper connected compact
superset exists in the original graph.

The separate `verify_evidence.py` re-enumerates triangles, checks every stored
flow allocation and capacity/conservation bound, recomputes the cut, traverses
the component, and rechecks every deletion without running the certificate's
flow code. It calls neither native solver. This is an exact certificate for the
disputed set on this graph, not a new proof of the general theorem or exhaustive
truth for the whole original top-20 list. The initially attempted 5-core bound
alone was inconclusive and remains labelled so in its saved record.

## Direct cause: IPPV-B07, fractional capacity truncation

`Graph::verify_LhCDS_small` computes rational verification capacities using
double, then passes them to `Network::AddEdge(..., const long capacity)`. The
conversion discards fractions. In the original case, the intended sink capacity
is `3*(56/13 - 1/N^2)`, approximately 12.9, but the network receives **12**.
Boundary-clique arc weights `h/r` and their source totals can be fractional too.
The altered network can leave an outside neighbor on the reachable side and
reject a valid candidate. The saved old trace prints `774 480` at that rejection.

Patch **0006-exact-verification-capacities.patch** keeps the same network,
epsilon, candidate procedure and Boost max-flow implementation. For candidate
clique count C, size n, verifier size N and boundary-footprint sizes r, it takes
a common integer scale divisible by n*N^2 and all r. The sink becomes exactly
`scale * h * (C*N^2-n)/(n*N^2)`; unit/reverse/partial-clique/source capacities all
use that same scale. Positive common scaling preserves the intended flow/cut
problem. No floating capacity decision or missing-output synthesis is introduced.

The new external header `ExactVerification.h` computes scale/products with
existing Boost cpp_int, then checks every conversion and the total-source bound
against the existing signed-long flow domain. Unsupported magnitudes throw an
explicit error; they do not wrap or round. This is exact construction inside the
existing bounded flow backend, not arbitrary-precision execution of the entire
baseline. Other floating pruning/bounds and unused legacy verifier overloads
remain unaudited limitations. Production VF's separate D005 backend is unchanged.

## Separate defect: IPPV-B08, PAVA workspace size

The new small regression also exposes an existing vector-size violation:
`check_sg_h_clique` shrinks `nag` to the previous block count, while the next
`pava_h_clique` writes provisional blocks without resizing it. libc++ bounds
checking aborts with native exit -6 in both the original five-patch and the
six-patch build. Spare vector capacity can hide this violation in a normal build.

Patch **0007-restore-pava-workspace.patch** restores the selected-vertex workspace
size at both PAVA entry points before writes. It changes no grouping criterion.
A separately built **PAVA-only sanitizer control**, retaining the old fractional
capacity code, no longer aborts but still omits the valid solution on both the
small fixture and original CA-GrQc. Thus fixing memory bounds alone does not fix
the original disagreement; the capacity repair is necessary.

## Regression and reduction evidence

The permanent fixture `baselines/ippv/fixtures/fractional-bridge.graph` has 13
vertices and 17 edges at h=2,k=2. It contains a K4, a K4 missing one edge, and a
six-edge path joining them. The unchanged all-superset reference returns exactly:

- vertices 4,5,6,7, density 3/2;
- vertices 0,1,2,3, density 5/4.

The old program and the PAVA-only control return only the first. The final build
returns both. `minimize_small.py` saves 31 deterministic attempts: the starting
witness, every one-edge removal, then every one-vertex removal. None retains the
recorded same-defect predicate with a smaller graph. This establishes one-edit
irreducibility under that predicate, not a global smallest counterexample. It is
a synthetic same-code-defect witness, not an induced reduction of original CA-GrQc.
The original graph/output/commands remain in the immutable stopped pilot.

## Actual final results

| Verification | Actual result |
|---|---|
| Seven-patch Release configure/build | Both commands exit 0 |
| Seven-patch ASan/UBSan + libc++ bounds configure/build | Both commands exit 0 |
| Fixed 13-vertex native regression | Both profiles return both definition-correct results; exits 0 |
| Original h=3,k=20 replay | Both IPPV profiles return 20 outputs and pass tie-aware comparison with a fresh VF replay |
| VF replay preservation | Canonical bytes equal the original VF output |
| Capacity scaling/range test | Strict-warning compile and execution succeed in both profiles; 4 commands exit 0 |
| Existing h=2,3,4,5 corpus | 48 native exits 0: 32 definition passes, 16 retained known zero-density mismatches |
| Sanitizer diagnostics | Final tiny/original runs and all 24 sanitizer corpus runs have empty native stderr |
| Combined pytest | **123 passed in 6.76 s**, exit 0 |
| Stored certificate/pin/patch replay checks | Pass; exit 0 |

The corpus driver still exits **1** because the 16 known zero-density omissions
remain failed semantic checks. This is the same known distribution as before,
not 48 semantic passes. No new failure occurs in that corpus. Original-case
strict comparison remains false because the baseline chooses different eligible
sets at the 10/3 cutoff; tie-aware comparison is true. The disputed 56/13 set is
now present. Complete original-output maximality is not relabelled as exhaustive
definition truth merely because the implementations agree.

The intermediate six-patch sanitizer abort, the old five-patch abort, all
minimization attempts, and the PAVA-only controls remain saved. The first numeric
test compile rejected an unnecessary range-loop copy under `-Werror`; the test
was corrected and both final builds passed. The first certificate script emitted
a docstring escape warning; its original source/output is retained under
`certificate-first/`, and the final corrected run has no such warning.

## Commands actually executed and logs

Working directory: `/Users/nost/Documents/VF-LhCDS`. Principal replay commands:

```sh
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-fixed-release --evidence evidence/m5/ippv/disagreement-20261005/build-final-release --cmake .venv/bin/cmake --boost .deps/boost_1_86_0
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-fixed-sanitize --evidence evidence/m5/ippv/disagreement-20261005/build-final-sanitize --cmake .venv/bin/cmake --boost .deps/boost_1_86_0 --sanitizers
.venv/bin/python baselines/ippv/check_fractional.py --binary build-ippv-fixed-release/IPPV --binary build-ippv-fixed-sanitize/IPPV --evidence evidence/m5/ippv/disagreement-20261005/final-fractional-regression
.venv/bin/python baselines/ippv/check_toys.py --binary build-ippv-fixed-release/IPPV --binary build-ippv-fixed-sanitize/IPPV --h 2 3 4 5 --iterations 10 --timeout 60 --evidence evidence/m5/ippv/disagreement-20261005/final-toy-coverage
.venv/bin/python -m pytest experiments/test_harness.py baselines/ippv/test_adapter.py reference/tests -q
.venv/bin/python evidence/m5/ippv/disagreement-20261005/minimize_small.py
.venv/bin/python evidence/m5/ippv/disagreement-20261005/certify_original.py
.venv/bin/python evidence/m5/ippv/disagreement-20261005/verify_evidence.py
git diff --check
```

The original replays were launched through the existing Python adapters. Exact
native/validator commands, arguments, exits and times are saved in each run's
`process.json`. Intermediate six-patch and PAVA-only build commands and compile
flags are also saved. The numeric C++ test compiles with C++14, `-Wall -Wextra
-Werror`, then repeats with ASan/UBSan/bounds flags; full commands are in
`numeric-final-tests/commands.json`. No production CMake/CTest rebuild ran because
the VF source/binary is unchanged. These are correctness diagnostics; their
wall times are not benchmark samples and are not pooled with D030.

## Changed files, versions and boundaries

Code symbols: external `Graph::verify_LhCDS_small`, `Graph::pava`,
`Graph::pava_h_clique`, and new `ExactVerification`; new permanent
`check_fractional.py`, `test_exact_verification.cpp`, and the fixture. Tracked
patches 0006/0007 and `source-lock.json` reproduce the author-tree edits; ignored
author-tree files are `Graph.cpp` and `ExactVerification.h`. The source lock now
has 18 file hashes and seven patches at the same upstream commit
`f61881d4752170c03585e4281f0c49d7ef14aa1e`.

Updated documents: baseline README/audit, task/claim ledgers, experiments README
and the M5 report. Evidence-only scripts, certificates, build logs, original/
reduced fixtures and run artifacts are under this directory. Exact paths/hashes
are in [files_changed.json](files_changed.json). There is no new commit.

Current binaries are `build-ippv-fixed-release/IPPV` and
`build-ippv-fixed-sanitize/IPPV`. Historical five-patch `build-ippv-original` and
`build-ippv-sanitize` stay unchanged; `build-ippv-exact-*` retain the intermediate
six-patch version. The PAVA-only control is explicitly diagnostic. No previously
recorded run is attributed to a newer binary.

Environment remains macOS 15.7.7 arm64, Apple M1/16 GiB, Python 3.12.2,
AppleClang 17 and existing Boost 1.86.0. Author C++14 Release flags are retained;
the sanitizer profile adds recorded instrumentation. Root HEAD remains
`56229397903813d3509ecb45b178bbde823e357b` with existing uncommitted M5 work.
No package installation, new dependency, DCLDS reading or technique import occurs.
D027/D028 and the user's explicit fix instruction authorize these external
repairs; no accepted theory/output policy is reopened.

Four paper hashes, 40 production-source pins, 23 independent-reference files,
old binary/provenance pins, 11 immutable draft files and all 216 stopped-pilot
inventory entries remain unchanged. Replaying patches 0006/0007 from the saved
five-patch sources reproduces the final Graph.cpp/header hashes exactly.

## Evidence index and remaining limitations

- [Candidate direct inspection](candidate-inspection.json),
  [maximality summary](original-maximality-summary.json),
  [integer certificate](original-maximality-certificate.json),
  [independent verification results](verification.json).
- [Small direct truth](fractional-bridge-truth.json),
  [reduction result](minimization/result.json), [attempts](minimization/attempts.json),
  [PAVA-only causal control](causal-control.json).
- [Final Release build](build-final-release/commands.json),
  [final sanitizer build](build-final-sanitize/commands.json),
  [numeric tests](numeric-final-tests/commands.json), [pytest](pytest/command.json).
- [New definition regression](final-fractional-regression/summary.json),
  [original comparisons](final-original-comparisons.json),
  [existing corpus results](final-toy-coverage/summary.json).

P09.1's B07/B08 repairs are complete; O01/O12 have precisely scoped new evidence.
No full M5 checkbox is promoted. Known zero-density output omissions, broader
baseline numerical/semantic coverage, full-output truth on large graphs, other
h strata of the original input, clean-host release reproduction and DCLDS work
remain unresolved/unrun as previously scoped. The original 28 pending benchmark
calls remain unrun. A campaign using the repaired baseline needs its own immutable
version pins; changing or mixing the old campaign is not part of this request.
