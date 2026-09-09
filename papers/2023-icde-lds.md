# Verification-Free Approaches to Efficient Locally Densest Subgraph Discovery<sub>V1</sub> <sub>V2</sub> <sub>V3</sub> <sub>V4</sub> <sub>V5</sub> <sub>V6</sub> <sub>V7</sub> <sub>V8</sub> <sub>V9</sub> <sub>V10</sub> <sub>V12</sub> <sub>V13</sub> 2,77-compact

Tran Ba Trung Hanoi University of Science and Technology batrung97@gmail.com 

<sub>Lijun</sub> <sub>Chang</sub> The University of Sydney lijun.chang@sydney.edu.au 

Kai Yao 

The University of Sydney 

kyao8420@uni.sydney.edu.au 

Nguyen Tien Long Hanoi University of Science and Technology long.nt180129@sis.hust.edu.vn 

Huynh Thi Thanh Binh Hanoi University of Science and Technology binhht@soict.hust.edu.vn 

Abstract—Finding dense subgraphs from a large graph is a fundamental graph mining task with many applications. The notion of locally densest subgraph (LDS) is recently formulated to identify multiple dense subgraphs that cover different regions of a large graph. Informally, an LDS is a subgraph with the highest density in its local region. The state-of-the-art algorithmg<sub>1</sub> g<sub>3</sub> for computing top-k LDSes with the highest densities is LDS. It iteratively computes the densest subgraph and removes it from the graph, where all the computed densest subgraphs form the candidates of LDSes. Then, each candidate is verified through a costly maximum flow computation. Although advanced pruning techniques are proposed in LDS, the verification step is still time consuming especially for not-so-small k values. In this paper, we aim to improve the efficiency of finding top-k LDSes by designing verification-free approaches. Our algorithms are based on our observation that the set of maximal λ-compact subgraphs<sup>V1</sup> <sup>V9</sup> <sup>V101</sup> <sup>2</sup> <sup>310 16 17</sup> for all possible λ values form a hierarchical structure, and LDSes are simply leaves in the hierarchical structure. Thus,<sup>V</sup>13 <sup>V</sup>8V<sup>V</sup>13 <sup>V20V</sup>8 we propose a divide-and-conquer algorithm LDS-DC as well as an optimized algorithm LDS-Opt to efficiently identify topk LDSes without constructing the entire hierarchical structure. Both of our algorithms have lower time complexities than<sup>V7</sup> <sup>V12</sup> <sup>V11V7</sup> <sup>V6</sup> <sup>V5V11 V18V19</sup> LDS. Extensive empirical studies on real graphs show that our optimized algorithm LDS-Opt outperforms LDS for all k values, and the improvement is up-to several orders of magnitude. 

Index Terms—Locally Densest Subgraphs, Locally Dense Subgraphs, Maximal λ-compact Subgraphs 

## I. INTRODUCTION

Finding dense subgraphs from a large graph is a fundamental graph mining task [1], [2], [3]. As real-world graphs are typically globally sparse, dense subgraphs usually indicate semantically important regions of a graph. Dense subgraph mining has been used in many applications, e.g., detecting communities in social networks [4], [5], identifying stories in social media [6], spotting spam links in web graphs [7], and finding regulatory motifs in biological graphs [8]. 

A widely adopted notion of graph density is the averagedegree density. Specifically, the density of an undirected graph $g = ( V ( g ) , E ( g ) )$ , denoted $\rho ( g )$ , is measured by the ratio of its number of edges to its number of vertices which is equal to half of its average degree, i.e., $\begin{array} { r } { \rho ( g ) = \frac { | E ( g ) | } { | V ( g ) | } } \end{array}$ . Given a large graph $G = ( V , E )$ , the densest subgraph of G is the subgraph g that maximizes the density among all of $G " s$ subgraphs. The <sup>4</sup>densest subgraph of an undirected graph G with n vertices and m edges can be computed in $\begin{array} { r } { \dot { \mathcal { O } } ( n m \log \frac { n ^ { 2 } } { m } ) } \end{array}$ time through network flow techniques [9], [10]. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/ee5ce79854b7062d1932eb6435263cc645bbd7e033d37baa0d089511bab781b7.jpg)



Fig. 1: An example graph


Reporting only a single densest subgraph however is often not sufficient for applications, as it covers only one region of a large input graph. In view of this, Qin et al. [11] recently formulated the notion of locally densest subgraph (LDS) aiming to find multiple dense subgraphs that cover different regions of a large graph. It is defined based on the notion of (maximal) λ-compact subgraphs. A graph is λ-compact if (1) it is connected and (2) removing any subset S of vertices and their associated edges from it will result in the removal <sup>5 V26</sup>of at least λ S edges. A subgraph of G is a maximal λ- compact subgraph of G if it is the largest subgraph that is λ-compact. LDSes are those maximal λ-compact subgraphs for λ being equal to the density, i.e., a subgraph g of G is an LDS if it is a maximal $\rho ( g )$ )-compact subgraph of G. The definition of LDS is parameter-free, and has the following elegant properties: (1) any subgraph of an LDS is not denser than itself, and (2) any proper supergraph of an LDS is not as compact as itself. Intuitively, an LDS is a subgraph with the highest density in its local region. Note that LDSes are vertexinduced subgraphs and are disjoint. For the graph in Figure 1, g<sub>1</sub> and $g _ { 3 }$ are the only two LDSes, which are representative for the two dense regions of the graph. 

The state-of-the-art algorithm for computing top-k LDSes with the highest densities is LDS proposed in [11], whose time complexity is $\mathcal { O } ( m ^ { 2 } n \log ^ { 2 } n )$ . The general idea is iteratively computing the densest subgraph and removing it from the graph; note that, as the graph keeps shrinking, the computed densest subgraphs are not necessarily the densest in the input graph $G .$ It is proved in [11] that connected components of all the computed densest subgraphs are the candidates of LDSes. For each candidate $g$ (i.e., connected component of the computed densest subgraphs), it verifies whether $g$ is indeed an LDS: g is an LDS if it is a connected component of $F ( \lambda )$ for $\lambda = \rho ( g )$ . This is based on the fact that the set of connected components of $F ( \lambda )$ is the set of all maximal λ-compact subgraphs in $G .$ . Here, $F ( \lambda )$ is defined as the subgraph (or vertex subset) $S$ that maximizes $| E ( S ) | - \lambda | S |$ where tie is broken by taking the largest vertex subset and $E ( S )$ denotes the set of edges of $G$ with both end-points in $S ; F ( \lambda )$ can be computed via network flow [11]. Consider the graph in Figure 1, $g _ { 1 }$ is the densest subgraph in the input graph and $g _ { 1 }$ is also an LDS. After removing $g _ { 1 }$ from the graph, $g _ { 2 }$ becomes the densest subgraph; however, $g _ { 2 }$ is not an LDS since $g _ { 1 } \cup g _ { 2 }$ is maximal $\rho ( g _ { 2 } )$ -compact. After further removing $g _ { 2 }$ from the graph, $g _ { 3 }$ becomes the densest subgraph and is an LDS. Pruning techniques are also proposed in [11] to improve the efficiency of LDS. Firstly, vertices that are guaranteed to be not in any LDS are removed from the graph; this speeds up the computation of densest subgraphs. Secondly, for verification, $F ( \lambda )$ is computed on the λ -core of G instead of on the entire graph $G ,$ where l-core is the largest subgraph of $G$ whose minimum degree is at least l. For large λ values, the λ -core is small and thus verification is relatively efficient. However, for small λ values, the λ -core remains large, which makes verification expensive. As a result, LDS becomes inefficient when it needs to verify candidates with relatively low density. 

In this paper, we propose verification-free approaches for efficiently computing top-k LDSes. Instead of first generating densest subgraphs and then verifying them through computing F(λ) on G, we compute maximal λ-compact subgraphs and obtain LDSes from them. This is based on our observation that the set of LDSes is a subset of all maximal λ-compact subgraphs for all possible λ values. To eliminate the need of expensive verification, we prove that (1) a maximal λ-compact subgraph is an LDS if and only if it does not contain any other maximal λ<sup>′</sup>-compact subgraph as a proper subgraph, and (2) the set of maximal λ-compact subgraphs for all possible λ values form a hierarchical structure; consequently, LDSes are simply leaves in the hierarchical structure. To efficiently construct the hierarchical structure, we prove that maximal λ-compact subgraphs are the same as connected components of locally dense subgraphs that are computed in [12].<sup>1</sup> However, directly invoking the algorithm of [12] to construct the hierarchical structure and then reporting the leaves as LDSes is inefficient for finding top-k LDSes. In view of this, we propose a divide-and-conquer algorithm LDS-DC by following the general idea of [12] while integrating top-k LDSes identification into the process such that we can stop as soon as k LDSes have been identified. We prove that the identified k LDSes have the highest densities, and that the time complexity of LDS-DC is $\mathcal { O } ( n ^ { 2 } m )$ . Our empirical studies show that LDS-DC runs much faster than LDS for relatively large k values $( \mathrm { e } . \mathrm { g } . , k \geq 2 0 )$ , but may be outperformed by LDS when k is smaller. To resolve the inefficiency of LDS-DC for very small k values, we further propose an optimized approach LDS-Opt which consistently outperforms LDS-DC, especially for small k values. 

Our main contributions are summarized as follows: 

• We are the first to demonstrate the relationship between LDSes and locally dense subgraphs. 

• We propose a verification-free algorithm LDS-DC that has a lower time complexity than the state of the art for finding top-k LDSes. 

• We further propose an optimized algorithm LDS-Opt which is suitable for finding top-k LDSes for all k values. 

• We conduct extensive experiments on real graphs to demonstrate the efficiency of our verification-free algorithms. The results show that LDS-DC outperforms the state-of-the-art algorithm LDS for $k \ \geq \ 2 0$ , while LDS-Opt outperforms LDS for all k values. 

The remainder of the paper is organized as follows. Section II defines the problem and presents preliminaries. We briefly review the state-of-the-art algorithm LDS and discuss its inefficiency in Section III. We formally characterize LDSes from maximal λ-compact subgraphs in Section IV, and propose two verification-free algorithms LDS-DC and LDS-Opt in Section V. The results of our empirical studies are presented in Section VI, and related works are discussed in Section VII. Finally, Section VIII concludes the paper. 

## II. PRELIMINARIES

In this paper, we consider an unweighted and undirected graph $G = ( V , E )$ with $n = | V ( G ) |$ vertices and $m = | E ( G ) |$ undirected edges. For each vertex $v \in V$ , we use $N _ { G } ( v ) =$ $\{ u \in V \mid ( v , u ) \in E \}$ to denote the set of neighbors of v in G. The degree of v in G is denoted $d _ { G } ( v ) = | N _ { G } ( v ) |$ . Given a vertex subset $X \subseteq V .$ , we use $E _ { G } ( X )$ to denote the set of edges of G whose both end-points are in X, i.e., $E _ { G } ( X ) =$ $\{ ( u , v ) \in E \mid u , v \in X \}$ . The subgraph of G induced by X is denoted by $G [ X ] , \mathrm { i . e . , } G [ X ] = ( X , E _ { G } ( X ) )$ . When the context is clear, we omit the subscript G from the notations. 

Given an arbitrary graph g, we use $V ( g )$ and $E ( g )$ , respectively, to denote its vertex set and its edge set. The density of $^ { g , }$ denoted $\rho ( g )$ , is defined as half of its average degree, i.e., 

