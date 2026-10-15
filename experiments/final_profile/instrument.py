"""Hash- and anchor-checked generated observers; production files are never written."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def generate(path, original):
    text = original.decode()
    edits = []

    def replace(old, new, count=1):
        nonlocal text
        if text.count(old) != count:
            raise ValueError(f'{path}: ambiguous/missing anchor {old!r}')
        edits.append((old, new))
        text = text.replace(old, new)

    def before(anchor, code):
        replace(anchor, code + '\n' + anchor)

    def after(anchor, code):
        replace(anchor, anchor + '\n' + code)

    def cleanup(declaration, name, owner):
        replace(declaration, f'fp::CleanupEnd fp_end_{name};\n' + declaration
                + f'\nfp::CleanupBegin fp_begin_{name}(fp_end_{name}, "cleanup_{owner}");')

    if path == 'src/cli/main.cpp':
        after('    try {', '        fp::Session fp_session(argc, argv);')
        before('        return result;', '        fp::state.status = result;')
    elif path == 'src/cli/dispatch.cpp':
        after('std::size_t& output_count, const StopRequested& stop) {',
              '    fp::Scope fp_operation("input"); fp::checkpoint("input");')
        cleanup('const auto graph = parse_graph(read_text_file(options.at("--graph")));', 'graph', 'graph')
        before('const MaterializedCliques index(graph, h, enumeration, counting);',
               'fp_operation.change("enumeration_index"); fp::checkpoint("enumeration_index");')
        cleanup('const MaterializedCliques index(graph, h, enumeration, counting);', 'index', 'index')
        after('postindex = Clock::now();', '        fp::index_summary(index); fp_operation.change("orchestration");')
        cleanup('const auto answer = solve(index, k, CapacityPolicy::Auto, &*run_stats, {}, stop, execution);', 'answer', 'result')
        cleanup('std::optional<SolveStats> run_stats;', 'run_stats', 'telemetry')
        cleanup('std::string result, semantic_hash;', 'serialized', 'output')
        after('k_reached = answer.k_reached;', '            fp_operation.change("output");')
        before('result = oracle_json(index, lambda, answer);', 'fp_operation.change("output");')
        before('if (destination == "-") { out << result;', 'fp_operation.change("output"); fp::checkpoint("output");')
    elif path == 'src/clique/materialized.cpp':
        after('void MaterializedCliques::append(const VertexSet& tuple) {',
              '    fp::Scope fp_incidence("incidence_append"); fp::add("cliques_appended"); fp::add("incidence_entries_appended", tuple.size());')
        after('BigInt MaterializedCliques::count(const VertexSet& set) const {',
              '    fp::Scope fp_count("count"); fp::checkpoint("count"); fp::count_add("calls");')
        cleanup('Membership members(graph_.size());', 'count_members', 'count')
        replace('for (const auto& clique : cliques_)\n            if (std::all_of(clique.begin(), clique.end(),\n                            [&](const VertexId vertex) { return members.contains(vertex); })) ++result;',
                'for (const auto& clique : cliques_) {\n'
                '            fp::count_add("clique_visits");\n'
                '            if (std::all_of(clique.begin(), clique.end(),\n'
                '                            [&](const VertexId vertex) { fp::count_add("membership_vertex_tests"); return members.contains(vertex); })) ++result;\n'
                '        }')
        replace('for (const auto& clique : cliques_) if (subset(clique, set)) ++result;',
                'for (const auto& clique : cliques_) { fp::count_add("clique_visits"); if (fp::count_subset(clique, set)) ++result; }')
        before('    return result;\n}', '    fp::count_add("matches", result);')
        cleanup('std::vector<Frame> stack;', 'enum_stack', 'enumeration')
        cleanup('VertexSet prefix;', 'enum_prefix', 'enumeration')
        cleanup('VertexSet tuple(k);', 'enum_tuple', 'enumeration')
    elif path == 'src/clique/core.cpp':
        after('VertexSet peel_core(const MaterializedCliques& index, const BigInt& threshold, CoreStats* progress) {',
              '    fp::Scope fp_core("core_initialization"); fp::checkpoint("core_initialization"); fp::add("core_calls");')
        after('const auto n = index.graph().size();',
              '    fp::add("core_vertex_slots_initialized", n); fp::add("core_clique_slots_initialized", index.cliques().size());')
        cleanup('std::vector<std::size_t> degrees(n);', 'core_degrees', 'core')
        cleanup('std::vector<unsigned char> active(n, 1), queued(n, 0), live_clique(index.cliques().size(), 1);', 'core_arrays', 'core')
        cleanup('VertexSet queue;', 'core_queue', 'core')
        before('for (std::size_t head = 0; head < queue.size(); ++head) {',
               'fp_core.change("core_peeling"); fp::checkpoint("core_peeling");')
        for field in ('vertices_removed', 'incidence_visits', 'cliques_invalidated', 'degree_decrements'):
            after(f'++stats.{field};', f' fp::add("core_{field}");')
    elif path == 'src/oracle/closure.cpp':
        after('const BigInt& sink_capacity, const BigInt& infinity, QueryStats& stats) {',
              '    fp::Scope fp_execute("network_build"); fp::checkpoint("network_build");')
        cleanup('Dinic<Capacity> network(nodes);', 'network', 'network')
        cleanup('std::vector<std::size_t> local(graph.size(), nodes);', 'local_map', 'network')
        cleanup('const auto reachable = network.reachable(source);', 'reachable', 'query')
        before('(void)network.max_flow(source, sink);', 'fp_execute.change("max_flow"); fp::checkpoint("max_flow");')
        before('const auto reachable = network.reachable(source);', 'fp_execute.change("cut_extraction"); fp::checkpoint("cut_extraction");')
        after('const FootprintMode mode, const CliqueRange* range) {',
              '    fp::Scope fp_aggregate("footprint_aggregation"); fp::checkpoint("footprint_aggregation"); fp::add("aggregation_calls");')
        cleanup('std::map<VertexSet, BigInt> weights;', 'weights', 'footprints')
        cleanup('std::optional<Membership> lower, upper;', 'markers', 'footprints')
        cleanup('VertexSet residual;', 'residual', 'footprints')
        after('++result.scanned;', '        fp::add("footprint_clique_visits");')
        replace('return upper->contains(v);', 'fp::add("footprint_membership_vertex_tests"); return upper->contains(v);')
        replace('if (!lower->contains(v))', 'if ((fp::add("footprint_membership_vertex_tests"), !lower->contains(v)))')
        replace('if (!subset(clique, request.y_oracle)) continue;',
                'if (!fp::footprint_subset(clique, request.y_oracle)) { fp::upper_rejected(clique); continue; }')
        replace('return upper->contains(v); })) continue;',
                'return upper->contains(v); })) { fp::upper_rejected(clique); continue; }')
        replace('std::back_inserter(residual));', 'std::back_inserter(residual), fp::footprint_less);')
        before('if (!residual.empty()) {', 'fp::add("footprint_eligible_tuples");')
        after('++result.total_weight;', ' fp::add("footprint_contributions");')
        before('    return result;\n}\n}  // namespace\nFootprints', '    fp::footprint_summary(result);')
        # Identical calls occur in global_chain_point and separate; tag by function body.
        before('auto result = global_F(full_graph_request(std::move(lambda)), policy, progress, options);',
               'fp::CountSite fp_site("standalone");')
        before('auto result = global_impl(separator_request(interval), policy, &stats, options, range);',
               'fp::CountSite fp_site("separator");')
        after('QueryStats* progress, const OracleOptions options, const CliqueRange* range) const {',
              '    fp::Scope fp_global("oracle_preparation");')
        after('const auto& original = request.request_;', '    fp::OriginalBound fp_bound(original.y_oracle);')
        after('if (options.core == CoreMode::Safe && original.lambda.numerator() > 0) {',
              '        fp::Scope fp_core_scope("core_preparation");')
        cleanup('RestrictedRequest reduced = original;', 'reduced', 'query')
        cleanup('const auto core = peel_core(index_, *stats.core_threshold, &*stats.core);', 'core_result', 'core')
        after('QueryStats& stats, const FootprintMode mode, const CliqueRange* range) const {',
              '    fp::Scope fp_oracle("oracle_preparation"); fp::OracleEnd fp_oracle_end{request, stats};')
        cleanup('VertexSet interval;', 'interval', 'query')
        cleanup('const auto footprints = range ? local_footprints(request, mode, *range) : aggregate_footprints(index_, request, mode);', 'footprints', 'footprints')
        cleanup('VertexSet result;', 'oracle_result', 'query')
        after('if (reuse) {', '            fp::Scope fp_reuse("count_reuse"); fp::add("reused_endpoint_counts");')
    elif path == 'src/solver/traversal.cpp':
        after('std::size_t CliqueRange::partition(const VertexSet& z) {',
              '    fp::Scope fp_partition("clique_partition"); fp::checkpoint("clique_partition"); fp::add("partition_calls");')
        cleanup('Membership members(index_.graph().size());', 'partition_members', 'partition')
        after('Membership members(index_.graph().size());', '    fp::add("partition_marker_slots", index_.graph().size());')
        after('const auto& clique = index_.cliques()[ids_[i]];', '        fp::add("partition_clique_visits");')
        replace('return members.contains(v);', 'fp::add("partition_membership_vertex_tests"); return members.contains(v);')
        before('std::swap(ids_[middle], ids_[i]);', 'fp::add("partition_left_cliques"); fp::add("partition_swap_calls");')
        before('    return middle;', '    fp::add("partition_right_cliques", end_ - middle);')
        after(': oracle_(oracle), work_(work) {', '    fp::Scope fp_init("clique_id_setup");')
        after('std::iota(ids_.begin(), ids_.end(), std::size_t{0});', '        fp::add("clique_ids_initialized", ids_.size());')
        cleanup('const auto frame = std::move(stack_.back());', 'frame', 'interval')
        replace('stack_.pop_back();', '{ fp::Scope fp_pop("cleanup_pending_intervals"); stack_.pop_back(); }')
        before('const auto z = oracle_.separate_impl', 'fp::CleanupEnd fp_end_z;')
        after('work_ == CliqueWork::Global ? nullptr : &range, work_ == CliqueWork::IntervalReuse, &middle);',
              '    fp::CleanupBegin fp_begin_z(fp_end_z, "cleanup_query");')
    elif path == 'src/solver/solver.cpp':
        after('const TraceSink& trace, const StopRequested& stop, const OracleOptions options) {',
              '    fp::Scope fp_solver("orchestration"); fp::SolveScope fp_solve;')
        cleanup('IntervalTraversal traversal(oracle, options.clique_work);', 'traversal', 'clique_worklists')
        after('stats.clique_id_size = traversal.id_size(); stats.clique_id_capacity = traversal.id_capacity();',
              '    fp::worklist_summary(traversal);')
        cleanup('Membership lower(index.graph().size());', 'lower', 'solver')
        after('while (!traversal.empty()) {\n        cancelled();', '        fp::QueryScope fp_query;')
        cleanup('QueryStats query;', 'query_stats', 'query')
        before('const auto step = [&] {', 'fp::CleanupEnd fp_end_step;')
        after('        }();', '        fp::CleanupBegin fp_begin_step(fp_end_step, "cleanup_query");')
        after('if (trace) trace(interval, z, query);', '        fp::query_semantics(index.graph(), interval, z); fp::worklist_summary(traversal);')
        after('if (z.vertices() != y) {', '            fp::split();')
        before('VertexSet added;', 'fp::Scope fp_terminal("terminal_extraction"); fp::checkpoint("terminal_extraction");')
        cleanup('VertexSet added;', 'added', 'terminal')
        cleanup('std::vector<VertexSet> accepted;', 'accepted', 'terminal')
        replace('for (auto& component : index.graph().induced_components(added)) {',
                '{ fp::CleanupEnd fp_end_components;\n'
                '        auto fp_components = index.graph().induced_components(added);\n'
                '        fp::CleanupBegin fp_begin_components(fp_end_components, "cleanup_terminal");\n'
                '        for (auto& component : fp_components) {')
        before('        // Internal IDs are in numeric original-ID order;', '        } // original range-for temporary lifetime ends here')
        after('if (!touches_lower) accepted.push_back(std::move(component));', '            else fp::add("rejected_components");')
        after('std::sort(accepted.begin(), accepted.end());', '        fp::layer(accepted.size());')
        before('const auto count = index.count(component);', 'fp::CountSite fp_site("emitted");')
        after('result.solutions.push_back({std::move(component), count, density});', '            fp::rank(result.solutions.size());')
    else:
        raise ValueError(path)

    # Every edit is invertible and cannot silently consume another anchor.
    restored = text
    for old, new in reversed(edits):
        restored = restored.replace(new, old)
    if restored.encode() != original:
        raise ValueError(f'{path}: failed reversible-edit check')
    return ('#include "observer.hpp"\n' + text).encode(), len(edits)


SOURCES = ['src/cli/main.cpp', 'src/cli/dispatch.cpp', 'src/clique/materialized.cpp',
           'src/clique/core.cpp', 'src/oracle/closure.cpp', 'src/solver/traversal.cpp', 'src/solver/solver.cpp']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    pins = json.loads((HERE / 'source_pins.json').read_text())
    for path, digest in pins.items():
        if sha((args.root / path).read_bytes()) != digest:
            raise ValueError(f'production source drift: {path}')
    generated = {path: generate(path, (args.root / path).read_bytes()) for path in SOURCES}
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {'schema': 1, 'production': pins, 'observer': {}, 'generated': {}}
    for path, (data, edits) in generated.items():
        target = args.output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
        manifest['generated'][path] = {'sha256': sha(data), 'reversible_edits': edits}
    for path in sorted(HERE.iterdir()):
        if path.is_file():
            manifest['observer'][path.name] = sha(path.read_bytes())
    (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
