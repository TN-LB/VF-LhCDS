#pragma once

#include <iosfwd>
#include <string_view>
#include <vector>

namespace vflhcds {
// Arguments exclude argv[0]. Only help/build-info execute in M0.
int run_cli(const std::vector<std::string_view>& args,
            std::ostream& out, std::ostream& err);
}  // namespace vflhcds
