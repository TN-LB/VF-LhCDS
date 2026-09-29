#include "vflhcds/oracle/closure.hpp"
#include <iostream>
int main() {
    using namespace vflhcds;
    const Graph graph({0,1},{{0,1}});
    const MaterializedCliques index(graph,2);
    const ClosureOracle oracle(index);
    auto original = oracle.full_graph_request(Fraction(0));
    auto transferred = std::move(original);
    const auto kept = oracle.global_F(transferred);
    const auto reused = oracle.global_F(original);
    std::cout << "transferred size=" << kept.vertices.size() << ", original size=" << reused.vertices.size() << '\n';
    return kept.vertices == graph.all_vertices() && reused.vertices == graph.all_vertices() ? 0 : 1;
}
