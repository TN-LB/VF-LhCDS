#pragma once

#include <string_view>

namespace vflhcds {
struct BuildInfo {
    std::string_view version;
    std::string_view compiler;
    std::string_view compiler_version;
    std::string_view build_type;
    std::string_view sanitizers;
};

[[nodiscard]] BuildInfo build_info() noexcept;
}  // namespace vflhcds
