"""Preserve one diagnostic driver launch and its logs; no automatic retries."""
import datetime,json
from pathlib import Path
import subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
assert not (HERE/'command.json').exists()
cmd=[str(ROOT/'.venv/bin/python'),str(HERE/'run_diagnostic.py')]
start=time.monotonic()
record={'command':cmd,'cwd':str(ROOT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(HERE/'launch.json').write_text(json.dumps(record,indent=2)+'\n')
with (HERE/'driver.stdout').open('w') as out,(HERE/'driver.stderr').open('w') as err:
    proc=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=err)
record.update(exit_code=proc.returncode,wall_seconds=time.monotonic()-start,
              finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(HERE/'command.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
raise SystemExit(proc.returncode)
