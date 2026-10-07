# Baseline Audit and Integration Checklist

Plan revision: 2026-09-09; execution notes appended below. This is a plan and
audit checklist; only the dated notes linked to logs report executed work.
No baseline has yet passed its complete build and validation gate.

D040 scope (2026-10-08): the final local batch compares the existing seven-patch
IPPV with VF on two bundled graphs at h=3/4/5. No further baseline acquisition is
part of this batch. DCLDS remains deferred; h=2 is unmeasured. LDS-Opt/LDScvx and
LTDScvx/flow specializations are excluded from this bounded VF-versus-IPPV study,
not established unavailable or inferior. Accordingly no h=3 specialization/SOTA
claim is made. P10.1's broader audit and IPPV's zero-density coverage gap remain
open; see [the completion plan](M5_COMPLETION_PLAN.md).

Current scope under owner decision D029 (2026-10-02): further DCLDS reading,
acquisition, comparison and integration are deferred. Continue independent
VF-LhCDS/IPPV work. The DCLDS stop record below is historical and does not block
that work; its task remains incomplete. Existing freeze/evidence records remain.

## 1. Preserve the already accepted D012 decision

The uploaded decision log already identifies Zhou et al. (PVLDB 2026, DCLDS) as an
independent parallel study with substantial overlap. Do not ask again whether it
is the owner's repository. Preserve the uploaded proof/design snapshot and its
hashes before detailed algorithm comparison. A snapshot now records supplied
content; it does not independently establish historical priority or novelty.

DCLDS is a primary related-work and experimental target, not an optional mystery
repository. Detailed code/theory comparison and adaptation remain future tasks;
no DCLDS techniques may enter the proposed solver without the approval in D012.

The public publication/repository metadata consulted on 2026-09-09 identify:

- Yingli Zhou, Taohua Huang, and Yixiang Fang, *Efficient Locally h-Clique Densest
  Subgraph Discovery via Divide-and-Conquer*, PVLDB 19(10), 2577-2590, 2026,
  DOI `10.14778/3828612.3828616` [E1].
- Author repository `s01bvral/DCLDS`; its README uses a different working title
  and describes LhCDS and density-layer outputs [E2]. Confirm the pinned
  publication-to-code mapping during integration; do not infer code exactness.

## 2. Prioritized comparison matrix

| Priority | Method / source | Comparison stratum | Work still required |
|---|---|---|---|
| Primary | IPPV, `Elssky/IPPV`, arXiv:2408.14022 | general h | Pin commit/license; build; audit parameters, vertex sets, ties, enumeration and verification timing |
| Primary | DCLDS, `s01bvral/DCLDS` | general-h target, subject to pinned-code audit | Preserve freeze boundary; map publication to code; audit exact arithmetic/ties, output and timing; independent tests |
| Claim-dependent | LDS-Opt / LDS-DC (2023 ICDE reference) | h=2 only | Locate licensed author source; otherwise record unavailability; label any reimplementation separately |
| Claim-dependent | LDScvx, `chenhao-ma/LDScvx` | h=2 only | Pin/build; inspect candidate verification, iteration defaults and exact output |
| Claim-dependent | LTDScvx (arXiv:2504.10937) | h=3 only | Locate and validate actual triangle implementation, not assumed from LDScvx repository |
| Optional diagnostic | LDSflow / LTDSflow | h=2 / h=3 | Use if licensed source is available and the diagnostic comparison is informative |

The supplied IPPV paper describes a propose-prune-and-verify framework [E3].
The supplied convex-programming paper distinguishes edge and triangle density
methods [E4]. These establish intended scope, not executable validation.

Do not require every historical baseline to be reimplemented before M3 or M5.
State an unavailable primary competitor as a limitation and avoid unsupported
SOTA claims. Specialized methods become necessary when making comparative claims
in their specific h stratum. No h=2/3-only code is an arbitrary-h baseline.

## 3. Adapter contract

