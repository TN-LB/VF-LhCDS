#pragma once
#include <array>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <ostream>

// Diagnostic-only, single-threaded exclusive wall-time accounting.
namespace vf_profile {
using Clock = std::chrono::steady_clock;
enum class Phase : std::size_t {
    Idle, SolverOther, Count, Footprints, OracleOther, NetworkBuild,
    MaxFlow, CutExtract, NetworkCleanup, Trace, Size
};
constexpr std::size_t size = static_cast<std::size_t>(Phase::Size);
inline constexpr std::array<const char*, size> names{
    "idle", "solver_other", "count", "footprints", "oracle_other", "network_build",
    "max_flow", "cut_extract", "network_cleanup", "trace"
};
struct Bucket { std::int64_t nanoseconds = 0; std::uint64_t calls = 0; };
struct Collector {
    std::array<Bucket, size> buckets{};
    Phase active = Phase::Idle;
    Clock::time_point last{};
};
inline Collector collector;
inline Clock::time_point (*now)() = Clock::now;
inline void switch_phase(Phase phase, bool entered) noexcept {
    const auto timestamp = now();
    if (collector.active != Phase::Idle)
        collector.buckets[static_cast<std::size_t>(collector.active)].nanoseconds +=
            std::chrono::duration_cast<std::chrono::nanoseconds>(timestamp - collector.last).count();
    collector.active = phase;
    collector.last = timestamp;
    if (entered) ++collector.buckets[static_cast<std::size_t>(phase)].calls;
}
class Scope {
public:
    explicit Scope(Phase phase) noexcept : previous_(collector.active) { switch_phase(phase, true); }
    ~Scope() { switch_phase(previous_, false); }
    Scope(const Scope&) = delete;
    Scope& operator=(const Scope&) = delete;
    void change(Phase phase) noexcept { switch_phase(phase, true); }
private:
    Phase previous_;
};
inline std::array<Bucket, size> snapshot() {
    auto result = collector.buckets;
    if (collector.active != Phase::Idle)
        result[static_cast<std::size_t>(collector.active)].nanoseconds +=
            std::chrono::duration_cast<std::chrono::nanoseconds>(now() - collector.last).count();
    return result;
}
inline void write_json(std::ostream& out) {
    const auto buckets = snapshot();
    out << '{';
    for (std::size_t i = 1; i < size; ++i) {
        if (i > 1) out << ',';
        out << '"' << names[i] << "\":{\"nanoseconds\":" << buckets[i].nanoseconds
            << ",\"calls\":" << buckets[i].calls << '}';
    }
    out << '}';
}
}  // namespace vf_profile
