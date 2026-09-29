#include "vflhcds/cli/dispatch.hpp"
#include "vflhcds/io/status.hpp"

#include <exception>
#include <csignal>
#include <iostream>
#include <new>
#include <string_view>
#include <vector>

namespace {
volatile std::sig_atomic_t interrupted = 0;
void request_stop(int) { interrupted = 1; }
}
int main(int argc, char* argv[]) {
    std::signal(SIGINT, request_stop);
    std::signal(SIGTERM, request_stop);
    try {
        std::vector<std::string_view> args;
        for (int i = 1; i < argc; ++i) {
            args.emplace_back(argv[i]);
        }
        const int result = vflhcds::run_cli(args, std::cout, std::cerr, [] { return interrupted != 0; });
        std::cout.flush();
        std::cerr.flush();
        if (!std::cout || !std::cerr) {
            return vflhcds::exit_code(vflhcds::RunStatus::io_error);
        }
        return result;
    } catch (const std::bad_alloc&) {
        vflhcds::write_failure_status(std::cerr, vflhcds::RunStatus::oom);
        return vflhcds::exit_code(vflhcds::RunStatus::oom);
    } catch (const std::exception&) {
        vflhcds::write_failure_status(std::cerr, vflhcds::RunStatus::internal_error);
        return vflhcds::exit_code(vflhcds::RunStatus::internal_error);
    }
}
