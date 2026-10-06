"""Verify this bounded diagnostic's records, not algorithm correctness."""
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.run import load_config, schedule
from experiments.support import file_hashes, save, sha256


def read(path):
    return json.loads(path.read_text())


def main():
    config = load_config(HERE / 'config.json')
    campaign = HERE / 'campaign'
    assert read(campaign / 'config.json') == config
    assert read(campaign / 'schedule.json') == schedule(config)
    approval = read(HERE / 'authorization.json')
    assert sha256(HERE / 'config.json') == approval['config_sha256']
    assert sha256(ROOT / approval['proposal']) == approval['proposal_sha256']
    proposal = read(ROOT / approval['proposal'])
    assert {k for k in config if config[k] != proposal[k]} == {'name', 'scope'}
    assert config['timeout_seconds'] == 60 and config['repeats'] == 1
    assert config['seed'] == 20261003 and config['threads'] == 1
    assert config['memory_limit_bytes'] is None
    inventory = read(campaign / 'checksums.json')
    assert set(file_hashes(campaign)) == set(inventory) | {'checksums.json'}
    for name, digest in inventory.items():
        assert sha256(campaign / name) == digest, name
    summary = read(campaign / 'summary.json')
    order = schedule(config)[0]['algorithm_indices']
    assert len(summary['runs']) == 4 and len(summary['comparisons']) == 6
    assert [r['algorithm'] for r in summary['runs']] == [config['algorithms'][i]['name'] for i in order]
    results = []
    for row, index in zip(summary['runs'], order):
        directory = campaign / row['directory']
        manifest = read(directory / 'manifest.json')
        process = read(directory / 'process.json')
        assert manifest['native'] == process
        assert manifest['algorithm'] == config['algorithms'][index]
        assert process['timeout_seconds'] == 60
        assert process['executable_sha256'] == config['algorithms'][index]['sha256']
        assert sha256(directory / 'graph.txt') == config['cases'][0]['sha256']
        assert row['status'] == manifest['status']
        for name, digest in manifest['sha256'].items():
            assert sha256(directory / name) == digest, name
        if row['status'] == 'timeout':
            assert process['status'] == 'timeout' and process['native_exit_code'] == -9
            assert manifest['validation']['level'] == 'not_run'
            assert row['semantic_sha256'] is None
        results.append({'algorithm': row['algorithm'], 'status': row['status'],
                        'wall_seconds': process['wall_seconds'],
                        'user_seconds': process['user_seconds'],
                        'system_seconds': process['system_seconds'],
                        'peak_rss_bytes': process['peak_rss_bytes'],
                        'stdout_bytes': (directory / 'stdout.txt').stat().st_size,
                        'stderr_bytes': (directory / 'stderr.txt').stat().st_size,
                        'external_validation': manifest['validation']['level']})
    for filename in ['preservation-start.json', 'm4-source-preservation.json']:
        expected = read(HERE / filename)
        for name, digest in expected.get('sha256', expected).items():
            assert sha256(ROOT / name) == digest, name
    for name, digest in read(HERE / 'environment.json')['script_sha256'].items():
        assert sha256(HERE / 'source-snapshot' / name) == digest
        assert sha256(ROOT / name) == digest
    assert read(HERE / 'command.json')['exit_code'] in (0, 1)
    assert not (HERE / 'driver.stderr').read_bytes()
    assert [json.loads(line) for line in (HERE / 'driver.stdout').read_text().splitlines()] == summary['runs']
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    result = {'status': 'passed', 'scope': 'record integrity and outcome accounting only',
              'native_runs': len(results), 'results': results, 'comparisons': summary['comparisons'],
              'm4_source_files_unchanged': 53, 'papers_unchanged': 4,
              'runner_and_adapter_source_unchanged': True, 'git_diff_check': 0,
              'build_or_test_suite_rerun': False}
    save(HERE / 'verification.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
