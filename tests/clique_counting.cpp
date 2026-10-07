#include "vflhcds/oracle/closure.hpp"
#include <iostream>

using namespace vflhcds;
namespace {
void require(bool value) { if (!value) throw std::runtime_error("T04-COUNT failed"); }
template<class F> void rejects(F function) {
    try { function(); } catch (const std::invalid_argument&) { return; }
    throw std::runtime_error("T04-COUNT missing invalid-set/mode rejection");
}
void check() {
    const BigInt huge = BigInt(1) << 200U;
    const Graph graph({-huge, 0, 7, 11, 17, huge}, {{-huge,0},{-huge,7},{0,7},{7,11},{11,17},{7,17}});
    for (const auto enumeration : {CliqueEnumeration::Combinations, CliqueEnumeration::Adjacency}) {
        for (const BigInt& h : std::vector<BigInt>{2,3,4,6,7,huge}) {
            const MaterializedCliques sorted(graph, h, enumeration, CliqueCounting::Sorted);
            const MaterializedCliques membership(graph, h, enumeration, CliqueCounting::Membership);
            require(sorted.cliques() == membership.cliques() && sorted.incidence() == membership.incidence());
            for (std::size_t mask = 0; mask < (std::size_t{1} << graph.size()); ++mask) {
                VertexSet set;
                for (VertexId v = 0; v < graph.size(); ++v)
                    if ((mask & (std::size_t{1} << v)) != 0) set.push_back(v);
                require(sorted.count(set) == membership.count(set));
                require(membership.count({}) == 0);  // No marker leakage across unrelated queries.
                require(membership.count(graph.all_vertices()) == BigInt(membership.cliques().size()));
                require(sorted.count(set) == membership.count(set));
            }
            for (const VertexSet& invalid : std::vector<VertexSet>{{1,0},{0,0},{graph.size()}}) {
                rejects([&] { (void)sorted.count(invalid); });
                rejects([&] { (void)membership.count(invalid); });
            }
        }
        rejects([&] { (void)MaterializedCliques(graph, huge, enumeration, static_cast<CliqueCounting>(99)); });
    }
    const Graph isolate({huge}, {});
    require(MaterializedCliques(isolate, 2, CliqueEnumeration::Adjacency, CliqueCounting::Membership).count({0}) == 0);
    const MaterializedCliques index(graph, 2, CliqueEnumeration::Adjacency, CliqueCounting::Membership);
    const ClosureOracle oracle(index);
    QueryStats stats;
    const Fraction lambda((BigInt(1) << 130U) + 1, (BigInt(1) << 131U) + 3);
    const auto point = oracle.global_chain_point(lambda, CapacityPolicy::Auto, &stats);
    require(stats.capacity_backend == "arbitrary_precision" && stats.mincut_calls == 1);
    require(point.cliques() == index.count(point.vertices()));
}
}  // namespace
int main() {
    try { check(); }
    catch (const std::exception& error) { std::cerr << error.what() << '\n'; return 1; }
    std::cout << "T04-COUNT: subset counts, repeated sets, invalid sets, both enumerators and real fallback passed\n";
}
