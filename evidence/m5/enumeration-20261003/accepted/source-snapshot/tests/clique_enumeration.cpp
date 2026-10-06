#include "enumeration_equivalence.hpp"
#include "vflhcds/oracle/closure.hpp"
#include <iostream>

using namespace vflhcds;
namespace {
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
template<class Function> void rejects(Function function) {
    try { function(); } catch (const std::invalid_argument&) { return; }
    throw std::runtime_error("T04-EDGE missing argument rejection");
}
void check() {
    const Graph k4({9, -2, 1, 4}, {{-2,1},{-2,4},{-2,9},{1,4},{1,9},{4,9}});
    const auto triangles = checked_adjacency_index(k4, 3);
    require(triangles.cliques() == std::vector<VertexSet>({{0,1,2},{0,1,3},{0,2,3},{1,2,3}}),
            "T04-ADJ lexicographic triangles");
    require(triangles.incidence() == std::vector<std::vector<std::size_t>>({{0,1,2},{0,1,3},{0,2,3},{1,2,3}}),
            "T04-ADJ exact clique IDs");
    const BigInt huge = BigInt(1) << 200U;
    const Graph mixed({huge, -huge, 0, 7, 11, 17}, {{-huge,0},{-huge,7},{0,7},{7,11},{11,17},{7,17}});
    for (int h = 2; h <= 7; ++h) {
        const auto adjacency = checked_adjacency_index(mixed, h);
        const MaterializedCliques control(mixed, h);
        BigInt degree_sum = 0;
        for (VertexId v = 0; v < mixed.size(); ++v) degree_sum += adjacency.degree(v);
        require(degree_sum == BigInt(h) * adjacency.cliques().size(), "T04-ADJ degree sum");
        for (std::size_t mask = 0; mask < (std::size_t{1} << mixed.size()); ++mask) {
            VertexSet set;
            for (VertexId v = 0; v < mixed.size(); ++v) if ((mask & (std::size_t{1} << v)) != 0) set.push_back(v);
            require(adjacency.count(set) == control.count(set), "T04-ADJ induced subset counts");
        }
    }
    const auto absent = checked_adjacency_index(mixed, huge);
    require(absent.cliques().empty() && absent.incidence().size() == mixed.size(), "T04-EDGE huge h preserves vertices");
    const Graph isolated({-1, 0, 1}, {});
    require(checked_adjacency_index(isolated, 2).cliques().empty(), "T04-EDGE no edges");
    for (const auto mode : {CliqueEnumeration::Combinations, CliqueEnumeration::Adjacency})
        rejects([&] { (void)MaterializedCliques(mixed, 1, mode); });
    rejects([&] { (void)MaterializedCliques(mixed, huge, static_cast<CliqueEnumeration>(99)); });
    // h=n follows a deep unique branch; no recursive C++ call stack is needed.
    std::vector<BigInt> vertices;
    std::vector<OriginalEdge> edges;
    for (int i = 0; i < 128; ++i) {
        vertices.emplace_back(i);
        for (int j = 0; j < i; ++j) edges.emplace_back(j, i);
    }
    const Graph complete(std::move(vertices), edges);
    const auto deep = checked_adjacency_index(complete, 128);
    require(deep.cliques() == std::vector<VertexSet>{complete.all_vertices()}, "T04-EDGE high h unique clique");
    const auto index = checked_adjacency_index(mixed, 2);
    const ClosureOracle oracle(index);
    const Fraction lambda((BigInt(1) << 130U) + 1, (BigInt(1) << 131U) + 3);
    const auto answer = oracle.global_F(oracle.full_graph_request(lambda));
    require(answer.stats.capacity_backend == "arbitrary_precision" && answer.stats.mincut_calls == 1,
            "T05 adjacency uses actual automatic arbitrary-precision flow");
}
}  // namespace
int main() {
    try { check(); }
    catch (const std::exception& error) { std::cerr << error.what() << '\n'; return 1; }
    std::cout << "T04-ADJ/T04-EDGE/T05: ordered enumeration, boundaries and fallback passed\n";
}
