#pragma once

#include <iosfwd>
#include <functional>
#include <string_view>
#include <vector>

namespace vflhcds {
// Arguments exclude argv[0]. Optional stop is polled at safe execution boundaries.
int run_cli(const std::vector<std::string_view>& args,
            std::ostream& out, std::ostream& err, const std::function<bool()>& stop = {});
}  // namespace vflhcds
