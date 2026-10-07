#pragma once
#include "vflhcds/clique/materialized.hpp"

// Test-only control comparison. Mathematical truth still comes from Python.
inline vflhcds::MaterializedCliques checked_adjacency_index(const vflhcds::Graph& graph,
                                                          const vflhcds::BigInt& h) {
    using namespace vflhcds;
    const MaterializedCliques control(graph, h, CliqueEnumeration::Combinations);
#ifdef VFLHCDS_TEST_COUNT_MEMBERSHIP
    MaterializedCliques adjacency(graph, h, CliqueEnumeration::Adjacency, CliqueCounting::Membership);
#else
    MaterializedCliques adjacency(graph, h, CliqueEnumeration::Adjacency);
#endif
    if (control.cliques() != adjacency.cliques() || control.incidence() != adjacency.incidence())
        throw std::runtime_error("T04-ADJ ordered clique/incidence equivalence failed");
    return adjacency;
}
