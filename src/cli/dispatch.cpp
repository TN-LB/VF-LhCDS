#include "vflhcds/cli/dispatch.hpp"

#include "vflhcds/core/build_info.hpp"
#include "vflhcds/io/status.hpp"

#include <ostream>

namespace vflhcds {
int run_cli(const std::vector<std::string_view>& args,
            std::ostream& out, std::ostream& err) {
    if (args.size() == 1 && (args[0] == "--help" || args[0] == "help")) {
        out << "VF-LhCDS M0 skeleton (no algorithm implementation)\n"
               "Usage: vflhcds --help | print-build-info\n"
               "Reserved: solve, oracle, inspect-graph\n"
               "Contracts: docs/INTERFACE_CONTRACT.md\n";
        return exit_code(RunStatus::completed);
    }
    if (args.size() == 1 && args[0] == "print-build-info") {
        const auto info = build_info();
        out << "version=" << info.version << "\nstage=M0\ncxx_standard=17\n"
            << "compiler=" << info.compiler << '\n'
            << "compiler_version=" << info.compiler_version << '\n'
            << "build_type=" << info.build_type << '\n'
            << "sanitizers=" << info.sanitizers << '\n';
        return exit_code(RunStatus::completed);
    }
    if (!args.empty() && (args[0] == "solve" || args[0] == "oracle"
                          || args[0] == "inspect-graph")) {
        write_failure_status(err, RunStatus::not_implemented);
        return exit_code(RunStatus::not_implemented);
    }
    write_failure_status(err, RunStatus::invalid_argument);
    return exit_code(RunStatus::invalid_argument);
}
}  // namespace vflhcds
