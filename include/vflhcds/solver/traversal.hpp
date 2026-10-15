#pragma once
#include "vflhcds/oracle/closure.hpp"

namespace vflhcds {
struct IntervalTestAccess;
// Borrowed only within next(). Construction is sealed; no caller-supplied ID list
// can enter an oracle query. Original endpoints survive temporary core filtering.
class CliqueRange {
    friend class IntervalTraversal;
    friend class ClosureOracle;
    friend struct IntervalTestAccess;
public:
    std::size_t size() const noexcept { return end_ - begin_; }
    const VertexSet& at(std::size_t offset) const {
        if (offset >= size()) throw std::out_of_range("clique range offset");
        return index_.cliques().at(ids_.at(begin_ + offset));
    }
private:
    CliqueRange(const MaterializedCliques& index, std::vector<std::size_t>& ids,
                std::size_t begin, std::size_t end, const VertexSet& x, const VertexSet& y);
    std::size_t partition(const VertexSet& z);
    void verify() const; // exhaustive invariant audit for the internal test probe
    const MaterializedCliques& index_;
    std::vector<std::size_t>& ids_;
    const std::size_t begin_, end_;
    const VertexSet& x_;
    const VertexSet& y_;
};
struct TraversalStep { ChainInterval interval; ChainPoint z; };
class IntervalTraversal {
public:
    IntervalTraversal(const ClosureOracle& oracle, CliqueWork work);
    IntervalTraversal(const IntervalTraversal&) = delete;
    IntervalTraversal& operator=(const IntervalTraversal&) = delete;
    IntervalTraversal(IntervalTraversal&&) = delete;
    IntervalTraversal& operator=(IntervalTraversal&&) = delete;
    bool empty() const noexcept { return stack_.empty(); }
    TraversalStep next(CapacityPolicy policy, QueryStats& query, OracleOptions options);
    std::size_t id_size() const noexcept { return ids_.size(); }
    std::size_t id_capacity() const noexcept { return ids_.capacity(); }
    std::size_t frontier_size() const noexcept { return stack_.size(); }
    std::size_t frontier_capacity() const noexcept { return stack_.capacity(); }
private:
    struct Frame { ChainInterval interval; std::size_t begin, end, depth; };
    const ClosureOracle& oracle_;
    const CliqueWork work_;
    std::vector<std::size_t> ids_;
    std::vector<Frame> stack_;
    bool failed_ = false;
};
}  // namespace vflhcds
