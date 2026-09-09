#include "vflhcds/cli/dispatch.hpp"
#include "vflhcds/core/build_info.hpp"
#include "vflhcds/io/status.hpp"

#include <iostream>
#include <sstream>

int main() {
    // Runtime checks remain enabled in Release builds (no assert/NDEBUG gate).
    const auto info = vflhcds::build_info();
    if (info.compiler.empty() || info.compiler_version.empty()) {
        std::cerr << "Missing build provenance\n";
        return 1;
    }
    std::ostringstream out;
    std::ostringstream err;
    const int result = vflhcds::run_cli({"solve"}, out, err);
    if (result != vflhcds::exit_code(vflhcds::RunStatus::not_implemented)
        || !out.str().empty()
        || err.str().find("\"complete\":false") == std::string::npos) {
        std::cerr << "Unimplemented algorithm must not appear complete\n";
        return 1;
    }
    return 0;
}
