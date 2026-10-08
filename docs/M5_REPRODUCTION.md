# Reproducing the bounded M5 evaluation

The selected scope is [D040/D041](M5_COMPLETION_PLAN.md): two pinned graphs,
h=3/4/5, k=5/10/15/20, five repeats, serial execution. Reproduction has three
separate levels: regenerate saved numbers, rebuild/check on the current host,
and install/build/check in a clean software environment. A fresh local directory
alone does not establish the third level. [Executed local checks](../evidence/m5/reproduction-20261008/REPORT.md)
pass 16/16 CTest, 164 pytest and four separate definition fixtures. Both newly
built binary hashes match D041; this remains a same-host result.
[Fresh Ubuntu checks](../evidence/m5/clean-env-20261008/REPORT.md) also pass 16 CTest,
164 pytest and four definition fixtures, with all 26 saved aggregate/review files
regenerated identically. This is a new Linux root filesystem and dependency
installation under OrbStack on the same Mac, not independent hardware/kernel.

## Versions, inputs and contracts

- VF production sources: commit `0315c5d`, unchanged during D040/D041. Exact
  source/compiler/binary hashes are pinned in each campaign's provenance.
- IPPV upstream: `f61881d4752170c03585e4281f0c49d7ef14aa1e`, with all eight
  [disclosed patches and source hashes](../baselines/ippv/source-lock.json).
  Follow [baseline setup](../baselines/ippv/README.md). Its upstream license is
  unidentified; the existing local-use boundary does not establish redistribution
  permission. No baseline source/binary distribution is supplied here.
- [CA-GrQc normalization](../evidence/m5/harness-20261003/data/ca-grqc/) and
  [CA-CondMat normalization](../evidence/m5/campaign-proposal-20261005/data/ca-condmat/)
  retain the input identity and all declared vertices. Exact normalized graph
  hashes are in every configuration and run manifest. No additional datasets
  are acquired by the reproduction script.
- [Input/output, IDs, errors and fixed-k ordering](INTERFACE_CONTRACT.md),
  [exact solver semantics](ALGORITHM_SPEC.md), [phase boundaries](M3_IMPLEMENTATION.md),
  and [external validation](../experiments/README.md) remain separate contracts.
- [Dependencies](DEPENDENCIES.md): Boost 1.86.0 headers, CMake, C++17, Python
  and pytest. See [build instructions](BUILD.md) for offline headers and supported
  compiler requirements. No dependency fetch occurs during a build.
- [Paper snapshot](../review/source_snapshot_sha256.json) and the existing
  [D012 freeze](../evidence/m5/dclds/preflight-20261002/freeze.json) remain unchanged.
  DCLDS remains deferred; this package does not read or acquire it.

## Regenerate recorded measurements without algorithms

Use a new output directory for each invocation, from the repository root:

```sh
.venv/bin/python evidence/m5/final-main-repaired-20261008/postprocess.py --aggregate /tmp/vf-d041-main-new
.venv/bin/python evidence/m5/final-evaluation-20261008/summarize.py --suite core --output /tmp/vf-d040-core-new
.venv/bin/python evidence/m5/final-evaluation-20261008/summarize.py --suite stop --output /tmp/vf-d040-stop-new
```

Each aggregation verifies its saved raw checksum inventory before reading
manifests. Compare generated files with the corresponding saved `aggregate/`
directory; the saved regeneration records identify byte-identical replays.
The main suite uses only the eight-patch IPPV campaign; the two VF-only ablations
use their completed D040 campaigns. Do not substitute seven-patch timings.

Per-run `process.json` records exact commands, wall/user/system time and RSS;
`manifest.json` separates native and external validation; `canonical_output.jsonl`
preserves selected sets. Configurations, randomized schedules, per-block power/
load/VM/swap observations, completion/stop records and aggregate provenance are
retained. The stopped seven-patch main remains in
[D040 evidence](../evidence/m5/final-evaluation-20261008/REPORT.md), including its
failed comparison and 58 unrun calls. Historical development trials are not pooled.

