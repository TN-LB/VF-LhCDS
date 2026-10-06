"""Capture aggregation/check commands and reproduce tables without solver reruns."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.support import file_hashes, save, sha256
HERE = Path(__file__).resolve().parent


def main():
    assert (HERE / 'completion.json').exists(), 'Wait for the native campaign to finish'
    commands = []
    for label, args in [
        ('aggregate', [str(HERE / 'summarize.py')]),
        ('verify', [str(HERE / 'verify.py')]),
        ('regenerate', [str(HERE / 'summarize.py'), '--output', str(HERE / 'aggregate-replay')]),
    ]:
        command = [sys.executable, *args]
        stdout, stderr = HERE / f'{label}.stdout', HERE / f'{label}.stderr'
        assert not stdout.exists() and not stderr.exists(), 'Preserve prior command evidence'
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        clock = time.monotonic()
        with stdout.open('w') as out, stderr.open('w') as err:
            process = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err)
        commands.append({'command': command, 'cwd': str(ROOT), 'started_utc': started,
                         'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         'exit_code': process.returncode, 'wall_seconds': time.monotonic() - clock,
                         'stdout': str(stdout.relative_to(ROOT)), 'stderr': str(stderr.relative_to(ROOT)),
                         'script_sha256': sha256(Path(args[0]))})
        save(HERE / 'postprocess-commands.json', commands)
        print(f'{label}: exit {process.returncode}', flush=True)
        if process.returncode:
            print(stderr.read_text(), flush=True)
            return process.returncode
    original, replay = file_hashes(HERE / 'aggregate'), file_hashes(HERE / 'aggregate-replay')
    assert original == replay, 'Regenerated artifacts differ'
    save(HERE / 'regeneration.json', {'passed': True, 'identical_artifact_sha256': original,
                                    'native_solver_calls': 0, 'clean_machine_tested': False})
    print(json.dumps({'regenerated_identical_artifacts': len(original), 'native_solver_calls': 0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
