#pragma once
#include "vflhcds/io/solution.hpp"
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <exception>
#include <filesystem>
#include <fstream>
#include <limits>
#include <map>
#include <sstream>

// Diagnostic-only. Never included or linked by the production control target.
namespace fp {
using vflhcds::BigInt;
using Clock = std::chrono::steady_clock;
using Totals = std::map<std::string, BigInt>;
inline Clock::time_point (*now)() = Clock::now;
struct Frame { BigInt parent; std::size_t depth; };
struct State {
    Totals phases, work;
    std::string active = "unassigned", count_site = "standalone";
    Clock::time_point start{}, last{};
    std::ofstream stream;
    BigInt sequence = 0, bytes = 0, query_id = 0, current_id = 0;
    std::vector<Frame> pending;
    Frame current{0, 0};
    std::size_t pending_peak = 0;
    bool failed = false, solving = false;
    int status = -1;
    const vflhcds::VertexSet* original_upper = nullptr;
};
inline State state;
inline void reset() {
    state = State{};
    state.start = state.last = now();
    for (const auto* key : {"cliques_appended", "incidence_entries_appended", "aggregation_calls",
         "footprint_clique_visits", "footprint_upper_rejected", "footprint_eligible_tuples",
         "footprint_contributions", "footprint_unique_keys", "footprint_core_filtered_tuples",
         "footprint_membership_vertex_tests", "footprint_sorted_operand_visits",
         "observer_core_classification_tuples", "core_calls", "core_vertex_slots_initialized",
         "core_clique_slots_initialized", "core_incidence_visits", "core_cliques_invalidated",
         "core_degree_decrements", "core_vertices_removed", "logical_queries", "mincuts",
         "internal_intervals", "terminal_layers", "non_output_layers", "accepted_components",
         "rejected_components", "outputs", "network_nodes_sum", "network_arcs_sum", "network_residual_arcs_sum"})
        state.work[key] = 0;
    for (const auto* site : {"", "separator_", "emitted_", "standalone_"})
        for (const auto* field : {"calls", "clique_visits", "membership_vertex_tests", "sorted_operand_visits", "matches"})
            state.work[std::string("count_") + site + field] = 0;
}
inline void switch_phase(const std::string& phase) {
    const auto time = now();
    if (time < state.last) throw std::logic_error("observer clock reversed");
    state.phases[state.active] += std::chrono::duration_cast<std::chrono::nanoseconds>(time - state.last).count();
    state.last = time;
    state.active = phase;
}
inline Totals snapshot() {
    auto result = state.phases;
    const auto time = now();
    if (time < state.last) throw std::logic_error("observer clock reversed");
    result[state.active] += std::chrono::duration_cast<std::chrono::nanoseconds>(time - state.last).count();
    return result;
}
class Scope {
public:
    explicit Scope(const char* phase) : previous_(state.active) { switch_phase(phase); }
    ~Scope() noexcept { try { switch_phase(previous_); } catch (...) { state.failed = true; } }
    void change(const char* phase) { switch_phase(phase); }
    Scope(const Scope&) = delete;
    Scope& operator=(const Scope&) = delete;
private:
    std::string previous_;
};
// Declared immediately before and after each original object. Reverse destruction
// enters the phase, destroys the original object, then restores the parent phase.
struct CleanupEnd {
    std::string previous;
    bool entered = false;
    ~CleanupEnd() noexcept {
        if (entered) try { switch_phase(previous); } catch (...) { state.failed = true; }
    }
};
struct CleanupBegin {
    CleanupEnd& end;
    const char* phase;
    CleanupBegin(CleanupEnd& e, const char* p) : end(e), phase(p) {}
    ~CleanupBegin() noexcept {
        try { end.previous = state.active; switch_phase(phase); end.entered = true; }
        catch (...) { state.failed = true; }
    }
};
inline void add(const std::string& key, const BigInt& value = 1) { state.work[key] += value; }
inline void maximum(const std::string& key, const BigInt& value) {
    auto& target = state.work[key]; if (value > target) target = value;
}
inline std::string object(const Totals& values) {
    std::ostringstream out; out << '{'; bool first = true;
    for (const auto& item : values) {
        if (!first) out << ',';
        first = false; out << '"' << item.first << "\":" << item.second;
    }
    out << '}'; return out.str();
}
inline void event(const char* type, const std::string& fields = "") {
    if (!state.stream.is_open()) return;
    Scope observe("observer");
    const auto totals = snapshot();
    BigInt accounted = 0; for (const auto& item : totals) accounted += item.second;
    const BigInt elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(now() - state.start).count();
    std::ostringstream out;
    out << "{\"schema\":\"vflhcds.final_profile\",\"version\":1,\"seq\":" << ++state.sequence
        << ",\"event\":\"" << type << "\",\"elapsed_ns\":" << elapsed
        << ",\"boundary_residual_ns\":" << elapsed - accounted
        << ",\"phases_ns\":" << object(totals) << ",\"work\":" << object(state.work)
        << ",\"query_id\":" << state.current_id << fields << "}\n";
    const auto line = out.str(); state.stream << line << std::flush;
    state.bytes += line.size();
    if (!state.stream) state.failed = true;
}
inline void checkpoint(const char* phase) { event("phase_begin", ",\"phase\":\"" + std::string(phase) + "\""); }
struct CountSite {
    std::string previous;
    explicit CountSite(const char* site) : previous(state.count_site) { state.count_site = site; }
    ~CountSite() { state.count_site = previous; }
};
inline void count_add(const char* field, const BigInt& value = 1) {
    add(std::string("count_") + field, value);
    add("count_" + state.count_site + "_" + field, value);
}
inline bool count_subset(const vflhcds::VertexSet& a, const vflhcds::VertexSet& b) {
    return std::includes(b.begin(), b.end(), a.begin(), a.end(), [](auto x, auto y) {
        count_add("sorted_operand_visits", 2); return x < y;
    });
}
inline bool footprint_less(vflhcds::VertexId a, vflhcds::VertexId b) {
    add("footprint_sorted_operand_visits", 2); return a < b;
}
inline bool footprint_subset(const vflhcds::VertexSet& a, const vflhcds::VertexSet& b) {
    return std::includes(b.begin(), b.end(), a.begin(), a.end(), footprint_less);
}
struct OriginalBound {
    const vflhcds::VertexSet* previous;
    explicit OriginalBound(const vflhcds::VertexSet& upper) : previous(state.original_upper) { state.original_upper = &upper; }
    ~OriginalBound() { state.original_upper = previous; }
};
inline void upper_rejected(const vflhcds::VertexSet& clique) {
    add("footprint_upper_rejected");
    // This extra observation is NOT production clique work. It distinguishes
    // rejection by the original bound from additional query-local core filtering.
    Scope scope("observer");
    if (state.original_upper) {
        add("observer_core_classification_tuples");
        if (std::includes(state.original_upper->begin(), state.original_upper->end(), clique.begin(), clique.end()))
            add("footprint_core_filtered_tuples");
    }
}
inline void footprint_summary(const vflhcds::Footprints& result) {
    Scope scope("observer"); Totals unique, weighted;
    for (const auto& row : result.records) {
        const auto size = std::to_string(row.vertices.size());
        ++unique[size]; weighted[size] += row.weight;
    }
    add("footprint_unique_keys", result.records.size());
    event("footprints", ",\"unique_by_size\":" + object(unique) + ",\"weight_by_size\":" + object(weighted)
          + ",\"total_weight\":" + vflhcds::decimal(result.total_weight)
          + ",\"histogram_bound\":\"actual_query_bound\",\"before_core_histogram\":null");
}
inline void index_summary(const vflhcds::MaterializedCliques& index) {
    Scope scope("observer"); BigInt tuple_size = 0, tuple_capacity = 0, incidence_size = 0, incidence_capacity = 0;
    for (const auto& c : index.cliques()) { tuple_size += c.size(); tuple_capacity += c.capacity(); }
    for (const auto& ids : index.incidence()) { incidence_size += ids.size(); incidence_capacity += ids.capacity(); }
    event("index", ",\"n\":" + std::to_string(index.graph().size()) + ",\"m\":" + std::to_string(index.graph().edges().size())
          + ",\"h\":" + vflhcds::decimal(index.h()) + ",\"cliques\":" + std::to_string(index.cliques().size())
          + ",\"tuple_slots\":" + vflhcds::decimal(tuple_size) + ",\"tuple_capacity\":" + vflhcds::decimal(tuple_capacity)
          + ",\"incidence_slots\":" + vflhcds::decimal(incidence_size)
          + ",\"incidence_capacity\":" + vflhcds::decimal(incidence_capacity));
}
inline void oracle_summary(const vflhcds::RestrictedRequest& request, const vflhcds::QueryStats& stats) {
    Scope scope("observer");
    if (stats.forward_nodes) { add("network_nodes_sum", *stats.forward_nodes); maximum("network_nodes_max", *stats.forward_nodes); }
    if (stats.forward_arcs) { add("network_arcs_sum", *stats.forward_arcs); maximum("network_arcs_max", *stats.forward_arcs); }
    if (stats.residual_arcs) { add("network_residual_arcs_sum", *stats.residual_arcs); maximum("network_residual_arcs_max", *stats.residual_arcs); }
    if (stats.capacity_bit_length) maximum("capacity_bits_max", *stats.capacity_bit_length);
    add("mincuts", stats.mincut_calls);
    const auto shortcut = request.x == request.y_oracle ? "empty_interval"
        : request.lambda.numerator() == 0 ? "zero_lambda" : "none";
    event("oracle", ",\"shortcut\":\"" + std::string(shortcut) + "\",\"stats\":" + vflhcds::query_stats_json(stats));
}
struct OracleEnd {
    const vflhcds::RestrictedRequest& request;
    const vflhcds::QueryStats& stats;
    int exceptions = std::uncaught_exceptions();
    ~OracleEnd() noexcept {
        try { if (std::uncaught_exceptions() == exceptions) oracle_summary(request, stats);
              else event("oracle_incomplete"); } catch (...) { state.failed = true; }
    }
};
struct SolveScope {
    SolveScope() { state.pending = {{0, 0}}; state.solving = true; state.pending_peak = 1; }
    ~SolveScope() noexcept {
        try { event("solve_end", ",\"pending_intervals\":" + std::to_string(state.pending.size())); }
        catch (...) { state.failed = true; }
        state.solving = false;
    }
};
struct QueryScope {
    int exceptions = std::uncaught_exceptions();
    QueryScope() {
        if (state.pending.empty()) throw std::logic_error("observer traversal divergence");
        state.current = state.pending.back(); state.pending.pop_back();
        state.current_id = ++state.query_id;
        add("logical_queries"); add("depth_" + std::to_string(state.current.depth));
        maximum("maximum_depth", state.current.depth);
        event("query_begin", ",\"parent\":" + vflhcds::decimal(state.current.parent)
              + ",\"depth\":" + std::to_string(state.current.depth));
    }
    ~QueryScope() noexcept {
        try { event(std::uncaught_exceptions() == exceptions ? "query_end" : "query_incomplete",
                    ",\"pending_intervals\":" + std::to_string(state.pending.size())); }
        catch (...) { state.failed = true; }
        state.current_id = 0;
    }
};
inline void split() {
    if (state.current.depth == std::numeric_limits<std::size_t>::max()) throw std::overflow_error("observer depth");
    state.pending.push_back({state.current_id, state.current.depth + 1});
    state.pending.push_back({state.current_id, state.current.depth + 1});
    state.pending_peak = std::max(state.pending_peak, state.pending.size());
    add("internal_intervals");
}
inline void query_semantics(const vflhcds::Graph& graph, const vflhcds::ChainInterval& interval,
                            const vflhcds::ChainPoint& z) {
    Scope scope("observer"); const auto lambda = interval.lambda();
    event("separator", ",\"x\":" + vflhcds::vertices_json(graph, interval.x().vertices())
          + ",\"y\":" + vflhcds::vertices_json(graph, interval.y().vertices())
          + ",\"z\":" + vflhcds::vertices_json(graph, z.vertices())
          + ",\"mu_x\":\"" + vflhcds::decimal(interval.x().cliques())
          + "\",\"mu_y\":\"" + vflhcds::decimal(interval.y().cliques())
          + "\",\"lambda\":\"" + vflhcds::decimal(lambda.numerator()) + "/" + vflhcds::decimal(lambda.denominator()) + "\"");
}
inline void layer(std::size_t accepted) {
    add("terminal_layers"); add("accepted_components", accepted);
    if (accepted == 0) add("non_output_layers");
    event("layer", ",\"accepted\":" + std::to_string(accepted));
}
inline void rank(std::size_t value) {
    add("outputs"); event("rank_ready", ",\"rank\":" + std::to_string(value)
                         + ",\"pending_intervals\":" + std::to_string(state.pending.size()));
}
struct Session {
    Session(int argc, char** argv) {
        reset();
        const auto* path = std::getenv("VF_PROFILE_OUTPUT");
        if (!path || !*path) throw std::invalid_argument("VF_PROFILE_OUTPUT is required");
        if (std::filesystem::exists(path)) throw std::invalid_argument("observer output already exists");
        std::vector<std::string> inputs;
        for (int i = 1; i + 1 < argc; ++i) {
            const std::string arg = argv[i];
            if (arg == "--graph" || arg == "--x" || arg == "--y" || arg == "--output")
                inputs.emplace_back(argv[i + 1]);
        }
        vflhcds::reject_input_alias(path, inputs);
        state.stream.open(path, std::ios::out | std::ios::trunc);
        if (!state.stream) throw std::runtime_error("cannot open observer stream");
        event("start", ",\"coverage\":\"development\",\"partition_reuse\":null");
    }
    ~Session() noexcept {
        try {
            event("finish", ",\"native_exit\":" + std::to_string(state.status)
                  + ",\"complete\":" + (state.status == 0 && !state.failed ? "true" : "false")
                  + ",\"active_phase\":\"" + state.active + "\",\"observer_bytes_before_finish\":" + vflhcds::decimal(state.bytes)
                  + ",\"observer_pending_peak\":" + std::to_string(state.pending_peak)
                  + ",\"observer_pending_capacity\":" + std::to_string(state.pending.capacity())
                  + ",\"observer_counter_keys\":" + std::to_string(state.work.size())
                  + ",\"observer_phase_keys\":" + std::to_string(state.phases.size())
                  + ",\"partition_reuse\":null");
            state.stream.close();
        } catch (...) { state.failed = true; }
    }
};
}  // namespace fp
