#include "vflhcds/core/graph.hpp"
#include <algorithm>
#include <numeric>
#include <set>

namespace vflhcds {
Graph::Graph(std::vector<BigInt> vertices, const std::vector<OriginalEdge>& edges)
    : originals_(std::move(vertices)) {
    std::sort(originals_.begin(), originals_.end());
    if (originals_.empty() || std::adjacent_find(originals_.begin(), originals_.end()) != originals_.end())
        throw InvalidGraph("empty universe or duplicate vertex");
    adjacency_.resize(size());
    for (const auto& edge : edges) {
        auto u = internal_id(edge.first), v = internal_id(edge.second);
        if (u == v) throw InvalidGraph("self-loop");
        if (u > v) std::swap(u, v);
        edges_.emplace_back(u, v);
    }
    std::sort(edges_.begin(), edges_.end());
    if (std::adjacent_find(edges_.begin(), edges_.end()) != edges_.end()) throw InvalidGraph("duplicate edge");
    for (const auto& edge : edges_) {
        adjacency_[edge.first].push_back(edge.second);
        adjacency_[edge.second].push_back(edge.first);
    }
    for (auto& neighbors : adjacency_) std::sort(neighbors.begin(), neighbors.end());
}
VertexId Graph::internal_id(const BigInt& original) const {
    const auto found = std::lower_bound(originals_.begin(), originals_.end(), original);
    if (found == originals_.end() || *found != original) throw InvalidGraph("undeclared endpoint");
    return static_cast<VertexId>(found - originals_.begin());
}
bool Graph::adjacent(const VertexId u, const VertexId v) const {
    const auto& neighbors = adjacency_.at(u);
    if (v >= size()) throw std::out_of_range("vertex");
    return std::binary_search(neighbors.begin(), neighbors.end(), v);
}
VertexSet Graph::all_vertices() const {
    VertexSet set(size()); std::iota(set.begin(), set.end(), VertexId{0}); return set;
}
void Graph::validate_set(const VertexSet& set) const {
    if (!std::is_sorted(set.begin(), set.end())
        || std::adjacent_find(set.begin(), set.end()) != set.end()
        || (!set.empty() && set.back() >= size())) throw std::invalid_argument("noncanonical vertex set");
}
void Membership::assign(const VertexSet& set) {
    std::fill(marked_.begin(), marked_.end(), 0);
    for (const auto vertex : set) marked_.at(vertex) = 1;
}
bool subset(const VertexSet& a, const VertexSet& b) {
    return std::includes(b.begin(), b.end(), a.begin(), a.end());
}
std::vector<VertexSet> Graph::induced_components(const VertexSet& set) const {
    validate_set(set);
    Membership allowed(size()); allowed.assign(set);
    std::vector<unsigned char> seen(size(), 0);
    std::vector<VertexSet> components;
    for (const auto root : set) {
        if (seen[root] != 0) continue;
        VertexSet queue{root}; seen[root] = 1;
        for (std::size_t i = 0; i < queue.size(); ++i) {
            for (const auto v : neighbors(queue[i])) {
                if (allowed.contains(v) && seen[v] == 0) { seen[v] = 1; queue.push_back(v); }
            }
        }
        std::sort(queue.begin(), queue.end()); components.push_back(std::move(queue));
    }
    return components;
}
NormalizedGraph normalize_graph(std::vector<BigInt> vertices, const std::vector<OriginalEdge>& edges) {
    const Graph universe(vertices, {});
    std::set<OriginalEdge> unique;
    BigInt loops = 0, duplicates = 0;
    for (auto edge : edges) {
        (void)universe.internal_id(edge.first); (void)universe.internal_id(edge.second);
        if (edge.first == edge.second) { ++loops; continue; }
        if (edge.first > edge.second) std::swap(edge.first, edge.second);
        if (!unique.insert(std::move(edge)).second) ++duplicates;
    }
    return {Graph(std::move(vertices), {unique.begin(), unique.end()}), loops, duplicates};
}
}  // namespace vflhcds
