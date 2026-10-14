"""Losslessly package this runner's raw run directories after verifying every byte."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import tarfile

from reports import build, load_bundle


def pack(directory):
    bundle_path = directory / 'bundle.json'
    bundle = json.loads(bundle_path.read_text())
    def report_outcome():
        try:
            return build(load_bundle(bundle_path))
        except ValueError as error:
            if not (directory / 'failure.json').exists():
                raise
            return {'preserved_report_failure': str(error)}
    before = report_outcome()
    files = sorted(p for row in bundle['rows'] for p in (directory / row['run_id']).rglob('*') if p.is_file())
    archive_path = directory / 'raw-runs.tar.gz'
    with archive_path.open('xb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode='w') as archive:
            for path in files:
                data = path.read_bytes(); name = str(path.relative_to(directory))
                info = tarfile.TarInfo(name); info.size = len(data); info.mode = 0o644
                archive.addfile(info, io.BytesIO(data))
    with tarfile.open(archive_path, 'r:gz') as archive:
        for path in files:
            assert archive.extractfile(str(path.relative_to(directory))).read() == path.read_bytes()
    bundle['raw_archive'] = {'path': archive_path.name,
                             'sha256': hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                             'files': len(files), 'uncompressed_bytes': sum(p.stat().st_size for p in files)}
    bundle_path.write_text(json.dumps(bundle, sort_keys=True, indent=2) + '\n')
    for row in bundle['rows']:
        shutil.rmtree(directory / row['run_id'])
    assert report_outcome() == before, 'archive report regeneration'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    pack(args.directory.resolve())


if __name__ == '__main__':
    main()
