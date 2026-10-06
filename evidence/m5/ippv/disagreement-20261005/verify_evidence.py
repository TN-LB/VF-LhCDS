"""Read-only arithmetic, pin, patch-replay and regression evidence checks."""
from collections import deque
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'reference'))
from vflhcds_reference.io import parse_graph


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes(root, entries):
    for path, digest in entries.items():
        assert sha(root / path) == digest, path
    return len(entries)


def main():
    checks = {}
    before = read(HERE / 'preflight.json')['prior_pins']
    for field in ['paper_sha256', 'reference_sha256', 'production_source_sha256', 'binary_sha256', 'provenance_sha256', 'draft_artifacts_sha256']:
        checks[field] = check_hashes(ROOT, before[field])
    pilot = ROOT / 'evidence/m5/pilot-20261005/campaign'
    checks['historical_pilot_files'] = check_hashes(pilot, read(pilot / 'checksums.json'))
    lock = read(ROOT / 'baselines/ippv/source-lock.json')
    checks['current_patched_source_files'] = check_hashes(ROOT / '.deps/baselines/ippv', lock['patched_source_sha256'])
    for patch in lock['patches']:
        assert sha(ROOT / patch['path']) == patch['sha256']
    # Reconstruct the current bytes from the saved five-patch version, without
    # modifying the author checkout or any recorded build.
    with tempfile.TemporaryDirectory() as directory:
        scratch = Path(directory)
        for p in (HERE / 'source-before').iterdir():
            shutil.copyfile(p, scratch / p.name)
        for patch in lock['patches'][5:]:
            result = subprocess.run(['patch', '-p1'], cwd=scratch,
                                    input=(ROOT / patch['path']).read_text(), text=True, capture_output=True)
            assert result.returncode == 0, result.stdout + result.stderr
        for name in ['Graph.cpp', 'ExactVerification.h']:
            assert sha(scratch / name) == lock['patched_source_sha256'][name]
    checks['patches_0006_0007_replay_exactly'] = True
    graph = parse_graph((pilot / 'runs/0009-0/graph.txt').read_text())
    certificate = read(HERE / 'original-maximality-certificate.json')
    # Re-enumerate all triangles from graph bytes, and check the stored feasible
    # flow and cut using arithmetic only. Do not run the certificate's flow code.
    adjacency = {v: set() for v in graph.vertices}
    for u, v in graph.edges:
        adjacency[u].add(v); adjacency[v].add(u)
    triangles = [[u, v, w] for u in graph.vertices for v in sorted(adjacency[u]) if u < v
                 for w in sorted(adjacency[u] & adjacency[v]) if v < w]
    assert triangles == certificate['triangles'] and len(triangles) == 48260
    p, q = certificate['p'], certificate['q']
    assert Fraction(p, q) == Fraction(certificate['theta']) < Fraction(56, 13)
    loads = {v: 0 for v in graph.vertices}
    allocation = certificate['clique_to_vertex_flow']
    assert len(allocation) == len(triangles)
    for triangle, values in zip(triangles, allocation):
        assert len(values) == 3 and all(type(x) is int and x >= 0 for x in values)
        assert sum(values) <= q
        for v, value in zip(triangle, values):
            loads[v] += value
    assert all(value <= p for value in loads.values())
    optimum = set(certificate['global_optimum_vertices'])
    assert optimum <= set(graph.vertices)
    cut = q * sum(not set(t) <= optimum for t in triangles) + p * len(optimum)
    assert cut == sum(loads.values()) == certificate['flow_value'] == 537086985
    candidate = set(read(HERE / 'candidate-inspection.json')['vertices'])
    assert candidate <= optimum
    reached = {min(candidate)}; todo = deque(reached)
    while todo:
        for v in (adjacency[todo.popleft()] & optimum) - reached:
            reached.add(v); todo.append(v)
    assert reached == candidate
    inside = [set(t) for t in triangles if set(t) <= candidate]
    assert len(inside) == 56
    vertices = sorted(candidate)
    # Enumerate every deleted subset, independently of the generator's Reference.
    for mask in range(1 << len(vertices)):
        deleted = {v for i, v in enumerate(vertices) if mask & (1 << i)}
        loss = sum(bool(t & deleted) for t in inside)
        assert 13 * loss >= 56 * len(deleted)
    checks['independent_stored_certificate_verified'] = True
    checks['deletion_subsets_rechecked'] = 8192
    checks['candidate_is_global_maximal_compact'] = True
    attempts = read(HERE / 'minimization/attempts.json')
    assert len(attempts) == 31 and sum(a['accepted'] for a in attempts) == 1
    assert sha(HERE / 'minimization/minimized.graph') == sha(ROOT / 'baselines/ippv/fixtures/fractional-bridge.graph')
    checks['minimization_attempts'] = 31
    assert all(r['numeric_defect_retained'] and r['native_exit_code'] == 0 for r in read(HERE / 'causal-control.json'))
    assert read(HERE / 'pava-preexisting.json')['old_native_exit_code'] == -6
    checks['pava_only_control_still_omits_positive_solution'] = True
    assert all(r['passed'] for r in read(HERE / 'final-fractional-regression/summary.json')['runs'])
    checks['final_tiny_definition_passes'] = 2
    assert all(r['comparison']['tie_aware_match'] for r in read(HERE / 'final-original-comparisons.json'))
    assert (HERE / 'final-vf-original/canonical_output.jsonl').read_bytes() == (pilot / 'runs/0009-0/canonical_output.jsonl').read_bytes()
    checks['final_original_pair_matches'] = 2
    toys = read(HERE / 'final-toy-coverage/summary.json')
    assert toys['executed_native_runs'] == 48 and toys['unrun'] == 0
    assert toys['counts'] == {'definition_pass': 32, 'known_zero_density_mismatch': 16}
    for row in toys['runs']:
        manifest = read(HERE / 'final-toy-coverage' / row['manifest'])
        assert manifest['native']['native_exit_code'] == 0
        if row['profile'] == 1:
            assert not (HERE / 'final-toy-coverage' / row['manifest']).with_name('stderr.txt').read_text()
    checks['toy_results'] = toys['counts']
    for profile in ['release', 'sanitize']:
        assert all(c['exit_code'] == 0 for c in read(HERE / f'build-final-{profile}/commands.json'))
        provenance = read(ROOT / f'build-ippv-fixed-{profile}/IPPV.provenance.json')
        assert provenance['executable_sha256'] == sha(ROOT / f'build-ippv-fixed-{profile}/IPPV')
        assert provenance['patched_source_sha256'] == lock['patched_source_sha256']
        assert provenance['patches'] == lock['patches']
    assert all(c['exit_code'] == 0 for c in read(HERE / 'numeric-final-tests/commands.json'))
    assert read(HERE / 'pytest/command.json')['exit_code'] == 0
    assert '123 passed' in (HERE / 'pytest/stdout.txt').read_text()
    checks['pytest_passed'] = 123
    checks['numeric_compile_and_run_commands_passed'] = 4
    checks['final_configure_and_build_commands_passed'] = 4
    checks['benchmark_resumed'] = False
    (HERE / 'verification.json').write_text(json.dumps(checks, indent=2) + '\n')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