$$
\rho (g) = \frac {| E (g) |}{| V (g) |}
$$

Definition II.1 (λ-compact [11]). Given a graph g and a positive value $\lambda , \ g$ is λ-compact $i f \left( I \right)$ it is connected, and (2) removing any subset S of vertices and their associated edges from it will result in the removal of at least λ S edges. 

It is easy to see that any λ-compact graph is also λ<sup>′</sup>-compact for any $\lambda ^ { \prime } < \lambda$ . A subgraph g of G is a maximal λ-compact subgraph of G if every proper supergraph of g in G is not λ- compact. The concept of locally densest subgraph is defined based on maximal λ-compact subgraph, as follows. 

Definition II.2 (Locally Densest Subgraph (LDS) [11]). A subgraph g of G is a locally densest subgraph $i f g$ is a maximal $\rho ( g )$ -compact subgraph in G. 

LDSes of a graph satisfy the following properties [11]: 

• The density of any subgraph of an LDS g is at most $\rho ( g )$ i.e., any subgraph of an LDS is not denser than itself. 

• Any proper supergraph of an LDS g is not $\rho ( g )$ -compact, i.e., any proper supergraph of an LDS is not as compact as itself. 

• LDSes are disjoint, i.e., $V ( g ) \cap V ( g ^ { \prime } ) = \emptyset$ for any two distinct LDSes g and $g ^ { \prime }$ 

It is easy to see from the definition that both a maximal λ- compact subgraph of G and an LDS of G are vertex-induced subgraphs of G. For presentation simplicity, we also use a vertex subset to refer to the corresponding vertex-induced subgraph. 

Example II.1. Consider the graph in Figure 1. g<sub>1</sub> is the subgraph induced by vertices $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 8 } \}$ which consists of 8 vertices and 24 undirected edges. Thus, the density of $g _ { 1 }$ is $\textstyle \rho ( g _ { 1 } ) = { \frac { 2 4 } { 8 } } = 3 .$ g<sub>1</sub> is an LDS since itself is a maximal 3-compact subgraph. 

g<sub>2</sub> is the subgraph induced by vertices $\{ v _ { 9 } , v _ { 1 0 } , \ldots , v _ { 1 3 } \}$ which consists of 5 vertices and 10 undirected edges. Thus, the density of g<sub>2</sub> is $\rho ( g _ { 2 } ) = 2 .$ . Although g<sub>2</sub> does not have any subgraph that is denser than itself, g is not an LDS. This is because $g _ { 2 }$ is not a maximal 2-compact subgraph; instead, its proper supergraph $g _ { 1 } \cup g _ { 2 }$ is a maximal 2-compact subgraph. 

g is the subgraph induced by vertices $\{ v _ { 1 6 } , v _ { 1 7 } , \ldots , v _ { 2 0 } \}$ consisting of 5 vertices and 8 undirected edges. Its density is $\textstyle \rho ( g _ { 3 } ) = { \frac { 8 } { 5 } } . \ g _ { 3 }$ is an LDS, since itself is a maximal ${ \frac { 8 } { 5 } } - c o m p a c t$ subgraph. 

Problem Statement. Given an unweighted and undirected graph G and an integer k, we study the problem of finding the k LDSes of G that have the highest densities. 

Frequently used notations are summarized in Table I. 

## A. Locally Dense Subgraphs

We will show in Section V-A that LDSes are closely related to locally dense subgraphs defined in [12]. Thus, in this subsection, we briefly review the definition and properties of locally dense subgraph. Note that, to avoid confusion of the concept of locally densest subgraph defined in [11] and the concept of locally dense subgraph defined in [12], we always use the abbreviation LDS to refer to locally densest subgraph while do not abbreviate locally dense subgraph in this paper. 


TABLE I: Frequently used notations


<table><tr><td>Notation</td><td>Meaning</td></tr><tr><td><eq>G = (V, E)</eq></td><td>A graph <eq>G</eq> with vertex set <eq>V</eq> and edge set <eq>E</eq></td></tr><tr><td><eq>X, Y, Z, S, U, W</eq></td><td>Vertex subsets of <eq>V</eq></td></tr><tr><td><eq>E(X)</eq></td><td>The set of edges of <eq>G</eq> whose both end-points are in <eq>X</eq>, i.e., <eq>E(X) = \{(u, v) \in E \mid u, v \in X\}</eq></td></tr><tr><td><eq>G[X]</eq></td><td>The subgraph of <eq>G</eq> induced by vertex subset <eq>X</eq>, i.e., <eq>G[X] = (X, E(X))</eq></td></tr><tr><td><eq>\rho(g)</eq></td><td>The density of graph <eq>g = (V(g), E(g))</eq>, i.e., <eq>\rho(g) = \frac{|E(g)|}{|V(g)|}</eq></td></tr><tr><td><eq>E(X, Y)</eq></td><td>The cross edges between disjoint vertex set <eq>X</eq> and <eq>Y</eq>, i.e., <eq>E(X, Y) = \{(u, v) \in E \mid u \in X, v \in Y\}</eq></td></tr><tr><td><eq>\rho(X, Y)</eq></td><td>The outer density of <eq>X</eq> with respect to <eq>Y</eq>, i.e., <eq>\rho(X, Y) = \frac{|E(X)| + |E(X, Y)|}{|X|}</eq> for disjoint vertex sets <eq>X</eq> and <eq>Y</eq>; <eq>\rho(X, Y) = \rho(X \setminus Y, Y)</eq> otherwise</td></tr><tr><td><eq>B_0, B_1, \ldots, B_r</eq></td><td>Locally dense subgraphs</td></tr><tr><td><eq>F(\lambda)</eq></td><td>The vertex subset <eq>S</eq> that maximizes <eq>|E(S)| - \lambda |S|</eq>, i.e., <eq>F(\lambda) = \argmax_{S \subseteq V} |E(S)| - \lambda |S|</eq></td></tr></table>

Firstly, we need the definition of outer density. Given a graph $G \ : = \ : ( V , E )$ and two disjoint vertex subsets X and Y of V, the outer density of X with respect to Y, denoted $\rho ( X , Y )$ , is defined as 

$$
\rho (X, Y) = \frac {| E (X) | + | E (X , Y) |}{| X |}
$$

where $E ( X , Y ) ~ = ~ \{ ( u , v ) ~ \in ~ E ~ | ~ u ~ \in ~ X , v ~ \in ~ Y \}$ denotes the set of cross edges between X and Y. Note that, $\rho ( X , \emptyset ) = \rho ( X )$ and $\rho ( \emptyset , X ) = 0$ . In the case that X and Y are overlapping, the outer density will be expanded as: 

$$
\rho (X, Y) = \rho (X \setminus Y, Y)
$$

Locally dense subgraph is defined based on the notion of outer density as follows. 

Definition II.3 (Locally Dense Subgraph [12]). Given a graph $G \ = \ ( V , E )$ , a vertex subset $W \subseteq V$ is a locally dense subgraph if there are no $X \subseteq W$ and $Y \subseteq V \setminus \left. \begin{array} { l } { V } \end{array} \right\downarrow$ W such that $\rho ( X , W \setminus X ) \leq \rho ( Y , W )$ 

It is shown in [12] that locally dense subgraphs are nested, i.e., for any two locally dense subgraphs U and $W ,$ either $U \subseteq W \ \mathrm { o r } \ W \subseteq U$ . Thus, the set of locally dense subgraphs can be arranged into a sequence 

$$
\emptyset = B _ {0} \subsetneq B _ {1} \subsetneq \dots \subsetneq B _ {r} = V
$$

where $r \leq n .$ . Moreover, it satisfies the property that 

$$
\rho (B _ {i}, B _ {i - 1}) > \rho (B _ {i + 1}, B _ {i}), \text {   for   } 0 <   i <   r.
$$

Example II.2. Consider the graph in Figure 1, there are five non-empty locally dense subgraphs. $B _ { 1 } \ = \ \{ v _ { 1 } , v _ { 2 } , . . . , v _ { 8 } \}$ $B _ { 2 } = B _ { 1 } \cup \{ v _ { 9 } , v _ { 1 0 } , \dotsc , v _ { 1 3 } \} , B _ { 3 } = B _ { 2 } \cup \{ v _ { 1 6 } , v _ { 1 7 } , \dotsc , v _ { 2 0 } \}$ $B _ { 4 } = B _ { 3 } \cup \{ v _ { 1 4 } , v _ { 1 5 } \}$ , and $B _ { 5 } = V . \rho ( B _ { 1 } , \emptyset ) = \rho ( B _ { 1 } ) =$ 3, $\rho ( B _ { 2 } , B _ { 1 } ) = { \textstyle \frac { 1 2 } { 5 } } , \rho ( B _ { 3 } , B _ { 2 } ) = { \textstyle \frac { 8 } { 5 } } , \rho ( B _ { 4 } , B _ { 3 } ) = { \textstyle \frac { 3 } { 2 } }$ , and $\rho ( B _ { 5 } , B _ { 4 } ) = 1 .$ 

## III. INEFFICIENCY OF THE STATE-OF-THE-ART APPROACH

The state-of-the-art approach for computing top-k LDSes is LDS proposed in [11]. The general idea of LDS is based on the following two lemmas. 

Lemma III.1. [11] Any densest subgraph component of $G$ is an LDS of $G ,$ where a densest subgraph component is a connected component of the densest subgraph. 

Lemma III.2. [11] Let g be an LDS of G. Any LDS g $( g ^ { \prime } \neq g )$ in $G$ is still an LDS in $G ^ { \prime }$ where $G ^ { \prime }$ is the residual graph of G after removing $g .$ 

Thus, LDS iteratively computes the densest subgraph of $G ^ { \prime }$ which is initialized as $G ,$ and removes the densest subgraph from $G ^ { \prime }$ , until top-k LDSes have been obtained or $G ^ { \prime }$ becomes empty. For each connected component $g$ of the computed densest subgraphs, it verifies whether $g$ is an LDS based on the following lemma, which says that g is an LDS if it is a connected component of $F ( \lambda )$ for $\lambda = \rho ( g )$ . Here, $F ( \lambda )$ is defined as the subgraph (or vertex subset) S that maximizes $| E ( S ) | - \lambda | S |$ where tie is broken by taking the largest vertex subset, i.e., $F ( \lambda ) = \operatorname { a r g m a x } _ { S \subseteq V } | E ( S ) | - \lambda | S |$ 

Lemma III.3. [11] If G contains maximal λ-compact subgraphs, then the set of connected components of $F ( \lambda ) \ =$ argmax $_ { \cdot S \subseteq V } | E ( S ) | - \lambda | S |$ is the set of all maximal λ-compact subgraphs in G. 

Algorithm 1: LDS [11]

Input: A graph $G = (V, E)$ and an integer $k$ Output: Top- $k$ LDSes $\mathcal{R}$ 1 $G' \leftarrow \text{prune}(G)$ ;
2 Initialize a priority queue $\mathcal{H} \leftarrow \emptyset$ ;
3 for each connected component $g$ of $G'$ do
4 $\mathcal{H}.push(g, \bar{\rho}^*(g), \text{false})$ ;
5 $\mathcal{R} \leftarrow \emptyset$ ;
6 while $\mathcal{H} \neq \emptyset$ and $|\mathcal{R}| < k$ do
7 $(g, ub, \text{densest}) \leftarrow \mathcal{H}.pop()$ ;
8 if densest = true then
9 if verify( $g, G$ ) then $\mathcal{R} \leftarrow \mathcal{R} \cup \{g\}$ ;
10 else
11 $g' \leftarrow \text{any connected component of the densest subgraph of } g$ ;
12 $\mathcal{H}.push(g', \rho(g'), \text{true})$ ;
13 $G' \leftarrow \text{the residual graph of } g \text{ after removing } g'$ ;
14 $G' \leftarrow \text{prune}(G')$ ;
15 for each connected component $g$ of $G'$ do
16 $\mathcal{H}.push(g, \bar{\rho}^*(g), \text{false})$ ;

