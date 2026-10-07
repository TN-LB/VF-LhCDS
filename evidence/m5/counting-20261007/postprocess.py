"""Record postprocessing commands and check byte-identical regeneration."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from experiments.support import file_hashes, save, sha256


def main():
    rows = []
    for name, extra in [('aggregate', []), ('regenerate', ['--output', str(HERE / 'aggregate-replay')])]:
        command = [sys.executable, str(HERE / 'summarize.py'), *extra]
        row = {'command': command, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'stdout': name + '.stdout', 'stderr': name + '.stderr'}
        assert not (HERE / row['stdout']).exists()
        with (HERE / row['stdout']).open('w') as out, (HERE / row['stderr']).open('w') as err:
            process = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err)
        row.update(exit_code=process.returncode, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        for stream in ('stdout', 'stderr'): row[stream + '_sha256'] = sha256(HERE / row[stream])
        rows.append(row)
        save(HERE / 'postprocess-commands.json', rows)
        print(name, process.returncode, flush=True)
        if process.returncode:
            print((HERE / row['stderr']).read_text())
            return process.returncode
    original = file_hashes(HERE / 'aggregate')
    assert original == file_hashes(HERE / 'aggregate-replay')
    save(HERE / 'regeneration.json', {'passed': True, 'identical_artifact_sha256': original, 'native_reruns': 0})
    print(json.dumps({'identical_artifacts': len(original), 'native_reruns': 0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
