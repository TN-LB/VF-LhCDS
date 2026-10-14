#include "observer.hpp"
#include <csignal>
#include <iostream>

// Test-only adapter. Forced interruption does not represent a solver benchmark.
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    fp::Session session(argc, argv);
    const std::string mode = argv[1];
    if (mode == "kill") {
        fp::Scope scope("test_interrupted_phase");
        fp::checkpoint("test_interrupted_phase");
        std::raise(SIGKILL);
        return 2;
    }
    using namespace vflhcds;
    const Graph graph({0,1,2,3,4}, {{0,1},{0,2},{1,2}});
    const MaterializedCliques index(graph, 3, CliqueEnumeration::Adjacency, CliqueCounting::Membership);
    const ClosureOracle oracle(index);
    if (mode == "fallback") {
        const Fraction huge((BigInt(1)<<130U)+1, (BigInt(1)<<131U)+3);
        const auto actual = oracle.global_F(oracle.full_graph_request(huge), CapacityPolicy::Auto, nullptr,
                                          {CoreMode::Off, FootprintMode::Membership});
        if (actual.stats.capacity_backend != "arbitrary_precision" || actual.stats.mincut_calls != 1)
            return 2;
        fp::state.status = 0;
        std::cout << vertices_json(graph, actual.vertices) << '\n';
        return 0;
    }
    if (mode == "cancel") {
        bool cancel = false;
        try {
            (void)solve(index, std::nullopt, CapacityPolicy::Auto, nullptr,
                        [&](const ChainInterval&, const ChainPoint&, const QueryStats&) { cancel = true; },
                        [&] { return cancel; }, {CoreMode::Off, FootprintMode::Membership});
        } catch (const Incomplete&) {
            fp::state.status = 7;
            return 7;
        }
    }
    return 2;
}
