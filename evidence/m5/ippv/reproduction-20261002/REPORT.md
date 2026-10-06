# IPPV automatic reproduction fixes and scoped validation

Date: 2026-10-02 local time (Australia/Sydney); command records use UTC.
Task P09.1 / obligation O12 remains incomplete for the project's complete domain.
Routine source fixes proceed under D028 without renewed per-defect approval.
Three disclosed patches now build and run, but an output-domain mismatch remains:
the tested author implementation omits required zero-density solutions.
No mathematical theorem or general numerical-exactness claim is established here.

## Source and changes

Author repository: https://github.com/Elssky/IPPV, commit
`f61881d4752170c03585e4281f0c49d7ef14aa1e`. License unidentified; project use
authorized by D027, with no invented upstream license/redistribution grant.
The ignored source directory is `.deps/baselines/ippv`; VF-LhCDS and the independent
reference are unchanged. No third-party algorithmic techniques were imported.

| Patch | Reason / behavior | Evidence |
|---|---|---|
| 0001 remove unused omp.h | Current AppleClang lacked the unused OpenMP header; no live OpenMP call/pragma found | Earlier original build failure and approved compatibility build |
| 0002 initialize hc_num | Constructor read an indeterminate member as the initial alpha_c size; set it to zero, retain later actual clique-size allocation | Source finding IPPV-B02, new build and runtime checks |
| 0003 preserve selected storage | selected.clear() destroyed the vector's logical size before prune_by_core indexed it; retain the existing n-entry flags and prior degree-filter decisions | Triangle aborts under libc++ bounds checks before the fix and passes afterward |

Patches and SHA-256 pins are in
[source-lock.json](source-lock.json), the retained three-patch snapshot for these runs.
[Patch replay](patch-replay.json) applies all three patches to fresh copies of
the pinned author files and confirms all 17 final hashes. The source-based
initialization/storage reasoning supports the repairs; observed output agreement
is finite evidence, not a proof about previously undefined behavior.

New external tools and symbols:

- `baselines/ippv/build.py:main`: verify pin, patch/source hashes and existing
  Boost version, configure/build, retain exact commands and emit binary provenance.
- `baselines/ippv/process.py:capture`: native wait4 exit/RSS, explicit timeout,
  immutable per-run stdout/stderr/process record. No guessed OOM or wrapper exit.
- `baselines/ippv/adapter.py:native_input,parse_native,count_cliques,validate,run`:
  lossless vertex mapping, parse actual author sets, separate exact structural and
  exhaustive-definition checks, keep native rank/selection, preserve failures.
- `baselines/ippv/test_adapter.py`: 17 tests for IDs/isolates, malformed output,
  tie-aware selection, maximality and missing-zero rejection, independent structural
  count comparisons, native exit/timeout and evidence overwrite protection.

`baselines/ippv/README.md`, task/audit/traceability records and D028 document scope.
The complete new/modified file/hash list for this M5 working tree is in
[files_changed.json](files_changed.json). Earlier stop/failure records are retained.

## Builds, environment and actual checks

macOS 15.7.7 arm64; AppleClang 17.0.0.17000603; CMake 4.4.3; Python 3.12.2;
pytest 8.4.2; existing Boost 1.86.0 headers. Author C++14/Release compilation
remains. No dependency was installed. ASan/UBSan and macOS libc++ debug hardening
are diagnostic flags. Remaining author compiler warnings are visible in logs.
There is no claim of leak-sanitizer, GCC/Linux or all-code-path validation.

| Executed check | Actual result | Evidence |
|---|---|---|
| Build after member initialization | exit 0 | [commands](commands.json), 01-build logs |
| Sanitizer configure and build before storage repair | both exit 0 | same manifest, 02/03-sanitizer logs |
| Rebuild Release and sanitizer after storage repair | both exit 0 | same manifest, 04/05-build logs |
| Reproducible build script, Release | configure/build both exit 0 | [final-build](final-build/commands.json) |
| Reproducible build script, ASan/UBSan + libc++ checks | configure/build both exit 0 | [final-build-sanitize](final-build-sanitize/commands.json) |
| Cache-safe build-script refinement, both profiles | four configure/build commands exit 0; binary and compiler-command hashes unchanged | [Release](verified-build/commands.json), [sanitizer](verified-build-sanitize/commands.json) |
| Adapter pytest | 17 passed | [adapter-tests.stdout](adapter-tests.stdout) |
| Adapter + unchanged reference pytest | 91 passed in 1.86 s | [final-tests.stdout](final-tests.stdout) |
| Three patches on pristine pinned files | 3 apply commands exit 0; 17 file hashes match | [patch-replay.json](patch-replay.json) |

