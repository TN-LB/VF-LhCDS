#include "vflhcds/solver/solver.hpp"
#include "vflhcds/io/solution.hpp"
#include "vflhcds/cli/dispatch.hpp"
#include <iostream>
#include <sstream>
#include <type_traits>

using namespace vflhcds;
namespace {
std::size_t checks = 0;
void require(bool value, const char* name) { ++checks; if (!value) throw std::runtime_error(name); }
template<class Error, class Function> void rejects(Function function) {
    try { function(); } catch (const Error&) { ++checks; return; }
    throw std::runtime_error("expected rejection");
}
void certificates() {
    static_assert(!std::is_default_constructible_v<ChainPoint>);
    static_assert(!std::is_constructible_v<ChainPoint, VertexSet, BigInt>);
    static_assert(!std::is_default_constructible_v<ChainInterval>);
    static_assert(!std::is_constructible_v<ChainInterval, ChainPoint, ChainPoint>);
    static_assert(!std::is_copy_assignable_v<ChainPoint>);
    static_assert(!std::is_copy_assignable_v<ChainInterval>);
    static_assert(!std::is_move_assignable_v<CertifiedGlobalRequest>);
    const Graph graph({0,1,2,3,4}, {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3},{3,4}});
    const MaterializedCliques index(graph, 2); const ClosureOracle oracle(index), other(index);
    const auto root = oracle.root_interval();
    require(root.lambda() == Fraction(7,5), "T10 original outer density");
    const auto z = oracle.separate(root);
    require(z.vertices() == VertexSet({0,1,2,3}) && z.cliques() == 6, "T10 proper separator");
    require(root.x().vertices().empty() && root.y().vertices() == graph.all_vertices(), "T10 immutable root");
    const auto right = oracle.chain_interval(z, root.y());
    require(right.lambda() == Fraction(1) && oracle.separate(right).vertices() == root.y().vertices(), "T10 consecutive terminal");
    rejects<std::invalid_argument>([&] { (void)other.separator_request(root); });
    rejects<std::invalid_argument>([&] { (void)oracle.chain_interval(root.y(), root.x()); });
    rejects<std::invalid_argument>([&] { (void)oracle.chain_interval(z,z); });
    const auto from_global = oracle.global_chain_point(Fraction(3,2));
    require(from_global.vertices() == z.vertices(), "T10 genuine global point");
    auto point_source = oracle.global_chain_point(Fraction(3,2));
    const auto point_destination = std::move(point_source);
    require(point_source.vertices() == point_destination.vertices() && point_source.cliques() == point_destination.cliques(),
            "T10 immutable token move preserves source certification");
    require(oracle.chain_interval(point_source,root.y()).lambda() == Fraction(1), "T10 moved source retains endpoint count");
    auto certificate_source = oracle.full_graph_request(Fraction(0));
    const auto certificate_destination = std::move(certificate_source);
    require(oracle.global_F(certificate_source).vertices == graph.all_vertices()
            && oracle.global_F(certificate_destination).vertices == graph.all_vertices(), "T08 moved certificate retains original bounds");
    auto interval_source = oracle.root_interval();
    const auto interval_destination = std::move(interval_source);
    require(interval_source.lambda() == interval_destination.lambda()
            && oracle.separate(interval_source).vertices() == z.vertices(), "T10 moved interval remains valid");
    const auto foreign = other.global_chain_point(Fraction(3,2));
    rejects<std::invalid_argument>([&] { (void)oracle.chain_interval(foreign,root.y()); });
    SolveStats full_stats, prefix_stats;
    std::vector<VertexSet> lefts, rights, zs;
    const auto full = solve(index, std::nullopt, CapacityPolicy::Auto, &full_stats,
        [&](const ChainInterval& interval, const ChainPoint& point, const QueryStats&) {
            lefts.push_back(interval.x().vertices()); rights.push_back(interval.y().vertices()); zs.push_back(point.vertices());
        });
    require(full.solutions.size() == 1 && full.solutions[0].vertices == z.vertices(), "T11 pendant layer emits nothing");
    require(full.solutions[0].density == Fraction(3,2), "T11 emitted density");
    require(full_stats.logical_interval_queries == 3 && full_stats.mincut_calls == 3, "T13 full 2r-1");
    require(lefts == std::vector<VertexSet>({{}, {}, z.vertices()}) && rights[1] == z.vertices() && zs[2] == graph.all_vertices(), "T11 left-first trace");
    const auto prefix = solve(index, BigInt(1), CapacityPolicy::Auto, &prefix_stats);
    require(prefix.k_reached && prefix.solutions.size() == 1 && prefix_stats.logical_interval_queries == 2,
            "T12 stop before querying non-emitting right child");
    const auto large_k = solve(index, BigInt(1)<<200U);
    require(!large_k.k_reached && large_k.solutions.size() == 1, "T12 exact oversized k exhausts");
    rejects<std::invalid_argument>([&] { (void)solve(index, BigInt(0)); });
    rejects<std::invalid_argument>([&] { (void)solve(index, BigInt(-1)); });
    SolveStats cancelled;
    bool stop = false;
    rejects<Incomplete>([&] {
        (void)solve(index, std::nullopt, CapacityPolicy::Auto, &cancelled,
            [&](const ChainInterval&, const ChainPoint&, const QueryStats&) { stop = true; }, [&] { return stop; });
    });
    require(cancelled.logical_interval_queries == 1 && cancelled.mincut_calls == 1, "T16 cancelled retains work");
}
void ties_and_zero() {
    const Graph graph({-90,-2,5,11,100}, {{-90,-2},{5,11}}); const MaterializedCliques index(graph,2);
    SolveStats all_stats, one_stats;
    const auto all = solve(index,std::nullopt,CapacityPolicy::Auto,&all_stats);
    require(all.solutions.size() == 3 && all.solutions[0].vertices == VertexSet({0,1})
            && all.solutions[1].vertices == VertexSet({2,3}) && all.solutions[2].vertices == VertexSet({4}), "T12 tie order and isolate");
    const auto one = solve(index,BigInt(1),CapacityPolicy::Auto,&one_stats);
    require(one.solutions.size()==1 && one.solutions[0].vertices == VertexSet({0,1}), "T12 do not expand tie");
    require(all_stats.logical_interval_queries == 3 && all_stats.mincut_calls == 2
            && !all_stats.queries.back().capacity_backend, "T13 zero query counts but no cut");
    const auto forced = solve(index,std::nullopt,CapacityPolicy::ForceBig);
    for (std::size_t i=0;i<all.solutions.size();++i)
        require(solution_json(index,all.solutions[i],i+1)==solution_json(index,forced.solutions[i],i+1),"T16 exact backend output equivalence");
    const MaterializedCliques absent(graph,BigInt(1)<<180U);
    SolveStats absent_stats;
    const auto zero=solve(absent,std::nullopt,CapacityPolicy::Auto,&absent_stats);
    require(zero.solutions.size()==3 && absent_stats.logical_interval_queries==1 && absent_stats.mincut_calls==0,
            "T01/T13 no cliques means original ordinary components");
    for (const auto& s:zero.solutions) require(s.density==Fraction(0) && s.cliques==0,"T12 zero results");
    const Graph bridge({0,1,2,3,4,5},{{0,1},{0,2},{1,2},{3,4},{3,5},{4,5},{2,3}});
    const MaterializedCliques triangles(bridge,3);
    require(solve(triangles).solutions.front().vertices == bridge.all_vertices(),"T11 ordinary bridge with no crossing h-clique");
}
void failure_statuses() {
    const std::vector<std::string_view> args{"solve","--graph","unused","--h","2","--all"};
    for (const int code : {5,6,7}) {
        std::ostringstream out, err;
        const auto stop=[&]() -> bool {
            if(code==5)throw ResourceLimit("test resource exhaustion");
            if(code==6)throw std::bad_alloc();
            return true;
        };
        require(run_cli(args,out,err,stop)==code && out.str().empty() && err.str().find("\"complete\":false")!=std::string::npos,
                "T16 explicit resource/oom/incomplete status");
    }
}
}
int main() {
    try { certificates(); ties_and_zero(); failure_statuses(); }
    catch(const std::exception& error) { std::cerr<<error.what()<<'\n'; return 1; }
    std::cout<<"M3 T10-T16: "<<checks<<" runtime checks passed; certificate types cannot be fabricated\n";
}
