#pragma once
#include "vflhcds/core/exact.hpp"
#include <algorithm>
#include <limits>
#include <type_traits>
#include <vector>

namespace vflhcds {
template<class Capacity> struct CapacityOps {
    static Capacity add(const Capacity& a, const Capacity& b) {
        if constexpr (std::is_same_v<Capacity, UInt128>) return checked_add(a, b);
        else return a + b;
    }
    static Capacity sub(const Capacity& a, const Capacity& b) {
        if constexpr (std::is_same_v<Capacity, UInt128>) return checked_sub(a, b);
        else {
            if (b > a) throw std::logic_error("negative residual");
            return a - b;
        }
    }
};

// One algorithm for both exact capacity domains. Blocking paths use heap-backed
// stacks; no DFS recursion can consume the process stack on a long input path.
template<class Capacity> class Dinic {
    static_assert(std::is_same_v<Capacity, UInt128> || std::is_same_v<Capacity, BigInt>);
public:
    struct Arc { std::size_t to, reverse; Capacity residual; };
    explicit Dinic(std::size_t nodes) : arcs_(nodes), level_(nodes), next_(nodes) {}
    void add_arc(std::size_t from, std::size_t to, Capacity capacity) {
        if (used_) throw std::logic_error("network already executed");
        if (capacity < 0) throw std::invalid_argument("negative capacity");
        if (from >= arcs_.size() || to >= arcs_.size()) throw std::out_of_range("arc endpoint");
        const auto forward = arcs_[from].size();
        const auto reverse = arcs_[to].size() + (from == to ? 1U : 0U);
        arcs_[from].push_back({to, reverse, std::move(capacity)});
        arcs_[to].push_back({from, forward, Capacity{0}});
    }
    Capacity max_flow(std::size_t source, std::size_t sink) {
        if (used_) throw std::logic_error("max_flow is single-use");
        if (source == sink || source >= arcs_.size() || sink >= arcs_.size())
            throw std::invalid_argument("invalid terminals");
        // A sufficient total-flow bound; checked even for generic callers.
        Capacity bound = 0;
        for (const auto& arc : arcs_[source]) bound = CapacityOps<Capacity>::add(bound, arc.residual);
        used_ = true;
        Capacity total = 0;
        while (levels(source, sink)) {
            std::fill(next_.begin(), next_.end(), 0);
            while (true) {
                const Capacity pushed = augment(source, sink, bound);
                if (pushed == 0) break;
                total = CapacityOps<Capacity>::add(total, pushed);
            }
        }
        return total;
    }
    std::vector<unsigned char> reachable(std::size_t source) const {
        if (source >= arcs_.size()) throw std::out_of_range("source");
        std::vector<unsigned char> seen(arcs_.size(), 0);
        std::vector<std::size_t> queue{source}; seen[source] = 1;
        for (std::size_t i = 0; i < queue.size(); ++i)
            for (const auto& arc : arcs_[queue[i]])
                if (arc.residual > 0 && seen[arc.to] == 0) { seen[arc.to] = 1; queue.push_back(arc.to); }
        return seen;
    }
    const std::vector<std::vector<Arc>>& residual() const noexcept { return arcs_; }
private:
    bool levels(std::size_t source, std::size_t sink) {
        std::fill(level_.begin(), level_.end(), std::numeric_limits<std::size_t>::max());
        std::vector<std::size_t> queue{source}; level_[source] = 0;
        for (std::size_t i = 0; i < queue.size(); ++i)
            for (const auto& arc : arcs_[queue[i]])
                if (arc.residual > 0 && level_[arc.to] == std::numeric_limits<std::size_t>::max()) {
                    level_[arc.to] = level_[queue[i]] + 1; queue.push_back(arc.to);
                }
        return level_[sink] != std::numeric_limits<std::size_t>::max();
    }
    Capacity augment(std::size_t source, std::size_t sink, const Capacity& bound) {
        std::vector<std::size_t> path{source};
        std::vector<Capacity> bottleneck{bound};
        while (!path.empty()) {
            const auto u = path.back();
            if (u == sink) {
                const Capacity pushed = bottleneck.back();
                for (std::size_t i = 0; i + 1 < path.size(); ++i) {
                    auto& arc = arcs_[path[i]][next_[path[i]]];
                    auto& reverse = arcs_[arc.to][arc.reverse];
                    arc.residual = CapacityOps<Capacity>::sub(arc.residual, pushed);
                    reverse.residual = CapacityOps<Capacity>::add(reverse.residual, pushed);
                }
                return pushed;
            }
            auto& current = next_[u];
            while (current < arcs_[u].size()) {
                const auto& arc = arcs_[u][current];
                if (arc.residual > 0 && level_[arc.to] == level_[u] + 1) break;
                ++current;
            }
            if (current == arcs_[u].size()) {
                path.pop_back(); bottleneck.pop_back();
                if (!path.empty()) ++next_[path.back()];
            } else {
                const auto& arc = arcs_[u][current];
                bottleneck.push_back(std::min(bottleneck.back(), arc.residual));
                path.push_back(arc.to);
            }
        }
        return Capacity{0};
    }
    std::vector<std::vector<Arc>> arcs_;
    std::vector<std::size_t> level_, next_;
    bool used_ = false;
};
}  // namespace vflhcds
