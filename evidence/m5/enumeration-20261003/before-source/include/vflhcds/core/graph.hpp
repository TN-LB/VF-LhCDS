#pragma once
#include "vflhcds/core/exact.hpp"
#include <utility>
#include <vector>

namespace vflhcds {
using VertexId = std::size_t;
using VertexSet = std::vector<VertexId>;
using OriginalEdge = std::pair<BigInt, BigInt>;

class Graph {
public:
    Graph(std::vector<BigInt> vertices, const std::vector<OriginalEdge>& edges);
    std::size_t size() const noexcept { return originals_.size(); }
    const std::vector<BigInt>& originals() const noexcept { return originals_; }
    const std::vector<std::pair<VertexId, VertexId>>& edges() const noexcept { return edges_; }
    const VertexSet& neighbors(VertexId vertex) const { return adjacency_.at(vertex); }
    VertexId internal_id(const BigInt& original) const;
    bool adjacent(VertexId u, VertexId v) const;
    VertexSet all_vertices() const;
    void validate_set(const VertexSet& set) const;
    std::vector<VertexSet> induced_components(const VertexSet& set) const;
private:
    std::vector<BigInt> originals_;
    std::vector<std::pair<VertexId, VertexId>> edges_;
    std::vector<VertexSet> adjacency_;
};

class Membership {
public:
    explicit Membership(std::size_t size) : marked_(size, 0) {}
    void assign(const VertexSet& set);
    bool contains(VertexId vertex) const { return marked_.at(vertex) != 0; }
private:
    std::vector<unsigned char> marked_;
};
struct NormalizedGraph { Graph graph; BigInt removed_loops; BigInt removed_duplicates; };
NormalizedGraph normalize_graph(std::vector<BigInt> vertices, const std::vector<OriginalEdge>& edges);
bool subset(const VertexSet& a, const VertexSet& b);
}  // namespace vflhcds
