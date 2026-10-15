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
enum class CliqueWork { Global, IntervalScan, IntervalReuse };
struct OracleOptions {
    CoreMode core = CoreMode::Off;
    FootprintMode footprints = FootprintMode::Sorted;
    CliqueWork clique_work = CliqueWork::Global; // solve only; standalone queries always scan globally
};
class CliqueRange;
class IntervalTraversal;
struct IntervalTestAccess;
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
    friend class IntervalTraversal;
    friend struct IntervalTestAccess;
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
    ChainPoint separate_impl(const ChainInterval& interval, CapacityPolicy policy, QueryStats* progress,
                             OracleOptions options, CliqueRange* range, bool reuse, std::size_t* middle) const;
    OracleResult global_impl(const CertifiedGlobalRequest& request, CapacityPolicy policy,
                             QueryStats* progress, OracleOptions options, const CliqueRange* range) const;
    Footprints local_footprints(const RestrictedRequest& request, FootprintMode mode, const CliqueRange& range) const;
    OracleResult restricted_impl(const RestrictedRequest& request, CapacityPolicy policy,
                                 QueryStats& stats, FootprintMode mode, const CliqueRange* range = nullptr) const;
    const MaterializedCliques& index_;
};
}  // namespace vflhcds
