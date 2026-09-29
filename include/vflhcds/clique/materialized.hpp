#pragma once
#include "vflhcds/core/graph.hpp"

namespace vflhcds {
// The immutable graph must outlive this index. Copying preserves that reference.
class MaterializedCliques {
public:
    MaterializedCliques(const Graph& graph, BigInt h);
    const Graph& graph() const noexcept { return graph_; }
    const BigInt& h() const noexcept { return h_; }
    const std::vector<VertexSet>& cliques() const noexcept { return cliques_; }
    const std::vector<std::vector<std::size_t>>& incidence() const noexcept { return incidence_; }
    BigInt count(const VertexSet& set) const;
    BigInt degree(VertexId vertex) const { return BigInt(incidence_.at(vertex).size()); }
private:
    const Graph& graph_;
    BigInt h_;
    std::vector<VertexSet> cliques_;
    std::vector<std::vector<std::size_t>> incidence_;
};
}  // namespace vflhcds
