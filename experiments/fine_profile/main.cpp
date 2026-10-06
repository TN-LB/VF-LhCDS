#include "vflhcds/io/solution.hpp"
#include "profile.hpp"
#include <iomanip>
#include <iostream>

int main(int argc, char** argv) {
    if (argc != 4) return 2;  // GRAPH H K; adjacency/membership/core-off are fixed.
    using namespace vflhcds;
    const auto start = vf_profile::Clock::now();
    const auto elapsed = [&] { return std::chrono::duration<double>(vf_profile::Clock::now() - start).count(); };
    const auto mark = [&](const char* phase, const char* event) {
        std::cerr << std::setprecision(17) << "{\"schema\":1,\"phase\":\"" << phase
                  << "\",\"event\":\"" << event << "\",\"elapsed_seconds\":" << elapsed() << "}\n" << std::flush;
        if (!std::cerr) throw std::runtime_error("cannot flush diagnostic marker");
    };
    try {
        const BigInt h = parse_integer(argv[2]), k = parse_integer(argv[3]);
        if (h < 2 || k < 1) return 2;
        mark("parse", "begin");
        const auto graph = parse_graph(read_text_file(argv[1]));
        mark("parse", "end");
        mark("index", "begin");
        const MaterializedCliques index(graph, h, CliqueEnumeration::Adjacency);
        mark("index", "end");
        OracleOptions options;
        options.core = CoreMode::Off;
        options.footprints = FootprintMode::Membership;
        SolveStats stats;
        const TraceSink trace = [&](const ChainInterval&, const ChainPoint&, const QueryStats& query) {
            vf_profile::Scope measure(vf_profile::Phase::Trace);
            std::cerr << "{\"schema\":1,\"phase\":\"query\",\"event\":\"end\",\"elapsed_seconds\":"
                      << elapsed() << ",\"query_index\":" << stats.logical_interval_queries
                      << ",\"stats\":" << query_stats_json(query) << ",\"exclusive\":";
            vf_profile::write_json(std::cerr);
            std::cerr << "}\n" << std::flush;
            if (!std::cerr) throw std::runtime_error("cannot flush diagnostic query");
        };
        mark("solve", "begin");
        const auto result = [&] {
            vf_profile::Scope measure(vf_profile::Phase::SolverOther);
            return solve(index, k, CapacityPolicy::Auto, &stats, trace, {}, options);
        }();
        mark("solve", "end");
        std::cerr << "{\"schema\":1,\"phase\":\"summary\",\"exclusive\":";
        vf_profile::write_json(std::cerr);
        std::cerr << ",\"stats\":" << solve_stats_json(stats) << "}\n" << std::flush;
        mark("serialize", "begin");
        BigInt rank = 0;
        for (const auto& solution : result.solutions)
            std::cout << solution_json(index, solution, ++rank);
        std::cout << std::flush;
        if (!std::cout) throw std::runtime_error("cannot write diagnostic output");
        mark("serialize", "end");
        return 0;
    } catch (const std::exception&) {
        std::cerr << "{\"schema\":1,\"status\":\"error\"}\n" << std::flush;
        return 1;
    }
}
