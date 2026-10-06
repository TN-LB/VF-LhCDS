#include "vflhcds/clique/core.hpp"

namespace vflhcds {
VertexSet peel_core(const MaterializedCliques& index, const BigInt& threshold, CoreStats* progress) {
    CoreStats local;
    CoreStats& stats = progress ? *progress : local;
    stats = CoreStats{};
    if (threshold < 0) throw std::invalid_argument("negative core threshold");
    if (threshold == 0) return index.graph().all_vertices();
    const auto n = index.graph().size();
    std::vector<std::size_t> degrees(n);
    std::vector<unsigned char> active(n, 1), queued(n, 0), live_clique(index.cliques().size(), 1);
    VertexSet queue;
    for (VertexId v = 0; v < n; ++v) {
        degrees[v] = index.incidence()[v].size();
        if (BigInt(degrees[v]) < threshold) { queue.push_back(v); queued[v] = 1; }
    }
    for (std::size_t head = 0; head < queue.size(); ++head) {
        const auto v = queue[head]; active[v] = 0; ++stats.vertices_removed;
        for (const auto id : index.incidence()[v]) {
            ++stats.incidence_visits;
            if (live_clique[id] == 0) continue;
            live_clique[id] = 0; ++stats.cliques_invalidated;
            for (const auto u : index.cliques()[id]) {
                if (active[u] == 0) continue;
                if (degrees[u] == 0) throw std::logic_error("core degree underflow");
                --degrees[u]; ++stats.degree_decrements;
                if (queued[u] == 0 && BigInt(degrees[u]) < threshold) {
                    queue.push_back(u); queued[u] = 1;
                }
            }
        }
    }
    VertexSet result;
    for (VertexId v = 0; v < n; ++v) if (active[v] != 0) result.push_back(v);
    return result;
}
}  // namespace vflhcds
