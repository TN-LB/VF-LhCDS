"""Reference import isolation and dependency boundary (P01.5)."""

import ast
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
import vflhcds_reference.io
import vflhcds_reference.cli
import vflhcds_reference.generators
assert not any(name == 'vflhcds' or name.startswith('vflhcds.') for name in sys.modules)
"""
    subprocess.run([sys.executable, "-I", "-c", code, str(reference_root)], check=True)


def test_reference_package_imports_only_standard_library_and_itself():
    package = Path(__file__).resolve().parents[1] / "vflhcds_reference"
    for path in package.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                roots = [name.name.split(".")[0] for name in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                roots = [node.module.split(".")[0]]
            else:
                continue
            assert all(name in sys.stdlib_module_names or name == "vflhcds_reference" for name in roots), path
