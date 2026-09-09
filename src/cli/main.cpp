#include "vflhcds/cli/dispatch.hpp"
#include "vflhcds/io/status.hpp"

#include <exception>
#include <iostream>
#include <new>
#include <string_view>
#include <vector>

int main(int argc, char* argv[]) {
    try {
        std::vector<std::string_view> args;
        for (int i = 1; i < argc; ++i) {
            args.emplace_back(argv[i]);
        }
        const int result = vflhcds::run_cli(args, std::cout, std::cerr);
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
