"""Fail closed on drift or unequal production/diagnostic compile options."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def verify(directory):
    manifest = json.loads((directory / 'instrumented/manifest.json').read_text())
    for relative, digest in manifest['production'].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    for name, digest in manifest['observer'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
    commands = json.loads((directory / 'compile_commands.json').read_text())
    by_source = {}
    for row in commands:
        tokens = shlex.split(row['command'])
        if not any('CMakeFiles/vflhcds_lib.dir/' in token or 'CMakeFiles/final_profile_lib.dir/' in token for token in tokens):
            continue
        role = 'control' if any('CMakeFiles/vflhcds_lib.dir/' in token for token in tokens) else 'diagnostic'
        candidates = [path for path in manifest['production']
                      if path.startswith('src/') and str(row['file']).endswith('/' + path)]
        source = candidates[0] if len(candidates) == 1 else 'generated/build_info.cpp'
        assert candidates or Path(row['file']).name == 'build_info.cpp', 'unrecognized translation unit'
        flags = []; i = 0
        while i < len(tokens):
            token = tokens[i]; i += 1
            if token in ('-o', '-c'):
                i += 1; continue
            if token == '-I' + str(HERE): continue
            flags.append(token)
        by_source.setdefault(source, {})[role] = flags
    assert len(by_source) == 13, 'complete production source list'
    for source, roles in by_source.items():
        assert roles.get('control') == roles.get('diagnostic'), (source, roles)
    nm = subprocess.run(['nm', '-g', str(directory / 'production/libvflhcds_lib.a')],
                        capture_output=True, text=True, check=True)
    assert not any('_ZN2fp' in line or '_ZNK2fp' in line for line in nm.stdout.splitlines()), 'observer in control'
    return {'source_pin_checks': len(manifest['production']), 'observer_pin_checks': len(manifest['observer']),
            'matched_translation_units': len(by_source), 'control_has_observer_symbols': False,
            'build_directory': str(directory), 'compile_commands_sha256': hashlib.sha256(
                (directory / 'compile_commands.json').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('build', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(verify(args.build.resolve()), indent=2) + '\n')


if __name__ == '__main__':
    main()
