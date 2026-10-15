// T21/T22/T24/T25: arbitrary-set worklists never mint chain certificates.
#include "vflhcds/solver/traversal.hpp"
#include "vflhcds/solver/solver.hpp"
#include <algorithm>
#include <iostream>
#include <numeric>
#include <set>
#include <type_traits>
using namespace vflhcds;
namespace vflhcds {
struct IntervalTestAccess {
    static CliqueRange range(const MaterializedCliques& index, std::vector<std::size_t>& ids,
                             const VertexSet& x, const VertexSet& y) {
        CliqueRange result(index, ids, 0, ids.size(), x, y);
        result.verify(); return result;
    }
    static std::size_t partition(CliqueRange& range, const VertexSet& z) { return range.partition(z); }
    static Footprints aggregate(const MaterializedCliques& index, const RestrictedRequest& request,
                                FootprintMode mode, const CliqueRange& range) {
        return ClosureOracle(index).local_footprints(request, mode, range);
    }
};
}
namespace {
std::size_t checks=0, triples=0;
void require(bool ok,const char* name){++checks;if(!ok)throw std::runtime_error(name);}
template<class E,class F> void rejects(F f){try{f();}catch(const E&){++checks;return;}throw std::runtime_error("expected rejection");}
VertexSet vertices(std::size_t n,std::size_t mask){VertexSet r;for(std::size_t v=0;v<n;++v)if(mask&(std::size_t{1}<<v))r.push_back(v);return r;}
std::vector<std::size_t> ids_for(const MaterializedCliques& index,const VertexSet& x,const VertexSet& y){
    std::vector<std::size_t> r;
    for(std::size_t i=0;i<index.cliques().size();++i)if(subset(index.cliques()[i],y)&&!subset(index.cliques()[i],x))r.push_back(i);
    return r;
}
bool same(const Footprints& a,const Footprints& b){
    if(a.total_weight!=b.total_weight||a.records.size()!=b.records.size())return false;
    for(std::size_t i=0;i<a.records.size();++i)if(a.records[i].vertices!=b.records[i].vertices||a.records[i].weight!=b.records[i].weight)return false;
    return true;
}
void nested(const Graph& graph,const BigInt& h){
    for(const auto enumeration:{CliqueEnumeration::Combinations,CliqueEnumeration::Adjacency})
    for(const auto counting:{CliqueCounting::Sorted,CliqueCounting::Membership}){
        const MaterializedCliques index(graph,h,enumeration,counting);
        // Independent tuple enumeration by vertex subsets, no production enumerator.
        std::vector<VertexSet> truth;
        const auto end=std::size_t{1}<<graph.size();
        for(std::size_t mask=0;mask<end;++mask){const auto c=vertices(graph.size(),mask);if(BigInt(c.size())!=h)continue;
            bool complete=true;for(const auto u:c)for(const auto v:c)if(u<v&&!graph.adjacent(u,v))complete=false;
            if(complete)truth.push_back(c);
        }
        auto actual=index.cliques();std::sort(actual.begin(),actual.end());std::sort(truth.begin(),truth.end());require(actual==truth,"T21 independent clique tuples");
        for(std::size_t ym=0;ym<end;++ym)for(std::size_t zm=0;zm<=ym;++zm)if((zm&ym)==zm)
        for(std::size_t xm=0;xm<=zm;++xm)if((xm&zm)==xm){
            const auto x=vertices(graph.size(),xm),z=vertices(graph.size(),zm),y=vertices(graph.size(),ym);
            auto ids=ids_for(index,x,y);const auto before=ids;
            auto range=IntervalTestAccess::range(index,ids,x,y);
            const auto middle=IntervalTestAccess::partition(range,z);
            auto left=std::vector<std::size_t>(ids.begin(),ids.begin()+static_cast<std::ptrdiff_t>(middle));
            auto right=std::vector<std::size_t>(ids.begin()+static_cast<std::ptrdiff_t>(middle),ids.end());
            std::sort(left.begin(),left.end());std::sort(right.begin(),right.end());
            require(left==ids_for(index,x,z)&&right==ids_for(index,z,y),"T21 partition complete/disjoint/crossing");
            require(index.count(z)==index.count(x)+BigInt(left.size()),"T22 exact left count");
            require(index.count(y)-index.count(x)==BigInt(before.size()),"T22 original endpoint difference");
            for(const auto mode:{FootprintMode::Sorted,FootprintMode::Membership}){
                // Every intermediate bound is tested; partitioned order must not affect weights.
                for(std::size_t bm=xm;bm<=ym;++bm)if((bm&xm)==xm&&(bm&ym)==bm){
                    const RestrictedRequest request{x,vertices(graph.size(),bm),Fraction(1)};
                    const auto local=IntervalTestAccess::aggregate(index,request,mode,range);
                    const auto global=aggregate_footprints(index,request,mode);
                    require(local.scanned==BigInt(ids.size())&&same(local,global),"T21/T24 temporary bound footprint equality");
                }
            }
            ++triples;
        }
    }
}
void exhaustive(){
    for(std::size_t n=1;n<=4;++n){std::vector<OriginalEdge> universe;std::vector<BigInt> labels;
        for(std::size_t u=0;u<n;++u){labels.push_back(u);for(std::size_t v=u+1;v<n;++v)universe.emplace_back(u,v);}
        for(std::size_t mask=0;mask<(std::size_t{1}<<universe.size());++mask){std::vector<OriginalEdge> edges;
            for(std::size_t i=0;i<universe.size();++i)if(mask&(std::size_t{1}<<i))edges.push_back(universe[i]);
            const Graph graph(labels,edges);nested(graph,2);nested(graph,3);
        }
    }
    for(std::size_t n:{std::size_t{4},std::size_t{5}}){std::vector<BigInt> labels;std::vector<OriginalEdge> edges;
        for(std::size_t u=0;u<n;++u){labels.push_back(u);for(std::size_t v=u+1;v<n;++v)edges.emplace_back(u,v);}
        nested(Graph(labels,edges),BigInt(n));
    }
}
void rejection(){
    const Graph graph({0,1,2,3},{{0,1},{0,2},{1,2},{1,3},{2,3}});const MaterializedCliques index(graph,3),foreign(graph,3);
    const VertexSet x{},y=graph.all_vertices(),z{0,1,2};std::vector<std::size_t> ids{0,1};
    auto range=IntervalTestAccess::range(index,ids,x,y);
    rejects<std::invalid_argument>([&]{(void)IntervalTestAccess::aggregate(foreign,{x,y,Fraction(1)},FootprintMode::Sorted,range);});
    for(auto bad:std::vector<std::vector<std::size_t>>{{0},{0,0},{0,2}})
        rejects<std::invalid_argument>([&]{(void)IntervalTestAccess::range(index,bad,x,y);});
    require(IntervalTestAccess::partition(range,z)==1,"T21 crossing triangle goes right");
    std::vector<std::size_t> right{ids[1]};auto residual=IntervalTestAccess::range(index,right,z,y);
    const auto footprints=IntervalTestAccess::aggregate(index,{z,y,Fraction(1)},FootprintMode::Sorted,residual);
    require(footprints.records.size()==1&&footprints.records[0].vertices==VertexSet{3},"T21 crossing singleton residual");
    static_assert(!std::is_copy_constructible_v<IntervalTraversal>);
    static_assert(!std::is_move_constructible_v<IntervalTraversal>);
}
void recovery(){
    const Graph graph({0,1,2,3,4,5,6,7},{{0,1},{0,2},{0,3},{1,2},{1,3},{2,3},{4,5},{4,6},{5,6},{4,7}});
    const MaterializedCliques index(graph,2);
    for(const auto work:{CliqueWork::Global,CliqueWork::IntervalScan,CliqueWork::IntervalReuse})
    for(const auto core:{CoreMode::Off,CoreMode::Safe})for(const auto policy:{CapacityPolicy::ForceUInt128,CapacityPolicy::ForceBig}){
        const OracleOptions options{core,FootprintMode::Membership,work};SolveStats stats;
        const auto result=solve(index,std::nullopt,policy,&stats,{}, {},options);
        require(result.solutions.size()==2&&result.solutions[1].vertices==VertexSet({4,5,6,7}),"T24 pendant restored");
        require(result.solutions[1].cliques==4&&stats.logical_interval_queries==3,"T22 exact original terminal");
        const auto prefix=solve(index,BigInt(1),policy,&stats,{}, {},options);
        require(prefix.k_reached&&stats.logical_interval_queries==2,"T25 early stop pending cleanup");
        int polls=0;rejects<Incomplete>([&]{(void)solve(index,std::nullopt,policy,&stats,{},[&]{return ++polls==4;},options);});
        rejects<std::runtime_error>([&]{(void)solve(index,std::nullopt,policy,&stats,[](const auto&,const auto&,const auto&){throw std::runtime_error("trace failure");}, {},options);});
    }
    const ClosureOracle oracle(index);IntervalTraversal walk(oracle,CliqueWork::IntervalReuse);
    QueryStats query;while(!walk.empty())(void)walk.next(CapacityPolicy::Auto,query,{});
    rejects<std::logic_error>([&]{(void)walk.next(CapacityPolicy::Auto,query,{});});
}
}
int main(){try{rejection();recovery();exhaustive();}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
    std::cout<<"T21/T22/T24/T25: "<<checks<<" checks; "<<triples<<" nested triples passed\n";}
