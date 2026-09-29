#include "vflhcds/oracle/closure.hpp"
#include "vflhcds/flow/dinic.hpp"
#include <algorithm>
#include <iterator>
#include <map>

namespace vflhcds {
namespace {
void validate(const Graph& graph, const RestrictedRequest& request) {
    graph.validate_set(request.x); graph.validate_set(request.y_oracle);
    if (!subset(request.x, request.y_oracle)) throw std::invalid_argument("X is not a subset of Y");
    if (request.lambda.numerator() < 0) throw std::invalid_argument("negative lambda");
}
template<class Capacity> Capacity capacity(const BigInt& value) {
    if constexpr (std::is_same_v<Capacity, UInt128>) return to_uint128(value);
    else return value;
}
template<class Capacity> VertexSet execute(const Graph& graph, const RestrictedRequest& request,
        const Footprints& footprints, const VertexSet& interval, const BigInt& source_factor,
        const BigInt& sink_capacity, const BigInt& infinity, QueryStats& stats) {
    const auto n = interval.size(), p = footprints.records.size();
    const auto nodes = to_size(BigInt(n) + p + 2);
    (void)to_size(*stats.residual_arcs);
    const auto source = nodes - 2, sink = nodes - 1;
    Dinic<Capacity> network(nodes);
    std::vector<std::size_t> local(graph.size(), nodes);
    for (std::size_t i = 0; i < n; ++i) {
        local[interval[i]] = i;
        network.add_arc(i, sink, capacity<Capacity>(sink_capacity));
    }
    for (std::size_t i = 0; i < p; ++i) {
        const auto node = n + i;
        const auto& footprint = footprints.records[i];
        network.add_arc(source, node, capacity<Capacity>(source_factor * footprint.weight));
        for (const auto v : footprint.vertices) network.add_arc(node, local[v], capacity<Capacity>(infinity));
    }
    stats.capacity_backend = std::is_same_v<Capacity, UInt128> ? "uint128" : "arbitrary_precision";
    ++stats.mincut_calls;
    (void)network.max_flow(source, sink);
    const auto reachable = network.reachable(source);
    VertexSet result = request.x;
    for (std::size_t i = 0; i < n; ++i) if (reachable[i] != 0) result.push_back(interval[i]);
    std::sort(result.begin(), result.end());
    return result;
}
}  // namespace
Footprints aggregate_footprints(const MaterializedCliques& index, const RestrictedRequest& request) {
    validate(index.graph(), request);
    Footprints result;
    std::map<VertexSet, BigInt> weights;
    for (const auto& clique : index.cliques()) {
        ++result.scanned;
        if (!subset(clique, request.y_oracle)) continue;
        VertexSet residual;
        std::set_difference(clique.begin(), clique.end(), request.x.begin(), request.x.end(),
                            std::back_inserter(residual));
        if (!residual.empty()) { ++weights[std::move(residual)]; ++result.total_weight; }
    }
    for (auto& item : weights) result.records.push_back({item.first, std::move(item.second)});
    return result;
}
CertifiedGlobalRequest ClosureOracle::full_graph_request(Fraction lambda) const {
    if (lambda.numerator() < 0) throw std::invalid_argument("negative lambda");
    return CertifiedGlobalRequest(this, {{}, index_.graph().all_vertices(), std::move(lambda)});
}
ChainInterval ClosureOracle::root_interval() const {
    return ChainInterval(ChainPoint(this, {}, 0),
                         ChainPoint(this, index_.graph().all_vertices(), BigInt(index_.cliques().size())));
}
ChainInterval ClosureOracle::chain_interval(const ChainPoint& x, const ChainPoint& y) const {
    if (x.owner_ != this || y.owner_ != this || x.vertices_ == y.vertices_
        || !subset(x.vertices_, y.vertices_)) throw std::invalid_argument("invalid certified chain endpoints");
    return ChainInterval(x, y);
}
ChainPoint ClosureOracle::global_chain_point(Fraction lambda, const CapacityPolicy policy, QueryStats* progress) const {
    auto result = global_F(full_graph_request(std::move(lambda)), policy, progress);
    const auto count = index_.count(result.vertices);
    return ChainPoint(this, std::move(result.vertices), count);
}
CertifiedGlobalRequest ClosureOracle::separator_request(const ChainInterval& interval) const {
    if (interval.x_.owner_ != this || interval.y_.owner_ != this)
        throw std::invalid_argument("chain interval belongs to another oracle");
    return CertifiedGlobalRequest(this, {interval.x_.vertices_, interval.y_.vertices_, interval.lambda()});
}
ChainPoint ClosureOracle::separate(const ChainInterval& interval, const CapacityPolicy policy, QueryStats* progress) const {
    auto result = global_F(separator_request(interval), policy, progress);
    if (result.vertices == interval.x_.vertices_ || !subset(interval.x_.vertices_, result.vertices)
        || !subset(result.vertices, interval.y_.vertices_)) throw std::logic_error("separator progress invariant");
    if (result.vertices == interval.y_.vertices_) return interval.y_;
    const auto count = index_.count(result.vertices);
    return ChainPoint(this, std::move(result.vertices), count);
}
OracleResult ClosureOracle::global_F(const CertifiedGlobalRequest& request, const CapacityPolicy policy,
                                   QueryStats* progress) const {
    if (request.owner_ != this) throw std::invalid_argument("certificate belongs to another oracle");
    auto result = largest_restricted(request.request_, policy, progress);
    result.global = true; return result;
}
OracleResult ClosureOracle::largest_restricted(const RestrictedRequest& request, const CapacityPolicy policy,
                                              QueryStats* progress) const {
    QueryStats local_stats;
    QueryStats& stats = progress ? *progress : local_stats;
    stats = QueryStats{};
    validate(index_.graph(), request);
    VertexSet interval;
    std::set_difference(request.y_oracle.begin(), request.y_oracle.end(), request.x.begin(), request.x.end(),
                        std::back_inserter(interval));
    stats.original_interval_size = interval.size(); stats.oracle_interval_size = interval.size();
    if (interval.empty()) return {request.x, false, stats};
    if (request.lambda.numerator() == 0) return {request.y_oracle, false, stats};
    const auto footprints = aggregate_footprints(index_, request);
    stats.cliques_scanned = footprints.scanned; stats.unique_footprints = footprints.records.size();
    const BigInt n = interval.size(), L = n + 1;
    const BigInt source_factor = L * request.lambda.denominator();
    const BigInt sink_capacity = L * request.lambda.numerator() - 1;
    // All preflight arithmetic is unbounded, including finite infinity and totals.
    const BigInt infinity = 1 + source_factor * footprints.total_weight + n * sink_capacity;
    const bool safe = infinity <= to_big(uint128_max);
    if (policy == CapacityPolicy::ForceUInt128 && !safe) throw std::overflow_error("unsafe forced uint128");
    const BigInt nodes = n + footprints.records.size() + 2;
    BigInt arcs = n + footprints.records.size();
    for (const auto& footprint : footprints.records) arcs += footprint.vertices.size();
    stats.forward_nodes = nodes; stats.forward_arcs = arcs; stats.residual_arcs = 2 * arcs;
    stats.capacity_bit_length = bit_length(footprints.records.empty() ? sink_capacity : infinity);
    VertexSet result;
    if (policy == CapacityPolicy::ForceBig || !safe)
        result = execute<BigInt>(index_.graph(), request, footprints, interval, source_factor, sink_capacity, infinity, stats);
    else result = execute<UInt128>(index_.graph(), request, footprints, interval, source_factor, sink_capacity, infinity, stats);
    return {std::move(result), false, stats};
}
}  // namespace vflhcds
