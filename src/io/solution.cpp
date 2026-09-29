#include "vflhcds/io/solution.hpp"
#include <sstream>

namespace vflhcds {
std::string solution_json(const MaterializedCliques& index, const Solution& solution, const BigInt& rank) {
    std::ostringstream out;
    out << "{\"rank\":" << rank << ",\"h\":" << index.h()
        << ",\"vertex_count\":" << solution.vertices.size() << ",\"clique_count\":\"" << solution.cliques
        << "\",\"density_num\":\"" << solution.density.numerator() << "\",\"density_den\":\""
        << solution.density.denominator() << "\",\"vertices\":" << vertices_json(index.graph(), solution.vertices) << "}\n";
    return out.str();
}
std::string semantic_header(const Graph& graph, const BigInt& h) {
    return "{\"schema_version\":1,\"graph_sha256\":\"" + sha256(canonical_graph(graph)) + "\",\"h\":" + decimal(h) + "}\n";
}
}  // namespace vflhcds
