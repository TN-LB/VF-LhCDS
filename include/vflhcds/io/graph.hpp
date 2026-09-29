#pragma once
#include "vflhcds/core/graph.hpp"
#include "vflhcds/oracle/closure.hpp"
#include <string_view>

namespace vflhcds {
Graph parse_graph(std::string_view text);
VertexSet parse_set(std::string_view text, const Graph& graph);
std::string canonical_graph(const Graph& graph);
std::string sha256(std::string_view bytes);
std::string vertices_json(const Graph& graph, const VertexSet& vertices);
std::string inspect_json(const Graph& graph);
std::string oracle_json(const MaterializedCliques& index, const Fraction& lambda, const OracleResult& result);
std::string read_text_file(const std::string& path);
void reject_input_alias(const std::string& output, const std::vector<std::string>& inputs);
void atomic_write(const std::string& path, std::string_view text);
}  // namespace vflhcds
