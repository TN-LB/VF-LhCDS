#include "vflhcds/telemetry/query.hpp"
#include <sstream>
#include <iomanip>

namespace vflhcds {
std::string query_stats_json(const QueryStats& s) {
    const auto optional = [](const std::optional<BigInt>& x) { return x ? decimal(*x) : "null"; };
    std::ostringstream out;
    out << "{\"logical_interval_queries\":" << s.logical_interval_queries
        << ",\"mincut_calls\":" << s.mincut_calls
        << ",\"original_interval_size\":" << s.original_interval_size
        << ",\"oracle_interval_size\":" << s.oracle_interval_size
        << ",\"cliques_scanned\":" << optional(s.cliques_scanned)
        << ",\"unique_footprints\":" << optional(s.unique_footprints)
        << ",\"forward_nodes\":" << optional(s.forward_nodes)
        << ",\"forward_arcs\":" << optional(s.forward_arcs)
        << ",\"residual_arcs\":" << optional(s.residual_arcs)
        << ",\"capacity_bit_length\":" << optional(s.capacity_bit_length)
        << ",\"capacity_backend\":" << (s.capacity_backend ? "\"" + *s.capacity_backend + "\"" : "null")
        << ",\"core_threshold\":" << optional(s.core_threshold) << ",\"core\":";
    if (s.core) out << "{\"vertices_removed\":" << s.core->vertices_removed
        << ",\"cliques_invalidated\":" << s.core->cliques_invalidated
        << ",\"incidence_visits\":" << s.core->incidence_visits
        << ",\"degree_decrements\":" << s.core->degree_decrements << '}';
    else out << "null";
    out << ",\"core_reduction_seconds\":";
    if (s.core_reduction_seconds) out << std::setprecision(17) << *s.core_reduction_seconds;
    else out << "null";
    out << '}';
    return out.str();
}
}  // namespace vflhcds