For each included method: pin source and license, reproduce a documented command,
convert the same canonical graph losslessly, invoke explicit parameters, capture
raw outputs/status, and parse already-computed sets without changing selection.
Record self-loops/duplicates/isolate policy and the vertex-universe checksum.

Minimal compatibility/output patches are kept as diffs. Changing core algorithms,
exactness, pruning, or tie selection requires a separately labelled variant.
Never silently repair invalid outputs. Log build-failed, blocked-license,
blocked-source, semantic-mismatch and output-incomplete separately.

Use direct-definition validation on tiny inputs, then structural checks and
qualified cross-implementation agreement on larger ones. Counts and connectivity
alone are not a proof of compactness/maximality. Record missing vertex sets or
unrecoverable kth ties rather than pretending a strict comparison was possible.

## 4. One audit record per baseline

```text
name / publication / intended_problem / supported_h
repository / commit / license / retrieval_date / publication_code_mapping
compiler / flags / threads / dependencies / patches
input_format / normalization / parameters / defaults
top_k_policy / tie_policy / output_completeness / exact_arithmetic_behavior
timing_start_stop / enumeration_scope / native_verification_scope / peak_rss_scope
build_command / smoke_command / raw_logs
definition_validation_cases / structural_checks / cross_implementation_cases
status / unresolved_issue / exclusion_reason
```

Required before the main comparison: reproducible build, one shared toy and one
real smoke run, exact supported scope, documented output/timing behavior, and
validation evidence. Documentation or README claims are not this evidence.

## 5. Source register (metadata only in this revision)

[E1] PVLDB publisher record surfaced at
`https://www.vldb.org/pvldb/vol19/p2577-zhou.pdf` (bibliographic metadata only; no
new algorithmic techniques imported during this review).

[E2] Author repository: `https://github.com/s01bvral/DCLDS`.

[E3] Author preprint metadata: `https://arxiv.org/abs/2408.14022`;
local supplied text: `papers/2408.14022v1.md`.

[E4] Author preprint metadata: `https://arxiv.org/abs/2504.10937`;
local supplied text: `papers/2504.10937v1.md`.

## M5 preflight stop (2026-10-01)

P09.1 is blocked on license clarification, not marked complete. The live
GitHub repository metadata at `https://api.github.com/repos/Elssky/IPPV` returned
`license: null`; the public repository page listed no license. This establishes
only that a license was not identified in that metadata, not that no separate
author permission or source-file notice exists. The complete source inventory,
pinned commit and permitted usage scope are still unverified.

The initial sandbox request failed DNS resolution (curl exit 6). The approved
read-only network retry succeeded (exit 0), revealing the license question.
[Preflight record](../evidence/m5/preflight-20261001.json) contains the actual
command, selected response fields, prerequisite hashes and explicit unrun work.
M4 is committed as `56229397903813d3509ecb45b178bbde823e357b`; all 53 accepted
source hashes still match, all four papers verify, and the M3 tag is unchanged.

Decision pending under AGENTS.md's licensing/experimental-fairness boundary:

- Recommended: identify or obtain the author's applicable license/permission
  before adapting, building or running IPPV. No permission request has been sent
  to the author.
- Alternative: explicitly retain IPPV as blocked and resume other M5 work.
  Missing this primary competitor must limit subsequent comparison conclusions;
  it cannot silently disappear from the experiment record.

The owner's instruction requires stopping all work on any blocker/decision, so
DCLDS and independent experiment-harness work have not continued. No baseline
source was downloaded, patched, built or run; no benchmark was started, final
configuration accepted or M5 task completed. Existing decisions remain unchanged.

## IPPV acquisition and original build stop (2026-10-01)

The owner's subsequent "可以，用吧" authorizes proceeding with IPPV as an external
baseline (D027). This resolves the project-use decision in the preceding historical
stop record; it does not fabricate an upstream license or author redistribution
grant. The downloaded tree also contains no license file or identified permission
notice. Baseline source stays in ignored `.deps/baselines/ippv/`.