17 return $\mathcal{R}$ ; 

The pseudocode of LDS is shown in Algorithm 1. For time efficiency consideration, it processes the graph in a component-by-component manner where the connected components are stored in a priority queue (Lines 3–4 and 15– 16), and conducts vertex pruning by removing from the graph all vertices that are guaranteed to be not in any LDS (Lines 1 and 14). Specifically, stores both connected components and densest subgraph components, which are distinguished via the third element $( \mathrm { i . e . }$ , densest) of each entry; that is, densest = true means that this entry stores a densest subgraph component (Line 8). The priority of a component $g$ in is an upper bound of the densest subgraph in g, denoted $\bar { \rho } ^ { * } ( g )$ (Lines 4 and 16); if $g$ itself is a densest subgraph component, then the upper bound is defined as $\rho ( g )$ 

LDS works as follows. It initially puts all the connected components of the pruned graph $G ^ { \prime }$ into the priority queue (Lines 2–4). Then, it iteratively computes the next LDS that has the highest density (Lines 6–16). To do so, it pops from the component $g$ that has the highest upper bound (Line 7). If g is a densest subgraph component (Line $^ { 8 ) }$ , it verifies whether $g$ is an LDS by calling ${ \mathsf { v e r i f y } } ( g , G )$ (Line 9); note that, if $g$ is an LDS, then due to the nature of $\mathcal { H } , g$ is guaranteed to be the next LDS that has the highest density. Otherwise, $g$ is not a densest subgraph component (Line 10), it computes the densest subgraph in $^ { g , }$ and let $g ^ { \prime }$ be any connected component of this densest subgraph (Line 11). Then, it inserts into the densest subgraph component $g ^ { \prime }$ (Line 12), as well as the connected components of the residual graph of $g$ after removing $g ^ { \prime }$ and conducting vertex pruning (Lines 13–16). 

Inefficiency of LDS. Despite that LDS incorporates several advanced pruning techniques, it is still inefficient in the following two aspects. Firstly, to compute the densest subgraph of $^ { g , }$ it needs to compute $F ( \lambda )$ on $g$ for multiple λ values by binary searching on λ [10]. Secondly, to verify whether g is truely an LDS, it needs to compute $F ( \lambda )$ on $G$ for $\lambda = \rho ( g )$ The inefficiency of LDS becomes severer when there are many false-positives (i.e., we need to conduct the above computation for many more subgraphs $g ) ,$ and/or when λ is small which is the case when k becomes large. 

We remark that verifying whether $g$ is an LDS becomes extremely time consuming when $\rho ( g )$ is small, as it needs to compute $F ( \lambda )$ on G for a small value $\lambda = \rho ( g )$ . It is proved in [11] that when computing $F ( \lambda )$ on G, we only need to work on the λ -core of G, where the l-core of $G$ is the largest subgraph of $G$ whose minimum degree is at least $l ;$ this is intuitive, since the minimum degree of a λ-compact subgraph must be at least λ. For large λ values, the $\left\lceil \lambda \right\rceil$ -core of $G$ is small and thus the computation of $F ( \lambda )$ is relatively efficient. However, for small λ values, the λ -core of $G$ is large, which makes the computation of $F ( \lambda )$ time consuming. This motivates us to design verification-free approaches for computing LDSes in Section V. 

## IV. CHARACTERIZING LDSES FROM MAXIMAL λ-COMPACT SUBGRAPHS

According to Definition II.2, an LDS of $G$ must be a maximal λ-compact subgraph of G for some λ. Thus, the set of all LDSes of G is a subset of all maximal λ-compact subgraphs of G for all possible λ values. In this section, we characterize LDSes from maximal λ-compact subgraphs, which will enable us to design efficient algorithms to explore all LDSes in the next section. In the following, we first in Section IV-A prove the condition for a maximal λ-compact subgraph to be an LDS, then in Section IV-B prove the hierarchical structure of all maximal λ-compact subgraphs for all possible λ-values, and finally in Section IV-C show that LDSes are simply leaves of the hierarchical structure. 

A. Condition for a Maximal λ-Compact Subgraph to be an LDS 

To prove the condition for a maximal λ-compact subgraph to be an LDS, we first define the notion of compactness of a graph and build the connection between compactness and the density. 

Definition IV.1 (Compactness). The compactness of a connected graph $^ { g , }$ denoted $\eta ( g )$ , is the largest λ such that $g$ is λ-compact. The compactness of a disconnected graph is defined to be 0. 

Lemma IV.1. For any connected graph g, $\eta ( g ) \leq \rho ( g )$ 

Proof. According to the definition of compactness, $g$ is $\eta ( g ) .$ compact. Thus, $| E ( g ) | \geq \eta ( g ) \times | V ( g )$ since the set of vertices to be removed can be $V ( g )$ , and consequently $\begin{array} { r } { \rho ( g ) = \frac { | E ( g ) | } { | V ( g ) | } \geq } \end{array}$ $\eta ( g )$ □ 

Lemma IV.2. For any connected graph $g , \eta ( g ) < \rho ( g )$ if and only if there is a subgraph g<sup>′</sup> of g such that $\rho ( g ^ { \prime } ) > \rho ( g )$ 

Proof. $( \implies ) \mathrm { I f } \ \eta ( g ) < \rho ( g )$ , then there is a vertex subset S of $g$ whose removal from $g$ will result in the removal of less than $\rho ( g ) \times | S |$ edges. Let $g ^ { \prime }$ be the resulting graph of $g$ obtained by removing vertices of S and their associated edges. Then $| \dot { E } ( g ^ { \prime } ) | > | \dot { E } ( g ) | - \rho ( g ) \times | S | = _ { , } \rho ( g ) \times ( | V ( g ) | - | S | ) =$ $\rho ( g ) \times | V ( g ^ { \prime } ) |$ . Thus, $\begin{array} { r } { \rho ( g ^ { \prime } ) = \frac { | E ( g ^ { \prime } ) | } { | V ( g ^ { \prime } ) | } > \rho ( g ) } \end{array}$ 

( =) If there is a subgraph $\dot { g } ^ { \prime }$ of g such that $\rho ( g ^ { \prime } ) > \rho ( g )$ then we also have $\rho ( g ^ { \prime \prime } ) > \rho ( g )$ where $g ^ { \prime \prime }$ denotes the subgraph of $g$ induced by $V ( g ^ { \prime } )$ . Let S be $V ( g ) \setminus V ( g ^ { \prime \prime } )$ Then, removing S from $g$ will result in the removal of $| E ( g ) | - | E ( g ^ { \prime \prime } )$ edges. Note that, $| E ( g ) | = \rho ( g ) \times | V ( g )$ | <sup>and</sup> $| E ( g ^ { \prime \prime } ) | = \rho ( g ^ { \prime \prime } ) \times | V ( g ^ { \prime \prime } ) | > \rho ( g ) \times | V ( g ^ { \prime \prime } ) |$ . Thus, $| E ( g ) | -$ $| E ( g ^ { \prime \prime } ) | < \rho ( g ) \times ( | V ( g ) | - | V ( g ^ { \prime \prime } ) | ) = \rho ( g ) \times | S |$ . Consequently, g cannot be $\rho ( g ) { \mathrm { - c o m p a c t . } }$ , and $\eta ( g ) < \rho ( g )$ □ 

Corollary IV.1. For any connected graph g, $\eta ( g ) = \rho ( g )$ if and only if the density of every subgraph of g is at most $\rho ( g )$ 

Proof. This directly follows from Lemma IV.2. 

□ 

Now, we are ready to prove the condition for a maximal λ-compact subgraph of G to be an LDS of G. 

Lemma IV.3. For any maximal λ-compact subgraph g of G, g is an LDS if and only if g contains no λ<sup>′</sup>-compact subgraph for $\lambda ^ { \prime } > \eta ( g )$ 

Proof. First, we prove by contradiction that if $g$ is an LDS, then g contains no $\lambda ^ { \prime } .$ -compact subgraph for $\lambda ^ { \prime } ~ > ~ \eta ( g )$ Suppose there is such a subgraph $g ^ { \prime }$ of $g$ that is λ<sup>′</sup>-compact for $\lambda ^ { \prime } > \eta ( g ) , \mathrm { i . e . , } \eta ( g ^ { \prime } ) > \eta ( g )$ . As $g$ is an LDS, from Definition II.2 and Lemma IV.1, we have $\eta ( g ) = \rho ( g )$ ; thus $\eta ( g ^ { \prime } ) > \rho ( g )$ . From Lemma IV.1, we know that $\rho ( g ^ { \prime } ) \ge \eta ( g ^ { \prime } )$ 

Thus $\rho ( g ^ { \prime } ) > \rho ( g )$ , which implies that $\eta ( g ) < \rho ( g )$ following Lemma IV.2; contradiction. Thus, g contains no λ<sup>′</sup>-compact subgraph for $\lambda ^ { \prime } > \eta ( g )$ 

Second, we prove that if $g$ is not an LDS, then $g$ must have a λ<sup>′</sup>-compact subgraph for $\lambda ^ { \prime } > \eta ( g )$ . Since $g$ is not an LDS, we have $\eta ( g ) < \rho ( g )$ according to Definition II.2 and Lemma IV.1. Then, from Lemma IV.2 we know that $g$ must have a subgraph $g ^ { \prime }$ such that $\rho ( g ^ { \prime } ) > \rho ( g )$ . Let $g ^ { \prime \prime }$ be the densest subgraph of $^ { g ; }$ note that, $\rho ( g ^ { \prime \prime } ) \ge \rho ( g ^ { \prime } ) > \rho ( g )$ From Corollary IV.1, we have $\eta ( g ^ { \prime \prime } ) = \rho ( g ^ { \prime \prime } )$ . Consequently, $\eta ( g ^ { \prime \prime } ) > \rho ( g ) > \eta ( g )$ 

Now, the lemma follows. 

## B. Hierarchical Structure of Maximal λ-Compact Subgraphs

In this subsection, we prove that the set of maximal $\lambda -$ compact subgraphs of $G$ for all possible λ-values form a hierarchical structure. 

We first prove in the lemma below that the union of two overlapping or adjacent λ-compact subgraphs is still λ- compact. For presentation simplicity, we only consider vertexinduced subgraphs since all maximal λ-compact subgraphs are vertex-induced subgraphs. 

Lemma IV.4. Given a graph G and two λ-compact subgraphs X and Y of G, $i f X \cap Y \neq \emptyset$ or $E ( X , Y ) \neq \emptyset ;$ , then $X \cup Y$ is also λ-compact. 

