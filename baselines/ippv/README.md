# P09.1: external IPPV reproduction

Author source: https://github.com/Elssky/IPPV, pinned commit
`f61881d4752170c03585e4281f0c49d7ef14aa1e`. The upstream license remains
unidentified; project use was authorized in D027. D028 authorizes routine
reproduction fixes. This directory contains our adapter and disclosed patches;
the author tree and build products stay in ignored directories.

## Patches and reproducible build

Apply the patches in order to the pinned author tree:

1. `0001-remove-unused-openmp-header.patch`: remove an unused header unavailable
   in the local AppleClang setup; no live OpenMP code existed.
2. `0002-initialize-clique-count.patch`: initialize an indeterminate member used
   as the initial vector allocation size; subsequent actual clique sizing remains.
3. `0003-preserve-selection-storage.patch`: retain the vertex selection vector
   rather than clearing its size before indexed use. This retains existing
   degree-filter flags; no pruning condition or result-selection rule is changed.
4. `0004-h2-enumeration-base-case.patch`: enumerate retained edges as 2-cliques;
   the author recursion starts at three vertices and otherwise writes to an empty
   buffer at h=2. The minimum one-edge failure is saved in the coverage evidence.
5. `0005-include-final-single-edge-component.patch`: correct the component loop's
   boundary so an already admitted final component with one edge is extracted.
6. `0006-exact-verification-capacities.patch`: retain the existing verifier's
   rational capacities by exact common-denominator scaling. The previous integer
   interface silently truncated `h*(g-1/N^2)` and fractional boundary-clique
   weights. Arbitrary-precision intermediate arithmetic checks the existing
   signed-long flow capacity and total-source bound before conversion; unsupported
   magnitudes raise an error rather than wrap or round.
7. `0007-restore-pava-workspace.patch`: restore `nag` to the selected-vertex count
   at each PAVA entry after `check_sg` shrinks it to a block count. The previous
   subsequent writes exceeded vector size, reproduced by libc++ bounds checks.
8. `0008-include-equal-density-verification-neighbors.patch`: include equal-density
   ordinary neighbors in the existing verification expansion; otherwise a candidate
   can survive despite a connected compact proper superset. Keep the existing
   DELTA tolerance and verify against the independent bridge regression.

`source-lock.json` records the pin, every patch hash and expected patched file
hash. The build script refuses other source bytes. It does not download or modify
source. To prepare a new local copy (network access is a separate setup step):

```sh
git clone https://github.com/Elssky/IPPV.git .deps/baselines/ippv
git -C .deps/baselines/ippv checkout --detach f61881d4752170c03585e4281f0c49d7ef14aa1e
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0001-remove-unused-openmp-header.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0002-initialize-clique-count.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0003-preserve-selection-storage.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0004-h2-enumeration-base-case.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0005-include-final-single-edge-component.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0006-exact-verification-capacities.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0007-restore-pava-workspace.patch
git -C .deps/baselines/ippv apply ../../../baselines/ippv/patches/0008-include-equal-density-verification-neighbors.patch
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-new-release --evidence evidence/m5/ippv/new-build --cmake .venv/bin/cmake --boost .deps/boost_1_86_0
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-new-sanitize --evidence evidence/m5/ippv/new-sanitizer-build --cmake .venv/bin/cmake --boost .deps/boost_1_86_0 --sanitizers
```

The historical `build-ippv-original`/`build-ippv-sanitize` binaries retain five
patches. Historical seven-patch binaries use the separate `build-ippv-fixed-*` paths;
intermediate `build-ippv-exact-*` binaries have six patches and retain the PAVA bug.
The measured eight-patch binaries use `build-ippv-equality-*`. Build into a new
directory to preserve every previous executable/provenance pair.
No global OpenMP installation is needed. Author C++14/Release flags are retained;
the diagnostic sanitizer profile adds ASan/UBSan and macOS libc++ bounds checks.
Remaining author warnings are retained, not suppressed. Build provenance beside
the executable records its SHA-256, source/patch hashes and actual compiler flags.
The adapter requires a matching executable/provenance pair.

## Adapter contract

```sh
.venv/bin/python baselines/ippv/adapter.py run --executable build-ippv-new-release/IPPV --graph reference/fixtures/bridged_triangles.graph --h 3 --k 1 --iterations 10 --timeout 60 --definition --evidence evidence/m5/ippv/new-toy
.venv/bin/python -m pytest baselines/ippv/test_adapter.py reference/tests -q
```

Every evidence directory must be new. The timeout and iteration count are explicit
inputs, not final experimental defaults. These example values are local diagnostics.
Input conversion preserves all declared vertices and uses a reversible map from
arbitrary original integer IDs to 0..n-1. A fixed relative input/output filename
avoids the author's filename-length assumptions. The adapter accepts positive
fixed-k requests, pattern 0 (cliques), and the audited native signed-int domain;
it offers no invented `all` or verification toggle.

Native result order and selected sets are retained. The parser checks two-line
records, vertex counts, duplicates, ranges and the stdout result count. Exact
densities are recomputed from the returned sets by a separate validator, rather
than reconstructed from the native four-decimal density. No missing result is
generated by the adapter. Structural checks do not establish maximality or
completeness; tiny definition validation uses the unchanged M1 all-superset truth.
It checks count, membership, cutoff and all higher-density sets. Different valid
selections at a tied cutoff pass tie-aware validation and retain `strict_match=false`.