The historical build directory `build-ippv-original` now contains the three-patch
binary. Actual compiler commands, patch set, source checksums and executable hashes
are in each final build's provenance record. Original failed builds were not
overwritten. Core solver CTest was not rerun for these external-only changes;
all 53 M4 accepted source hashes remain unchanged.

The final build script explicitly sets `CMAKE_CXX_FLAGS`: environment `CXXFLAGS`
alone is ignored after a CMake cache is initialized. Both existing build profiles
were reconfigured and built successfully with this refinement. Their executable
and compiler-command hashes exactly match those used for the saved native tests;
no redundant native run was needed. Earlier build-script bytes are retained in
the two `final-build*` evidence directories to preserve provenance.

## Reproductions, fixtures and evidence levels

Local diagnostics use the author example's h=3, t=10, k=20, p=0 on its bundled
CA-CondMat input. The binary target is `IPPV`; the README's `LhCDScvx` name and
unsupported `--args` token were corrected in the invocation, not the algorithm.
A 60-second debugging guard was recorded before these runs; it is not a final
benchmark timeout. No memory cap was imposed. Filesystem cache and workstation
load were uncontrolled. These are validation/reproduction runs, not benchmarks.

- [First example](native-example/manifest.json): author program produced output,
  but `/usr/bin/time -l` returned 1 because sandboxed `sysctl kern.clockrate` was
  denied. Only that wrapper exit is known; output existence is not native-success
  evidence. This failed measurement is retained.
- [Direct example retry](native-example-direct/process.json): native exit 0,
  20 sets, 5.6731665004 s wall and 185,778,176 bytes native peak RSS. This used
  patches 0001/0002 before the later storage fix; no large-graph correctness label.
- [Before storage fix](sanitizer-before/process.json): three-vertex triangle,
  h=3,k=1,t=10,p=0, SIGABRT (-6); libc++ reports vector<bool> index out of bounds.
  [stderr](sanitizer-before/stderr.txt) preserves the original failure.
- [After storage fix](sanitizer-after/process.json): same native triangle command,
  exit 0 and empty stderr under ASan/UBSan/libc++ checks.

The tiny corpus was declared in [toys/plan.json](toys/plan.json) before execution.
It has no random seed: triangle, ordinary-bridge triangles, tied triangles, and
triangle plus isolate. Iterations=10 and the diagnostic timeout=60 were unchanged.

| Case | Release | Sanitizer | Validation |
|---|---|---|---|
| triangle, h=3,k=1 | pass | pass | definition-checked, strict match |
| bridged triangles, h=3,k=1 | pass | pass | definition-checked, joint six-vertex maximal set |
| tied triangles, h=3,k=1 | pass | pass | definition-checked, tie-aware match; strict mismatch |
| triangle + isolate, h=3,k=2 | semantic mismatch, exit 0 | not run in the initial stop-on-mismatch corpus | Returned triangle is valid, but only 1 of the required 2 sets is emitted |

[Toy summary](toys/summary.json): six passed native/validation pairs and one
preserved semantic mismatch. In the tied case, the author selects the other valid
triangle; the comparator accepts it without changing the native selection/order.
The independent reference exhaustively checks maximality against all supersets.

The zero-output failure was minimized to one declared vertex `-2`, no edges,
h=3,k=1. No nonempty graph has fewer vertices. Both
[Release](minimal-zero/manifest.json) and
[sanitizer](minimal-zero-sanitizer/manifest.json) exit 0 and return no set, whereas
the reference returns `[-2]` with density 0. Original and minimum input/output
records are saved; no missing set was inserted by validation. These two runs
diagnose the already encountered issue rather than expanding an experiment grid.

The final three-patch build was also checked on losslessly normalized bundled
CA-CondMat: 23,133 declared vertices, 93,439 edges, no removed loops/duplicates,
h=3,k=20,t=10,p=0. [Final real-input manifest](real-structural/manifest.json): native
exit 0, 20 sets, all structural checks pass. Native wall time was 6.8890410410 s,
native peak RSS 201,048,064 bytes; separate validation took 0.3881042497 s.
That run overlapped the independent pytest process, so these diagnostic times
must not be used as controlled performance measurements. The validation process's
own RSS and native/external boundaries are recorded separately in its manifest.
Structural checking does not establish maximality, cutoff completeness or general
cross-implementation agreement on this real graph.

