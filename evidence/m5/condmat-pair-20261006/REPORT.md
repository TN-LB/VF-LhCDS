# CA-CondMat paired diagnostic — 2026-10-06

**Tie-aware comparison passed.** Both programs return five structurally checked
sets. Ranks 1–4 match exactly. Rank 5 selects different sets with the same exact
density **22**, so strict equality is false but the cutoff-tie rule is satisfied.
VF also reproduces its previous membership-mode output.

| Algorithm | Native wall time | Peak RSS | Native / validator exit |
|---|---:|---:|---:|
| VF adjacency + membership, core off | 38.525397500 s | 143589376 bytes | 0 / 0 |
| IPPV, seven patches, t=10,p=0 | 2.723666167 s | 168968192 bytes | 0 / 0 |

CA-CondMat: 23,133 vertices / 93,439 edges; h=3,k=5. One run each, one worker,
serial execution, seed 20261003 (IPPV first), 60-second limits for each native
child and separate validator, no memory cap or warm-up, uncontrolled cache.
[Config](config.json) pins graph and binaries. [Environment](environment.json):
Apple M1, 16 GiB, macOS 15.7.7 arm64, Python 3.12.2, existing AppleClang 17 Release
builds; fresh hardware/profile checks pass.

External validation is excluded from native timing; IPPV's own candidate
verification remains included. VF post-load/solver times are 38.481722625 /
38.408677750 s. Comparable IPPV wall-phase measurements are unavailable. IPPV is
faster in this observed pair; no repeated speedup or general performance claim
follows. Structural checks and output agreement do not establish real-graph
maximality/completeness or prove a theorem.

[Results](result.json), [cutoff difference](comparison-details.json),
[raw records](campaign/summary.json), [verification](verification.json) and
[executed commands](commands.json) contain the evidence. Main command:

```sh
.venv/bin/python experiments/run.py --config evidence/m5/condmat-pair-20261006/config.json --evidence evidence/m5/condmat-pair-20261006/campaign --stop-on-failure
```

Driver and saved-evidence verifier exit 0; diff check passes. Added run/verification
scripts, configs, logs and this report; updated experiment/task/traceability
summaries and the decision log. No production symbol changed. Source, paper and
historical evidence pins are intact; no build, CTest, pytest or sanitizer rerun.
[File inventory](files_changed.json) records this turn's changes.

P11.1/P11.2/P12.1/O12 gain this pair; M5 remains incomplete. No new blocking
conflict was observed. The [next repeated-pilot draft](next-pilot-draft.json)
retains the existing two graphs, h=3,k={5,10,15,20}, three repetitions and resource
limits, using membership VF and the same seven-patch IPPV (48 calls). It is unrun;
prior timeouts remain recorded and are not replaced by these measurements.
