#pragma once
#include "vflhcds/core/exact.hpp"
#include <optional>

namespace vflhcds {
struct QueryStats {
    BigInt logical_interval_queries = 0, mincut_calls = 0;
    BigInt original_interval_size = 0, oracle_interval_size = 0;
    std::optional<BigInt> cliques_scanned, unique_footprints, forward_nodes,
        forward_arcs, residual_arcs, capacity_bit_length;
    std::optional<std::string> capacity_backend;
};
std::string query_stats_json(const QueryStats& stats);
}  // namespace vflhcds