Across this turn: 14 native-program invocations including one wrapper measurement
failure, one pre-fix abort and 12 direct native exit-0 runs. Ten runs received the
external adapter validation: six tiny definition passes, three tiny zero-result
mismatches (original plus two minimal reproductions), one real structural pass.
No failure, partial output or inconvenient case has been discarded.

## Audited baseline scope and remaining decision

The author input header declares n,m; the adapter preserves that universe and
maps original IDs reversibly. The author's CLI exposes g,t,h,k,p; adapter pattern
is fixed to cliques. It has no audited `all` or verification-disabling option.
The source uses floating estimates/epsilon comparisons and fixed-width integral
flow capacities (plus other compiled flow code). It has no demonstrated equivalent
to VF-LhCDS's arbitrary-precision guarantees. The executed native scope here is
h=3; no general supported-h or numeric-range validation is claimed.

Every returned set is parsed from author output. Four-decimal native densities
are retained as approximate metadata; exact counts/densities are computed only
by the external validator. Rank order and kth-tie selection are not rewritten.
The native main uses clock() CPU timing. Native enumeration, verification,
final clustering diagnostics and output remain included in captured wall time.
Printed verification subtotals can omit the final early-break iteration, so they
are not treated as a complete comparable algorithm-time breakdown. Missing wall
phase metrics are null, not zero. No live parallel path was found in this scope.

The author's initial degree<h-1 filter excludes isolated/no-clique vertices. The
observed zero-density omission is a result-policy/domain difference with D017 and
the project's fixed-k min(k,q) contract, not a remaining build failure. Patching an
adapter to supply missing sets would conceal it and violate the adapter contract.

Recommended comparison treatment: retain the patched author implementation's
selection, keep zero-result cases explicitly incomplete/mismatched, include them
in counts, and qualify any later speed comparison by valid common completions.
An alternative is a separately named zero-density-complete IPPV variant with
additional selection logic and its own validation/timing; it cannot replace
the author baseline silently. No such extension or new comparison restriction is
being applied. Recording mismatches and limiting claims to their actual evidence
are already required by the existing experiment plan; they need no new decision.
The owner's subsequent "继续" permits proceeding with unaffected M5 audit work.
Any later variant or change to the final comparison policy still needs an explicit
decision under AGENTS.md. Routine reproduction fixes need no further approval.

Unrun: remaining initial sanitizer isolate case, broader h/k/random/exhaustive
IPPV validation, complete numeric/overflow audit, clean-host reproduction,
DCLDS/specialized baseline tasks, shared multi-algorithm smoke, final dataset/grid/
resource/thread/repeat/cache decisions, full benchmark and release reproduction.
P09.1 and all M5 completion checkboxes remain open. No finite test proves a theorem.

## Commands and records

Build commands are retained verbatim in the linked manifests, including UTC times
and stdout/stderr hashes. Every native/validation child has `process.json` with
its exact argv, cwd, binary checksum, timeout, exit/signal, time/RSS and log hashes.
The substantive top-level commands executed in addition to those manifests were:

```sh
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-original --evidence evidence/m5/ippv/reproduction-20261002/final-build --cmake .venv/bin/cmake --boost .deps/boost_1_86_0
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-sanitize --evidence evidence/m5/ippv/reproduction-20261002/final-build-sanitize --cmake .venv/bin/cmake --boost .deps/boost_1_86_0 --sanitizers
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-original --evidence evidence/m5/ippv/reproduction-20261002/verified-build --cmake .venv/bin/cmake --boost .deps/boost_1_86_0
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-sanitize --evidence evidence/m5/ippv/reproduction-20261002/verified-build-sanitize --cmake .venv/bin/cmake --boost .deps/boost_1_86_0 --sanitizers
.venv/bin/python -m pytest baselines/ippv/test_adapter.py -q
.venv/bin/python -m pytest baselines/ippv/test_adapter.py reference/tests -q
.venv/bin/python scripts/verify_papers.py
git diff --check
```

The ad hoc native/toy/minimization/real invocations called the saved `capture`/`run`
functions with arguments preserved in their manifests; they were actually run,
not merely suggested CLI commands. Dataset hashes and every converted input are
saved with each run. Patch replay commands are in `patch-replay.json`.
