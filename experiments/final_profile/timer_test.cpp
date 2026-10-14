#include "observer.hpp"
#include <stdexcept>

namespace {
std::int64_t ticks = 0;
fp::Clock::time_point fake_now() { return fp::Clock::time_point(std::chrono::nanoseconds(ticks)); }
void require(bool ok) { if (!ok) throw std::runtime_error("T18 exclusive timer/cleanup"); }
struct Resource { ~Resource() { ticks += 7; } };
}
int main() {
    fp::now = fake_now;
    fp::reset();
    {
        fp::Scope outer("orchestration");
        ticks = 10;
        {
            fp::Scope nested("network_build");
            ticks = 30;
            nested.change("max_flow");
            ticks = 60;
            require(fp::snapshot().at("max_flow") == 30);
        }
        ticks = 70;
        try {
            fp::Scope count("count");
            fp::CleanupEnd end;
            Resource resource;
            fp::CleanupBegin begin(end, "cleanup_network");
            ticks = 75;
            throw 1;
        } catch (int) {}
        ticks = 90;
    }
    const auto s = fp::snapshot();
    require(s.at("orchestration") == 28);
    require(s.at("network_build") == 20);
    require(s.at("max_flow") == 30);
    require(s.at("count") == 5);
    require(s.at("cleanup_network") == 7);
    require(fp::state.active == "unassigned");
    ticks = 100;
    require(fp::snapshot().at("unassigned") == 10);
    fp::add("large", vflhcds::BigInt(1) << 200U);
    fp::add("large", 1);
    require(fp::state.work.at("large") == (vflhcds::BigInt(1) << 200U) + 1);
}
