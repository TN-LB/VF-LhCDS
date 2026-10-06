#include "vflhcds/io/solution.hpp"
#include <chrono>
#include <iomanip>
#include <iostream>

namespace {
using Clock = std::chrono::steady_clock;
void mark(const Clock::time_point& start, const char* phase, const char* event) {
    std::cerr << std::setprecision(17)
              << "{\"diagnostic_schema\":1,\"phase\":\"" << phase
              << "\",\"event\":\"" << event << "\",\"elapsed_seconds\":"
              << std::chrono::duration<double>(Clock::now() - start).count()
              << "}\n" << std::flush;
    if (!std::cerr) throw std::runtime_error("cannot flush phase marker");
}
}  // namespace

int main(int argc, char** argv) {
    const auto start = Clock::now();
    if (argc != 4 && argc != 5) return 2;  // GRAPH H K [combinations|adjacency].
    try {
        using namespace vflhcds;
        const BigInt h = parse_integer(argv[2]), k = parse_integer(argv[3]);
        if (h < 2 || k < 1) return 2;
        const std::string mode = argc == 5 ? argv[4] : "combinations";
        if (mode != "combinations" && mode != "adjacency") return 2;
        const auto enumeration = mode == "adjacency" ? CliqueEnumeration::Adjacency
                                                     : CliqueEnumeration::Combinations;
        mark(start, "parse", "begin");
        const auto graph = parse_graph(read_text_file(argv[1]));
        mark(start, "parse", "end");
        mark(start, "index", "begin");
        const MaterializedCliques index(graph, h, enumeration);
        mark(start, "index", "end");
        mark(start, "solve", "begin");
        OracleOptions options;
        options.core = CoreMode::Off;
        options.footprints = FootprintMode::Sorted;
        SolveStats stats;
        const TraceSink trace = [&](const ChainInterval&, const ChainPoint&, const QueryStats& query) {
            std::cerr << std::setprecision(17)
                      << "{\"diagnostic_schema\":1,\"phase\":\"query\",\"event\":\"end\","
                      << "\"elapsed_seconds\":"
                      << std::chrono::duration<double>(Clock::now() - start).count()
                      << ",\"query_index\":" << stats.logical_interval_queries
                      << ",\"stats\":" << query_stats_json(query) << "}\n" << std::flush;
            if (!std::cerr) throw std::runtime_error("cannot flush query marker");
        };
        const auto result = solve(index, k, CapacityPolicy::Auto, &stats, trace, {}, options);
        mark(start, "solve", "end");
        mark(start, "serialize", "begin");
        BigInt rank = 0;
        std::string output;
        for (const auto& solution : result.solutions)
            output += solution_json(index, solution, ++rank);
        std::cout << output << std::flush;
        if (!std::cout) throw std::runtime_error("cannot write diagnostic output");
        mark(start, "serialize", "end");
        return 0;
    } catch (const std::exception&) {
        std::cerr << "{\"diagnostic_schema\":1,\"status\":\"error\"}\n" << std::flush;
        return 1;
    }
}
