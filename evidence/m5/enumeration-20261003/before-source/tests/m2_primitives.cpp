#include "vflhcds/io/graph.hpp"
#include "vflhcds/flow/dinic.hpp"
#include <algorithm>
#include <iostream>
#include <type_traits>

using namespace vflhcds;
namespace {
std::size_t checks = 0;
void require(bool condition, const char* message) {
    ++checks; if (!condition) throw std::runtime_error(message);
}
template<class Error, class Function> void rejects(Function function) {
    try { function(); } catch (const Error&) { ++checks; return; }
    throw std::runtime_error("expected rejection");
}
struct Edge { std::size_t from, to; BigInt capacity; };
template<class Capacity> void check_flow(std::size_t n, const std::vector<Edge>& edges) {
    Dinic<Capacity> flow(n);
    BigInt bound = 0;
    for (const auto& edge : edges) {
        if constexpr (std::is_same_v<Capacity, UInt128>) flow.add_arc(edge.from, edge.to, to_uint128(edge.capacity));
        else flow.add_arc(edge.from, edge.to, edge.capacity);
        bound += edge.capacity;
    }
    BigInt expected = bound;
    for (std::size_t bits = 0; bits < (std::size_t{1} << n); ++bits) {
        if ((bits & 1U) == 0 || (bits & (std::size_t{1} << (n - 1))) != 0) continue;
        BigInt cut = 0;
        for (const auto& edge : edges)
            if ((bits & (std::size_t{1} << edge.from)) != 0 && (bits & (std::size_t{1} << edge.to)) == 0) cut += edge.capacity;
        expected = std::min(expected, cut);
    }
    const auto result = flow.max_flow(0, n - 1);
    BigInt actual;
    if constexpr (std::is_same_v<Capacity, UInt128>) actual = to_big(result); else actual = result;
    require(actual == expected, "T07 flow versus independent cuts");
    const auto reachable = flow.reachable(0);
    require(reachable.back() == 0, "T07 no augmenting path");
    BigInt residual_cut = 0;
    for (const auto& edge : edges) if (reachable[edge.from] != 0 && reachable[edge.to] == 0) residual_cut += edge.capacity;
    require(residual_cut == expected, "T07 source-reachable cut");
    const auto& residual = flow.residual();
    for (std::size_t u = 0; u < residual.size(); ++u)
        for (std::size_t i = 0; i < residual[u].size(); ++i) {
            const auto& arc = residual[u][i];
            require(residual[arc.to][arc.reverse].to == u && residual[arc.to][arc.reverse].reverse == i,
                    "T07 paired reverse indices");
        }
    rejects<std::logic_error>([&] { (void)flow.max_flow(0, n - 1); });
}
void numbers() {
    const BigInt huge = BigInt(1) << 200U;
    require(parse_integer(decimal(-huge), true) == -huge, "T05 decimal round trip");
    require(Fraction(huge * 6, huge * 9) == Fraction(2, 3), "T05 gcd");
    require(Fraction(huge, huge + 1) < Fraction(huge + 1, huge + 2), "T05 exact cross multiplication");
    require(Fraction(0, huge) == Fraction(0, 1), "T05 canonical zero");
    require(scaled_objective(Fraction(huge, 3), 1, 2) == 3 - 2 * huge, "T05 signed objective");
    require(checked_add(uint128_max - 1, 1) == uint128_max, "T05 near addition limit");
    require(checked_mul(uint128_max / 3, 3) == uint128_max, "T05 exact multiplication limit");
    require(checked_sub(uint128_max, uint128_max) == 0, "T05 subtraction");
    require(to_big(to_uint128(to_big(uint128_max))) == to_big(uint128_max), "T05 conversion limit");
    rejects<std::overflow_error>([] { (void)checked_add(uint128_max, 1); });
    rejects<std::overflow_error>([] { (void)checked_sub(0, 1); });
    rejects<std::overflow_error>([] { (void)checked_mul(uint128_max, 2); });
    rejects<std::overflow_error>([] { (void)to_uint128(to_big(uint128_max) + 1); });
    rejects<std::overflow_error>([] { (void)to_uint128(-1); });
    rejects<ResourceLimit>([&] { (void)to_size(huge); });
    for (const auto* invalid : {"", "-0", "01", "+2", "2e3", "-", "--1"})
        rejects<std::invalid_argument>([&] { (void)parse_integer(invalid, true); });
    rejects<std::invalid_argument>([] { (void)Fraction(1, 0); });
    require(bit_length(huge) == 201 && bit_length(0) == 0, "T05 exact bit length");
}
void graphs() {
    const BigInt huge = BigInt(1) << 200U;
    const auto normalized = normalize_graph({huge, -huge, 0, 7}, {{0, 7}, {7, 0}, {huge, huge}});
    const auto& graph = normalized.graph;
    require(graph.size() == 4 && normalized.removed_loops == 1 && normalized.removed_duplicates == 1, "T01 raw normalization");
    require(graph.originals() == std::vector<BigInt>({-huge, 0, 7, huge}), "T01 exact sorted ID mapping");
    require(graph.internal_id(huge) == 3 && graph.internal_id(-huge) == 0, "T01 reversible mapping");
    require(graph.induced_components(graph.all_vertices()) == std::vector<VertexSet>({{0}, {1, 2}, {3}}), "T01 ordinary components");
    require(graph.induced_components({1, 3}) == std::vector<VertexSet>({{1}, {3}}), "T01 induced components");
    require(canonical_graph(parse_graph(canonical_graph(graph))) == canonical_graph(graph), "T01 canonical roundtrip");
    require(parse_graph("vflhcds-graph\t1 n 2 v 9 v -2 m 1 e 9 -2 ").originals() == std::vector<BigInt>({-2, 9}), "T01 accepted order/whitespace");
    rejects<InvalidGraph>([] { (void)Graph({}, {}); });
    rejects<InvalidGraph>([] { (void)Graph({0, 0}, {}); });
    rejects<InvalidGraph>([] { (void)Graph({0}, {{0, 1}}); });
    rejects<InvalidGraph>([] { (void)Graph({0}, {{0, 0}}); });
    rejects<InvalidGraph>([] { (void)Graph({0, 1}, {{0, 1}, {1, 0}}); });
    rejects<InvalidGraph>([] { (void)normalize_graph({0}, {{1, 1}}); });
    rejects<std::invalid_argument>([&] { graph.validate_set({2, 1}); });
    Membership marks(4); marks.assign({0, 3}); marks.assign({1});
    require(!marks.contains(0) && marks.contains(1) && !marks.contains(3), "T01 reusable markers");
    require(sha256("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "SHA empty");
    require(sha256("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "SHA abc");
    require(sha256(std::string(1000000, 'a')) == "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0", "SHA million a");
}
void flows() {
    for (unsigned bits = 0; bits < 64; ++bits) {
        std::vector<Edge> edges; unsigned position = 0;
        for (std::size_t u = 0; u < 3; ++u) for (std::size_t v = 0; v < 3; ++v) if (u != v) {
            if ((bits & (1U << position)) != 0) edges.push_back({u, v, BigInt(position + 1)});
            ++position;
        }
        check_flow<UInt128>(3, edges); check_flow<BigInt>(3, edges);
    }
    const BigInt large = BigInt(1) << 80U;
    const std::vector<Edge> tricky{{0,0,7}, {0,1,large}, {0,1,5}, {1,0,9}, {0,2,large},
        {1,2,large}, {2,1,large}, {1,3,large}, {2,3,large}, {3,3,3}, {1,3,0}};
    check_flow<UInt128>(4, tricky); check_flow<BigInt>(4, tricky);
    const std::vector<Edge> cancellation{{0,1,1},{0,2,1},{1,3,1},{1,4,1},{2,3,1},{3,5,1},{4,5,1}};
    check_flow<UInt128>(6, cancellation); check_flow<BigInt>(6, cancellation);
    check_flow<BigInt>(3, {{0,1,BigInt(1)<<180U}, {1,2,BigInt(1)<<181U}});
    check_flow<UInt128>(2, {{0,1,to_big(uint128_max)}});
    check_flow<BigInt>(2, {{0,1,to_big(uint128_max)}});
    Dinic<UInt128> overflow(2); overflow.add_arc(0, 1, uint128_max); overflow.add_arc(0, 1, 1);
    rejects<std::overflow_error>([&] { (void)overflow.max_flow(0, 1); });
    Dinic<BigInt> negative(2); rejects<std::invalid_argument>([&] { negative.add_arc(0, 1, -1); });
    constexpr std::size_t length = 20000;
    Dinic<UInt128> chain(length);
    for (std::size_t i = 1; i < length; ++i) chain.add_arc(i - 1, i, 3);
    require(chain.max_flow(0, length - 1) == 3, "T07 20000-node path without recursion");
}
void oracles() {
    static_assert(!std::is_default_constructible_v<CertifiedGlobalRequest>);
    static_assert(!std::is_constructible_v<CertifiedGlobalRequest, RestrictedRequest>);
    const Graph graph({-10, -1, 5, 9, 20}, {{-10,-1},{5,9}});
    const MaterializedCliques index(graph, 2);
    const ClosureOracle oracle(index), other(index);
    const auto tied = oracle.global_F(oracle.full_graph_request(Fraction(1, 2)));
    require(tied.vertices == VertexSet({0,1,2,3}), "T09 union of incomparable/empty/nested ties");
    require(tied.stats.mincut_calls == 1 && tied.stats.logical_interval_queries == 0, "T09 actual call counters");
    require(oracle.largest_restricted({tied.vertices, graph.all_vertices(), Fraction(1,2)}).vertices == tied.vertices,
            "T08 lower bound equals actual global F");
    require(oracle.global_F(oracle.full_graph_request(Fraction(4))).vertices.empty(), "T08 empty global");
    require(oracle.global_F(oracle.full_graph_request(Fraction(0))).vertices == graph.all_vertices(), "T08 global zero preserves isolates");
    const RestrictedRequest request{{0,1},{0,1,4},Fraction(1)};
    require(oracle.largest_restricted(request).vertices == request.x, "T08 X=F restricted");
    require(oracle.largest_restricted({{}, {0}, Fraction(0)}).vertices == VertexSet({0}), "T08 smaller zero upper restricted");
    const auto equal = oracle.largest_restricted({{0},{0},Fraction(100)});
    require(equal.vertices == VertexSet({0}) && equal.stats.mincut_calls == 0 && !equal.stats.capacity_backend, "T08 equal bounds bypass");
    require(!equal.stats.unique_footprints && !equal.stats.forward_nodes, "T08 bypass is null, not measured zero");
    rejects<std::invalid_argument>([&] { (void)other.global_F(oracle.full_graph_request(Fraction(1))); });
    rejects<std::invalid_argument>([&] { (void)oracle.largest_restricted({{1},{0},Fraction(1)}); });
    rejects<std::invalid_argument>([&] { (void)oracle.full_graph_request(Fraction(-1)); });
    const Fraction large((BigInt(1)<<130U)+1, (BigInt(1)<<131U)+3);
    const auto big = oracle.global_F(oracle.full_graph_request(large));
    require(big.vertices == tied.vertices && big.stats.capacity_backend == "arbitrary_precision" && big.stats.mincut_calls == 1,
            "T05 real nontrivial automatic fallback");
    const auto forced = oracle.global_F(oracle.full_graph_request(Fraction(1,2)), CapacityPolicy::ForceBig);
    require(forced.vertices == tied.vertices && forced.stats.capacity_backend == "arbitrary_precision", "T05 common-domain backend agreement");
    rejects<std::overflow_error>([&] { (void)oracle.global_F(oracle.full_graph_request(large), CapacityPolicy::ForceUInt128); });
    require(request.x == VertexSet({0,1}) && request.y_oracle == VertexSet({0,1,4}) && request.lambda == Fraction(1), "immutable request");
    const MaterializedCliques absent(graph, BigInt(1)<<200U);
    require(absent.cliques().empty() && absent.incidence().size() == 5, "T04 unbounded h>n");
    const Graph singleton({0}, {});
    const MaterializedCliques no_edges(singleton, 2);
    const ClosureOracle empty_oracle(no_edges);
    require(empty_oracle.global_F(empty_oracle.full_graph_request(Fraction((BigInt(1)<<127U)-1))).stats.capacity_backend == "uint128",
            "T05 preflight just below native bound");
    require(empty_oracle.global_F(empty_oracle.full_graph_request(Fraction(BigInt(1)<<127U))).stats.capacity_backend == "arbitrary_precision",
            "T05 preflight crosses native bound");
    const Graph k4({0,1,2,3}, {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}});
    const MaterializedCliques triangles(k4, 3);
    const auto footprints = aggregate_footprints(triangles, {{0,1}, {0,1,2,3}, Fraction(1)});
    require(footprints.records.size() == 3 && footprints.total_weight == 4, "T06 singleton/repeated/boundary footprints");
    require(footprints.records[0].vertices == VertexSet({2}) && footprints.records[1].vertices == VertexSet({2,3})
            && footprints.records[1].weight == 2, "T06 deterministic footprint aggregation");
    for (unsigned bits = 0; bits < 4; ++bits) {
        VertexSet s, xs{0,1};
        if ((bits & 1U) != 0) { s.push_back(2); xs.push_back(2); }
        if ((bits & 2U) != 0) { s.push_back(3); xs.push_back(3); }
        BigInt sum = 0; for (const auto& f : footprints.records) if (subset(f.vertices, s)) sum += f.weight;
        require(sum == triangles.count(xs) - triangles.count({0,1}), "T06 all-subset identity");
    }
}
}  // namespace
int main() {
    try { numbers(); graphs(); flows(); oracles(); }
    catch (const std::exception& error) { std::cerr << "FAIL: " << error.what() << '\n'; return 1; }
    std::cout << "T01/T04-T09 primitives: " << checks << " checks passed; 135 tiny cut/backend runs; 20000-node path\n";
    return 0;
}
