"""Render the concise result from checked aggregates; no native work."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(path):
    return json.loads(path.read_text())


correct = read(HERE / 'correctness.json')
totals = read(HERE / 'aggregate/totals.json')
cells = read(HERE / 'aggregate/cells.json')
lines = ['| Case (h=3,k=5) | Sorted median [min,max] s | Membership median [min,max] s | Median ratio sorted/member |',
         '|---|---:|---:|---:|']
for case in read(HERE / 'config.json')['cases']:
    old, new = [next(c for c in cells if c['case'] == case['name'] and c['algorithm'] == 'vf-count-' + mode)
                for mode in ('sorted', 'membership')]
    def timing(cell):
        if not cell['three_repeat_measurements_available']: return str(cell['statuses'])
        return f"{cell['wall_median_seconds']:.6f} [{cell['wall_min_seconds']:.6f}, {cell['wall_max_seconds']:.6f}]"
    eligible = old['three_repeat_agreement_available'] and new['three_repeat_agreement_available']
    ratio = f"{old['wall_median_seconds']/new['wall_median_seconds']:.2f}x" if eligible else 'unavailable'
    lines.append(f"| {case['name']} | {timing(old)} | {timing(new)} | {ratio} |")
table = '\n'.join(lines)
report = f'''# Exact count optimization — 2026-10-07

One measured bottleneck change is implemented: `--clique-count membership`
uses exact vertex markers in `MaterializedCliques::count`. Sorted counting remains
the default and control. Both modes use the same immutable clique tuples and
`BigInt` accumulator. [Preservation, preconditions and costs](../../../docs/COUNTING_IMPLEMENTATION.md).

{table}

Native results: **{totals['recorded_native_runs']}/{totals['planned_native_runs']} attempted**,
{totals['native_statuses']}; **{totals['unrun_native_runs']} unrun**.
All {totals['external_validators_completed']} completed external validators pass;
{totals['strict_matches']}/{totals['paired_comparisons']} pairs match strictly.
Completed outputs and full counters are identical within each graph and match
all three earlier corresponding core-off runs. Historical times are not pooled.
Time includes allocation/initialization of the new per-call marker array; external
validation is separate. These are three-repeat local measurements on two h=3,k=5
cases, not a general speedup, larger-k result or a new comparison with IPPV.
One GrQc pair is slower with membership; all measurements remain in the table.
[All times, RSS and censored outcomes](aggregate/TABLE.md).

## Validation and scope

- Debug, Release and ASan/UBSan: **16/16 CTest each**, including T04-COUNT,
  T04-COUNT-CLI (217 calls per build), numeric boundaries and real fallback.
- Python: **{correct['pytest']}**. No production code is imported by the reference.
- **{correct['campaigns_passed']} independent-reference campaigns pass**: existing
  M2/M4 exhaustive-small, seeded and higher-h tiers plus M4 smoke in Debug and
  ASan/UBSan. Every campaign executes automatic arbitrary-precision flow.
- **{correct['previous_response_records_matched']:,} prior responses match**, excluding
  only core-reduction wall time. Case manifests are identical to the previous
  corpus; all fixed-k prefixes, relabelings and four core/footprint modes remain
  covered. No sanitizer diagnostics or correctness counterexample occurred.
- Papers, independent reference, historical evidence and prior binaries are
  unchanged. Finite agreement is implementation evidence, not a theorem proof.

P12.1/O01/O04/O08/O11/O12 gain this scoped result; P14.1/P15.1 gain bounded
interpretation and reproducible aggregates. This completes the targeted count
change and its limited comparison, not M5 or the final benchmark gate.

Environment: Apple M1, 16 GiB, macOS 15.7.7 arm64, AppleClang 17.0.0.17000603,
C++17, Boost 1.86.0, Python 3.12.2. Same new Release binary for both modes;
adjacency enumeration, membership footprints, core off, seed 20261003, three
repeats, randomized within-pair order, one worker/serial runs, 60-second native
and validator guards, no memory cap, uncontrolled cache, no warmups or retries.

## Changed files and executed evidence

Core changes: `materialized.hpp/.cpp` (`CliqueCounting`, constructor, `count`),
CLI dispatch/help, CMake and test-only probe selection. Added count/CLI regression
tests; extended the existing experiment runner's optional count selector. The
historical profiler's tests now use its retained source snapshot; no profiler
or baseline was added. Contracts, task/claim records and reports are updated.
[Full changed-file inventory](files_changed.json).

Executed: CMake configure/build (`-j2`) and CTest for three profiles; all 14
campaigns; the existing Release builder; paper verification; pytest; saved-record
comparison; the existing experiment runner with strict agreement and timeout
retention; aggregation and byte-identical replay with no native reruns.
[25 build/validation commands](checks/commands.json), [pytest](pytest.json),
[equivalence verifier command/log](verify-process/process.json),
[performance command](launch.json), [postprocessing commands](postprocess-commands.json),
[fixture/seed manifest](fixture-manifest.json), [binary/source pins](preflight.json),
[environment](environment.json), [raw native runs](campaign/runs),
[regeneration](regeneration.json).

No new blocking semantic conflict. Larger k, other h/datasets, final experimental
scope, any new IPPV comparison, clean-machine smoke and the release package remain
unrun. DCLDS remains deferred. No additional optimization cycle is started.
'''
(HERE / 'REPORT.md').write_text(report)
main = f'''# M5 status — 2026-10-07

M5 remains **in progress**. The [targeted count optimization](counting-20261007/REPORT.md)
is implemented and validated. `--clique-count membership` uses exact vertex
membership checks to count induced cliques; the original sorted mode remains
the default and control. This addresses the counting cost identified by the
[previous profile](fine-profile-20261007/REPORT.md).

{table}

All {totals['recorded_native_runs']} planned native calls were attempted:
{totals['native_statuses']}, {totals['unrun_native_runs']} unrun;
{totals['strict_matches']}/{totals['paired_comparisons']} pairs match strictly.
All completed outputs pass separate structural validation and retain identical
query counters. This is a local three-repeat comparison of count modes, with no
new IPPV run or historical timing pooling. Larger-k/general-h benefits are untested.

Debug, Release and ASan/UBSan each pass 16/16 CTest; 144 pytest tests and 14
independent-reference campaigns pass. All 1,392,496 saved responses match the
earlier corpus after excluding only measured core time. Production optimization
changes no mathematical semantics; papers/reference and historical records remain
unchanged. Finite tests do not prove the theorem.

The next work package is to freeze the final experiment scope: datasets/h/k,
resource limits, applicable baseline comparisons and IPPV's known zero-density
coverage limitation. Then execute that suite and finish conclusion/reproduction
checks. This count change does not complete P12.1 or M5; no further optimization
loop is launched. DCLDS remains deferred.

Earlier [core ablation](core-ablation-20261006/REPORT.md) and
[VF/IPPV pilot](pilot-membership-20261006/REPORT.md) remain separate historical
results. No new claim that VF is faster than IPPV follows from this turn.

[Latest report and commands](counting-20261007/REPORT.md) ·
[Changed files](counting-20261007/files_changed.json) ·
[Preservation argument](../../docs/COUNTING_IMPLEMENTATION.md)
'''
(ROOT / 'evidence/m5/REPORT.md').write_text(main)
print(table)
