// Same frozen local diagnostic work as the M3 baseline, with explicit M4 modes.
#include "vflhcds/io/solution.hpp"
#include <chrono>
#include <algorithm>
#include <iterator>
#include <iomanip>
#include <iostream>
#include <sys/resource.h>
using namespace vflhcds;
int main(int argc, char** argv) {
    if (argc != 5) return 2;
    const std::string core_mode(argv[3]), scan_mode(argv[4]);
    if ((core_mode!="off"&&core_mode!="safe")||(scan_mode!="sorted"&&scan_mode!="membership")) return 2;
    const OracleOptions options{core_mode=="safe"?CoreMode::Safe:CoreMode::Off,
                                scan_mode=="membership"?FootprintMode::Membership:FootprintMode::Sorted};
    const auto graph = parse_graph(read_text_file(argv[1]));
    const BigInt h = parse_integer(argv[2]);
    using Clock = std::chrono::steady_clock;
    const auto start = Clock::now();
    const MaterializedCliques index(graph, h);
    const double enumeration = std::chrono::duration<double>(Clock::now()-start).count();
    std::vector<RestrictedRequest> requests;
    const auto first = solve(index, std::nullopt, CapacityPolicy::Auto, nullptr,
        [&](const ChainInterval& interval, const ChainPoint&, const QueryStats&) {
            if (interval.lambda().numerator() != 0) {
                VertexSet upper=interval.y().vertices();
                if(options.core==CoreMode::Safe){
                    const auto lambda=interval.lambda();
                    const auto core=peel_core(index,(lambda.numerator()+lambda.denominator()-1)/lambda.denominator());
                    VertexSet intersection;
                    std::set_intersection(upper.begin(),upper.end(),core.begin(),core.end(),std::back_inserter(intersection));
                    upper=std::move(intersection);
                }
                requests.push_back({interval.x().vertices(),std::move(upper),interval.lambda()});
            }
        },{},options);
    std::string canonical; BigInt rank=0;
    for(const auto& s:first.solutions) canonical+=solution_json(index,s,++rank);
    const auto solve_start=Clock::now();
    double core_seconds=0;
    BigInt original_vertices=0,oracle_vertices=0,nodes=0,arcs=0;
    for(int i=0;i<10;++i) {
        SolveStats stats;
        (void)solve(index,std::nullopt,CapacityPolicy::Auto,&stats,{}, {},options);
        for(const auto& query:stats.queries){
            if(query.core_reduction_seconds)core_seconds+=*query.core_reduction_seconds;
            original_vertices+=query.original_interval_size;oracle_vertices+=query.oracle_interval_size;
            if(query.forward_nodes)nodes+=*query.forward_nodes;
            if(query.forward_arcs)arcs+=*query.forward_arcs;
        }
    }
    const double solving=std::chrono::duration<double>(Clock::now()-solve_start).count()/10;
    BigInt work=0;
    const auto footprint_start=Clock::now();
    for(int i=0;i<10;++i) for(const auto& request:requests) work+=aggregate_footprints(index,request,options.footprints).scanned;
    const double footprints=std::chrono::duration<double>(Clock::now()-footprint_start).count()/10;
    struct rusage usage{};
    if(getrusage(RUSAGE_SELF,&usage)!=0) return 3;
    std::cout<<std::setprecision(17)<<"{\"enumeration_seconds\":"<<enumeration
        <<",\"solve_seconds_per_run\":"<<solving<<",\"footprints_seconds_per_full_trace\":"<<footprints
        <<",\"core_seconds_per_run\":"<<core_seconds/10
        <<",\"original_vertices_in_ten_runs\":"<<original_vertices<<",\"oracle_vertices_in_ten_runs\":"<<oracle_vertices
        <<",\"network_nodes_in_ten_runs\":"<<nodes<<",\"network_arcs_in_ten_runs\":"<<arcs
        <<",\"positive_queries\":"<<requests.size()<<",\"cliques\":"<<index.cliques().size()
        <<",\"scanned_in_ten_repeats\":"<<work<<",\"peak_rss_platform_units\":"<<usage.ru_maxrss
        <<",\"semantic_sha256\":\""<<sha256(semantic_header(graph,h)+canonical)<<"\"}\n";
}
