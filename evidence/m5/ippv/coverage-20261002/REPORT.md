# Independent M5 continuation and IPPV h=2..5 diagnostics

Date: 2026-10-02, Australia/Sydney. Tasks: P09.1; scoped evidence relevant to O12.
M5 remains incomplete. The owner deferred further DCLDS reading/integration in
D029 to continue the independently planned VF-LhCDS/IPPV work. No further DCLDS
retrieval or detailed reading occurred, and its licensing decision is not a
current prerequisite. Existing snapshots and historical evidence are preserved.

## Changes and repair arguments

The current external IPPV source remains pinned to
`f61881d4752170c03585e4281f0c49d7ef14aa1e`, with project use authorized by D027
despite unidentified upstream license. Routine repairs are authorized by D028.
The ignored author tree is separate from the proposed solver and reference.

Two more defects were found after the earlier three-patch reproduction:

1. **IPPV-B05, `onepass` in `KClistCore.cpp`:** at h=2 the author allocates zero
   elements for intersection buffers, writes `size[0]`, and enters a recursion
   whose first size is 3. A single edge produces no 2-cliques in Release and a
   heap-buffer-overflow abort under ASan. Patch 0004 adds the missing base case:
   each retained edge is one 2-clique, in the existing relabelled edge order, with
   both incidence entries filled using the existing vertex map. The h>=3 path
   is unchanged. The supplied IPPV paper's section 6.3.1 already includes h=2.
   [Finding and patch hash](patch.json); [original sanitizer error](h2-sanitizer-before/stderr.txt).
2. **IPPV-B06, `Graph::connected_components`:** after the enumeration repair,
   the edge is counted but still not emitted. Component boundary indices start
   at 1; `y < edge_count` skips the final single-edge component. Patch 0005 uses
   `y <= edge_count`; the inner loop still guards indexing with `<`. This extracts
   an already admitted positive component without replacing pruning, candidate
   verification, tie selection or zero-density policy.
   [Finding and patch hash](component-fix.json).

The source now has five separately hashed patches. [Source lock](source-lock.json)
and [pristine patch replay](patch-replay.json) reproduce all 17 final source hashes.
Intermediate three-/four-patch source locks and build provenance remain available.
Only baseline `Graph.cpp`, `Graph.h`, and `KClistCore.cpp` differ from the author pin.

New `baselines/ippv/check_toys.py` exposes `fixtures`, `classify`, and `main`:
it freezes deterministic input hashes before running, invokes the existing external
adapter, preserves all outcomes, and stops on a new failure. Known zero-density
omissions retain `semantic_mismatch` and a nonzero campaign exit; they are never
converted into passes or supplemented with synthesized sets.

Updated workflow documents: AGENTS.md, DECISIONS (D029), TASKS, BASELINE_AUDIT,
CLAIM_TRACEABILITY, EXPERIMENT_PLAN, and the current M5 report. The IPPV README and
source lock include the additional patches and diagnostic command. No paper,
VF-LhCDS solver, independent reference, or theoretical decision was modified.
[Changed-file manifest](files_changed.json) lists the whole uncommitted M5 tree.

## Fixtures and actual results

[Plan](after-component-fix/plan.json): h in {2,3,4,5}; each h uses a complete Kh,
two disjoint Kh with k=1 and k=2, two Kh joined by an ordinary bridge, a Kh plus
an isolate, and a singleton. Original vertex IDs are non-contiguous and include
a negative ID. These are 24 fixture requests (20 distinct graph/h pairs), executed
in Release and ASan/UBSan profiles. Maximum n=10. No random seed is involved.

Diagnostic controls reuse t=10, p=0, one algorithmic worker, a 60-second guard per
native/validation child, no memory cap and uncontrolled filesystem cache. They
are not accepted final benchmark settings. The independent reference checks all
proper supersets for maximality; each external validation runs after native timing.

| Stage | Executed result | Evidence |
|---|---|---|
| Original h=2 single edge, Release | native exit 0, semantic mismatch; planned 48-run corpus stops after 1 | [summary](summary.json), [command](command.json) |
| Original same edge, sanitizer | native -6/SIGABRT, ASan heap overflow | [manifest](h2-sanitizer-before/manifest.json) |
| After patch 0004, Release | edge now counted; native exit 0, still no output; stops after 1 | [summary](after-fix/summary.json) |
| After patch 0004, sanitizer | native exit 0, no sanitizer error; same remaining output omission | [manifest](h2-sanitizer-after-enumeration/manifest.json) |
| After patches 0004/0005, all 48 requests | 32 definition passes; 16 known zero-density mismatches; all native exit 0 | [summary](after-component-fix/summary.json) |
| Same author real smoke, final five-patch Release | native exit 0; 20 structural outputs; canonical bytes identical to prior three-patch run | [comparison](real-regression.json), [run](real-smoke/manifest.json) |

