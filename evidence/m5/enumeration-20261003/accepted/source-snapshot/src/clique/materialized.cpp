#include "vflhcds/clique/materialized.hpp"
#include <algorithm>
#include <numeric>

namespace vflhcds {
MaterializedCliques::MaterializedCliques(const Graph& graph, BigInt h, CliqueEnumeration enumeration)
    : graph_(graph), h_(std::move(h)), incidence_(graph.size()) {
    if (h_ < 2) throw std::invalid_argument("h must be at least 2");
    if (enumeration != CliqueEnumeration::Combinations && enumeration != CliqueEnumeration::Adjacency)
        throw std::invalid_argument("unknown clique enumeration");
    if (h_ > graph.size()) return;
    const auto k = to_size(h_);
    if (enumeration == CliqueEnumeration::Adjacency) enumerate_adjacency(k);
    else enumerate_combinations(k);
}
void MaterializedCliques::append(const VertexSet& tuple) {
    for (const auto vertex : tuple) incidence_[vertex].push_back(cliques_.size());
    cliques_.push_back(tuple);
}
void MaterializedCliques::enumerate_combinations(const std::size_t k) {
    VertexSet tuple(k); std::iota(tuple.begin(), tuple.end(), VertexId{0});
    while (true) {
        bool complete = true;
        for (std::size_t i = 0; i < k && complete; ++i)
            for (std::size_t j = i + 1; j < k; ++j)
                if (!graph_.adjacent(tuple[i], tuple[j])) { complete = false; break; }
        if (complete) append(tuple);
        std::size_t position = k;
        while (position > 0 && tuple[position - 1] == graph_.size() - k + position - 1) --position;
        if (position == 0) break;
        ++tuple[position - 1];
        for (std::size_t j = position; j < k; ++j) tuple[j] = tuple[j - 1] + 1;
    }
}
void MaterializedCliques::enumerate_adjacency(const std::size_t k) {
    struct Frame { VertexSet candidates; std::size_t next = 0; };
    std::vector<Frame> stack;
    stack.push_back({graph_.all_vertices(), 0});
    VertexSet prefix;
    prefix.reserve(k);
    while (!stack.empty()) {
        auto& frame = stack.back();
        // Candidates extend the entire increasing clique prefix. Once too few
        // remain, neither this sibling nor any later sibling can reach size k.
        if (frame.candidates.size() - frame.next < k - prefix.size()) {
            stack.pop_back();
            if (!prefix.empty()) prefix.pop_back();
            continue;
        }
        const auto vertex = frame.candidates[frame.next++];
        prefix.push_back(vertex);
        if (prefix.size() == k) {
            append(prefix);
            prefix.pop_back();
            continue;
        }
        const auto& neighbors = graph_.neighbors(vertex);
        VertexSet candidates;
        candidates.reserve(std::min(frame.candidates.size() - frame.next, neighbors.size()));
        std::size_t i = frame.next, j = 0;
        while (i < frame.candidates.size() && j < neighbors.size()) {
            if (frame.candidates[i] < neighbors[j]) ++i;
            else if (neighbors[j] < frame.candidates[i]) ++j;
            else { candidates.push_back(frame.candidates[i]); ++i; ++j; }
        }
        if (candidates.size() < k - prefix.size()) prefix.pop_back();
        else stack.push_back({std::move(candidates), 0});
    }
}
BigInt MaterializedCliques::count(const VertexSet& set) const {
    graph_.validate_set(set);
    BigInt result = 0;
    for (const auto& clique : cliques_) if (subset(clique, set)) ++result;
    return result;
}
}  // namespace vflhcds