- Repository: `https://github.com/Elssky/IPPV`.
- Pinned commit: `f61881d4752170c03585e4281f0c49d7ef14aa1e`.
- [Source manifest](../evidence/m5/ippv/source.json): SHA-256 of every tracked
  file, including bundled inputs; no source changes or patches.
- [Commands/log hashes](../evidence/m5/ippv/commands.json): clone exit 0,
  author CMake configuration exit 0, original build exit 2.
- Build environment: AppleClang 17.0.0.17000603, CMake 4.4.3, author C++14/Release
  flags, existing Boost 1.86.0 headers supplied through `CXXFLAGS`; no installation.
- Failure: `Graph.cpp:6:10: fatal error: 'omp.h' file not found`.
  [Original stderr](../evidence/m5/ippv/03-build.stderr) preserves warnings/errors;
  [compiler commands](../evidence/m5/ippv/compile_commands.json) preserve flags.

The source search found the `omp.h` include and commented-out OpenMP API/pragma
uses. Recommended next action is a separately hashed compatibility-only patch
removing or guarding the unused include, followed by a rebuild. An alternative is
to provide a compatible OpenMP development toolchain and rebuild unmodified code.
No patch or dependency change has been made because the owner explicitly requires
stopping at every new blocker. Either route can reveal further build issues;
neither has been tested or accepted as a completed build.

The README's executable name differs from the CMake target (`LhCDScvx` versus
`IPPV`); this is a source-inspected discrepancy, not a reproduced runtime result.
No documented native run, output/semantic validation, adapter, DCLDS work or
experiment campaign has run. [Current stop record](../evidence/m5/ippv/stop.json)
records actual outcomes and unrun work. No M5 task is complete; the 53 accepted
M4 source hashes still match.

## IPPV compatibility build and source-defect stop (2026-10-02)

The owner approved the proposed unused-OpenMP-header removal with "好的".
[Patch 0001](../baselines/ippv/patches/0001-remove-unused-openmp-header.patch)
removes exactly `#include <omp.h>` from `Graph.cpp`. Its SHA-256 is
`b0501215f6debf9bfe59d95de692fc9fb8f76d1a7a3c57b9e4c2b7d06c4452f5`.
[Patch metadata](../evidence/m5/ippv/compat-20261002/patch.json) records before/after
source hashes and authorization. No dependency was added and no algorithm,
parameter or output behavior was edited.

The rebuild succeeded with exit 0 and produced `build-ippv-original/IPPV`.
The directory name is historical: it now contains the patched executable.
[Commands](../evidence/m5/ippv/compat-20261002/commands.json),
[build stdout](../evidence/m5/ippv/compat-20261002/01-build.stdout) and
[compiler warnings](../evidence/m5/ippv/compat-20261002/01-build.stderr) are retained.
The original failed-build evidence remains unchanged. Environment and compiler
flags are the same as in the preceding configuration record.

Before any native run, source inspection found **IPPV-B02**:
`Graph.h:50` declares `int hc_num` without initialization; the user-provided
`Graph::Graph` constructor calls `alpha_c.resize(hc_num)` before assigning it
(patched `Graph.cpp:85`, original line 86). `main.cpp` constructs a local Graph,
so there is no guaranteed prior zero initialization. This reads an indeterminate
integer as the allocation length. The finding is static source evidence, not a
claimed observed crash, test counterexample or proof-manuscript conflict.

The recommended separate bug-fix patch is `int hc_num = 0;` in `Graph.h`.
Subsequent clique routines already size `alpha_c` from `h_cliques.size()` at
initialization. The change should be separately hashed and disclosed as a defect
fix to author code, then built and validated before any benchmark. Alternatively,
retain IPPV as blocked and proceed with other M5 tasks only on the owner's choice.
Neither option has been applied. The explicit stop-on-blocker instruction stops
all subsequent M5 execution pending this decision.

