#include "vflhcds/io/solution.hpp"
#include <iostream>
using namespace vflhcds;
namespace {
std::size_t checks=0;
void require(bool value,const char* name){++checks;if(!value)throw std::runtime_error(name);}
template<class Error,class Function> void rejects(Function function){
    try{function();}catch(const Error&){++checks;return;}throw std::runtime_error("expected rejection");
}
void witness(){
    const Graph graph({0,1,2,3,4,5,6,7},{{0,1},{0,2},{0,3},{1,2},{1,3},{2,3},{4,5},{4,6},{5,6},{4,7}});
    const MaterializedCliques index(graph,2);const ClosureOracle oracle(index),foreign(index);
    const OracleOptions safe{CoreMode::Safe,FootprintMode::Sorted};
    const auto root=oracle.root_interval();const auto core=peel_core(index,2);
    require(core==VertexSet({0,1,2,3,4,5,6}),"T17 non-chain root core");
    QueryStats stats;const auto z=oracle.separate(root,CapacityPolicy::Auto,&stats,safe);
    require(z.vertices()==VertexSet({0,1,2,3})&&root.lambda()==Fraction(5,4),"T17 original lambda and global set");
    require(stats.original_interval_size==8&&stats.oracle_interval_size==7&&stats.core_threshold==BigInt(2),"T17 reduced telemetry");
    require(stats.core&&stats.core->vertices_removed==1&&stats.core->cliques_invalidated==1,"T17 core work");
    require(stats.core_reduction_seconds&&*stats.core_reduction_seconds>=0,"T17 cost measured");
    const auto right=oracle.chain_interval(z,root.y());
    require(right.lambda()==Fraction(1)&&oracle.separate(right,CapacityPolicy::Auto,&stats,safe).vertices()==graph.all_vertices(),"T17 lower threshold restores pendant");
    require(stats.oracle_interval_size==4&&stats.core->vertices_removed==0,"T17 full original graph per query");
    SolveStats totals;
    const auto all=solve(index,std::nullopt,CapacityPolicy::Auto,&totals,{}, {},safe);
    require(all.solutions.size()==2&&all.solutions[1].vertices==VertexSet({4,5,6,7}),"T17 output retains pendant");
    require(all.solutions[1].density==Fraction(1)&&totals.logical_interval_queries==3,"T17 original terminal and count");
    for(const auto mode:{FootprintMode::Sorted,FootprintMode::Membership}){
        const OracleOptions options{CoreMode::Safe,mode};
        const auto prefix=solve(index,BigInt(1),CapacityPolicy::ForceBig,&totals,{}, {},options);
        require(prefix.k_reached&&prefix.solutions.size()==1&&totals.logical_interval_queries==2,"T17 fixed-k stops");
        const auto zero=oracle.global_F(oracle.full_graph_request(Fraction(0)),CapacityPolicy::Auto,&stats,options);
        require(zero.vertices==graph.all_vertices()&&!stats.core&&!stats.core_threshold&&!stats.core_reduction_seconds,"T17 zero bypass");
        const auto high=oracle.global_F(oracle.full_graph_request(Fraction(BigInt(1)<<200U)),CapacityPolicy::Auto,&stats,options);
        require(high.vertices.empty()&&stats.oracle_interval_size==0&&stats.mincut_calls==0&&!stats.forward_nodes,"T17 empty-core shortcut");
        auto request=oracle.full_graph_request(Fraction(5,4));const auto moved=std::move(request);
        require(oracle.global_F(request,CapacityPolicy::Auto,nullptr,options).vertices==z.vertices()
                &&oracle.global_F(moved,CapacityPolicy::Auto,nullptr,options).vertices==z.vertices(),"T17 moved certificate remains valid");
        rejects<std::invalid_argument>([&]{(void)foreign.global_F(request,CapacityPolicy::Auto,nullptr,options);});
    }
}
void peeling(){
    const Graph graph({0,1,2,3,4},{{0,1},{1,2},{2,3},{3,4}});const MaterializedCliques index(graph,2);
    CoreStats stats;require(peel_core(index,2,&stats).empty(),"T17 cascading removals");
    require(stats.vertices_removed==5&&stats.cliques_invalidated==4&&stats.degree_decrements==4&&stats.incidence_visits==8,"T17 each edge invalidated once");
    require(peel_core(index,1)==graph.all_vertices(),"T17 decreasing threshold restores graph");
    require(peel_core(index,0,&stats)==graph.all_vertices()&&stats.cliques_invalidated==0,"T17 threshold zero");
    rejects<std::invalid_argument>([&]{(void)peel_core(index,-1);});
    const MaterializedCliques triangles(graph,3);
    require(peel_core(triangles,1).empty(),"T17 ordinary degrees cannot replace triangle degrees");
    const Graph k4({0,1,2,3},{{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}});const MaterializedCliques tri(k4,3);
    require(peel_core(tri,3)==k4.all_vertices(),"T17 triangle degree exact equality");
    require(peel_core(tri,4,&stats).empty()&&stats.cliques_invalidated==4&&stats.degree_decrements==8,"T17 each triangle invalidated once");
    const ClosureOracle oracle(tri);QueryStats query;
    const Fraction huge((BigInt(1)<<130U)+1,(BigInt(1)<<131U)+3);
    const auto answer=oracle.global_F(oracle.full_graph_request(huge),CapacityPolicy::Auto,&query,{CoreMode::Safe,FootprintMode::Membership});
    require(answer.vertices==k4.all_vertices()&&query.capacity_backend=="arbitrary_precision"&&query.core_threshold==BigInt(1),"T17 safe exact fallback executes");
    for(const auto scan:{FootprintMode::Sorted,FootprintMode::Membership}){
        const MaterializedCliques none(graph,BigInt(1)<<200U);
        const auto result=solve(none,std::nullopt,CapacityPolicy::Auto,nullptr,{}, {},{CoreMode::Safe,scan});
        require(result.solutions.size()==1&&result.solutions[0].vertices==graph.all_vertices()&&result.solutions[0].density==Fraction(0),"T17 no-clique ordinary component");
    }
}
}
int main(){try{witness();peeling();}catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
    std::cout<<"M4 T17/P08: "<<checks<<" checks passed\n";}
