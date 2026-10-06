#pragma once
#include "vflhcds/clique/materialized.hpp"

namespace vflhcds {
struct CoreStats {
    BigInt vertices_removed = 0, cliques_invalidated = 0;
    BigInt incidence_visits = 0, degree_decrements = 0;
};
// Recomputes the exact core of the full immutable graph; no threshold cache.
VertexSet peel_core(const MaterializedCliques& index, const BigInt& threshold,
                    CoreStats* progress = nullptr);
}  // namespace vflhcds