[Current stop record](../evidence/m5/ippv/compat-20261002/stop.json) includes the
binary hash, finding, proposed one-line fix and unrun work. All 17 baseline file
hashes match the pinned source plus only approved patch 0001; all 53 accepted M4
source hashes remain unchanged. No IPPV runtime, adapter, shared smoke, benchmark
or DCLDS run has occurred. Build success alone does not complete P09.1.

## IPPV automatic source repairs and runtime evidence (2026-10-02)

D028 supersedes the preceding per-defect stop. The current state is recorded in
the [reproduction report](../evidence/m5/ippv/reproduction-20261002/REPORT.md),
with the [source and patch lock](../baselines/ippv/source-lock.json) and
[reproduction commands](../baselines/ippv/README.md). The earlier failure and stop
records remain historical evidence, not the current build status.

Three patches remove unused `omp.h`, initialize `hc_num`, and preserve the size
and existing flags of `selected` before indexed pruning. The last defect,
IPPV-B03, was reproduced as a libc++ bounds-check abort on a triangle; the same
case passes after repair. Release and ASan/UBSan builds succeed. Patch replay on
all 17 pristine pinned files reproduces the locked source hashes. No new dependency,
VF-LhCDS algorithm change or baseline technique import was introduced.

The external adapter preserves declared vertices through a reversible ID map,
keeps native selected sets/order, recomputes exact output densities, and separates
external validation from native end-to-end time/RSS. Native candidate verification
remains timed. Native CPU-clock prints do not establish wall-clock phase timing.
The baseline uses floating-point decisions and fixed-width flow arithmetic;
neither production exactness nor general numerical safety is attributed to it.

Executed evidence: 17 adapter tests plus 74 unchanged reference tests pass;
triangle, bridged triangles and tied triangles pass independent definition checks
in both build profiles (six native runs). Alternate valid cutoff ties are retained
and marked as differing from VF-LhCDS's lexicographic choice. The author's bundled
CA-CondMat graph (23,133 vertices, 93,439 edges), h=3,k=20,t=10,p=0, returns 20 sets
that pass structural checks. This does not certify maximality or completeness on
the real graph, and uncontrolled diagnostic timings are not benchmark results.

**IPPV-B04, output-domain mismatch:** a triangle plus an isolate returns one set
where two are required. The smallest nonempty graph, one isolated vertex with
h=3,k=1, returns no set in both Release and sanitizer builds. All three runs exit
normally and are preserved as `semantic_mismatch`; the native degree filter drops
zero-density vertices. No missing set is synthesized by the adapter.

The recommended comparison policy is to retain author selection and record these
failures, explicitly qualifying any common-completion comparison. The alternative
is a separately named zero-density-complete variant, with additional validation
and separately reported timings. Neither output-policy change nor experiment
exclusion has been applied. This consequential comparison decision is distinct
from D028's automatic source repair. P09.1 and M5 remain incomplete; broader h,
random/exhaustive baseline validation, DCLDS, final configuration and benchmarks
remain unrun. All 53 accepted M4 source hashes and the four papers remain unchanged.

After the owner's subsequent "继续", unaffected M5 audit work may proceed.
Recording IPPV mismatches under the existing experiment plan does not itself
require a new output-policy decision. No zero-completing variant or new exclusion
rule is being implemented.

## DCLDS pre-comparison snapshot and license decision (2026-10-02)

Before detailed comparison, [D012 snapshot](../evidence/m5/dclds/preflight-20261002/freeze.json)
records 98 theory/design/implementation/test file hashes, M4 commit
`56229397903813d3509ecb45b178bbde823e357b`, and the preserved M3 correctness tag.
The four audit/decision documents being appended during M5 also have their exact
snapshot bytes retained. This is a content/version boundary, not historical-priority
evidence. No DCLDS technique has been imported.

Read-only public GitHub metadata identifies `s01bvral/DCLDS`, main commit
`60093e582bc584815ab824c3e8b94efdef138200` (2026-02-23), tree
`8f23ab65e000bf6696c9230627156e47ac287b96`. The metadata reports `license: null`;
the complete, non-truncated inventory lists 16 files with no license/notice-named
path. This does not establish the absence of source-file notices or a separate
author grant; those remain unverified. Public responses, initial DNS failures and
successful read-only retries are retained in
[preflight commands](../evidence/m5/dclds/preflight-20261002/commands.json).

