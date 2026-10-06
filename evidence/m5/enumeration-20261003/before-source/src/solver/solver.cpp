#include "vflhcds/solver/solver.hpp"
#include <algorithm>
#include <iterator>
#include <sstream>

namespace vflhcds {
void SolveStats::record(const QueryStats& query) {
    mincut_calls += query.mincut_calls;
    if (query.cliques_scanned) cliques_scanned += *query.cliques_scanned;
    queries.push_back(query);
}
SolveResult solve(const MaterializedCliques& index, const std::optional<BigInt>& k,
                  const CapacityPolicy policy, SolveStats* progress,
                  const TraceSink& trace, const StopRequested& stop, const OracleOptions options) {
    if (k && *k < 1) throw std::invalid_argument("k must be positive");
    SolveStats local;
    SolveStats& stats = progress ? *progress : local;
    stats = SolveStats{};
    stats.cliques_enumerated = index.cliques().size();
    const auto cancelled = [&] { if (stop && stop()) throw Incomplete("controlled cancellation"); };
    cancelled();
    const ClosureOracle oracle(index);
    std::vector<ChainInterval> stack{oracle.root_interval()};
    SolveResult result;
    Membership lower(index.graph().size());
    while (!stack.empty()) {
        cancelled();
        const auto interval = std::move(stack.back()); stack.pop_back();
        ++stats.logical_interval_queries;
        QueryStats query;
        // The oracle resets its own standalone logical counter. Interval entries
        // belong to this orchestration, including zero-lambda queries and failures.
        const auto z = [&] {
            try { return oracle.separate(interval, policy, &query, options); }
            catch (...) { query.logical_interval_queries = 1; stats.record(query); throw; }
        }();
        query.logical_interval_queries = 1; stats.record(query);
        if (trace) trace(interval, z, query);
        const auto& x = interval.x().vertices(); const auto& y = interval.y().vertices();
        if (z.vertices() != y) {
            // Stack order guarantees no eager right-child oracle execution.
            stack.push_back(oracle.chain_interval(z, interval.y()));
            stack.push_back(oracle.chain_interval(interval.x(), z));
            continue;
        }
        VertexSet added;
        std::set_difference(y.begin(), y.end(), x.begin(), x.end(), std::back_inserter(added));
        lower.assign(x);
        std::vector<VertexSet> accepted;
        for (auto& component : index.graph().induced_components(added)) {
            bool touches_lower = false;
            for (const auto u : component) {
                for (const auto v : index.graph().neighbors(u))
                    if (lower.contains(v)) { touches_lower = true; break; }
                if (touches_lower) break;
            }
            if (!touches_lower) accepted.push_back(std::move(component));
        }
        // Internal IDs are in numeric original-ID order; lexicographic vectors
        // therefore implement D006 exactly, including arbitrary-size original IDs.
        std::sort(accepted.begin(), accepted.end());
        for (auto& component : accepted) {
            cancelled();
            const auto count = index.count(component);
            const Fraction density(count, component.size());
            result.solutions.push_back({std::move(component), count, density});
            if (k && BigInt(result.solutions.size()) == *k) {
                result.k_reached = true; return result;
            }
        }
    }
    return result;
}
std::string solve_stats_json(const SolveStats& stats) {
    std::ostringstream out;
    out << "{\"logical_interval_queries\":" << stats.logical_interval_queries
        << ",\"mincut_calls\":" << stats.mincut_calls << ",\"cliques_scanned\":" << stats.cliques_scanned
        << ",\"cliques_enumerated\":" << stats.cliques_enumerated
        << ",\"queries\":[";
    bool first = true;
    for (const auto& query : stats.queries) { if (!first) out << ','; first = false; out << query_stats_json(query); }
    out << "]}"; return out.str();
}
}  // namespace vflhcds
