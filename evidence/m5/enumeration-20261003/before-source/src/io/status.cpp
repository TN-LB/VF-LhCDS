#include "vflhcds/io/status.hpp"

#include <ostream>

namespace vflhcds {
std::string_view status_name(const RunStatus status) noexcept {
    switch (status) {
    case RunStatus::completed: return "completed";
    case RunStatus::invalid_argument: return "invalid_argument";
    case RunStatus::invalid_graph: return "invalid_graph";
    case RunStatus::io_error: return "io_error";
    case RunStatus::resource_limit: return "resource_limit";
    case RunStatus::oom: return "oom";
    case RunStatus::incomplete: return "incomplete";
    case RunStatus::not_implemented: return "not_implemented";
    case RunStatus::internal_error: return "internal_error";
    }
    return "internal_error";
}

int exit_code(const RunStatus status) noexcept {
    return static_cast<int>(status);
}

void write_failure_status(std::ostream& out, const RunStatus status) {
    out << "{\"schema_version\":1,\"status\":\"" << status_name(status)
        << "\",\"complete\":false,\"output_count\":0,\"semantic_sha256\":null}\n";
}
}  // namespace vflhcds