Proof. Firstly, we consider the case of $X \cap Y \neq \emptyset$ . Then, $G [ X \cup Y ]$ is connected. Let’s consider an arbitrary subset $S \subseteq$ $X \cup Y$ . Let $S _ { X } = S \cap ( X \setminus Y )$ and $S _ { Y } = S \cap Y ;$ then, $S _ { X } \cap S _ { Y } = \emptyset$ and $S _ { X } \cup S _ { Y } = S$ . Let $\bar { S }$ be $( X \cup Y ) \setminus S .$ If we remove S from $X \cup Y$ , then the set of edges that will be removed is $E ( S ) \cup E ( S , { \bar { S } } )$ . We have 

$$
\begin{array}{l} | E (S) \cup E (S, \bar {S}) | \\ = | E (S) | + | E (S, \bar {S}) | \\ = | E (S _ {X} \cup S _ {Y}) | + | E (S _ {X} \cup S _ {Y}, \bar {S}) | \\ = | E (S _ {X}) \cup E (S _ {X}, S _ {Y}) \cup E (S _ {Y}) | + | E (S _ {X}, \bar {S}) \cup E (S _ {Y}, \bar {S}) | \\ = \big (| E (S _ {X}) | + | E (S _ {X}, S _ {Y}) | + | E (S _ {X}, \bar {S}) | \big) + \\ \big (| E (S _ {Y}) | + | E (S _ {Y}, \bar {S}) | \big) \\ \geq \big (| E (S _ {X}) | + | E (S _ {X}, S _ {Y} \cap X) | + | E (S _ {X}, \bar {S} \cap X) | \big) + \\ \big (| E (S _ {Y}) | + | E (S _ {Y}, \bar {S} \cap Y) | \big) \\ = (| E (S _ {X}) | + | E (S _ {X}, X \setminus S _ {X}) |) + \\ (| E (S _ {Y}) | + | E (S _ {Y}, Y \setminus S _ {Y}) |) \end{array}
$$

where the last equality follows from the fact that $S _ { X } \cup S _ { Y } \cup$ ${ \bar { S } } = X \cup Y . { \mathrm { ~ A s } }$ both X and Y are λ-compact, it follows that $| E ( S _ { X } ) | + | E ( S _ { X } , X \setminus S _ { X } ) | \ge \lambda \times | S _ { X } |$ and $\vert E ( S _ { Y } ) \vert +$ $| E ( \bar { S } _ { Y } , Y \setminus \bar { S } _ { Y } ) | \geq \lambda \times | S _ { Y } |$ . Thus, $| E ( S ) \cup E ( S , { \bar { S } } ) | \ \geq$ $\lambda \times ( | S _ { X } | + | S _ { Y } | ) = \lambda \times | S |$ . Consequently, X Y is $\lambda -$ compact. 

Secondly, we consider the case of $X \cap Y \ = \varnothing$ and $E ( X , Y ) ~ \neq ~ \emptyset$ . Then, $G [ X \cup Y ]$ is connected. By using a similar argument as above, $| E ( S ) \bar { \cup } E ( S , \bar { S } ) | \geq \lambda | S |$ holds for any subset $S \subseteq X \cup Y$ , and thus $X \cup Y$ is λ-compact. 

Now, we prove the hierarchical structure of maximal $\lambda -$ compact subgraphs for all possible λ values in the following lemma. 

Lemma IV.5. Given a graph G, any two distinct maximal λ- compact subgraphs X and Y are disjoint (i.e., $X \cap Y = \emptyset$ and $E ( X , Y ) = \emptyset )$ . For any maximal λ-compact subgraph X and any maximal $\lambda ^ { \prime } .$ -compact subgraph $X ^ { \prime }$ with $\lambda > \lambda ^ { \prime } ,$ , either $X \subseteq X ^ { \prime }$ , or X and $X ^ { \prime }$ are disjoint (i.e., $X \cap X ^ { \prime } = \emptyset$ and $E ( X , X ^ { \prime } ) = \varnothing )$ 

Proof. The disjointness of X and Y directly follows from Lemma IV.4. We prove the relationship between X and $X ^ { \prime }$ by contradiction. Suppose that $X \not \subseteq X ^ { \prime }$ , and either $X \cap X ^ { \prime } \neq \emptyset$ or $E ( X , X ^ { \prime } ) ~ \neq ~ \varnothing$ . Then, from Lemma IV.4, we know that $X \cup X ^ { \prime }$ , which is not the same as $X ^ { \prime } ,$ , is also λ<sup>′</sup>-compact since X is λ<sup>′</sup>-compact for $\lambda ^ { \prime } < \lambda ;$ this contradicts that $X ^ { \prime }$ is a maximal λ<sup>′</sup>-compact subgraph. □ 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/b0f91098ee7471a870756f15bdd53b437aec6aa34cd9f2abb83e54c695c75c66.jpg)



Fig. 2: An example of hierarchical structure of all maximal λ-compact subgraphs


For example, Figure 2 illustrates the hierarchical structure of all maximal λ-compact subgraphs for all possible λ values for the graph in Figure 1. Note that, $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \}$ is both $\frac { 1 2 } { 5 }$ -compact and ${ \frac { 8 } { 5 } } \cdot$ -compact; we only show it as $\frac { 1 2 } { 5 }$ -compact in the figure, since $\frac { 1 2 } { 5 }$ is its compactness. 

## C. Put It Together

Now, we are ready to characterize LDSes in the hierarchical structure of all maximal λ-compact subgraphs for all possible λ values. 

Theorem IV.6. For any maximal λ-compact subgraph $g o f G ,$ g is an LDS if and only if g contains no maximal λ<sup>′</sup>-compact subgraph as a proper subgraph for any λ<sup>′</sup>. 

Proof. From Lemma IV.3, we know that $g$ is an LDS if and only if it contains no λ<sup>′</sup>-compact subgraph for $\lambda ^ { \prime } > \eta ( g )$ . As $g$ is a maximal λ-compact subgraph, from Lemma IV.5 we know that for $\lambda ^ { \prime } > \eta ( g ) , g$ contains a $\lambda ^ { \prime } .$ -compact subgraph if and only if $g$ contains a maximal $\lambda ^ { \prime } .$ -compact subgraph. Thus, $g$ is an LDS if and only if it contains no maximal $\lambda ^ { \prime } .$ -compact subgraph for $\lambda ^ { \prime } > \eta ( g )$ ; note that, any maximal $\lambda ^ { \prime } .$ -compact subgraph for $\lambda ^ { \prime } > \eta ( g )$ must be a proper subgraph of $g$ since $g$ is not $\lambda ^ { \prime } { \mathrm { - c o m p a c t . } }$ On the other hand, for $\lambda ^ { \prime } \leq \eta ( g )$ , it is trivial that any proper subgraph of $g$ is not a maximal λ<sup>′</sup>-compact subgraph. Thus, the theorem holds. □ 

It is worth pointing out that Theorem IV.6 is different from Lemma IV.3. Specifically, Theorem IV.6 specifies that g contains no maximal $\lambda ^ { \prime } .$ -compact subgraph, while Lemma IV.3 does not enforce maximality. It is from Theorem IV.6 that we can design verification-free approaches for computing LDSes. 

From Theorem IV.6, we can conclude that the leaves of the hierarchical structure of all maximal λ-compact subgraphs for all possible λ values are exactly the LDSes. Thus, from Figure 2, we can see that $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 8 } \}$ and $\{ v _ { 1 6 } , v _ { 1 7 } , \ldots , v _ { 2 0 } \}$ are the two LDSes. 

## V. VERIFICATION-FREE APPROACHES

In this section, we design verification-free approaches for efficiently computing LDSes by following Theorem IV.6. We first propose a divide-and-conquer approach in Section V-A, and then design optimization techniques in Section V-B. 

## A. A Divide-and-Conquer Approach

We have proved in Section IV that LDSes are simply leaves of the hierarchical structure of all maximal λ-compact subgraphs for all possible λ values. Thus, the remaining problem for computing LDSes is how to efficiently construct the hierarchical structure. We prove in the following lemma that maximal λ-compact subgraphs of $G$ are the same as connected components of locally dense subgraphs of $G ;$ thus, we can use the locally dense subgraph computation techniques of [12] to construct the hierarchical structure. Recall that (1) $F ( \lambda ) \ = \ \mathrm { a r g m a x } _ { S \subset V } | E ( S ) | \ - \ \lambda | S |$ where tie is broken by taking the largest vertex subset, and (2) the set of locally dense subgraphs can be arranged into a sequence $\emptyset = B _ { 0 } \subsetneq B _ { 1 } \subsetneq \cdots \subsetneq B _ { r } = V$ 

## Lemma V.1. Maximal λ-compact subgraphs of G are connected components of locally dense subgraphs of G.

Proof. We build the connection between maximal λ-compact subgraphs and locally dense subgraphs through $F ( \lambda )$ . Firstly, it is proved in [11] that the set of connected components of $F ( \lambda )$ is exactly the set of all maximal λ-compact subgraphs of G. Secondly, it is proved in [12] that $F ( \lambda )$ for any λ satisfying $\rho ( B _ { i + 1 } , B _ { i } ) < \lambda \leq \rho ( B _ { i } , B _ { i - 1 } )$ is the locally dense subgraph $B _ { i } ;$ ; note that, this also means that $F ( \lambda )$ remains the same for all λ values in the range $\left( \rho ( B _ { i + 1 } , B _ { i } ) , \rho ( B _ { i } , B _ { i - 1 } ) \right]$ . Thirdly, $F ( \lambda ) = \varnothing$ for any $\lambda > \rho ( B _ { 1 } , \emptyset ) = \rho ( B _ { 1 } )$ as $B _ { 1 }$ is the densest subgraph of G [12]. Thus, the lemma follows. □ 

Following Lemma V.1, we could first invoke the algorithm of [12] to construct the hierarchical structure of all maximal λ- compact subgraphs for all possible λ values, and then report the leaves of the hierarchical structure as LDSes. However, this would be inefficient for reporting top-k LDSes as it first constructs the entire hierarchical structure. Moreover, the implementation of [12] involves computing maximum flow over a graph with floating value capacities which may lead to inaccurate results [13]. In view of this, we propose a divideand-conquer algorithm in this subsection. 

Firstly, we prove the following lemma, which is central to our algorithm design. 

Lemma V.2. Let $\emptyset = B _ { 0 } \subsetneq B _ { 1 } \subsetneq \cdots \subsetneq B _ { r } = V$ be the sequence of locally dense subgraphs. Consider i and j such that $0 \leq i < j \leq r ,$ and let $B _ { l } = F ( \lambda ) f o r \lambda = \rho ( B _ { j } , B _ { i } )$ 

$I f i + 1 < j ,$ then $i < l < j .$ 

$I f i + 1 = j ,$ then $l = j .$ 

Proof. Let’s first consider the case that $i + 1 \ < \ j .$ Recall that locally dense subgraphs satisfy the property that $\rho ( B _ { i } , B _ { i - 1 } ) \ > \ \rho ( B _ { i + 1 } , B _ { i } )$ . Let’s denote $\rho ( B _ { i } , B _ { i - 1 } )$ by $\frac { a _ { i } } { b _ { i } }$ . Then, we have $\begin{array} { r } { \frac { a _ { i } } { b _ { i } } > \frac { a _ { i + 1 } } { b _ { i + 1 } } > \cdots > \frac { a _ { j - 1 } } { b _ { j - 1 } } > \frac { a _ { j } } { b _ { j } } , } \end{array}$ . As $\begin{array} { r } { \rho ( B _ { j } , B _ { i } ) \ = \ \sum _ { x = i + 1 } ^ { j } \frac { a _ { x } } { b _ { x } } , \ s } \end{array}$ simple calculation shows that $\rho ( B _ { j } , B _ { i } ) ~ > ~ { \frac { a _ { j } } { b _ { i } } } ~ = ~ \rho ( \tilde { B } _ { j } , B _ { j - 1 } )$ . Similarly, we also have $\begin{array} { r } { \rho ( B _ { j } , B _ { i } ) < \frac { a _ { i + 1 } } { b _ { i + 1 } } = \rho ( B _ { i + 1 } , B _ { i } ) } \end{array}$ . Thus, for $B _ { l } = F ( \lambda )$ with $\lambda = \rho ( B _ { j } , B _ { i } )$ , we have $i + 1 \le l \le j - 1$ 

