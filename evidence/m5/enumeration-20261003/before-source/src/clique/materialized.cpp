#include "vflhcds/clique/materialized.hpp"
#include <numeric>

namespace vflhcds {
MaterializedCliques::MaterializedCliques(const Graph& graph, BigInt h)
    : graph_(graph), h_(std::move(h)), incidence_(graph.size()) {
    if (h_ < 2) throw std::invalid_argument("h must be at least 2");
    if (h_ > graph.size()) return;
    const auto k = to_size(h_);
    VertexSet tuple(k); std::iota(tuple.begin(), tuple.end(), VertexId{0});
    while (true) {
        bool complete = true;
        for (std::size_t i = 0; i < k && complete; ++i)
            for (std::size_t j = i + 1; j < k; ++j)
                if (!graph.adjacent(tuple[i], tuple[j])) { complete = false; break; }
        if (complete) {
            for (const auto vertex : tuple) incidence_[vertex].push_back(cliques_.size());
            cliques_.push_back(tuple);
        }
        std::size_t position = k;
        while (position > 0 && tuple[position - 1] == graph.size() - k + position - 1) --position;
        if (position == 0) break;
        ++tuple[position - 1];
        for (std::size_t j = position; j < k; ++j) tuple[j] = tuple[j - 1] + 1;
    }
}
BigInt MaterializedCliques::count(const VertexSet& set) const {
    graph_.validate_set(set);
    BigInt result = 0;
    for (const auto& clique : cliques_) if (subset(clique, set)) ++result;
    return result;
}
}  // namespace vflhcds
