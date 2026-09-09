# Baseline Audit and Integration Checklist

Revision: 2026-09-09. This is a plan and metadata check, not a baseline build or
correctness audit. No current commit, license or executable has been validated here.

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
