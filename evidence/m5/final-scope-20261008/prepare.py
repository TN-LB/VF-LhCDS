"""Prepare a non-executable review pack; never launch a solver or benchmark.

Reuses the existing config validator and seeded scheduler. Historical records,
source, binaries and system settings are read only. Outputs must be fresh.
"""
import copy
import datetime
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import graph_sha256, parse_graph, save, sha256


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    path = HERE / name
    if path.exists():
        raise FileExistsError(path)
    save(path, value)


def observe(command):
    row = {'command': command, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=5)
        row.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
                   available=result.returncode == 0)
    except (OSError, subprocess.TimeoutExpired) as error:
        row.update(available=False, error=str(error))
    return row


def main():
    old = read(ROOT / 'evidence/m5/counting-20261007/config.json')
    pilot = read(ROOT / 'evidence/m5/pilot-membership-20261006/config.json')
    vf = copy.deepcopy(old['algorithms'][1])
    vf['name'] = 'vf-count-membership-core-off'
    ippv = copy.deepcopy(pilot['algorithms'][1])
    core = copy.deepcopy(vf)
    core['name'] = 'vf-count-membership-core-safe'
    core['options']['core'] = 'safe'
    inputs = []
    for case in old['cases']:
        graph = parse_graph((ROOT / case['graph']).read_text())
        assert graph_sha256(graph) == case['sha256'] == sha256(ROOT / case['graph'])
        inputs.append({'name': case['name'].split('-h3-')[0], 'path': case['graph'],
                       'sha256': case['sha256'], 'n': graph.n, 'm': len(graph.edges)})

    def cases(ks):
        return [{'name': f"{item['name']}-h{h}-k{k}", 'graph': item['path'],
                 'sha256': item['sha256'], 'h': h, 'k': k, 'definition': False}
                for item in inputs for h in (3, 4, 5) for k in ks]

    base = {key: copy.deepcopy(value) for key, value in old.items() if key not in ('algorithms', 'cases')}
    base.update(scope='draft', repeats=5)
    main_config = dict(base, name='final-local-main-draft-20261008', algorithms=[vf, ippv],
                       cases=cases((5, 10, 15, 20)))
    core_config = dict(base, name='final-local-core-draft-20261008', algorithms=[vf, core],
                       cases=cases((20,)))
    stop_spec = {'schema_version': 1, 'scope': 'draft', 'name': 'final-local-stop-draft-20261008',
                 'runner_ready': False, 'algorithm': vf, 'cases': cases((5,)),
                 'repeats': 5, 'seed': base['seed'], 'threads': base['threads'],
                 'timeout_seconds': base['timeout_seconds'], 'memory_limit_bytes': None,
                 'cache_policy': base['cache_policy'], 'modes': ['fixed-k', 'all'],
                 'native_scope_arguments': {'fixed-k': ['--k', '5'], 'all': ['--all']},
                 'comparison': 'strict fixed output equals full_output[:5], including exhaustion/ties',
                 'missing_support': ['explicit full-output config/validator support',
                                     'strict fixed/full prefix comparator in existing runner']}
    drafts = {'main.draft.json': main_config, 'core.draft.json': core_config,
              'stop.draft.json': stop_spec}
    guard_checks = []
    for name, config in drafts.items():
        write(name, config)
        if name == 'stop.draft.json':
            continue  # A task specification, explicitly not a supported runner config.
        try:
            load_config(HERE / name)
        except ValueError as error:
            assert 'draft' in str(error)
            guard_checks.append({'config': name, 'rejected_as_draft': True})
        else:
            raise AssertionError('draft unexpectedly launchable')
        # Check all real schema/source/graph pins without calling execute().
        # Temporary diagnostic scope is solely for this read-only validator.
        with tempfile.TemporaryDirectory(prefix='vf-scope-check-') as temporary:
            path = Path(temporary) / 'schema-check.json'
            checked = copy.deepcopy(config)
            checked['scope'] = 'diagnostic'
            save(path, checked)
            assert load_config(path) == checked
        guard_checks[-1]['remaining_schema_and_pins_validated_without_execution'] = True

    schedules = {key: schedule(config) for key, config in [('main', main_config), ('core', core_config)]}
    stop_order = {'seed': base['seed'], 'repeats': 5, 'cases': stop_spec['cases'],
                  'algorithms': stop_spec['modes']}
    schedules['stop'] = schedule(stop_order)
    counts = {key: 2 * len(blocks) for key, blocks in schedules.items()}
    assert counts == {'main': 240, 'core': 60, 'stop': 60}
    assert schedules['main'] == schedule(main_config)
    assert schedules['core'] == schedule(core_config)
    assert schedules['stop'] == schedule(stop_order)
    assert all(sorted(block['algorithm_indices']) == [0, 1] for blocks in schedules.values() for block in blocks)
    write('schedules.json', schedules)

    provenance = {}
    for algorithm in (vf, ippv):
        binary = ROOT / algorithm['executable']
        path = binary.with_suffix('.provenance.json')
        data = read(path)
        assert sha256(binary) == algorithm['sha256'] == data['executable_sha256']
        provenance[algorithm['name']] = {'binary': algorithm['executable'],
            'binary_sha256': sha256(binary), 'provenance': str(path.relative_to(ROOT)),
            'provenance_sha256': sha256(path), 'build_metadata': data}
    vf_source = provenance[vf['name']]['build_metadata']['source_sha256']
    for name, digest in vf_source.items():
        assert sha256(ROOT / name) == digest, name
    lock = read(ROOT / 'baselines/ippv/source-lock.json')
    for patch in lock['patches']:
        assert sha256(ROOT / patch['path']) == patch['sha256']
    papers = read(ROOT / 'review/source_snapshot_sha256.json')['sha256']
    for name, digest in papers.items():
        assert sha256(ROOT / name) == digest, name
    raw = ROOT / 'evidence/m5/counting-20261007/campaign'
    inventory = read(raw / 'checksums.json')
    for name, digest in inventory.items():
        assert sha256(raw / name) == digest, name

    plan = {'schema_version': 1, 'scope': 'draft', 'decision': 'D040 proposed',
            'production_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'inputs': inputs, 'builds': provenance, 'native_calls': counts,
            'total_native_calls': sum(counts.values()), 'max_external_validators': sum(counts.values()),
            'native_guard_sum_seconds': 21600, 'max_validator_guard_sum_seconds': 21600,
            'guard_sum_note': 'not predicted duration or whole-batch deadline; wrapper/setup time additional',
            'three_repeat_alternative': {'native_calls': 216, 'native_guard_sum_seconds': 12960,
                                         'max_validator_guard_sum_seconds': 12960},
            'suite_order': ['main', 'core', 'stop'], 'no_warmups_or_retries': True,
            'failure_policy': {'native_timeout': 'continue and retain censored result',
                               'other_failure': 'stop affected suite, retain failed/unrun records'},
            'required_comparison': {'main': 'cutoff-tie-aware, strict also reported',
                                    'core': 'strict entire output', 'stop': 'strict prefix'},
            'ready_to_launch': False,
            'pending': ['D040 final scope/resource decision', 'full-output/prefix support in existing harness',
                        'per-block power/load/VM observations', 'tiny readiness checks and final configuration freeze'],
            'unrun': ['all 360 proposed native calls', 'associated validators', 'new builds/CTest/sanitizers',
                      'final aggregation', 'clean-machine release', 'specialized baseline work', 'DCLDS work'],
            'draft_sha256': {name: sha256(HERE / name) for name in drafts},
            'schedule_sha256': sha256(HERE / 'schedules.json')}
    write('plan.json', plan)
    environment = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'platform': platform.platform(), 'python': sys.version,
                   'load_average': os.getloadavg(), 'observations': [observe(command) for command in (
                       ['/usr/sbin/sysctl', '-n', 'machdep.cpu.brand_string'],
                       ['/usr/sbin/sysctl', '-n', 'hw.memsize'],
                       ['/usr/sbin/sysctl', '-n', 'hw.logicalcpu'],
                       ['/usr/sbin/sysctl', 'vm.swapusage'],
                       ['/usr/bin/vm_stat'], ['/usr/bin/pmset', '-g', 'batt'],
                       ['/usr/bin/pmset', '-g', 'custom'])],
                   'scope': 'one preparation-time snapshot; not benchmark monitoring or a reserved/idle host',
                   'temperature': None, 'cpu_frequency': None, 'system_settings_changed': False}
    write('environment.json', environment)
    changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
    assert all(name.startswith('docs/') or name == 'evidence/m5/REPORT.md' for name in changed)
    checks = {'passed': True, 'draft_guards': guard_checks, 'native_calls_checked': counts,
              'schedules_reproducible_and_complete': True, 'graphs_checked': len(inputs),
              'binaries_checked': 2, 'production_source_hashes_checked': len(vf_source),
              'baseline_patch_hashes_checked': len(lock['patches']), 'papers_unchanged': len(papers),
              'prior_raw_inventory_entries_checked': len(inventory),
              'native_algorithms_executed': 0, 'performance_claims_added': False,
              'plan_sha256': sha256(HERE / 'plan.json'), 'ready_to_launch': False}
    write('checks.json', checks)
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
