#include "profile.hpp"
#include <stdexcept>

namespace {
std::int64_t ticks = 0;
vf_profile::Clock::time_point fake_now() {
    return vf_profile::Clock::time_point(std::chrono::nanoseconds(ticks));
}
void require(bool condition) { if (!condition) throw std::runtime_error("exclusive timer regression"); }
}  // namespace
int main() {
    using namespace vf_profile;
    now = fake_now;
    {
        Scope solve(Phase::SolverOther);
        ticks = 10;
        {
            Scope build(Phase::NetworkBuild);
            ticks = 30;
            build.change(Phase::MaxFlow);
            ticks = 60;
            {
                Scope count(Phase::Count);
                ticks = 65;
                const auto partial = snapshot();
                require(partial[static_cast<std::size_t>(Phase::Count)].nanoseconds == 5);
                ticks = 70;
            }
            ticks = 80;
        }
        ticks = 90;
        try { Scope count(Phase::Count); ticks = 95; throw 1; } catch (int) {}
        ticks = 100;
    }
    const auto result = snapshot();
    const auto at = [&](Phase p) { return result[static_cast<std::size_t>(p)]; };
    require(at(Phase::SolverOther).nanoseconds == 25);
    require(at(Phase::NetworkBuild).nanoseconds == 20);
    require(at(Phase::MaxFlow).nanoseconds == 40);
    require(at(Phase::Count).nanoseconds == 15 && at(Phase::Count).calls == 2);
    require(collector.active == Phase::Idle);
    ticks = 1000;
    require(snapshot()[static_cast<std::size_t>(Phase::SolverOther)].nanoseconds == 25);
}
