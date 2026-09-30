// Local diagnostic driver for the frozen M3 library; no production edits.
#include "vflhcds/io/solution.hpp"
#include <chrono>
#include <iomanip>
#include <iostream>
#include <sys/resource.h>
using namespace vflhcds;
int main(int argc, char** argv) {
    if (argc != 3) return 2;
    const auto graph = parse_graph(read_text_file(argv[1]));
    const BigInt h = parse_integer(argv[2]);
    using Clock = std::chrono::steady_clock;
    const auto start = Clock::now();
    const MaterializedCliques index(graph, h);
    const double enumeration = std::chrono::duration<double>(Clock::now()-start).count();
    std::vector<RestrictedRequest> requests;
    const auto first = solve(index, std::nullopt, CapacityPolicy::Auto, nullptr,
        [&](const ChainInterval& interval, const ChainPoint&, const QueryStats&) {
            if (interval.lambda().numerator() != 0)
                requests.push_back({interval.x().vertices(),interval.y().vertices(),interval.lambda()});
        });
    std::string canonical; BigInt rank=0;
    for(const auto& s:first.solutions) canonical+=solution_json(index,s,++rank);
    const auto solve_start=Clock::now();
    for(int i=0;i<10;++i) (void)solve(index);
    const double solving=std::chrono::duration<double>(Clock::now()-solve_start).count()/10;
    BigInt work=0;
    const auto footprint_start=Clock::now();
    for(int i=0;i<10;++i) for(const auto& request:requests) work+=aggregate_footprints(index,request).scanned;
    const double footprints=std::chrono::duration<double>(Clock::now()-footprint_start).count()/10;
    struct rusage usage{};
    if(getrusage(RUSAGE_SELF,&usage)!=0) return 3;
    std::cout<<std::setprecision(17)<<"{\"enumeration_seconds\":"<<enumeration
        <<",\"solve_seconds_per_run\":"<<solving<<",\"footprints_seconds_per_full_trace\":"<<footprints
        <<",\"positive_queries\":"<<requests.size()<<",\"cliques\":"<<index.cliques().size()
        <<",\"scanned_in_ten_repeats\":"<<work<<",\"peak_rss_platform_units\":"<<usage.ru_maxrss
        <<",\"semantic_sha256\":\""<<sha256(semantic_header(graph,h)+canonical)<<"\"}\n";
}
