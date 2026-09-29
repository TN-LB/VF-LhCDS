#include "vflhcds/cli/dispatch.hpp"
#include "vflhcds/core/build_info.hpp"
#include "vflhcds/io/graph.hpp"
#include "vflhcds/io/status.hpp"
#include <map>
#include <optional>
#include <ostream>

namespace vflhcds {
namespace {
int operation(const std::vector<std::string_view>& args, std::ostream& out,
              std::ostream& err, std::optional<QueryStats>& stats, std::size_t& output_count) {
    if (args.empty() || (args[0] != "oracle" && args[0] != "inspect-graph"))
        throw std::invalid_argument("unknown command");
    const bool oracle = args[0] == "oracle";
    std::map<std::string, std::string> options;
    for (std::size_t i = 1; i < args.size(); i += 2) {
        const auto key = args[i];
        if (i + 1 >= args.size() || (key != "--graph" && (!oracle || (key != "--h"
            && key != "--lambda" && key != "--x" && key != "--y" && key != "--output"))))
            throw std::invalid_argument("unknown or missing option");
        if (!options.emplace(std::string(key), std::string(args[i + 1])).second)
            throw std::invalid_argument("duplicate option");
    }
    if (options.count("--graph") == 0 || (oracle && (options.count("--h") == 0
        || options.count("--lambda") == 0 || options.count("--x") != options.count("--y"))))
        throw std::invalid_argument("missing required option");
    BigInt h = 2;
    Fraction lambda;
    if (oracle) {
        h = parse_integer(options.at("--h"));
        if (h < 2) throw std::invalid_argument("h < 2");
        lambda = Fraction::parse(options.at("--lambda"));
    }
    const auto graph = parse_graph(read_text_file(options.at("--graph")));
    const std::string destination = options.count("--output") != 0 ? options.at("--output") : "-";
    std::vector<std::string> inputs{options.at("--graph")};
    RestrictedRequest request{{}, graph.all_vertices(), lambda};
    const bool restricted = options.count("--x") != 0;
    if (restricted) {
        inputs.push_back(options.at("--x")); inputs.push_back(options.at("--y"));
        request.x = parse_set(read_text_file(inputs[1]), graph);
        request.y_oracle = parse_set(read_text_file(inputs[2]), graph);
        if (!subset(request.x, request.y_oracle)) throw std::invalid_argument("invalid bounds");
    }
    reject_input_alias(destination, inputs);
    std::string result;
    if (oracle) {
        const MaterializedCliques index(graph, h);
        const ClosureOracle closure(index);
        stats.emplace();
        const auto answer = restricted
            ? closure.largest_restricted(request, CapacityPolicy::Auto, &*stats)
            : closure.global_F(closure.full_graph_request(lambda), CapacityPolicy::Auto, &*stats);
        result = oracle_json(index, lambda, answer);
    } else result = inspect_json(graph);
    output_count = 1;  // Fully serialized; file commit may still fail.
    if (destination == "-") { out << result; out.flush(); if (!out) throw IoError("stdout write"); }
    else atomic_write(destination, result);
    err << "{\"schema_version\":1,\"status\":\"completed\",\"complete\":true,\"output_count\":1,"
           "\"semantic_sha256\":null,\"termination\":\"exhausted\"";
    if (stats) err << ",\"counters\":" << query_stats_json(*stats);
    err << "}\n";
    return exit_code(RunStatus::completed);
}
}  // namespace
int run_cli(const std::vector<std::string_view>& args, std::ostream& out, std::ostream& err) {
    if (args.size() == 1 && (args[0] == "--help" || args[0] == "help")) {
        out << "VF-LhCDS M2 exact primitives\n"
               "Usage: vflhcds --help | print-build-info | inspect-graph --graph G\n"
               "       vflhcds oracle --graph G --h H --lambda A/B [--x X --y Y] [--output P]\n"
               "Reserved: solve (M3)\nContracts: docs/INTERFACE_CONTRACT.md\n";
        return exit_code(RunStatus::completed);
    }
    if (args.size() == 1 && args[0] == "print-build-info") {
        const auto info = build_info();
        out << "version=" << info.version << "\nstage=M2\ncxx_standard=17\n"
            << "compiler=" << info.compiler << "\ncompiler_version=" << info.compiler_version
            << "\nbuild_type=" << info.build_type << "\nsanitizers=" << info.sanitizers << '\n';
        return exit_code(RunStatus::completed);
    }
    if (!args.empty() && args[0] == "solve") {
        write_failure_status(err, RunStatus::not_implemented);
        return exit_code(RunStatus::not_implemented);
    }
    std::optional<QueryStats> stats;
    std::size_t output_count = 0;
    RunStatus status = RunStatus::internal_error;
    try { return operation(args, out, err, stats, output_count); }
    catch (const InvalidGraph&) { status = RunStatus::invalid_graph; }
    catch (const std::invalid_argument&) { status = RunStatus::invalid_argument; }
    catch (const IoError&) { status = RunStatus::io_error; }
    catch (const ResourceLimit&) { status = RunStatus::resource_limit; }
    catch (const std::length_error&) { status = RunStatus::resource_limit; }
    catch (const std::bad_alloc&) { status = RunStatus::oom; }
    catch (const std::exception&) { status = RunStatus::internal_error; }
    err << "{\"schema_version\":1,\"status\":\"" << status_name(status)
        << "\",\"complete\":false,\"output_count\":" << output_count << ",\"semantic_sha256\":null";
    if (stats) err << ",\"counters\":" << query_stats_json(*stats);
    err << "}\n";
    return exit_code(status);
}
}  // namespace vflhcds
