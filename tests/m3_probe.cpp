// Persistent test-only adapter; no expected mathematical truth is computed here.
#include "vflhcds/io/solution.hpp"
#include <iostream>

using namespace vflhcds;
namespace {
std::string token() { std::string s; if(!(std::cin>>s))throw std::runtime_error("EOF"); return s; }
BigInt integer() { return parse_integer(token(),true); }
CapacityPolicy policy() {
    const auto s=token();
    if(s=="auto")return CapacityPolicy::Auto;
    if(s=="big")return CapacityPolicy::ForceBig;
    if(s=="uint128")return CapacityPolicy::ForceUInt128;
    throw std::invalid_argument("policy");
}
std::string without_lf(std::string s) { if(!s.empty()&&s.back()=='\n')s.pop_back(); return s; }
}
int main() {
    try {
        std::string command;
        while(std::cin>>command) {
            if(command!="case")throw std::invalid_argument("case");
            const auto n=to_size(integer()),m=to_size(integer()); const BigInt h=integer();
            if(n>12)throw std::invalid_argument("test probe size guard");
            std::vector<BigInt> vertices; std::vector<OriginalEdge> edges;
            for(std::size_t i=0;i<n;++i)vertices.push_back(integer());
            for(std::size_t i=0;i<m;++i){const auto u=integer(),v=integer();edges.emplace_back(u,v);}
            const Graph graph(std::move(vertices),edges); const MaterializedCliques index(graph,h);
            const ClosureOracle oracle(index); std::vector<ChainPoint> points;
            while((command=token())!="end") {
                const auto capacity=policy();
                if(command=="point") {
                    QueryStats stats;
                    points.push_back(oracle.global_chain_point(Fraction::parse(token()),capacity,&stats));
                    const auto& point=points.back();
                    std::cout<<"{\"token\":"<<points.size()-1<<",\"vertices\":"<<vertices_json(graph,point.vertices())
                             <<",\"clique_count\":\""<<point.cliques()<<"\",\"stats\":"<<query_stats_json(stats)<<"}\n";
                } else if(command=="separator") {
                    const auto x=to_size(integer()),y=to_size(integer());
                    const auto interval=oracle.chain_interval(points.at(x),points.at(y)); QueryStats stats;
                    const auto z=oracle.separate(interval,capacity,&stats); const auto lambda=interval.lambda();
                    std::cout<<"{\"vertices\":"<<vertices_json(graph,z.vertices())<<",\"clique_count\":\""<<z.cliques()
                             <<"\",\"lambda\":\""<<lambda.numerator()<<'/'<<lambda.denominator()<<"\",\"stats\":"<<query_stats_json(stats)<<"}\n";
                } else if(command=="solve") {
                    const auto mode=token(); const std::optional<BigInt> k=mode=="all"?std::nullopt:std::optional<BigInt>(parse_integer(mode));
                    SolveStats stats; std::vector<std::string> traces;
                    const auto result=solve(index,k,capacity,&stats,[&](const ChainInterval& interval,const ChainPoint& z,const QueryStats&) {
                        const auto lambda=interval.lambda();
                        traces.push_back("{\"x\":"+vertices_json(graph,interval.x().vertices())+",\"y\":"+vertices_json(graph,interval.y().vertices())
                            +",\"z\":"+vertices_json(graph,z.vertices())+",\"mu_x\":\""+decimal(interval.x().cliques())+"\",\"mu_y\":\""+decimal(interval.y().cliques())
                            +"\",\"lambda\":\""+decimal(lambda.numerator())+"/"+decimal(lambda.denominator())+"\"}");
                    });
                    std::string canonical; std::cout<<"{\"records\":["; bool first=true; BigInt rank=0;
                    for(const auto& s:result.solutions) {
                        if(!first)std::cout<<','; first=false; const auto line=solution_json(index,s,++rank);
                        canonical+=line; std::cout<<without_lf(line);
                    }
                    std::cout<<"],\"termination\":\""<<(result.k_reached?"k_reached":"exhausted")<<"\",\"semantic_sha256\":\""
                             <<sha256(semantic_header(graph,h)+canonical)<<"\",\"stats\":"<<solve_stats_json(stats)<<",\"trace\":[";
                    first=true; for(const auto& trace:traces){if(!first)std::cout<<',';first=false;std::cout<<trace;}
                    std::cout<<"]}\n";
                } else throw std::invalid_argument("command");
                std::cout.flush();
            }
        }
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
