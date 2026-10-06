#pragma once

#include <iosfwd>
#include <string_view>

namespace vflhcds {
// Wire names and exit codes are frozen in docs/INTERFACE_CONTRACT.md.
enum class RunStatus {
    completed = 0,
    invalid_argument = 2,
    invalid_graph = 3,
    io_error = 4,
    resource_limit = 5,
    oom = 6,
    incomplete = 7,
    not_implemented = 8,
    internal_error = 9,
};

[[nodiscard]] std::string_view status_name(RunStatus status) noexcept;
[[nodiscard]] int exit_code(RunStatus status) noexcept;
// M0 failures have no result stream, measurements, or semantic hash.
void write_failure_status(std::ostream& out, RunStatus status);
}  // namespace vflhcds
