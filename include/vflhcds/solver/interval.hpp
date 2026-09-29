#pragma once
#include "vflhcds/core/graph.hpp"

namespace vflhcds {
class ClosureOracle;
// A token is minted only for a proved extreme or the output of a certified global
// query. Read-only access cannot turn an arbitrary VertexSet into a chain point.
class ChainPoint {
    friend class ClosureOracle;
public:
    const VertexSet& vertices() const noexcept { return vertices_; }
    const BigInt& cliques() const noexcept { return cliques_; }
private:
    ChainPoint(const ClosureOracle* owner, VertexSet vertices, BigInt cliques)
        : owner_(owner), vertices_(std::move(vertices)), cliques_(std::move(cliques)) {}
    const ClosureOracle* const owner_;
    const VertexSet vertices_;
    const BigInt cliques_;
};
class ChainInterval {
    friend class ClosureOracle;
public:
    const ChainPoint& x() const noexcept { return x_; }
    const ChainPoint& y() const noexcept { return y_; }
    Fraction lambda() const {
        return Fraction(y_.cliques() - x_.cliques(), y_.vertices().size() - x_.vertices().size());
    }
private:
    ChainInterval(ChainPoint x, ChainPoint y) : x_(std::move(x)), y_(std::move(y)) {}
    const ChainPoint x_, y_;
};
}  // namespace vflhcds