## Fresh local build and correctness smoke

After preparing the existing local Python/Boost installation and pinned IPPV
checkout, run with unused build/evidence paths:

```sh
.venv/bin/python scripts/reproduce_release.py --build build-m5-reproduction-new --evidence evidence/m5/reproduction-new
```

This performs a new VF Release configure/build, all configured CTest smoke tests,
independent Python/harness/adapter tests, and a fresh local IPPV checkout with all
eight patches applied in order. The baseline builder checks every source/patch
hash before compiling. New IPPV fractional/equal-density/ordinary-bridge checks
and a VF definition-checked full-output fixture follow. Every actual command,
exit status, tool version and log is saved; a failed step stops this script.
It does not measure a new performance grid or overwrite benchmark executables.
The current driver preserves the virtualenv interpreter path. The historical
driver resolved its symlink to system Python, which fails on a fresh Linux system
without globally installed pytest; that failed attempt remains in the evidence.

The local IPPV clone comes from already acquired objects; Python/Boost, OS and
compiler are reused. This is an offline local rebuild, not a clean-machine
installation or a bit-for-bit binary reproducibility claim. Full previous
Debug/Release/ASan/UBSan and differential tiers remain linked from
[counting acceptance](../evidence/m5/counting-20261007/REPORT.md) and
[IPPV-B09 acceptance](../evidence/m5/ippv/equality-20261008/REPORT.md); a smoke run
does not silently rerun those tiers.

## Fresh Linux software environment

The executed [setup plan and command logs](../evidence/m5/clean-env-20261008/plan.json)
create Ubuntu Noble arm64 under OrbStack 2.0.1, install `build-essential`, Python
and venv support, Git, curl, CA certificates and bzip2, then install pytest 8.4.2
and CMake 4.4.3 in a new venv. `scripts/fetch_boost.py` downloads/checks Boost
1.86.0; the baseline is newly acquired at the locked commit. No Mac dependency
or binary is copied. See the [baseline setup](../baselines/ippv/README.md) before
running the release driver above in a fresh source checkout.

The successful tree is base `5cc0a76` plus the recorded reproduction driver and
two whitespace-only test-probe repairs. The source bundle hash, overlays, full
package inventory, compiler versions, emitted flags and every failed/successful
command are preserved. After installation repairs, the final attempt reuses those
new Linux dependencies with unused build/evidence directories. Three IPPV fixtures
and one VF fixture produce byte-identical canonical outputs on macOS and Linux;
binary hashes are platform-specific. The measured Mac binaries remain unchanged.

This verifies clean userspace installation and selected correctness/table
reproduction. It does not repeat the raw performance grid, full differential or
sanitizer campaigns, nor establish portability to every Linux system. OrbStack
shares its Linux kernel and the physical host; it is not an independent-machine
performance replication. Final M5 scope remains separately listed in the plan.

## Interpreting and repeating performance runs

The frozen configs/schedules describe exact measured inputs and switches. New
machine/compiler/binary pins require a new config, fresh raw directory and a
recorded environment/resource plan before launching `experiments/run.py`; old
hashes must not be bypassed. Use the unchanged five-repeat protocol for this
scope, no automatic retry or favorable sample removal, and no concurrent build.
The evidence-specific launch drivers deliberately reject restarting a saved batch.

Native IPPV verification is included in its process time. External checking is
excluded for both algorithms. Real-graph checks establish structure and agreement,
not exhaustive maximality/completeness. Tiny reference checks are finite
implementation evidence, not theorem proofs. Keep zero-density IPPV omissions,
cutoff-tie differences, host load/cache limitations and all unavailable metrics
explicit. Rank latency, a final detailed flow-phase breakdown, broad scalability,
specialization/SOTA comparisons and independent-machine performance replication
are not supplied by this bounded evaluation.
