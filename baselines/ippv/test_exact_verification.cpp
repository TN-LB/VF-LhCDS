#include "ExactVerification.h"
#include <cassert>
#include <limits>
#include <stdexcept>
#include <vector>

int main() {
    using Integer = ExactVerification::Integer;
    // All rational arc types, including fractional h/r boundary footprints.
    for (int h = 2; h <= 5; ++h) {
        std::vector<std::size_t> sizes;
        for (int r = 1; r <= h; ++r) sizes.push_back(static_cast<std::size_t>(r));
        for (std::size_t n = 2; n <= 13; ++n) {
            const std::size_t total = n + 7;
            const std::size_t count = n + 3;
            ExactVerification exact(count, n, total, h, sizes);
            for (auto r : sizes) assert(exact.share(r) * r == exact.unit() * h);
            assert(exact.reverse() == exact.unit() * (h - 1));
            assert(Integer(exact.sink()) * n * total * total ==
                   exact.unit() * h * (Integer(count) * total * total - n));
        }
    }
    // A 5/4-density candidate: integer truncation used to lower 2*g_epsilon to 2.
    ExactVerification example(5, 4, 8, 2, {1});
    assert(example.sink() == 632 && example.unit() == 256);
    assert(example.sink() != 2 * example.unit());
    assert(ExactVerification::checked(Integer((std::numeric_limits<long>::max)())) ==
           (std::numeric_limits<long>::max)());
    for (const Integer& value : {Integer(-1), Integer((std::numeric_limits<long>::max)()) + 1}) {
        bool rejected = false;
        try { ExactVerification::checked(value); }
        catch (const std::overflow_error&) { rejected = true; }
        assert(rejected);
    }
    bool rejected = false;
    try { ExactVerification huge(1, 2, (std::numeric_limits<std::size_t>::max)(), 3, {2}); }
    catch (const std::overflow_error&) { rejected = true; }
    assert(rejected);
}