$$
i + 1 = j
$$

$$
\lambda =
$$

$\rho ( B _ { j } , B _ { i } ) = \rho ( B _ { i + 1 } , B _ { i } ) > \rho ( B _ { i + 2 } , B _ { i + 1 } ) = \rho ( B _ { j + 1 } , B _ { j } )$ and thus $l = i + 1 = j .$ □ 

Note that, Lemma V.2 is similar to Proposition 10 of [12] but different in setting the value for λ. Specifically, Proposition 10 of [12] considers $F ( \lambda )$ for $\begin{array} { r } { \lambda = \rho ( B _ { j } , B _ { i } ) + \frac { 1 } { n ^ { 2 } } } \end{array}$ where there is an additional term of $\textstyle { \frac { 1 } { n ^ { 2 } } }$ , and thus leads to a different statement for the second bullet point: if $i + 1 = j$ then l = i. The advantage of our Lemma V.2 will become clear when we discuss the computation of $F ( \lambda )$ shortly. 

Corollary V.1. Given any two locally dense subgraphs X and Y such that $X \subsetneq Y ,$ , let $Z = F ( \lambda )$ where $\lambda = \rho ( Y , X )$ 

$I f Z = Y ,$ , then there is no locally dense subgraph W such that $X \subsetneq W \subsetneq Y$ 

$I f Z \neq Y ,$ then $X \subsetneq Z \subsetneq Y$ and Z is a locally dense subgraph. 

Proof. This directly follows from Lemma V.2. 

Following Corollary V.1, we can compute all locally dense subgraphs in G in a divide-and-conquer manner. As a special case, we know that $B _ { 0 } = \varnothing$ and $B _ { r } = V$ . Thus, we can initially let $X = \emptyset$ and $Y = V$ , and compute $F ( \lambda )$ for $\lambda = \rho ( Y , X )$ . If $F ( \lambda ) \neq Y$ , then we divide the problem into two sub-problems, one for X and $F ( \lambda )$ which will compute all locally dense subgraphs in-between X and $F ( \lambda )$ , and another for $F ( \lambda )$ and Y which will compute all locally dense subgraphs in-between $F ( \lambda )$ and Y. Otherwise, we reach a base case that there is no more locally dense subgraph in-between X and $Y .$ 

However, to efficiently obtain the top-k LDSes, we cannot afford to first construct the entire hierarchical structure of maximal λ-compact subgraphs. Thus, we propose to integrate top-k LDS identification into the process and stop as soon as k LDSes have been identified. Given the sequence of locally dense subgraphs $\emptyset \ = \ B _ { 0 } \ \subsetneq \ B _ { 1 } \ \subsetneq \ \cdots \ \subsetneq \ B _ { r } \ = \ V ,$ we know from Theorem IV.6 and Lemma $\mathrm { V . 1 }$ that LDSes are those connected components of $B _ { i }$ that do not include any vertex of $B _ { i - 1 }$ for $0 < i \leq r$ . However, obtaining connected components of $G [ B _ { i } ]$ may be time consuming since $B _ { i }$ could be large. We prove in the following lemma that we can check connected components of $G [ B _ { i } \backslash B _ { i - 1 } ]$ instead. 

Lemma V.3. Given the sequence of locally dense subgraphs $\emptyset = B _ { 0 } \subsetneq B _ { 1 } \subsetneq \cdots \subsetneq B _ { r } = V ,$ , LDSes of G are those connected components of $G [ B _ { i } \backslash B _ { i - 1 } ]$ that have no edge to $B _ { i - 1 } , f o r \ 0 < i \leq r .$ 

Proof. This can be easily seen from the fact that a connected component of $G [ B _ { i } ]$ does not include any vertex of $B _ { i - 1 }$ if and only if it is a connected component of $G [ B _ { i } \backslash B _ { i - 1 } ]$ that have no edge to $B _ { i - 1 }$ , since $B _ { i - 1 }$ is a subset of $B _ { i } . \quad \quad \sqcup$ 

```txt
Algorithm 2: LDS-DC(X, Y, k)

Input: Two locally dense subgraphs X and Y such that
    X ⊆ Y

Output: Top-k LDSes W such that W ⊆ Y\X

1 R ← ∅;
2 λ ← ρ(Y, X);
3 F(λ) ← LD(λ, X, Y);
4 if F(λ) = Y then
5    for each connected component W of G[Y\X] do
6    if E(W, X) = ∅ then R ← R ∪ {W};

7 else
8    if |R| < k then R ← R ∪ LDS-DC(X, F(λ), k - |R));
9    if |R| < k then R ← R ∪ LDS-DC(F(λ), Y, k - |R));

10 return R; 
```

Based on Lemma V.3 and the above discussions, the pseudocode of our divide-and-conquer algorithm for computing top-k LDSes is shown in Algorithm 2, where invoking $\mathsf { L D S - D C } ( \emptyset , V , k )$ returns the top-k LDSes in G. It works as follows. Given two locally dense subgraphs X and $Y$ such that $X \subsetneq Y ,$ , it first computes $F ( \lambda )$ for $\lambda \ : = \ : \rho ( Y , X )$ by invoking LD which will be introduced shortly. If $F ( \lambda ) = Y ,$ then we reach the first case of Corollary V.1 $( \mathrm { i . e . , } X = B _ { i - 1 }$ and $Y = B _ { i }$ for some i), and thus we know that connected components of $G [ Y \backslash X ]$ that do not have any edge to X are LDSes (Lines $5 \mathrm { - } 6 )$ . Note that, checking whether $E ( W , X )$ is empty or not for a connected component W of $G [ Y \backslash X ]$ can be conducted for free when obtaining the connected components of $G [ Y \backslash X ]$ ; thus, we call our approach as verification-free. If $F ( \lambda ) \neq Y$ , then we reach the second case of Corollary V.1, and thus we split the problem into two sub-problems and recursively solve them (Lines 8–9). The correctness of Algorithm 2 directly follows from the above discussions, and the following lemma which ensures that the LDSes are enumerated in nonincreasing density order. 

Lemma V.4. Given the sequence of locally dense subgraphs $\emptyset = B _ { 0 } \subsetneq B _ { 1 } \subsetneq \cdots \subsetneq B _ { r } = V ,$ 

• all LDSes in $B _ { i } \backslash B _ { i - 1 }$ have the same density, for $0 ~ <$ $i \leq r ,$ 

• all LDSes in $B _ { i } \backslash B _ { i - 1 }$ have strictly higher density than all LDSes in $B _ { i + 1 } \backslash B _ { i } ,$ for $0 < i < r .$ 

Proof. It is proved in [12] that $F ( \lambda )$ for any λ satisfying $\rho ( B _ { i + 1 } , B _ { i } ) < \lambda \leq \rho ( B _ { i } , B _ { i - 1 } )$ is the locally dense subgraph $B _ { i }$ . This suggests that $F ( \lambda )$ remains to be $B _ { i }$ for all λ values in the range $( \rho ( B _ { i + 1 } , B _ { i } ) , \rho ( B _ { i } , B _ { i - 1 } ) ]$ ]. Thus, the compactness of any connected component W of $G [ B _ { i } \backslash B _ { i - 1 } ]$ that has no edge to $B _ { i - 1 } ( \mathrm { i } . \mathrm { e } .$ , any LDS W in $B _ { i } \backslash B _ { i - 1 } )$ must be $\rho ( B _ { i } , B _ { i - 1 } ) ;$ note that, the compactness of W cannot be larger than $\rho ( B _ { i } , B _ { i - 1 } )$ , since otherwise it will be in $F ( \lambda ^ { \prime } )$ for $\lambda ^ { \prime } > \rho ( B _ { i } , B _ { i - 1 } )$ contradicting that W is not in $B _ { i - 1 }$ . Hence, the lemma follows. □ 

```m4
Algorithm 3: LD(λ, X, Y)

Input: A fraction value λ = a/b, and a locally dense subgraph X and another subgraph Y such that X ⊆ F(λ) ⊆ Y

Output: Locally dense subgraph F(λ)

1 Let g ← G[Y\X];

2 Assign a weight of b to each edge of g;

3 Add a source vertex s and a sink vertex t to g;

4 for each vertex v ∈ Y\X do

5 Add an undirected edge (s, v) with weight (|E(v, Y\X)| + 2|E(v, X)|) × b into g;

6 Add an undirected edge (v, t) with weight 2 × a into g;

7 Compute a minimum cut ( {s} ∪ S, {t} ∪ S̄ ) between s and t in g such that |S| is maximized;

8 return X ∪ S; 
```

The pseudocode for computing the set of maximal $\lambda -$ compact subgraphs (i.e., $F ( \lambda ) )$ of $G = ( V , E )$ is shown in Algorithm 3. Here, λ is represented as a fractional value ${ \frac { a } { b } } .$ . In addition, it takes two other inputs — a locally dense subgraph X and another subgraph Y such that ${ \cal X } \subsetneq { \cal F } ( \lambda ) \subseteq { \cal Y } -$ which will be used for optimizing the computation. Specially, when Y is also a locally dense subgraph and $Y \supset X$ and $\lambda = \rho ( Y , X )$ which is the case of invoking Algorithm 3 by Algorithm 2, the condition $X \subsetneq F ( \lambda ) \subseteq Y$ is satisfied. Note that, we present Algorithm 3 in this general form because this general form is needed by our optimized algorithm that will be discussed in Section V-B. The inputs $X$ and $Y$ are used for optimizing the computation of $F ( \lambda )$ as follows. Firstly, all vertices of $V \backslash Y$ can be excluded from the computation since we know that they will not be in the result. Secondly, we can also exclude X from the computation while retaining the edges between $u \in Y \backslash X$ and X as self-loops on u. As a result, we only need to conduct the computation on the subgraph $G [ Y \backslash X ]$ , which can be small. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/618a4c918bbb874640013f2027fd6c7f2d3f88d8085151b10123f336f1760471.jpg)



Fig. 3: Augmented graph for computing F(λ) (for presentation simplicity, weights between s and $\{ v _ { 1 } , v _ { 2 } , v _ { 3 } \}$ are omitted)


Specifically, $F ( \lambda )$ is computed via a minimum cut on the augmented graph that is constructed from $G [ Y \backslash X ]$ by Algorithm 3, which is also shown in Figure 3. Let $( \{ s \} \cup S , \{ t \} \cup { \bar { S } } )$ be an s-t cut (i.e., a partitioning of the vertex set) in the augmented graph, see Figure 3. The value of the cut (i.e., total weight of cross partition edges) is 

