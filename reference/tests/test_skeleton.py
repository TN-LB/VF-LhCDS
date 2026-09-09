"""Bootstrap import isolation; no T01-T17 mathematical evidence is claimed."""

from pathlib import Path
import subprocess
import sys


def test_reference_imports_in_isolated_interpreter():
    reference_root = Path(__file__).resolve().parents[1]
    # -I removes cwd/PYTHONPATH/user-site: only the reference directory is added.
    code = """
import sys
sys.path.insert(0, sys.argv[1])
import vflhcds_reference
import vflhcds_reference.direct
import vflhcds_reference.parametric
assert not any(name == 'vflhcds' or name.startswith('vflhcds.') for name in sys.modules)
"""
    subprocess.run([sys.executable, "-I", "-c", code, str(reference_root)], check=True)
