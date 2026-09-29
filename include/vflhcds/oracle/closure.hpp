#pragma once
#include "vflhcds/clique/materialized.hpp"
#include "vflhcds/telemetry/query.hpp"

namespace vflhcds {
struct RestrictedRequest { VertexSet x, y_oracle; Fraction lambda; };
struct Footprint { VertexSet vertices; BigInt weight; };
struct Footprints { std::vector<Footprint> records; BigInt scanned = 0, total_weight = 0; };
Footprints aggregate_footprints(const MaterializedCliques& index, const RestrictedRequest& request);
enum class CapacityPolicy { Auto, ForceUInt128, ForceBig };
struct OracleResult { VertexSet vertices; bool global = false; QueryStats stats; };
class ClosureOracle;

// Only a full-graph factory exists in M2. Copying a valid certificate is fine;
// arbitrary bounds cannot acquire this type by choosing a public enum value.
class CertifiedGlobalRequest {
    friend class ClosureOracle;
public:
    const RestrictedRequest& request() const noexcept { return request_; }
private:
    CertifiedGlobalRequest(const ClosureOracle* owner, RestrictedRequest request)
        : owner_(owner), request_(std::move(request)) {}
    const ClosureOracle* owner_;
    RestrictedRequest request_;
};
class ClosureOracle {
public:
    explicit ClosureOracle(const MaterializedCliques& index) : index_(index) {}
    ClosureOracle(const ClosureOracle&) = delete;
    ClosureOracle& operator=(const ClosureOracle&) = delete;
    CertifiedGlobalRequest full_graph_request(Fraction lambda) const;
    OracleResult global_F(const CertifiedGlobalRequest& request, CapacityPolicy policy = CapacityPolicy::Auto,
                          QueryStats* progress = nullptr) const;
    OracleResult largest_restricted(const RestrictedRequest& request, CapacityPolicy policy = CapacityPolicy::Auto,
                                    QueryStats* progress = nullptr) const;
private:
    const MaterializedCliques& index_;
};
}  // namespace vflhcds
