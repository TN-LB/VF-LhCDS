#pragma once
#include "vflhcds/oracle/closure.hpp"
#include <functional>

namespace vflhcds {
struct Incomplete : std::runtime_error { using std::runtime_error::runtime_error; };
using StopRequested = std::function<bool()>;
struct Solution { VertexSet vertices; BigInt cliques; Fraction density; };
struct SolveResult { std::vector<Solution> solutions; bool k_reached = false; };
struct SolveStats {
    BigInt logical_interval_queries = 0, mincut_calls = 0, cliques_scanned = 0;
    BigInt cliques_enumerated = 0;
    std::vector<QueryStats> queries;
    void record(const QueryStats& query);
};
using TraceSink = std::function<void(const ChainInterval&, const ChainPoint&, const QueryStats&)>;
// No definition-level validator or post-hoc output repair is accepted by this API.
SolveResult solve(const MaterializedCliques& index, const std::optional<BigInt>& k = std::nullopt,
                  CapacityPolicy policy = CapacityPolicy::Auto, SolveStats* progress = nullptr,
                  const TraceSink& trace = {}, const StopRequested& stop = {});
std::string solve_stats_json(const SolveStats& stats);
}  // namespace vflhcds
