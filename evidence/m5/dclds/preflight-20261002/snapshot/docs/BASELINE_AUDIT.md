# Baseline Audit and Integration Checklist

Plan revision: 2026-09-09; execution notes appended below. This is a plan and
audit checklist; only the dated notes linked to logs report executed work.
No baseline has yet passed its complete build and validation gate.

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
