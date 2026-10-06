"""Shared external graph/record contracts and child-process capture."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'reference'))
sys.path.insert(0, str(ROOT / 'baselines/ippv'))
from adapter import count_cliques, run as run_ippv
from process import capture, sha256
from vflhcds_reference.direct import Reference, direct_lhcds
from vflhcds_reference.io import canonical_graph, graph_sha256, json_line, parse_graph


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def semantic_hash(graph, h, records):
    header = json_line({'schema_version': 1, 'graph_sha256': graph_sha256(graph), 'h': h})
    return hashlib.sha256((header + ''.join(json_line(r) for r in records)).encode()).hexdigest()


def file_hashes(directory):
    return {str(p.relative_to(directory)): sha256(p) for p in sorted(directory.rglob('*')) if p.is_file()}
