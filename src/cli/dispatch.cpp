#include "vflhcds/cli/dispatch.hpp"
#include "vflhcds/core/build_info.hpp"
#include "vflhcds/io/solution.hpp"
#include "vflhcds/io/status.hpp"
#include <chrono>
#include <iomanip>
#include <map>
#include <optional>
#include <ostream>
#include <sstream>

namespace vflhcds {
namespace {
using Clock = std::chrono::steady_clock;
int operation(const std::vector<std::string_view>& args, std::ostream& out,
              std::ostream& err, std::optional<QueryStats>& stats, std::optional<SolveStats>& run_stats,
              std::size_t& output_count, const StopRequested& stop) {
    if (args.empty() || (args[0] != "oracle" && args[0] != "inspect-graph" && args[0] != "solve"))
        throw std::invalid_argument("unknown command");
    const bool oracle = args[0] == "oracle", solving = args[0] == "solve";
    std::map<std::string, std::string> options;
    for (std::size_t i = 1; i < args.size();) {
        const std::string key(args[i++]);
        const bool flag = solving && key == "--all";
        const bool known = key == "--graph" || ((oracle || solving) && (key == "--h" || key == "--output"))
            || (oracle && (key == "--lambda" || key == "--x" || key == "--y"))
            || (solving && (key == "--k" || key == "--core-reduction" || flag));
        if (!known || (!flag && i == args.size())) throw std::invalid_argument("unknown or missing option");
        const std::string value = flag ? "" : std::string(args[i++]);
        if (!options.emplace(key, value).second) throw std::invalid_argument("duplicate option");
    }
    if (options.count("--graph") == 0 || ((oracle || solving) && options.count("--h") == 0)
        || (oracle && (options.count("--lambda") == 0 || options.count("--x") != options.count("--y")))
        || (solving && options.count("--k") + options.count("--all") != 1))
        throw std::invalid_argument("missing required option");
    BigInt h = 2;
    Fraction lambda;
    std::optional<BigInt> k;
    if (oracle || solving) {
        h = parse_integer(options.at("--h"));
        if (h < 2) throw std::invalid_argument("h < 2");
    }
    if (oracle) lambda = Fraction::parse(options.at("--lambda"));
    if (solving) {
        if (options.count("--k") != 0) {
            k = parse_integer(options.at("--k"));
            if (*k < 1) throw std::invalid_argument("k < 1");
        }
        if (options.count("--core-reduction") != 0 && options.at("--core-reduction") != "off")
            throw std::invalid_argument("only core off is implemented");
    }
    const auto cancelled = [&] { if (stop && stop()) throw Incomplete("controlled cancellation"); };
    cancelled();
    const auto graph = parse_graph(read_text_file(options.at("--graph")));
    const auto postload = Clock::now();
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
    cancelled();
    std::string result, semantic_hash;
    bool k_reached = false;
    std::optional<Clock::time_point> postindex;
    if (oracle || solving) {
        const MaterializedCliques index(graph, h);
        postindex = Clock::now();
        cancelled();
        if (solving) {
            run_stats.emplace();
            const auto answer = solve(index, k, CapacityPolicy::Auto, &*run_stats, {}, stop);
            k_reached = answer.k_reached;
            BigInt rank = 0;
            for (const auto& solution : answer.solutions) {
                cancelled();
                result += solution_json(index, solution, ++rank);
                ++output_count;
            }
            semantic_hash = sha256(semantic_header(graph, h) + result);
        } else {
            const ClosureOracle closure(index);
            stats.emplace();
            const auto answer = restricted
                ? closure.largest_restricted(request, CapacityPolicy::Auto, &*stats)
                : closure.global_F(closure.full_graph_request(lambda), CapacityPolicy::Auto, &*stats);
            result = oracle_json(index, lambda, answer);
            output_count = 1;
        }
    } else { result = inspect_json(graph); output_count = 1; }
    cancelled();
    if (destination == "-") { out << result; out.flush(); if (!out) throw IoError("stdout write"); }
    else atomic_write(destination, result);
    const auto finished = Clock::now();
    std::ostringstream timing;
    timing << std::setprecision(17) << "{\"T_e2e\":null,\"T_postload\":"
           << std::chrono::duration<double>(finished - postload).count() << ",\"T_core\":";
    if (postindex) timing << std::chrono::duration<double>(finished - *postindex).count(); else timing << "null";
    timing << '}';
    err << "{\"schema_version\":1,\"status\":\"completed\",\"complete\":true,\"output_count\":" << output_count
        << ",\"semantic_sha256\":" << (solving ? "\"" + semantic_hash + "\"" : "null")
        << ",\"termination\":\"" << (k_reached ? "k_reached" : "exhausted") << "\"";
    if (stats) err << ",\"counters\":" << query_stats_json(*stats);
    if (run_stats) err << ",\"counters\":" << solve_stats_json(*run_stats);
    err << ",\"timing\":" << timing.str() << "}\n";
    return exit_code(RunStatus::completed);
}
}  // namespace
int run_cli(const std::vector<std::string_view>& args, std::ostream& out, std::ostream& err,
            const std::function<bool()>& stop) {
    if (args.size() == 1 && (args[0] == "--help" || args[0] == "help")) {
        out << "VF-LhCDS M3 exact fixed-k solver\n"
               "Usage: vflhcds --help | print-build-info | inspect-graph --graph G\n"
               "       vflhcds solve --graph G --h H (--k K | --all) [--core-reduction off] [--output P]\n"
               "       vflhcds oracle --graph G --h H --lambda A/B [--x X --y Y] [--output P]\n"
               "Contracts: docs/INTERFACE_CONTRACT.md\n";
        return exit_code(RunStatus::completed);
    }
    if (args.size() == 1 && args[0] == "print-build-info") {
        const auto info = build_info();
        out << "version=" << info.version << "\nstage=M3\ncxx_standard=17\n"
            << "compiler=" << info.compiler << "\ncompiler_version=" << info.compiler_version
            << "\nbuild_type=" << info.build_type << "\nsanitizers=" << info.sanitizers << '\n';
        return exit_code(RunStatus::completed);
    }
    std::optional<QueryStats> stats;
    std::optional<SolveStats> run_stats;
    std::size_t output_count = 0;
    RunStatus status = RunStatus::internal_error;
    try { return operation(args, out, err, stats, run_stats, output_count, stop); }
    catch (const InvalidGraph&) { status = RunStatus::invalid_graph; }
    catch (const std::invalid_argument&) { status = RunStatus::invalid_argument; }
    catch (const IoError&) { status = RunStatus::io_error; }
    catch (const ResourceLimit&) { status = RunStatus::resource_limit; }
    catch (const std::length_error&) { status = RunStatus::resource_limit; }
    catch (const Incomplete&) { status = RunStatus::incomplete; }
    catch (const std::bad_alloc&) { status = RunStatus::oom; }
    catch (const std::exception&) { status = RunStatus::internal_error; }
    err << "{\"schema_version\":1,\"status\":\"" << status_name(status)
        << "\",\"complete\":false,\"output_count\":" << output_count << ",\"semantic_sha256\":null";
    if (stats) err << ",\"counters\":" << query_stats_json(*stats);
    if (run_stats) err << ",\"counters\":" << solve_stats_json(*run_stats);
    err << "}\n";
    return exit_code(status);
}
}  // namespace vflhcds