`process.py` uses native `wait4` status/RSS. Timeout is explicit and no signal is
guessed to mean OOM. Native and validation processes have separate timing and RSS.
Native enumeration, candidate verification, final clustering diagnostics and
serialization remain included in end-to-end time. Native `clock()` CPU phase
prints are not relabelled wall-clock phase times; unavailable wall phases are null.
No result is accepted merely because a timed wrapper produced an output file.

## Executed scope and limitation

The following original reproduction results used patches 0001-0003. Later h=2
diagnostics identified and repaired two additional source defects with patches
0004/0005. Their separate pre/post-fix evidence is in
`evidence/m5/ippv/coverage-20261002`; do not attribute older runs to newer binaries.

The deterministic diagnostic runner writes all fixture/parameter hashes before
execution, stops on a new failure, and preserves known zero-density mismatches as
failures. For both existing build profiles:

```sh
.venv/bin/python baselines/ippv/check_toys.py --binary build-ippv-new-release/IPPV --binary build-ippv-new-sanitize/IPPV --h 2 3 4 5 --iterations 10 --timeout 60 --evidence evidence/m5/ippv/new-toy-coverage
.venv/bin/python baselines/ippv/check_fractional.py --binary build-ippv-new-release/IPPV --binary build-ippv-new-sanitize/IPPV --evidence evidence/m5/ippv/new-fractional-regression
.venv/bin/python baselines/ippv/check_equality.py --binary build-ippv-new-release/IPPV --binary build-ippv-new-sanitize/IPPV --evidence evidence/m5/ippv/new-equality-regression
```

These are correctness diagnostics, not accepted final experiment settings. A
completed diagnostic corpus with known mismatches still exits nonzero.

The author CA-CondMat example runs after correcting its README executable name
(`IPPV`, not `LhCDScvx`) and omitting the unimplemented `--args` token. The fixed
case uses h=3, k=20, t=10, p=0. The final three-patch build returns 20 sets that pass
structural checking. This is not definition-level validation on that real graph
or a comparative benchmark.

Triangle, ordinary-bridge triangles and tied triangles pass definition checks in
both Release and sanitizer profiles: six native runs. Tied triangles demonstrate
an actual difference from VF-LhCDS's lexicographic cutoff choice.

**Known output-domain difference:** triangle plus isolate at h=3,k=2 returns only
the triangle; the reference requires the zero-density isolated vertex as well.
The minimum one-vertex graph at h=3,k=1 also returns no set, in both profiles.
These are retained `semantic_mismatch` results with native exit 0. They are not
silently repaired or dropped. The author's early `degree < h-1` filter explains
the omitted zero-density vertices. A full-domain IPPV comparison gate therefore
remains unmet; deciding to extend its output policy or narrow a claimed comparison
requires a separately documented experimental decision.

See the [original report](../../evidence/m5/ippv/reproduction-20261002/REPORT.md)
and [later h=2..5 diagnostics](../../evidence/m5/ippv/coverage-20261002/REPORT.md).
The final five-patch corpus has 32 definition passes and 16 zero-density omissions
across 48 native runs; the real h=3 smoke returns the same 20 structural outputs.
Broad random/exhaustive campaigns, clean-host installation and final resource/data
settings remain unrun/unfrozen. Further DCLDS work is deferred by owner decision D029.

The [2026-10-05 discrepancy repair](../../evidence/m5/ippv/disagreement-20261005/REPORT.md)
adds patches 0006/0007. Independent all-deletion checks and a separately verified
flow/cut certificate establish that the disputed density-56/13 set is maximal
compact on original CA-GrQc; the old IPPV omission is incorrect. The fixed release
and sanitizer builds recover it and pass tie-aware comparison on h=3,k=20.
The 13-vertex `fixtures/fractional-bridge.graph` is checked against every proper
superset by the reference under an explicit local size guard of 13; defaults
remain unchanged. `test_exact_verification.cpp` checks rational scaling and
capacity rejection boundaries. The broad baseline remains limited: other
floating pruning/bounds and unused legacy verifiers are not upgraded by this
patch, and zero-density omission remains. Do not silently substitute new binaries
into the stopped D030 campaign or merge its old/new timing samples.

The [2026-10-08 equality repair](../../evidence/m5/ippv/equality-20261008/REPORT.md)
adds patch 0008. Two ordinary-neighbor verification bounds now include equality
within the existing DELTA tolerance. A K5–K4–K4 bridge fixture at h=3 has exact
all-superset truth consisting only of the K5; the seven-patch binary incorrectly
also emitted the final K4. `check_equality.py` checks both repaired profiles under
the existing local size-13 reference guard. Both original CA-CondMat h=4,k=15
correctness replays remove the certified nonmaximal K10 and pass tie-aware
comparison. Old binaries/campaigns remain historical. Current eight-patch builds
are `build-ippv-equality-release` and `build-ippv-equality-sanitize`; no old/new
benchmark timings may be pooled. Zero-density and other floating-bound/legacy
limitations remain; this is not a complete numerical correctness audit.
