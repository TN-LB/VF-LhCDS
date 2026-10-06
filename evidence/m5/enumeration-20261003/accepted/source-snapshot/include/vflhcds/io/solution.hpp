#pragma once
#include "vflhcds/io/graph.hpp"
#include "vflhcds/solver/solver.hpp"

namespace vflhcds {
std::string solution_json(const MaterializedCliques& index, const Solution& solution, const BigInt& rank);
std::string semantic_header(const Graph& graph, const BigInt& h);
}  // namespace vflhcds