The [decision record](../evidence/m5/dclds/preflight-20261002/stop.json) proposes
proceeding with local external-baseline acquisition/build/validation while
explicitly retaining unidentified-license status, as the owner previously allowed
for IPPV. The alternative is to leave DCLDS blocked pending license/permission and
limit comparison claims accordingly. D027/D028 are IPPV-specific, so neither option
is labelled accepted for DCLDS. AGENTS.md requires a decision for this new licensing/
use choice. Further M5 execution stops here under the owner's stop-on-decision rule.
No DCLDS clone, build, patch, adapter, definition test, real smoke, or detailed
publication/code comparison has run. No M5 checkbox is promoted.

## Independent work resumed under D029 (2026-10-02)

The owner deferred further DCLDS reading/integration to continue the independent
plan. Its preceding licensing stop is historical and is not an active question.
No further DCLDS retrieval, source reading or execution followed this direction.

IPPV's new deterministic h=2,3,4,5 corpus exposed two routine source defects:
`onepass` allocates zero-length intersection buffers for h=2 but writes `size[0]`,
and `connected_components` skips a final single-edge component because its boundary
index starts at 1 and is compared with `< edge_count`. Patch 0004 emits retained
edges as 2-cliques, filling the existing incidence lists; patch 0005 corrects that
component boundary to `<=`. These are disclosed reproduction fixes under D028,
not a replacement algorithm, zero-output extension or imported external technique.

[Coverage report](../evidence/m5/ippv/coverage-20261002/REPORT.md): eight configure/
build commands succeed across the two repair stages and profiles. A pristine
five-patch replay reproduces all 17 locked source hashes. The final 48-run corpus
has 32 definition passes and 16 known zero-density omissions, all native exit 0;
the latter remain semantic failures and the campaign exits 1. All 24 final
sanitizer runs have empty stderr. Pre-fix normal-output failures and the ASan
heap-buffer-overflow abort are retained. Each of h=2,3,4,5 has only the six named
tiny fixtures tested, not broad general-h or numerical-safety coverage.

The final real smoke repeats the same CA-CondMat h=3,k=20,t=10,p=0 request. All
20 outputs pass structural checks and their canonical bytes match the prior
three-patch run. This does not prove their maximality/completeness or establish a
performance result. Source hashes, raw outputs, diagnostic controls and unrun work
are in the report. The proposed solver/reference and four papers remain unchanged.

## Shared harness diagnostic (2026-10-03)

The new [shared runner](../experiments/README.md) exercised IPPV and the unchanged
VF Release solver on identical canonical inputs. The tiny corpus correctly
retains alternate valid kth ties and IPPV's known zero omissions. On normalized
CA-GrQc (n=5,242,m=14,484), h=3,k=5,t=10,p=0, IPPV returns five structurally checked
sets; VF basic mode reaches the preregistered local 60-second guard. The raw
timeout is retained, output comparison is unavailable, and no speedup or real
maximality/completeness conclusion is made. [Report](../evidence/m5/harness-20261003/REPORT.md).
There was no new IPPV source modification or DCLDS activity. Further experiment
expansion pauses at the owner's requested blocker/decision boundary.

## D030 discrepancy: IPPV-B07/B08 repaired (2026-10-05)

The owner explicitly requested identifying the correct result, diagnosing the
cause and fixing it. [Executed evidence](../evidence/m5/ippv/disagreement-20261005/REPORT.md)
establishes that VF's disputed 13-vertex, 56-triangle set is an LhCDS on original
CA-GrQc: all 8,192 deletion subsets pass exact compactness checks, and an
independently constructed integer flow/cut certificate at theta=293607/68159
establishes a global optimum whose relevant connected component is exactly that
set. Every 56/13-compact superset must lie in this optimum. This is a finite
instance certificate for the disputed set, not exhaustive truth for all top-20
outputs or a proof of the general theorem.