$\begin{aligned} & \left(\sum_{v\in \bar{S}}b(|E(v,Y\backslash X)| + 2|E(v,X)|)\right) + b|E(S,\bar{S})| + 2a|S|\\ & = \left(\sum_{v\in Y\backslash X}b(|E(v,Y\backslash X)| + 2|E(v,X)|)\right) + b|E(S,\bar{S})| + \\ & 2a|S| - \left(\sum_{v\in S}b(|E(v,Y\backslash X)| + 2|E(v,X)|)\right)\\ & = 2b(|E(Y\backslash X)| + |E(Y\backslash X,X)|) + b|E(S,\bar{S})| + 2a|S| - \\ & (2b|E(S)| + b|E(S,\bar{S})| + 2b|E(S,X)|)\\ & = 2b(|E(Y\backslash X)| + |E(Y\backslash X,X)| + |E(X)|) + 2a|S| - \\ & (2b|E(S)| + 2b|E(S,X)| + 2b|E(X)|)\\ & = 2b|E(Y)| + 2a|S| - 2b|E(S\cup X)|\\ & = 2b|E(Y)| - 2a|X| - 2b(|E(S\cup X)| - \lambda |S\cup X|) \end{aligned}$ 

Since $2 b | E ( Y ) | \ : - \ : 2 a | X |$ is constant given $\lambda , \ X$ and ${ \cal Y } ,$ minimizing the value of the cut is equivalent to maximizing $| E ( S \cup X ) | \ : - \ : \lambda | S \cup X |$ for $S ~ \subseteq ~ Y \backslash X$ . Consequently, Algorithm 3 correctly computes $F ( \lambda )$ 

Compared with the algorithm of [12], Algorithm 3 is different in the following two aspects. Firstly, the input Y does not need to be a locally dense subgraph. Secondly, all the edge weights of the augmented graph are integers, while [12] uses float-value weights (because $\bar { \lambda = \rho ( Y , X ) } + \frac { 1 } { n ^ { 2 } } )$ which creates a challenge for computing the minimum cut via maximum flow [13]. Note that, in Algorithm 3, the edge weights are at most $3 n ^ { 2 }$ since $b \leq n$ which can be easily stored in 64bit integers. While it is also possible to convert the edge weights of the augmented graph of [12] to integers by multiplying them by the denominator of the fractional representation of $\textstyle \rho ( Y , X ) + { \frac { 1 } { n ^ { 2 } } }$ , the resulting edge weights cannot be stored in 64bit integers since they can be up to $3 n ^ { 4 }$ 

Theorem V.5. The time complexity of running LDS-DC( , V, k) is $\mathcal { O } ( n ^ { 2 } m )$ 

Proof. This can be proved in a similar way to the proof of Proposition 12 of [12]; we omit the details. The general idea is that Algorithm 3 will be invoked for at most $2 r - 3$ times and each invocation takes time $\mathcal { O } ( n m )$ , where $r \leq n$ is the total number of locally dense subgraphs. We remark that the total time complexity of Lines 5–6 of Algorithm 2 during the whole running process is $\mathcal { O } ( m )$ , by noting that those connected components are disjoint. □ 

Example V.1. Consider the graph G in Figure 1, Figure 4 illustrates the detailed running process of $\mathsf { L D S - D C } ( \emptyset , V , 2 )$ Initially, $X ~ = ~ \emptyset , ~ Y ~ = ~ V ~ = ~ \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 2 6 } \}$ , and $\lambda \ =$ $\textstyle \rho ( Y , X ) = { \frac { 5 3 } { 2 6 } }$ , which are shown in the root node of Figure 4. By invoking LD, we obtain $F ( \textstyle { \frac { 5 3 } { 2 6 } } ) = \{ v _ { 1 } , v _ { 2 } , . . . , \dot { v _ { 1 3 } } \}$ , which is not the same as Y. Thus, we split the problem into two subproblems, which are denoted by the two children of the root node in Figure 4. 

Let’s first consider the subproblem with $X = \emptyset$ and $Y =$ $F ( \textstyle { \frac { 5 3 } { 2 6 } } ) = \{ v _ { 1 } , v _ { 2 } , . . . , v _ { 1 3 } \}$ . We have $\lambda = { \frac { 3 6 } { 1 3 } }$ and $F \big ( \frac { 3 6 } { 1 3 } \big ) \ =$ $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 8 } \}$ which is not the same as $Y$ . Thus, we futher split this subproblem into two subproblems, which are denoted by its two children in Figure 4. For the left sub-problem, we have $X ~ = ~ \emptyset , ~ Y ~ = ~ \{ v _ { 1 } , v _ { 2 } , \dotsc , v _ { 8 } \} , ~ \lambda ~ = ~ 3$ and $F ( 3 ) =$ $\{ v _ { 1 } , \ldots , v _ { 8 } \} \ = \ Y ;$ thus, we know that there is no locally dense subgraph in-between $X = \emptyset$ and $Y = \{ v _ { 1 } , v _ { 2 } , \dots , v _ { 8 } \}$ Consequently, $B _ { 1 } = \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 8 } \}$ is the first locally dense subgraph and it is also an LDS. for the right sub-problem, we have $X = \{ v _ { 1 } , v _ { 2 } , . . . , v _ { 8 } \} , Y = \{ v _ { 1 } , v _ { 2 } , . . . , v _ { 1 3 } \} , \lambda =$ $\frac { 1 2 } { 5 }$ and $F ( \lambda ) = \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \} = Y ;$ consequently, $B _ { 2 } =$ $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \}$ is the second locally dense subgraph. As the connected component $\{ v _ { 9 } , v _ { 1 0 } , \ldots , v _ { 1 3 } \}$ of $Y \backslash X$ have edges to $X = \{ v _ { 1 } , \ldots , v _ { 8 } \} , \ \{ v _ { 9 } , v _ { 1 0 } , \ldots , v _ { 1 3 } \}$ is not an LDS. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/1f58de03557a90ea62fac48bbfa25a4cb6d711c5c56d8547a6716a1246b03667.jpg)



Fig. 4: Running example of LDS-DC


Now, let’s consider the second subproblem of the initial problem (i.e. the root). $X ~ = ~ \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \} , ~ Y ~ =$ $\begin{array} { r } { \{ v _ { 1 } , v _ { 2 } , . . . , v _ { 2 6 } \} , \lambda = \frac { 1 7 } { 1 3 } } \end{array}$ and $F ( \scriptstyle { \frac { 1 7 } { 1 3 } } ) = \{ v _ { 1 } , v _ { 2 } , \dotsc , v _ { 2 0 } \} \neq$ Y. We thus split the problem into two subproblems and go into the left subproblem which has $X ~ = ~ \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \}$ $Y \ = \ F ( { \frac { 1 7 } { 1 3 } } ) \ = \ \{ v _ { 1 } , v _ { 2 } , . . . , v _ { 2 0 } \}$ , $\ \lambda \ = \ \frac { 1 1 } { 7 }$ and $F ( { \textstyle { \frac { 1 1 } { 7 } } } ) \ =$ $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } , v _ { 1 6 } , v _ { 1 7 } , \ldots , v _ { 2 0 } \} \ \ne \ Y$ . Consequently, we further split it into two subproblemws and go into the left one with $\begin{array} { l l l r } { X } & { = } & { \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \} , Y = F ( \frac { 1 1 } { 7 } ) = } \end{array}$ $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } , v _ { 1 6 } , v _ { 1 7 } , \ldots , v _ { 2 0 } \} , \lambda \ = \ { \frac { 8 } { 5 } } ,$ and $F \big ( \frac { 8 } { 5 } \big ) \ =$ $\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } , v _ { 1 6 } , v _ { 1 7 } , \ldots , v _ { 2 0 } \}$ which is the same as $Y .$ Thus, $B _ { 3 } \ = \ \left\{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } , v _ { 1 6 } , v _ { 1 7 } , \ldots , v _ { 2 0 } \right\}$ is the third locally dense subgraph. $Y \backslash X \ = \ \{ v _ { 1 6 } , v _ { 1 7 } , . . . , v _ { 2 0 } \}$ is the second LDS since it has no edge to $X = \{ v _ { 1 } , v _ { 2 } , \ldots , v _ { 1 3 } \}$ Now, we have identified the top-2 LDSes, and we stop. 

## B. An Optimized Approach

From Example V.1, we can see that in the first few invocations to Algorithm 3, X = and Y is shrinking while λ is increasing; note that, the time complexity of Algorithm 3 is generally proportional to the size of $Y \backslash X$ . Thus, when k is small for computing top-k LDSes, the first few invocations to Algorithm 3 may become the bottleneck. This is also confirmed by our empirical studies (see Section VI) which show that LDS-DC takes longer time than the state-of-the-art algorithm LDS to get the first few LDSes. In this subsection, we propose techniques to improve the performance, especially for reporting the first few LDSes. 

The general idea of our improvement is based on the fact that $F ( \lambda )$ is a subgraph of the λ -core of G [11]. Here, the l-core of G is the maximal subgraph of G whose minimum degree is at least $l ;$ the larger the value of l, the smaller the size of the l-core. Moreover, once we have obtained $F ( \lambda )$ which will be a locally dense subgraph $B _ { i }$ for some i, the graph that we need to work on for computing $F ( \lambda ^ { \prime } )$ for $\lambda ^ { \prime } \ > \ \lambda$ will be a subgraph of $B _ { i }$ which could be small, and the graph that we need to work on for computing $F ( \lambda ^ { \prime \prime } )$ for $\lambda ^ { \prime \prime } < \lambda$ can all contract/remove $B _ { i }$ from it. Thus, it will be beneficial to efficiently compute a locally dense subgraph initially, i.e., the first λ should be large enough while ensuring that $F ( \lambda ) \neq \emptyset$ . Motivated by this, we propose an optimized algorithm LDS-Opt in Algorithm 4, which first splits the chain of locally dense subgraphs into multiple sub-chains and then solves each sub-chain by invoking LDS-DC (Line 9). 

```txt
Algorithm 4: LDS-Opt(G, k)

Input: A graph G = (V, E) and an integer k
Output: Top-k LDSes R

1 Compute a core decomposition of G;
2 Let λ be the density of a 2-approximate solution to the densest subgraph of G;
3 R ← ∅;
4 c ← [λ]; p ← n;
5 X ← ∅; Y ← ∅;
6 while c > 0 and |R| < k do
7    Y ← Y ∪ {vertices of G whose core numbers are within the range [c, p)};
8    F(c) ← LD(c, X, Y);
9    R ← R ∪ LDS-DC(X, F(c), k - |R));
10    X ← F(c);
11    p ← c; c ← ⌊c/2⌋;
12 if X ≠ Y and |R| < k then
13    R ← R ∪ LDS-DC(X, Y, k - |R));
14 return R; 
```

LDS-Opt works as follows. We first compute a core decomposition of G [14], [15] (Line 1), which iteratively removes the minimum-degree vertex from the graph and assigns a core number for each vertex, denoted core(v). Note that, from the core numbers, we can efficiently obtain the l-core for any l, which simply consists of all vertices with core number at least l (Line 7). From the core decomposition, we can also obtain a 2-approximate solution to the densest subgraph of G [16], [17], which is the one with the highest density among the n subgraphs obtained during the process. Let λ be the density of the 2-approximate solution (Line 2). We first compute $F ( c )$ for $c \ = \ \lfloor \lambda \rfloor$ (Line 8) on the c-core which is obtained at Line 7, and then obtain all locally dense subgraphs (as well as LDSes contained therein) between X and $F ( c )$ by invoking LDS-DC (Line 9). After solving the sub-chain between X and $F ( c )$ , we then solve the next sub-chain which is between $F ( c )$ and $F ( \lceil \frac { c } { 2 } \rceil )$ (Line 10–11). Note that, to solve the sub-chain between $F ( c )$ and $F ( \lceil \frac { c } { 2 } \rceil )$ , all vertices of $F ( c )$ are removed from the graph with self-loops being added to their neighbors. It is easy to see that the time complexity of LDS-Opt remains to be $\mathcal { O } ( n ^ { 2 } m )$ 

