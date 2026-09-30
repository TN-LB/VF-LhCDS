#pragma once
#include "vflhcds/clique/materialized.hpp"
#include "vflhcds/clique/core.hpp"
#include "vflhcds/telemetry/query.hpp"
#include "vflhcds/solver/interval.hpp"

namespace vflhcds {
struct RestrictedRequest { VertexSet x, y_oracle; Fraction lambda; };
struct Footprint { VertexSet vertices; BigInt weight; };
struct Footprints { std::vector<Footprint> records; BigInt scanned = 0, total_weight = 0; };
enum class CoreMode { Off, Safe };
enum class FootprintMode { Sorted, Membership };
struct OracleOptions { CoreMode core = CoreMode::Off; FootprintMode footprints = FootprintMode::Sorted; };
Footprints aggregate_footprints(const MaterializedCliques& index, const RestrictedRequest& request,
                               FootprintMode mode = FootprintMode::Sorted);
enum class CapacityPolicy { Auto, ForceUInt128, ForceBig };
struct OracleResult { VertexSet vertices; bool global = false; QueryStats stats; };
class ClosureOracle;

// Copying a valid certificate is fine; arbitrary bounds cannot acquire this type
// by choosing a public enum value. Chain separators require sealed chain tokens.
class CertifiedGlobalRequest {
    friend class ClosureOracle;
public:
    const RestrictedRequest& request() const noexcept { return request_; }
private:
    CertifiedGlobalRequest(const ClosureOracle* owner, RestrictedRequest request)
        : owner_(owner), request_(std::move(request)) {}
    const ClosureOracle* const owner_;
    const RestrictedRequest request_;
};
class ClosureOracle {
public:
    explicit ClosureOracle(const MaterializedCliques& index) : index_(index) {}
    ClosureOracle(const ClosureOracle&) = delete;
    ClosureOracle& operator=(const ClosureOracle&) = delete;
    CertifiedGlobalRequest full_graph_request(Fraction lambda) const;
    ChainInterval root_interval() const;
    ChainInterval chain_interval(const ChainPoint& x, const ChainPoint& y) const;
    ChainPoint global_chain_point(Fraction lambda, CapacityPolicy policy = CapacityPolicy::Auto,
                                  QueryStats* progress = nullptr, OracleOptions options = {}) const;
    CertifiedGlobalRequest separator_request(const ChainInterval& interval) const;
    ChainPoint separate(const ChainInterval& interval, CapacityPolicy policy = CapacityPolicy::Auto,
                        QueryStats* progress = nullptr, OracleOptions options = {}) const;
    OracleResult global_F(const CertifiedGlobalRequest& request, CapacityPolicy policy = CapacityPolicy::Auto,
                          QueryStats* progress = nullptr, OracleOptions options = {}) const;
    OracleResult largest_restricted(const RestrictedRequest& request, CapacityPolicy policy = CapacityPolicy::Auto,
                                    QueryStats* progress = nullptr, FootprintMode mode = FootprintMode::Sorted) const;
private:
    OracleResult restricted_impl(const RestrictedRequest& request, CapacityPolicy policy,
                                 QueryStats& stats, FootprintMode mode) const;
    const MaterializedCliques& index_;
};
}  // namespace vflhcds
