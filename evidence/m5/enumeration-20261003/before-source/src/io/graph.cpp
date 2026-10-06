#include "vflhcds/io/graph.hpp"
#include <algorithm>
#include <array>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <unistd.h>

namespace vflhcds {
namespace {
class Tokens {
public:
    explicit Tokens(std::string_view text) : text_(text) {}
    std::string_view next() {
        while (position_ < text_.size() && whitespace(text_[position_])) ++position_;
        const auto start = position_;
        while (position_ < text_.size() && !whitespace(text_[position_])) ++position_;
        return text_.substr(start, position_ - start);
    }
    void expect(std::string_view expected) {
        if (next() != expected) throw std::invalid_argument("unexpected graph/set token");
    }
    BigInt integer(bool signed_value = false) { return parse_integer(next(), signed_value); }
private:
    static bool whitespace(char ch) { return ch == ' ' || ch == '\n' || ch == '\r' || ch == '\t' || ch == '\v' || ch == '\f'; }
    std::string_view text_;
    std::size_t position_ = 0;
};
}  // namespace
Graph parse_graph(const std::string_view text) {
    try {
        Tokens tokens(text); tokens.expect("vflhcds-graph"); tokens.expect("1"); tokens.expect("n");
        const auto n = to_size(tokens.integer());
        if (n == 0) throw InvalidGraph("empty graph");
        std::vector<BigInt> vertices;
        // Grow only while reading actual records: a dishonest huge count cannot
        // turn a short malformed input into an enormous speculative allocation.
        for (std::size_t i = 0; i < n; ++i) { tokens.expect("v"); vertices.push_back(tokens.integer(true)); }
        tokens.expect("m"); const auto m = to_size(tokens.integer());
        std::vector<OriginalEdge> edges;
        for (std::size_t i = 0; i < m; ++i) {
            tokens.expect("e"); BigInt u = tokens.integer(true); BigInt v = tokens.integer(true);
            edges.emplace_back(std::move(u), std::move(v));
        }
        tokens.expect(""); return Graph(std::move(vertices), edges);
    } catch (const std::invalid_argument& error) { throw InvalidGraph(error.what()); }
}
VertexSet parse_set(const std::string_view text, const Graph& graph) {
    Tokens tokens(text); tokens.expect("vflhcds-set"); tokens.expect("1"); tokens.expect("n");
    const auto n = to_size(tokens.integer());
    if (n > graph.size()) throw std::invalid_argument("set exceeds universe");
    VertexSet set;
    for (std::size_t i = 0; i < n; ++i) {
        tokens.expect("v");
        try { set.push_back(graph.internal_id(tokens.integer(true))); }
        catch (const InvalidGraph& error) { throw std::invalid_argument(error.what()); }
    }
    tokens.expect(""); std::sort(set.begin(), set.end()); graph.validate_set(set); return set;
}
std::string canonical_graph(const Graph& graph) {
    std::ostringstream out; out << "vflhcds-graph 1\nn " << graph.size() << '\n';
    for (const auto& id : graph.originals()) out << "v " << id << '\n';
    out << "m " << graph.edges().size() << '\n';
    for (const auto& edge : graph.edges()) out << "e " << graph.originals()[edge.first] << ' ' << graph.originals()[edge.second] << '\n';
    return out.str();
}
std::string vertices_json(const Graph& graph, const VertexSet& vertices) {
    graph.validate_set(vertices); std::ostringstream out; out << '[';
    bool first = true;
    for (const auto vertex : vertices) { if (!first) out << ','; first = false; out << graph.originals()[vertex]; }
    out << ']'; return out.str();
}
std::string inspect_json(const Graph& graph) {
    std::ostringstream out;
    out << "{\"graph_sha256\":\"" << sha256(canonical_graph(graph)) << "\",\"vertex_count\":" << graph.size()
        << ",\"edge_count\":" << graph.edges().size() << ",\"vertices\":" << vertices_json(graph, graph.all_vertices()) << "}\n";
    return out.str();
}
std::string oracle_json(const MaterializedCliques& index, const Fraction& lambda, const OracleResult& result) {
    std::ostringstream out;
    out << "{\"scope\":\"" << (result.global ? "global" : "restricted") << "\",\"h\":" << index.h()
        << ",\"lambda_num\":\"" << lambda.numerator() << "\",\"lambda_den\":\"" << lambda.denominator()
        << "\",\"vertex_count\":" << result.vertices.size() << ",\"clique_count\":\"" << index.count(result.vertices)
        << "\",\"vertices\":" << vertices_json(index.graph(), result.vertices) << "}\n";
    return out.str();
}
std::string read_text_file(const std::string& path) {
    std::error_code error;
    if (std::filesystem::is_directory(path, error) || error) throw IoError("input is not a readable file");
    std::ifstream input(path, std::ios::binary);
    if (!input) throw IoError("cannot open input");
    std::string text;
    std::array<char, 8192> buffer{};
    while (input) {
        input.read(buffer.data(), static_cast<std::streamsize>(buffer.size()));
        text.append(buffer.data(), static_cast<std::size_t>(input.gcount()));
    }
    if (input.bad() || !input.eof()) throw IoError("cannot read input");
    return text;
}
void reject_input_alias(const std::string& output, const std::vector<std::string>& inputs) {
    if (output == "-") return;
    try {
        for (const auto& input : inputs) {
            if ((std::filesystem::exists(output) && std::filesystem::equivalent(output, input))
                || std::filesystem::weakly_canonical(output) == std::filesystem::weakly_canonical(input))
                throw std::invalid_argument("output aliases an input");
        }
    } catch (const std::filesystem::filesystem_error& error) { throw IoError(error.what()); }
}
void atomic_write(const std::string& path, const std::string_view text) {
    // POSIX mkstemp is exclusive and creates the file in the destination directory.
    std::string pattern = path + ".tmp.XXXXXX";
    std::vector<char> name(pattern.begin(), pattern.end()); name.push_back('\0');
    const int descriptor = ::mkstemp(name.data());
    if (descriptor < 0) throw IoError("cannot create sibling temporary");
    std::FILE* file = ::fdopen(descriptor, "wb");
    if (!file) { ::close(descriptor); std::remove(name.data()); throw IoError("cannot open temporary stream"); }
    const bool written = std::fwrite(text.data(), 1, text.size(), file) == text.size();
    const bool flushed = std::fflush(file) == 0;
    const bool closed = std::fclose(file) == 0;
    if (!written || !flushed || !closed || std::rename(name.data(), path.c_str()) != 0) {
        std::remove(name.data()); throw IoError("cannot commit result");
    }
}
}  // namespace vflhcds
