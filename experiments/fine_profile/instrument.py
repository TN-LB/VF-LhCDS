"""Generate diagnostic copies; reject drift from the profiled production source."""
import argparse
import hashlib
import json
from pathlib import Path

PINS = {
    'src/clique/materialized.cpp': '8b34a667a2b4440731802486a5da13980aedf4310e2829774cc2638b8d458e50',
    'src/oracle/closure.cpp': 'adca32d55b37756a6f44addb06f70c1d92a467e0aff78f35382a7099284e94d0',
}


def instrument(path, data):
    if hashlib.sha256(data).hexdigest() != PINS[path]:
        raise ValueError(f'production source drift: {path}')
    text = data.decode()
    additions = ['#include "profile.hpp"\n']
    text = additions[0] + text

    def after(anchor, statement):
        nonlocal text
        if text.count(anchor) != 1:
            raise ValueError(f'ambiguous instrumentation anchor: {anchor}')
        addition = '    ' + statement + ' // VF_PROFILE\n'
        text = text.replace(anchor, anchor + addition)
        additions.append(addition)

    if path.endswith('materialized.cpp'):
        after('BigInt MaterializedCliques::count(const VertexSet& set) const {\n',
              'vf_profile::Scope measure(vf_profile::Phase::Count);')
    else:
        after('        const BigInt& sink_capacity, const BigInt& infinity, QueryStats& stats) {\n',
              'vf_profile::Scope measure(vf_profile::Phase::NetworkBuild);')
        after('    ++stats.mincut_calls;\n', 'measure.change(vf_profile::Phase::MaxFlow);')
        after('    (void)network.max_flow(source, sink);\n', 'measure.change(vf_profile::Phase::CutExtract);')
        after('    std::sort(result.begin(), result.end());\n', 'measure.change(vf_profile::Phase::NetworkCleanup);')
        after('Footprints aggregate_footprints(const MaterializedCliques& index, const RestrictedRequest& request, const FootprintMode mode) {\n',
              'vf_profile::Scope measure(vf_profile::Phase::Footprints);')
        after('                                          QueryStats& stats, const FootprintMode mode) const {\n',
              'vf_profile::Scope measure(vf_profile::Phase::OracleOther);')
    restored = text
    for addition in additions:
        restored = restored.replace(addition, '', 1)
    if restored.encode() != data:
        raise ValueError('instrumentation changed original bytes')
    return text.encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    generated = {path: instrument(path, (args.root / path).read_bytes()) for path in PINS}
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {'original_sha256': PINS, 'generated_sha256': {}}
    for path, data in generated.items():
        target = args.output / Path(path).name
        target.write_bytes(data)
        manifest['generated_sha256'][target.name] = hashlib.sha256(data).hexdigest()
    (args.output / 'instrumentation.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
