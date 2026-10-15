#include "vflhcds/solver/traversal.hpp"
#include <algorithm>
#include <numeric>

namespace vflhcds {
CliqueRange::CliqueRange(const MaterializedCliques& index, std::vector<std::size_t>& ids,
                         const std::size_t begin, const std::size_t end, const VertexSet& x, const VertexSet& y)
    : index_(index), ids_(ids), begin_(begin), end_(end), x_(x), y_(y) {
    if (begin > end || end > ids.size()) throw std::invalid_argument("invalid clique range");
}
void CliqueRange::verify() const {
    index_.graph().validate_set(x_); index_.graph().validate_set(y_);
    if (!subset(x_, y_)) throw std::invalid_argument("invalid range endpoints");
    std::vector<unsigned char> seen(index_.cliques().size(), 0);
    for (std::size_t i = begin_; i < end_; ++i) {
        const auto id = ids_[i];
        if (id >= seen.size() || seen[id] != 0) throw std::invalid_argument("invalid or duplicate clique ID");
        seen[id] = 1;
    }
    for (std::size_t i = 0; i < seen.size(); ++i) {
        const auto& clique = index_.cliques()[i];
        if ((seen[i] != 0) != (subset(clique, y_) && !subset(clique, x_)))
            throw std::invalid_argument("incomplete or extraneous interval cliques");
    }
}
std::size_t CliqueRange::partition(const VertexSet& z) {
    if (!subset(x_, z) || !subset(z, y_)) throw std::logic_error("partition outside original endpoints");
    Membership members(index_.graph().size()); members.assign(z);
    std::size_t middle = begin_;
    for (std::size_t i = begin_; i < end_; ++i) {
        const auto& clique = index_.cliques()[ids_[i]];
        if (std::all_of(clique.begin(), clique.end(), [&](const VertexId v) { return members.contains(v); })) {
            std::swap(ids_[middle], ids_[i]); ++middle;
        }
    }
    return middle;
}
IntervalTraversal::IntervalTraversal(const ClosureOracle& oracle, const CliqueWork work)
    : oracle_(oracle), work_(work) {
    if (work != CliqueWork::Global && work != CliqueWork::IntervalScan && work != CliqueWork::IntervalReuse)
        throw std::invalid_argument("unknown clique work mode");
    if (work != CliqueWork::Global) {
        ids_.resize(oracle_.index_.cliques().size());
        std::iota(ids_.begin(), ids_.end(), std::size_t{0});
    }
    stack_.push_back({oracle_.root_interval(), 0, ids_.size(), 0});
}
TraversalStep IntervalTraversal::next(const CapacityPolicy policy, QueryStats& query, const OracleOptions options) {
    if (failed_ || stack_.empty()) throw std::logic_error("inactive interval traversal");
    // An exception may leave a consumed frame or a partially scheduled frontier.
    // It is never legal to resume that traversal with a different configuration.
    failed_ = true;
    try {
    const auto frame = std::move(stack_.back()); stack_.pop_back();
    const auto& interval = frame.interval;
    CliqueRange range(oracle_.index_, ids_, frame.begin, frame.end, interval.x().vertices(), interval.y().vertices());
    std::size_t middle = frame.begin;
    const auto z = oracle_.separate_impl(interval, policy, &query, options,
        work_ == CliqueWork::Global ? nullptr : &range, work_ == CliqueWork::IntervalReuse, &middle);
    query.depth = frame.depth;
    if (z.vertices() != interval.y().vertices()) {
        stack_.push_back({oracle_.chain_interval(z, interval.y()), middle, frame.end, frame.depth + 1});
        stack_.push_back({oracle_.chain_interval(interval.x(), z), frame.begin, middle, frame.depth + 1});
    }
    failed_ = false;
    return {interval, z};
    } catch (...) { failed_ = true; throw; }
}
}  // namespace vflhcds
