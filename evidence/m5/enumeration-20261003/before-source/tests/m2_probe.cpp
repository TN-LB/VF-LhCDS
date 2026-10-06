// Test-only persistent adapter. Exhaustive subset inspection is guarded here,
// outside the production library and CLI; Python owns expected truth.
#include "vflhcds/io/graph.hpp"
#include <algorithm>
#include <iostream>

using namespace vflhcds;
namespace {
std::string token() { std::string value; if (!(std::cin >> value)) throw std::runtime_error("unexpected EOF"); return value; }
BigInt integer() { return parse_integer(token(), true); }
VertexSet read_set(const Graph& graph) {
    const auto size = to_size(integer()); VertexSet set;
    for (std::size_t i = 0; i < size; ++i) set.push_back(graph.internal_id(integer()));
    std::sort(set.begin(), set.end()); graph.validate_set(set); return set;
}
void inspect(const Graph& graph, const MaterializedCliques& index) {
    if (graph.size() > 12) throw std::invalid_argument("test adapter exhaustive guard");
    std::cout << "{\"graph_sha256\":\"" << sha256(canonical_graph(graph)) << "\",\"cliques\":[";
    bool first = true;
    for (const auto& clique : index.cliques()) { if (!first) std::cout << ','; first = false; std::cout << vertices_json(graph, clique); }
    std::cout << "],\"degrees\":[";
    for (std::size_t v = 0; v < graph.size(); ++v) { if (v != 0) std::cout << ','; std::cout << index.degree(v); }
    std::cout << "],\"incidences\":[";
    for (std::size_t v = 0; v < graph.size(); ++v) {
        if (v != 0) std::cout << ',';
        std::cout << '['; first = true;
        for (const auto id : index.incidence()[v]) { if (!first) std::cout << ','; first = false; std::cout << id; }
        std::cout << ']';
    }
    std::cout << "],\"counts\":[";
    for (std::size_t mask = 0; mask < (std::size_t{1} << graph.size()); ++mask) {
        if (mask != 0) std::cout << ',';
        VertexSet set;
        for (std::size_t v = 0; v < graph.size(); ++v) if ((mask & (std::size_t{1} << v)) != 0) set.push_back(v);
        std::cout << index.count(set);
    }
    std::cout << "]}\n";
}
}  // namespace
int main() {
    try {
        std::string command;
        while (std::cin >> command) {
            if (command != "case") throw std::invalid_argument("expected case");
            const auto n = to_size(integer()), m = to_size(integer()); const BigInt h = integer();
            if (n > 12) throw std::invalid_argument("test adapter graph guard");
            std::vector<BigInt> vertices;
            for (std::size_t i = 0; i < n; ++i) vertices.push_back(integer());
            std::vector<OriginalEdge> edges;
            for (std::size_t i = 0; i < m; ++i) { BigInt u = integer(); BigInt v = integer(); edges.emplace_back(u, v); }
            const Graph graph(std::move(vertices), edges); const MaterializedCliques index(graph, h); const ClosureOracle oracle(index);
            while ((command = token()) != "end") {
                if (command == "inspect") inspect(graph, index);
                else if (command == "footprints") {
                    auto x = read_set(graph); auto y = read_set(graph);
                    const auto footprints = aggregate_footprints(index, {x, y, Fraction(1)});
                    std::cout << "{\"scanned\":" << footprints.scanned << ",\"total_weight\":" << footprints.total_weight << ",\"footprints\":[";
                    bool first = true;
                    for (const auto& footprint : footprints.records) {
                        if (!first) std::cout << ','; first = false;
                        std::cout << "{\"vertices\":" << vertices_json(graph, footprint.vertices) << ",\"weight\":" << footprint.weight << '}';
                    }
                    std::cout << "]}\n";
                } else if (command == "global" || command == "restricted") {
                    const auto mode = token();
                    CapacityPolicy policy;
                    if (mode == "auto") policy = CapacityPolicy::Auto;
                    else if (mode == "big") policy = CapacityPolicy::ForceBig;
                    else if (mode == "uint128") policy = CapacityPolicy::ForceUInt128;
                    else throw std::invalid_argument("unknown policy");
                    const auto lambda = Fraction::parse(token());
                    OracleResult result;
                    if (command == "global") result = oracle.global_F(oracle.full_graph_request(lambda), policy);
                    else { auto x = read_set(graph); auto y = read_set(graph); result = oracle.largest_restricted({x, y, lambda}, policy); }
                    std::string record = oracle_json(index, lambda, result); record.pop_back(); record.pop_back();
                    std::cout << record << ",\"stats\":" << query_stats_json(result.stats) << "}\n";
                } else throw std::invalid_argument("unknown adapter command");
                std::cout.flush();
            }
        }
    } catch (const std::exception& error) { std::cerr << error.what() << '\n'; return 1; }
    return 0;
}