Each h has eight final definition passes (four positive/tie/component requests
times two builds), and four known zero-density mismatches. All 24 final sanitizer
native stderr files are empty. The final campaign exits **1** because its 16
semantic checks fail. Ties use the previously documented tie-aware comparator;
native chosen sets/order are retained. There is no claim of full-domain IPPV
correctness from this finite corpus.

The repeated real input is the same normalized CA-CondMat: 23,133 vertices,
93,439 edges, h=3,k=20,t=10,p=0. All 20 sets pass structural checks and their
canonical output SHA-256 is
`70e378ed3a96b0c5cdc3b6a9d6674260aa7f41e14689ca6461078a40edbdb704`, unchanged
from the earlier run. Native wall time is 9.4150625002 s and native peak RSS is
173,408,256 bytes; external validation is separately timed. These uncontrolled
diagnostics do not establish comparative performance or real-graph maximality.

Across all repair stages in this report: **53 native invocations**, including
one retained sanitizer abort and 52 exit-0 runs. Adapter statuses are 33 completed
(32 tiny passes plus the real structural pass), 19 semantic mismatches (three
development-stage omissions plus the final 16), and one native error. Repeated
repair stages are not additional distinct test graphs. No failure was discarded.

## Builds, environment, commands and integrity

[Environment](environment.json): macOS 15.7.7 arm64, AppleClang 17.0.0, CMake 4.4.3,
Python 3.12.2, existing Boost 1.86.0 headers. Author C++14 Release/O3 flags remain;
the second profile adds ASan/UBSan and libc++ bounds hardening. No dependency was
installed. The initial ASan log reports external-symbolizer startup warnings in
addition to the explicit heap-buffer-overflow; no complete symbolization claim.

All **eight** configure/build commands exit 0: two profiles after each of the
two fixes. Actual argv, flags, stdout/stderr hashes and binary provenance are in
[first Release](build-release/commands.json), [first sanitizer](build-sanitize/commands.json),
[final Release](build-release-component/commands.json), and
[final sanitizer](build-sanitize-component/commands.json).

The top-level build invocation pattern actually used is:

```sh
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-original --evidence evidence/m5/ippv/coverage-20261002/build-release-component --cmake .venv/bin/cmake --boost .deps/boost_1_86_0
.venv/bin/python baselines/ippv/build.py --source .deps/baselines/ippv --build build-ippv-sanitize --evidence evidence/m5/ippv/coverage-20261002/build-sanitize-component --cmake .venv/bin/cmake --boost .deps/boost_1_86_0 --sanitizers
.venv/bin/python baselines/ippv/check_toys.py --binary build-ippv-original/IPPV --binary build-ippv-sanitize/IPPV --h 2 3 4 5 --iterations 10 --timeout 60 --evidence evidence/m5/ippv/coverage-20261002/after-component-fix
.venv/bin/python baselines/ippv/adapter.py run --executable build-ippv-original/IPPV --graph evidence/m5/ippv/reproduction-20261002/real-structural/graph.txt --h 3 --k 20 --iterations 10 --timeout 60 --evidence evidence/m5/ippv/coverage-20261002/real-smoke
.venv/bin/python scripts/verify_papers.py
git diff --check
```

The earlier two build commands used `build-release`/`build-sanitize` evidence
directories. All three campaign argv are in their plan/command JSON files; the
first two stopped on a new error. The two isolated sanitizer probes called the
saved adapter `run` with h=2,k=1,t=10,definition=true,timeout=60. Every native and
validator child has exact argv/cwd in its own `process.json`. Patch replay commands
and outcomes are recorded separately. No documented-only command is counted as run.

[Verification](verification.json): all 53 run manifests and 105 native/validator
process records match their saved log hashes; all five patches replay; four paper
hashes and 53 accepted M4 source hashes match; tracked `git diff --check` exits 0.
The earlier 91 Python test passes remain historical evidence; pytest and core
CTest were not rerun here. Validation of the new diagnostic driver and C++ patches
is the executed corpus and real smoke above, not an invented unit-test result.

## Remaining scope

P09.1 remains partial: known zero-density omissions, broad random/exhaustive
coverage, numeric-limit/overflow audit and clean-host reproduction remain open.
Final data/resource/grid/repeat/cache configuration, shared VF-LhCDS/IPPV benchmark
harness/campaign, comparative conclusions and release reproduction are unfinished.
DCLDS is deferred by the owner, not completed, and is not a current blocker.
No new owner decision is needed for these two routine repairs. No mathematical
theorem is claimed to follow from the tests.