**IPPV-B07:** `verify_LhCDS_small` computed fractional capacities in double but
`Network::AddEdge(..., long)` truncated them. In particular,
`h*(g-1/N^2)` for g=56/13,h=3 becomes 12 instead of approximately 12.9. Fractional
boundary-clique weights h/r were also truncated. The resulting different network
can spuriously reach outside vertices and reject a valid candidate (the original
trace reports edge 774--480). Patch 0006 scales the original rational network by
a common positive integer. `ExactVerification` uses cpp_int intermediate products,
exact lcm scaling and checked conversion to the existing long-capacity flow
domain, including the total-source bound. It preserves the existing epsilon and
topology and does not substitute a VF oracle, alternate flow method or candidate
output synthesis. Other floating bounds/pruning and unused verifier overloads
remain separate limitations; this is not a full arbitrary-input numeric audit.

**IPPV-B08:** `check_sg_h_clique` shrank `nag` to the preceding block count, but
the next PAVA pass wrote provisional blocks without restoring its logical size.
The five-patch and six-patch sanitizer builds abort on the 13-vertex regression.
Patch 0007 restores the workspace size at both PAVA entries. A PAVA-only sanitizer
control stops aborting but still omits the same positive solution, separating
B08 from the numeric cause of the original disagreement.

The synthetic fractional-bridge witness has 13 vertices and 17 edges, h=2,k=2;
all-superset reference truth has densities 3/2 and 5/4. The old program returns
only the first. Deterministic deletion attempts (31 saved cases) find it
one-edge/one-vertex irreducible under the recorded missing-positive-solution
predicate; no global-minimum or induced-original-reduction claim is made.
The permanent fixture and `check_fractional.py` use an explicit local reference
guard of 13 without raising general adapter/reference defaults.

Final seven-patch Release and ASan/UBSan/bounds-check builds succeed. Both return
the complete tiny truth and pass the original h=3,k=20 tie-aware comparison against
a fresh unchanged VF replay. Capacity scaling/range tests compile with strict
warnings and pass in both profiles. The 48 existing h=2..5 native cases again
yield 32 definition passes and 16 retained zero-density omissions; no new failure.
All 24 sanitizer toy stderr files and final regression sanitizer logs are empty.
Combined pytest: 123 passed. Old binaries, failed runs and the stopped pilot are
preserved; corrected binaries have new paths/hashes. No timings are pooled across
versions and no benchmark campaign is resumed. DCLDS remains deferred.

## IPPV-B09 — equal-density neighbor exclusion (2026-10-08)

The D040 main comparison stops at CA-CondMat h=4,k=15 after 182 native calls.
IPPV emits a nonmaximal density-21 K10. An independent exact witness joins it to
another K10 by an ordinary edge; their 20-vertex induced union is 21-compact.
Thus the omission by VF is correct for this disputed set. Structural validation
alone had passed the invalid candidate; maximality is a separate condition.

`verify_LhCDS_small` excluded equality at two ordinary-neighbor bound tests.
Patch 0008 changes the existing tolerance directions to include the equality
boundary, preserving the existing verifier/parameters. A 13-vertex K5–K4–K4
fixture with ordinary bridges reproduces the false positive at h=3,k=3, and
unchanged exhaustive all-superset truth rejects it. New Release and ASan/UBSan
builds pass two equality and two prior fractional definition checks, plus the
48-case h=2..5 corpus (32 passes, 16 retained zero-density mismatches). Both
original-case repair replays pass structural/tie-aware checks and remove the
invalid set. Adapter/reference pytest: 91 passed. [Repair report and logs](../evidence/m5/ippv/equality-20261008/REPORT.md).

The baseline now has eight recorded patches; old binaries and D040 measurements
remain intact. D041 repeats only the main comparison as fresh paired measurements
under unchanged D040 settings. It is not a performance optimization, a new output
policy or a claim of full-domain baseline correctness.