## VI. EXPERIMENTS

In this section, we evaluate the efficiency of our algorithms for computing top-k LDSes on real-world graphs. As the effectiveness of the LDS model has already been demonstrated in [11], we do not conduct effectiveness testing in this paper. 

Algorithms. We compare the following algorithms. 

1) LDS: the state-of-the-art algorithm proposed in [11]. 

2) LDS-DC: our divide-and-conquer algorithm proposed in Section V-A. 

3) LDS-Opt: our optimized algorithm proposed in Section V-B. 

The source code of LDS is obtained from the authors of [11]. All the three algorithms are implemented in C++ and run in main memory.<sup>2</sup> All experiments are conducted on a machine with an Intel(R) 3.2GHz CPU and 64GB main memory running Ubuntu 18.04.5. 


TABLE II: Statistics of datasets


<table><tr><td>Dataset</td><td>|V|</td><td>|E|</td><td><eq>d_{ave}</eq></td><td>|R|</td><td>r</td><td>Type</td></tr><tr><td>DBLP</td><td>317,080</td><td>1,049,866</td><td>6.62</td><td>146</td><td>1,087</td><td>Coauthor</td></tr><tr><td>Stanford</td><td>281,903</td><td>1,992,636</td><td>14.13</td><td>600</td><td>2,193</td><td>Web</td></tr><tr><td>Amazon</td><td>403,394</td><td>2,443,408</td><td>12.11</td><td>102</td><td>1,866</td><td>Trade</td></tr><tr><td>Google</td><td>875,713</td><td>4,322,051</td><td>9.87</td><td>3,118</td><td>3,876</td><td>Web</td></tr><tr><td>wiki-Talk</td><td>2,394,385</td><td>4,659,565</td><td>3.89</td><td>2,555</td><td>655</td><td>Editing</td></tr><tr><td>BerkStan</td><td>685,230</td><td>6,649,470</td><td>19.4</td><td>1,137</td><td>4,139</td><td>Web</td></tr><tr><td>as-Skitter</td><td>1,696,415</td><td>11,095,298</td><td>13.08</td><td>761</td><td>3,501</td><td>Internet</td></tr><tr><td>Patent</td><td>3,774,768</td><td>16,518,947</td><td>8.75</td><td>3,670</td><td>6,956</td><td>Citation</td></tr><tr><td>LiveJournal</td><td>4,846,609</td><td>42,851,237</td><td>17.68</td><td>1,102</td><td>9,024</td><td>Social</td></tr><tr><td>UK-2002</td><td>18,459,128</td><td>261,556,721</td><td>28.34</td><td>9,584</td><td>40,809</td><td>Web</td></tr></table>

Datasets. We evaluate the algorithms on 10 large real graphs from different domains, which are downloaded from the Stanford Network Analysis Platform<sup>3</sup>. For each graph, we removed edge directions, self-loops, and parallel edges. Statistics of these real graphs are shown in Table II, where the graphs are listed in increasing order regarding their numbers of edges; $d _ { a v e }$ in the fourth column shows the average degree of the graphs,  in the fifth column shows the number of LDSes in the graphs and r in the sixth column shows the number of locally dense subgraphs in the graphs. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/aa9e224cb497a0c5be810d634c94c407d68f5a4fbc0c00b55ba5d534513cead1.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/228f872c771d1c1f38b5e5a098b94144223a8ad130392c039c84d97eb53762ba.jpg)



(a) DBLP



(b) Stanford


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/17c170bf43a55397c5471d4d1d2932aadfd8eb507bf7d46b15e8b965e04233e1.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/5d70e5f57c6b768db632263fe378f39b5935d67fc5da79b07d1feb783aa8ed60.jpg)



(c) Amazon


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/1c284ba893215db23b7d0f3a19c938ebb36aaa0040adb3c0c37632294d2171b1.jpg)



(d) Google


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/58f6dc58001ba7b1d1131a4f0665d2f6cef150743f3971b5efded02eace8d3b2.jpg)



(e) wiki-Talk


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/a8967a8e796518a79f480f9c1b9b78622b31bc971860dde82d3cf6a05d3d2c05.jpg)



(f) BerkStan



(g) as-Skitter


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/34f4ae3a2a76f6189000c356140feb635a87e2daaa84726529e6a1183f72cbdb.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/0b46781e645e20c7eab7078ecd66564d64904a2421cfc8ce071c37fe323d2951.jpg)



(i) LiveJournal



(h) Patent


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/c55db66b95fd07c848a790e1aa4903ce0a211049a2398cfbe6198ac350820f3e.jpg)



(j) UK-2002



Fig. 5: Efficiency on detecting all LDSes, i.e., $k = \infty$ (best viewed in color)


Evaluation Metrics. We report the processing time, which is the total running time excluding only the I/O time of loading a graph from disk to main memory. We set a timeout of 2 hours for running an algorithm on a graph, with an exception of 5 hours for processing the largest graph UK-2002. 

## A. Experimental Results

Efficiency on Detecting All LDSes $( { \bf i . e . , \mit k = \infty } )$ . In this experiment, we evaluate the efficiency of the algorithms on detecting all LDSes, by setting k to be . The results are shown in Figure 5, which reports the processing time for each $k \in [ 1 , | \mathcal { R } | + 1 ]$ where is the total number of LDSes and is listed in Table II; note that, the processing time for any $\begin{array} { r } { k > | \mathcal { R } | + 1 } \end{array}$ would be the same as that for $\begin{array} { r } { k = \left| \mathcal { R } \right| + 1 } \end{array}$ . The state-of-the-art algorithm LDS runs the slowest and runs outof-time for all the datasets except the two smallest ones, DBLP and Stanford, when k is . This is because the lower-ranked LDSes have lower densities, which makes verification (i.e., computing $F ( \lambda )$ on G) time consuming. On the other hand, both of our algorithms, LDS-DC and LDS-Opt, successfully report all the LDSes within the time limit. The improvement of our algorithms over LDS is at least two orders of magnitude on Amazon, Google, wiki-Talk, BerkStan, and as-Skitter, for $k = \infty$ . Besides, our optimized algorithm LDS-Opt consistently runs faster than LDS-DC on all datasets. For example, on wiki-Talk, LDS-Opt is 4 times faster than LDS-DC on detecting all LDSes (i.e., 2.8 seconds v.s. 12 seconds). This demonstrates the efficiency of our optimization techniques. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/9d380a40bb6e702dbc9c5a82ea4b19acd013b42eb0a575644e922a62e520c8b3.jpg)



(a) DBLP


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/32d8eb40483cc2ed6d5d1dc2c856b0332dd91cdf6ca415bc0fb4b5c4b6e3eabc.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/60394310af29b8160655bf81ed26471ed0d6b5db19a149dd92e61f1fabf6386b.jpg)



(b) Stanford


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/d174405b84eecb250a4b1c072b40ef06f4be624a5e9790c04e8a12326ef93e38.jpg)



(c) Amazon


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/2e02e3b6c8561f9d83185c3a41f945a48c35cf9a550b3e315c095fd3cb29d6f0.jpg)



(d) Google


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/dd972c451cd9cadba33e7a988d4ab45d73ba8205e605419a582e901bd6bff442.jpg)



(e) wiki-Talk


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/9153b26c1f62df02ac691f11c70ad5f8247c66568b9e633a1e26f88982365101.jpg)



(f) BerkStan


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/563ee879957890385729b8e30a59486738f650bae3583e6db89be1c99ae6ca34.jpg)



(g) as-Skitter


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/6575262b71670af589364284fb374313d30ce55f7d7c054e144fa6c213bc1a6d.jpg)



(h) Patent



(i) LiveJournal


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/077c6830fc8982417d51252645a7aaf87aa31b5f6d47e9fba1aa4f8fe28ffdf6.jpg)



(j) UK-2002



Fig. 6: Efficiency evaluation for small k $( k \le 2 0 )$


Efficiency Evaluation for Small k. Considering that it is not easy to distinguish the algorithms in Figure 5 when k is small, we also report the processing time of the algorithms for small k values in Figure 6; specifically, $k \leq 2 0 .$ Although LDS-DC is significantly faster than LDS when k is large (see Figure 5), LDS-DC is generally slower in reporting the first few results (see Figure 6) which motivates us to design the optimized algorithm LDS-Opt. From Figure 6, we can also see that LDS-Opt runs faster than LDS for most of the cases, and the improvement can also be up to several orders of magnitude (e.g., on Amazon, wiki-Talk, and as-Skitter). Moreover, LDS-Opt consistently runs faster than LDS in reporting the top-1 result. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/8f8a61ac343303d8eb09ee57522f9abf680e224e7f85e46c19c9106d17c2b005.jpg)



(a) wiki-Talk


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/02411062e10c679f94d86ca6c869a64bf1962299ad46baa2e55c070f68fdc254.jpg)



(b) BerkStan


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/5ac57b11650322184f1789d5bc61c81a315cd20474ea3d81a68a44b7096792c5.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/f06b91da59399b3ae4f948ff843eac61a4ec2d39a485608cb13015b1e64d9d86.jpg)



(c) as-Skitter



(d) Patent


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/5eb58ce01e24566037558dd26918699898d8091930c507a477272dfbb384ba93.jpg)



(e) LiveJournal


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/063195c4c47da4b03556212d2c08ac910c81daa9a54ae0f51b19f7c95efaf8e3.jpg)



(f) UK-2002



Fig. 7: Scalability evaluation $( k = \infty ,$ , vary graph size)


Scalability Evaluation. In this experiment, we evaluate the scalability of the algorithms on six of the large graphs. For each graph, we randomly sample 20%, 40%, 60%, 80% vertices and then construct the corresponding vertex-induced subgraph. The results for $k = \infty$ are reported in Figure 7. We can see that as expected, all algorithms run slower when the graph size increases. Nevertheless, our algorithms LDS-DC and LDS-Opt scale much better than the state-of-the-art algorithm LDS. Also, LDS-Opt consistently runs faster than LDS-DC. Thus, LDS-Opt has a good scalability. 

Distribution of LDS Densities and Sizes. In this experiment, we report the distribution of LDSes in terms of their densities and sizes. The results are illustrated in Figure 8. We organize all detected LDSes into two groups, i.e., top-20 and non top-20, and use different colors to differentiate them. We can see that besides the top-20 LDSes, there are also many other LDSes with large size and high density. For example, on UK-2002, there are 323 LDSes with density higher than 50 and 1438 LDSes with density higher than 20. Detecting these highdensity LDSes may reveal meaningful subgraph patterns and thus be beneficial to applications. As a result, it is meaningful and necessary to identify top-k LDSes for large k values. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/c886a976735c1885b190a9dcff05f696f53839fcbcf7f47f6a94db4d4a7e12f1.jpg)



(a) DBLP


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/0da12edc565bc22fd6bb0e3a62d7c11c54adc6545356cca7f7c086261880741e.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/db31c45a24f4800faf45e678a6dbf07632197d10c03ca466904f49e30919d009.jpg)



(b) Stanford


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/14fc786531722b2ea596e4f990d7812507ded83ec69a7accc19e9efc3c1339bc.jpg)



(c) Amazon


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/7d8a03c0bc2edbdc6a41070d067fd3297b9a1c17066dec666a3a98dd3a6a6dfb.jpg)



(d) Google



(e) LiveJournal


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-19/fc1dcbc3-b25a-4380-9322-c95f02e8640e/7fa44262bbc6dfdd891270e9afa8624059781e9b652f416ebec31037ef806225.jpg)



(f) UK-2002



Fig. 8: Distribution of LDS densities and sizes


## VII. RELATED WORK

The problem of finding dense subgraphs from a large graph has been widely studied [1], [2], [3]. The subgraph with the largest average degree, referred to as the densest subgraph in the literature, can be computed exactly in $\begin{array} { r } { \mathcal { O } ( n m \log { \frac { n ^ { 2 } } { m } } ) } \end{array}$ time by parametric network flow [9], [10]. A 2-approximation to the densest subgraph can be found in linear time by iteratively removing the vertex with the smallest degree [16], [17]. Approximately computing the densest subgraph in MapReduce, streaming and dynamic environments has also been studied [18], [19], [20]. Besides, the problem of enumerating all densest subgraphs in a large graph has been recently studied in [21] and the problem of anchored densest subgraph is studied in [22]. However, all these works only aim to find the globally densest subgraphs, while subgraphs that are locally dense in specific regions are ignored. 

Recently, the notion of locally dense/densest subgraphs have been formulated to identify subgraphs that are locally dense [23], [11], [12]. Specifically, locally densest subgraph (LDS) is formulated in [11], which is also the notion we use in this paper. On the other hand, locally dense subgraph is formulated and studied in [12], [23]. LDSes are disjoint, while locally dense subgraphs form a nested structure. Both notions include the globally densest subgraph as one of their solutions, e.g., connected components of the globally densest subgraph are the top LDSes while the globally densest subgraph itself is the inner-most one in the chain of locally dense subgraphs. We in this paper are the first to demonstrate the relationship between LDSes and locally dense subgraphs, i.e., LDSes are connected components of locally dense subgraphs that do not contain parts of any other denser locally dense subgraphs. Based on this connection, we in this paper propose verification-free approaches for finding top-k LDSes that have the highest densities. Our algorithms not only have lower time complexities, but also empirically perform better than the state-of-the-art algorithm proposed in [11]. 

Higher-order variants of the densest subgraph problem has also been recently studied in the literature. That is, instead of maximizing the average number of edges (per vertex) in a subgraph, it maximizes the average number of l-cliques (per vertex) in a subgraph [24], [25], [26]. Note that, the higher-order variant captures classic densest subgraph (i.e., average degree-based) as a special case, since an edge is a 2-clique. Inspired by [24], higher-order version of locally densest subgraph, termed locally triangle-densest subgraph, is formulated and studied in [27]. The techniques we propose in this paper can also be used to speed up the computation of locally triangle-densest subgraphs. 

Other density measures have also been used in the literature for finding dense subgraphs [3], e.g., minimum-degree based k-core computation [28], [29], triangle based k-truss computation [30], [31], [32], edge-connectivity based k-edge connected component computation [33], [34], [35], clique [36] and its relaxations (e.g., k-plex [37], n-clique [38], n-clans [39]). However, these techniques cannot be applied to compute LDSes, due to inherent different problem natures. 

## VIII. CONCLUSION

In this paper, we proposed efficient algorithms for computing top-k locally densest subgraphs (LDSes) with the highest densities. Our algorithms are designed based on a thorough investigation on the properties of maximal λ-compact subgraphs, which connect LDSes with locally dense subgraphs. As a result, our algorithms are verification free, and can be applied to efficiently obtain top-k LDSes for any k value. Our algorithms not only have lower time complexities but also empirically perform better than the state-of-the-art algorithm, and the improvement can be up to several orders of magnitude. One possible direction of future work is to incorporate convex programming techniques that are proposed in [23] to our implementation. Another possible direction of future work is to extend our implementation to compute locally triangle-dense subgraphs that are studied in [27]. 

Acknowledgements. Tran Ba Trung was funded by Vingroup JSC and supported by the Master, PhD Scholarship Program of Vingroup Innovation Foundation (VINIF), Institute of Big Data, code VINIF.2020.ThS.BK.04. Lijun Chang was supported by the Australian Research Council Fundings of FT180100256 and DP220103731. 

## REFERENCES



[1] V. E. Lee, N. Ruan, R. Jin, and C. C. Aggarwal. A survey of algorithms for dense subgraph discovery. In Managing and Mining Graph Data, pages 303–336. 2010. 





[2] Aristides Gionis and Charalampos E. Tsourakakis. Dense subgraph discovery: KDD 2015 tutorial. In Proc. of KDD’15, pages 2313–2314, 2015. 





[3] Lijun Chang and Lu Qin. Cohesive Subgraph Computation over Large Sparse Graphs. Springer Series in the Data Sciences, 2018. 





[4] Jie Chen and Yousef Saad. Dense subgraph extraction with application to community detection. IEEE Transactions on knowledge and data engineering, 24(7):1216–1230, 2010. 





[5] Y. Dourisboure, F. Geraci, and M. Pellegrini. Extraction and classification of dense communities in the web. In Proc. of WWW’07, pages 461–470, 2007. 





[6] A. Angel, N. Koudas, N. Sarkas, and D. Srivastava. Dense subgraph maintenance under streaming edge weight updates for real-time stor identification. Proc. VLDB Endow., 5(6):574–585, 2012. 





[7] A. Beutel, W. Xu, V. Guruswami, C. Palow, and C. Faloutsos. Copycatch: stopping group attacks by spotting lockstep behavior in social networks. In Proc. of WWW’13, pages 119–130, 2013. 





[8] Eugene Fratkin, Brian T Naughton, Douglas L Brutlag, and Serafim Batzoglou. Motifcut: regulatory motifs finding with maximum density subgraphs. Bioinformatics, 22(14):e150–e157, 2006. 





[9] Giorgio Gallo, Michael D Grigoriadis, and Robert E Tarjan. A fast parametric maximum flow algorithm and applications. SIAM Journal on Computing, 18(1):30–55, 1989. 





[10] Andrew V Goldberg. Finding a maximum density subgraph. University of California Berkeley, 1984. 





[11] Lu Qin, Rong-Hua Li, Lijun Chang, and Chengqi Zhang. Locally densest subgraph discovery. In Proc. of KDD’15, pages 965–974, 2015. 





[12] Nikolaj Tatti and Aristides Gionis. Density-friendly graph decomposition. In Proc. of WWW’15, pages 1089–1099, 2015. 





[13] Jeff Erickson. Algorithms. 2019. 





[14] Vladimir Batagelj and Matjaz Zaversnik. An o (m) algorithm for cores decomposition of networks. arXiv preprint cs/0310049, 2003. 





[15] Stephen B. Seidman. Network structure and minimum degree. Social Networks, 5(3):269–287, 1983. 





[16] Yuichi Asahiro, Kazuo Iwama, Hisao Tamaki, and Takeshi Tokuyama. Greedily finding a dense subgraph. Journal of Algorithms, 34(2):203– 221, 2000. 





[17] Moses Charikar. Greedy approximation algorithms for finding dense components in a graph. In Proc. of APPROX’13, pages 84–95, 2000. 





[18] B. Bahmani, R. Kumar, and S. Vassilvitskii. Densest subgraph in streaming and mapreduce. PVLDB, 5(5):454–465, 2012. 





[19] S. Bhattacharya, M. Henzinger, D. Nanongkai, and C. E. Tsourakakis. Space- and time-efficient algorithm for maintaining dense subgraphs on one-pass dynamic streams. In Proc. of STOC’15, pages 173–182, 2015. 





[20] Alessandro Epasto, Silvio Lattanzi, and Mauro Sozio. Efficient densest subgraph computation in evolving graphs. In Proc. of WWW’15, pages 300–310, 2015. 





[21] Lijun Chang and Miao Qiao. Deconstruct densest subgraphs. In Proc. of WWW’20, pages 2747–2753, 2020. 





[22] Yizhou Dai, Miao Qiao, and Lijun Chang. Anchored densest subgraph. In Proc. of SIGMOD’22, pages 1200–1213, 2022. 





[23] M. Danisch, T.-H. H. Chan, and M. Sozio. Large scale density-friendly graph decomposition via convex programming. In Proc. of WWW’17, pages 233–242, 2017. 





[24] Charalampos E. Tsourakakis. The k-clique densest subgraph problem. In Proc. of WWW’15, pages 1122–1132, 2015. 





[25] Yixiang Fang, Kaiqiang Yu, Reynold Cheng, Laks V. S. Lakshmanan, and Xuemin Lin. Efficient algorithms for densest subgraph discovery. Proc. VLDB Endow., 12(11):1719–1732, 2019. 





[26] Lu Chen, Chengfei Liu, Kewen Liao, Jianxin Li, and Rui Zhou. Contextual community search over large social networks. In Proc. of ICDE’19, pages 88–99, 2019. 





[27] Raman Samusevich, Maximilien Danisch, and Mauro Sozio. Local triangle-densest subgraphs. In Proc. of ASONAM’16, pages 33–40, 2016. 





[28] M. Sozio and A. Gionis. The community-search problem and how to plan a successful cocktail party. In Proc. of KDD’10, pages 939–948, 2010. 





[29] Kai Yao and Lijun Chang. Efficient size-bounded community search over large networks. Proc. VLDB Endow., 14(8):1441–1453, 2021. 





[30] J. Cohen. Trusses: Cohesive subgraphs for social network analysis, 2008. 





[31] J. Wang and J. Cheng. Truss decomposition in massive networks. PVLDB, 5(9), 2012. 





[32] A. E. Sariyuce, C. Seshadhri, A. Pinar, and ¨ U. V. C¸ ataly <sup>¨</sup> urek. Finding¨ the hierarchy of dense subgraphs using nucleus decompositions. In Proc. of WWW’15, pages 927–937, 2015. 





[33] T. Akiba, Y. Iwata, and Y. Yoshida. Linear-time enumeration of maximal k-edge-connected subgraphs in large networks by random contraction. In Proc. of CIKM’13, 2013. 





[34] L. Chang, J. X. Yu, L. Q., X. Lin, C. Liu, and W. Liang. Efficiently computing k-edge connected components via graph decomposition. In Proc. of SIGMOD’13, 2013. 





[35] Lijun Chang and Zhiyi Wang. A near-optimal approach to edge connectivity-based hierarchical graph decomposition. Proc. VLDB Endow., 15(6):1146–1158, 2022. 





[36] Lijun Chang. Efficient maximum clique computation over large sparse graphs. In Proc. of KDD’19, pages 529–538, 2019. 





[37] S. B. Seidman and B. L. Foster. A graph-theoretic generalization of the clique concept. Journal of Mathematical Sociology, 6:139–154, 1978. 





[38] C. Bron and J. Kerbosch. Finding all cliques of an undirected graph (algorithm 457). CACM, 16(9):575–576, 1973. 





[39] Robert Mokken. Cliques, clubs and clans. Quality & Quantity, 13:161– 173, 1979. 

