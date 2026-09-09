## 1 Theoretical Proof

Let $G = ( V , E )$ be a finite undirected simple graph with $V \neq \emptyset$ , and let $h \geq 2$ be fixed. All subgraphs below are vertex-induced. For disjoint vertex sets $A , B \subseteq V$ , write 

$$
E (A, B) := \{\{u, v \} \in E: u \in A, v \in B \}.
$$

## 1.1 Definitions and basic properties

For a vertex set $S \subseteq V$ let 

$$
\Psi_ {h} (S) := \left\{C \subseteq S: | C | = h \text {   and   } G [ C ] \cong K _ {h} \right\}
$$

be the set of h-cliques contained in $G [ S ]$ , and let 

$$
\mu_ {h} (S) := | \Psi_ {h} (S) |.
$$

For every nonempty $S _ { ; }$ the h-clique density of G[S] is 

$$
d _ {h} (S) := \frac {\mu_ {h} (S)}{| S |}.
$$

For $U \subseteq S$ , define the h-clique deletion loss 

$$
\Delta_ {h} (U; S) := \mu_ {h} (S) - \mu_ {h} (S \setminus U) = \left| \{C \in \Psi_ {h} (S): C \cap U \neq \varnothing \} \right|.\tag{1}
$$

Definition 1.1 (h-clique λ-compact subgraph). For $\lambda \geq 0$ , a nonempty vertex set $S \subseteq V$ is h-clique λ-compact if G[S] is connected and 

$$
\Delta_ {h} (U; S) \geq \lambda | U | \quad \text {   for   every   } U \subseteq S.\tag{2}
$$

It is maximal h-clique λ-compact in G if no proper superset $T$ with 

$$
S \subsetneq T \subseteq V
$$

is h-clique λ-compact. 

Definition 1.2 (h-clique compactness). For a connected nonempty set $S ,$ its h-clique compactness is 

$$
\eta_ {h} (S) := \max \{\lambda \geq 0: S \text {   is   } h \text {-clique   } \lambda \text {-compact} \} = \min _ {\varnothing \neq U \subseteq S} \frac {\Delta_ {h} (U ; S)}{| U |}.\tag{3}
$$

For a disconnected set, define $\eta _ { h } ( S ) : = 0$ 

Definition 1.3 (Locally h-clique densest subgraph). A connected induced subgraph $G [ S ]$ is an LhCDS if S is a maximal h-clique $d _ { h } ( S )$ -compact vertex set in $G .$ 

Candidates are identified by their vertex sets. Let 

$$
\mathcal {D} _ {h} (G) := \{S \subseteq V: G [ S ] \text {   is   an   LhCDS } \}, \qquad q := | \mathcal {D} _ {h} (G) |.
$$

To make $\mathrm {  { ^ { 6 4 } t o p { - } } } k ^ { \prime }$ unambiguous, fix once and for all a total order ≺ on the subsets of V and rank the members of ${ \mathcal { D } } _ { h } ( G )$ first by nonincreasing $d _ { h }$ and then by ≺. In this paper, top-k means the first min $\{ k , q \}$ members in this order, where $k \geq 1$ . Thus the output has fixed cardinality when $k \leq q .$ If instead all solutions tied with the kth density are required, the algorithm below must finish the entire terminal layer containing the kth output. 

The next two lemmas connect compactness to induced-subgraph density and will be used throughout the hierarchy proof. 

Lemma 1.4. For every connected nonempty $S \subseteq V$ 

$$
\eta_ {h} (S) \leq d _ {h} (S).
$$

Proof. Apply Definition 1.1 to $U = S$ . Removing all vertices removes exactly $\mu _ { h } ( S )$ cliques. Hence 

$$
\mu_ {h} (S) = \Delta_ {h} (S; S) \geq \eta_ {h} (S) | S |,
$$

which is equivalent to $d _ { h } ( S ) \geq \eta _ { h } ( S )$ 

Lemma 1.5 (Compactness gap and denser induced subgraphs). Let $S \subseteq V$ be connected and nonempty. Then 

$$
\eta_ {h} (S) <   d _ {h} (S)
$$

if and only if there exists a nonempty proper subset $T \subsetneq S$ such that 

$$
d _ {h} (T) > d _ {h} (S).
$$

Moreover, whenever such a T exists, one can choose T so that $G [ T ]$ is connected. 

Proof. ⇒: Suppose that $\eta _ { h } ( S ) ~ < ~ d _ { h } ( S )$ . By Equation (3), there exists a nonempty $U \subseteq S$ such that 

$$
\Delta_ {h} (U; S) <   d _ {h} (S) | U |.
$$

The witness cannot be $U = S$ , because $\Delta _ { h } ( S ; S ) / | S | = d _ { h } ( S )$ . Thus $T : = S \setminus U$ is nonempty and proper. Using Equation (1), 

$$
\begin{array}{l} \mu_ {h} (T) = \mu_ {h} (S) - \Delta_ {h} (U; S) \\ \qquad > \mu_ {h} (S) - d _ {h} (S) | U | \\ \qquad = d _ {h} (S) (| S | - | U |) = d _ {h} (S) | T |. \end{array}
$$

Therefore $d _ { h } ( T ) > d _ { h } ( S )$ 

⇐: Suppose that a nonempty proper $T \subsetneq S$ satisfies $d _ { h } ( T ) > d _ { h } ( S )$ , and set $U : = S \setminus T$ . Then 

$$
\begin{array}{l} \Delta_ {h} (U; S) = \mu_ {h} (S) - \mu_ {h} (T) \\ <   d _ {h} (S) | S | - d _ {h} (S) | T | \\ = d _ {h} (S) | U |. \end{array}
$$

Hence $S$ is not h-clique $d _ { h } ( S )$ -compact; by Equation (3), 

$$
\eta_ {h} (S) \leq \frac {\Delta_ {h} (U ; S)}{| U |} <   d _ {h} (S).
$$

Finally, if $G [ T ]$ is disconnected, no h-clique can contain vertices from two diferent connected components of $G [ T ]$ . Thus both $\mu _ { h } ( T )$ and |T| are additive over the connected components, so $d _ { h } ( T )$ is a weighted average of their densities. At least one component has density at least $d _ { h } ( T ) > d _ { h } ( S )$ , and that component may be used in place of $T .$ □ 

Corollary 1.6 (Self-denseness). For every connected nonempty $S _ { i }$ 4 

$$
\eta_ {h} (S) = d _ {h} (S)
$$

if and only if every nonempty induced subgraph of $G [ S ]$ has h-clique density at most $d _ { h } ( S )$ 

Proof. This is the negation of Lemma 1.5, together with Lemma 1.4. □ 

Lemma 1.7 (Characterization inside a maximal compact subgraph). Let S be maximal h-clique λ-compact in G for some $\lambda \geq 0$ . Then $G [ S ]$ is an LhCDS if and only if S contains no h-clique λ<sup>′</sup>-compact vertex set for any $\lambda ^ { \prime } > \eta _ { h } ( S )$ 

Proof. ⇒: Assume first that $G [ S ]$ is an LhCDS. By Definition 1.3, S is h-clique $d _ { h } ( S )$ -compact. Lemma 1.4 therefore gives $\eta _ { h } ( S ) = d _ { h } ( S )$ . If $T \subseteq S$ were h-clique λ<sup>′</sup>-compact for some $\lambda ^ { \prime } > \eta _ { h } ( S )$ , then 

$$
d _ {h} (T) \geq \eta_ {h} (T) \geq \lambda^ {\prime} > d _ {h} (S),
$$

contradicting Corollary 1.6. 

⇐: Proof by contrapositive: 

Suppose that $G [ S ]$ is not an LhCDS. Because S is maximal h-clique λ- compact, we have $\lambda \le \eta _ { h } ( S )$ . If $\eta _ { h } ( S ) = d _ { h } ( S )$ , then S is h-clique $d _ { h } ( S ) .$ compact. Any proper h-clique $d _ { h } ( S )$ -compact supergraph of $S$ would also be h-clique λ-compact, contradicting the assumed maximality of S at level λ. Thus S would be an LhCDS, a contradiction. Consequently, $\eta _ { h } ( S ) < d _ { h } ( S )$ 

Let $T \subseteq S$ be a connected induced subgraph of maximum h-clique density among all connected induced subgraphs of $G [ S ]$ . By Lemma 1.5, some connected proper induced subgraph of $G [ S ]$ has density greater than $d _ { h } ( S )$ , and hence $d _ { h } ( T ) > d _ { h } ( S )$ 

We next verify that $T$ is densest within itself. Let $R \subseteq T$ be nonempty. If $G [ R ]$ is connected, the maximal choice of $T$ gives $d _ { h } ( R ) \leq d _ { h } ( T )$ . If $G [ R ]$ is disconnected, then $d _ { h } ( R )$ is a weighted average of the densities of the connected components of $G [ R ] ;$ ; each such component is a connected induced subgraph of $G [ S ]$ , so each has density at most $d _ { h } ( T )$ , and therefore $d _ { h } ( R ) \leq d _ { h } ( T )$ as well. Consequently, Corollary 1.6 gives 

$$
\eta_ {h} (T) = d _ {h} (T) > d _ {h} (S) > \eta_ {h} (S).
$$

Hence $T$ is an h-clique λ<sup>′</sup>-compact subset of S for $\lambda ^ { \prime } : = \eta _ { h } ( T ) > \eta _ { h } ( S )$ □ 

## 1.2 Union closure and the compactness hierarchy

The next lemma is the structural step at which higher-order motifs might appear to cause dificulty. The proof shows that they do not: cliques crossing the boundary of two sets only increase the deletion loss of their union. 

Lemma 1.8 (Union closure). Let $A , B \subseteq V$ be h-clique λ-compact. $I f G [ A \cup B ]$ is connected—equivalently, since $G [ A ]$ and $G [ B ]$ are connected, $i f A \cap B \neq \emptyset$ or $E ( A \setminus B , B \setminus A ) \neq \emptyset -$ then $A \cup B$ is h-clique λ-compact. 

Proof. For $R \subseteq V$ and $X \subseteq R .$ write 

$$
\mathcal {L} _ {R} (X) := \{C \in \Psi_ {h} (R): C \cap X \neq \varnothing \},
$$

so that $| { \mathcal { L } } _ { R } ( X ) | = { \Delta } _ { h } ( X ; R )$ 

Fix an arbitrary $Z \subseteq A \cup B .$ , and partition it as 

$$
Z _ {A} := Z \cap (A \setminus B), \quad Z _ {B} := Z \cap B.
$$

Then $Z _ { A } \cap Z _ { B } = \emptyset$ and $Z _ { A } \cup Z _ { B } = Z$ . Every clique in $\mathcal { L } _ { A } ( Z _ { A } )$ and every clique in $\mathcal { L } _ { B } ( Z _ { B } )$ belongs to $\mathcal { L } _ { A \cup B } ( Z )$ . Moreover, these two families are disjoint: a clique in $\mathcal { L } _ { A } ( Z _ { A } )$ contains a vertex of $A \backslash B$ , whereas every clique in $\Psi _ { h } ( B )$ is contained entirely in B. All other cliques of $G [ A \cup B ]$ that meet $Z ,$ including cross-boundary cliques, contribute only to the left-hand side. Therefore, 

$$
\begin{array}{r l} & {\Delta_ {h} (Z; A \cup B) = | \mathcal {L} _ {A \cup B} (Z) |} \\ & {\qquad \geq | \mathcal {L} _ {A} (Z _ {A}) | + | \mathcal {L} _ {B} (Z _ {B}) |} \\ & {\qquad = \Delta_ {h} (Z _ {A}; A) + \Delta_ {h} (Z _ {B}; B)} \\ & {\qquad \geq \lambda | Z _ {A} | + \lambda | Z _ {B} |} \\ & {\qquad = \lambda | Z |.} \end{array}
$$

Since $G [ A \cup B ]$ is connected, Definition 1.1 is satisfied. Notice that an h-clique using vertices from both $A \backslash B$ and $B \setminus A$ is an additional member of $\mathcal { L } _ { A \cup B } ( Z )$ and therefore can only strengthen the inequality. □ 

Theorem 1.9 (Laminar hierarchy of maximal compact subgraphs). The family of all distinct maximal h-clique λ-compact sets, over all $\lambda \geq 0$ , has the following properties. 

1. For a fixed λ, any two distinct maximal h-clique λ-compact sets A and B are vertex-disjoint and anti-adjacent, i.e., $A \cap B = \emptyset$ and $E ( A , B ) = \emptyset$ 

2. Let A be maximal h-clique $\lambda _ { 1 } \cdot$ -compact and let B be maximal h-clique λ<sub>2</sub>-compact, where $\lambda _ { 1 } > \lambda _ { 2 }$ . Then either $A \subseteq B$ , or A and B are vertexdisjoint and anti-adjacent. 

Consequently, after duplicate vertex sets are identified, all maximal h-clique λ- compact subgraphs over all $\lambda \geq 0$ form a rooted forest under set inclusion. This is a finite forest; its roots are the connected components of $G$ (the maximal sets at level $\lambda = 0 )$ , and a leaf is a node containing no proper hierarchy node. 

Proof. For the first statement, suppose that two distinct maximal h-clique λ- compact sets A and B overlap or are adjacent. $\mathrm { B y }$ Lemma 1.8, A ∪ B is h-clique λ-compact. Since $A \neq B$ , at least one of A and $B$ is a proper subset of $A \cup B$ which contradicts its maximality. Hence distinct maximal sets at the same level are disjoint and anti-adjacent. 

For the second statement, an h-clique $\lambda _ { \mathrm { 1 - c o m p a c t } }$ set is also h-clique $\lambda _ { 2 ^ { - } }$ compact because $\lambda _ { 1 } > \lambda _ { 2 }$ . If A and B overlap or are adjacent, Lemma 1.8 implies that $A \cup B$ is h-clique λ<sub>2</sub>-compact. The maximality of B at level $\lambda _ { 2 }$ forces $A \cup B = B$ , and hence $A \subseteq B$ . Otherwise they are disjoint and antiadjacent. These alternatives are precisely laminarity. □ 

Theorem 1.10 (Leaf characterization). Let ${ \mathcal { H } } _ { h } ( G )$ be the inclusion forest whose nodes are all distinct maximal h-clique λ-compact vertex sets over all $\lambda \geq 0$ . A node of ${ \mathcal { H } } _ { h } ( G )$ is a leaf if and only if it induces an LhCDS. 

Proof. Let S be a node, so $S$ is maximal h-clique λ-compact for at least one λ. Assume first that $G [ S ]$ is not an LhCDS. By Lemma 1.7, S contains an h-clique $\lambda ^ { \prime } .$ -compact set $T$ with $\lambda ^ { \prime } > \eta _ { h } ( S )$ . Extend $T$ to a maximal h-clique $\lambda ^ { \prime } -$ compact set $M ;$ such an extension exists because G is finite. The sets M and S intersect. Since S is maximal at some level $\lambda \le \eta _ { h } ( S ) < \lambda ^ { \prime }$ , Theorem 1.9 implies $M \subseteq S$ . The containment is proper because $S$ is not h-clique λ<sup>′</sup>-compact. Thus S has a proper descendant and is not a leaf. 

Conversely, suppose that S is an LhCDS and that a hierarchy node $M \subsetneq S$ exists. Let M be maximal h-clique γ-compact. Since S is an LhCDS, $\eta _ { h } ( S ) =$ $d _ { h } ( S )$ . If $\gamma \leq \eta _ { h } ( S )$ , then S itself is h-clique γ-compact, contradicting the maximality of M. $\mathrm { I f } \ \gamma > \ \eta _ { h } ( S )$ , then M contradicts Lemma 1.7. Therefore no proper hierarchy node is contained in $S ,$ and S is a leaf. □ 

## 1.3 A parametric h-clique decomposition

For $\lambda \geq 0$ , define 

$$
Q _ {\lambda} (S) := \mu_ {h} (S) - \lambda | S |, \qquad S \subseteq V,\tag{4}
$$

and let 

$$
F _ {h} (\lambda) := \text { the   unique   inclusion - wise   largest   maximizer   of } Q _ {\lambda} (S).\tag{5}
$$

The largest-maximizer convention is essential at a breakpoint and replaces an artificial infinitesimal perturbation of λ. 

Lemma 1.11 (Supermodularity). For all $A , B \subseteq V$ 2 

$$
\mu_ {h} (A) + \mu_ {h} (B) \leq \mu_ {h} (A \cup B) + \mu_ {h} (A \cap B).\tag{6}
$$

Consequen $t l y , Q _ { \lambda }$ is supermodular for every λ; its maximizers are closed under union and intersection; and $F _ { h } ( \lambda )$ is well-defined. 

Proof. For each h-clique C of G, let $f _ { C } ( S ) = 1 { \mathrm { ~ i f ~ } } C \subseteq S$ and let $f _ { C } ( S ) = 0$ otherwise. A direct case analysis gives 

$$
f _ {C} (A) + f _ {C} (B) \leq f _ {C} (A \cup B) + f _ {C} (A \cap B).
$$

Summing over all h-cliques proves Equation (6). Since $| S |$ is modular, subtracting λ|S| preserves supermodularity. 

If A and B both attain the maximum value M of $Q _ { \lambda }$ , then 

$$
Q _ {\lambda} (A \cup B) + Q _ {\lambda} (A \cap B) \geq Q _ {\lambda} (A) + Q _ {\lambda} (B) = 2 M.
$$

Neither term on the left exceeds M, so both equal M. Thus the union of all maximizers is itself a maximizer and is their unique inclusion-wise largest member. □ 

Lemma 1.12 (Nestedness of the parametric maximizers). $I f 0 \leq \lambda _ { 1 } < \lambda _ { 2 }$ , then 

$$
F _ {h} (\lambda_ {2}) \subseteq F _ {h} (\lambda_ {1}).
$$

Proof. Let $A : = F _ { h } ( \lambda _ { 1 } )$ and $B : = F _ { h } ( \lambda _ { 2 } )$ . Optimality gives 

$$
Q _ {\lambda_ {1}} (A) \geq Q _ {\lambda_ {1}} (A \cup B) \quad \text { and } \quad Q _ {\lambda_ {2}} (B) \geq Q _ {\lambda_ {2}} (A \cap B).
$$

Adding the inequalities and applying the definition of $Q _ { \lambda } ( S )$ then rearranging gives 

$$
\begin{array}{l} 0 \leq \mu_ {h} (A) + \mu_ {h} (B) - \mu_ {h} (A \cup B) - \mu_ {h} (A \cap B) \\ \quad - (\lambda_ {2} - \lambda_ {1}) | B \setminus A |. \end{array}
$$

The first line is nonpositive by Lemma 1.11, whereas the second term is strictly negative if $B \setminus A \neq \emptyset$ . Therefore $B \setminus A = \emptyset$ , proving $B \subseteq A$ □ 

Theorem 1.13 (Parametric characterization of maximal compact subgraphs). For every $\lambda \geq 0$ , the connected components of $G [ F _ { h } ( \lambda ) ]$ are exactly the maximal h-clique λ-compact subgraphs of G. 

Proof. Write $F : = F _ { h } ( \boldsymbol { \lambda } )$ 

First, let C be a connected component of $G [ F ]$ . For arbitrary $U \subseteq C .$ , no h-clique contains vertices from both C and $F \setminus C$ , because there is no edge between distinct connected components. Hence 

$$
\mu_ {h} (F) - \mu_ {h} (F \setminus U) = \mu_ {h} (C) - \mu_ {h} (C \setminus U) = \Delta_ {h} (U; C).
$$

Optimality of F against $F \setminus U$ gives 

$$
0 \leq Q _ {\lambda} (F) - Q _ {\lambda} (F \setminus U) = \Delta_ {h} (U; C) - \lambda | U |.
$$

Thus C is h-clique λ-compact. 

We next prove that C is maximal. Suppose that a proper superset $T \supseteq C$ is h-clique λ-compact. Since C is a full connected component of F and $T$ is connected, $T \setminus F \neq \emptyset$ . Applying compactness of T to $T \setminus F$ gives 

$$
\mu_ {h} (T) - \mu_ {h} (T \cap F) \geq \lambda | T \setminus F |.\tag{7}
$$

By supermodularity, 

$$
\mu_ {h} (F \cup T) - \mu_ {h} (F) \geq \mu_ {h} (T) - \mu_ {h} (F \cap T).
$$

Combining this with Equation (7) yields $Q _ { \lambda } ( F \cup T ) \geq Q _ { \lambda } ( F )$ . Thus $F \cup T$ is also a maximizer, but it strictly contains the largest maximizer $F .$ , a contradiction. Therefore every component of $F$ is maximal h-clique λ-compact. 

Conversely, let M be a maximal h-clique λ-compact set. Compactness applied to $M \setminus F$ , followed by supermodularity, gives 

$$
\begin{array}{c} \mu_ {h} (F \cup M) - \mu_ {h} (F) \geq \mu_ {h} (M) - \mu_ {h} (F \cap M) \\ \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \lambda | M \setminus F |. \end{array}
$$

Hence $Q _ { \lambda } ( F \cup M ) \geq Q _ { \lambda } ( F )$ . The largest-maximizer convention forces $M \subseteq F .$ Since M is connected, it is contained in one connected component C of $G [ F ]$ The first part of the proof shows that C is h-clique λ-compact, so maximality of M implies $M = C$ □ 

Theorem 1.14 (Principal chain and critical densities). As λ decreases from +∞ to 0, the distinct values of $F _ { h } ( \lambda )$ form a strictly nested chain 

$$
\varnothing = B _ {0} \subsetneq B _ {1} \subsetneq \dots \subsetneq B _ {r} = V, \quad r \leq | V |.\tag{8}
$$

For $i = 1 , \ldots , r ,$ , define 

$$
\beta_ {i} := \frac {\mu_ {h} (B _ {i}) - \mu_ {h} (B _ {i - 1})}{| B _ {i} | - | B _ {i - 1} |}.\tag{9}
$$

Then 

$$
\beta_ {1} > \beta_ {2} > \dots > \beta_ {r} \geq 0,
$$

and, with the conventions $\beta _ { 0 } : = + \infty$ and $\beta _ { r + 1 } : = - \infty$ , for every $\lambda > 0$ and every $i \in \{ 0 , 1 , \ldots , r \}$ 

$$
F _ {h} (\lambda) = B _ {i} \quad \Longleftrightarrow \quad \max \{0, \beta_ {i + 1} \} <   \lambda \leq \beta_ {i}.\tag{10}
$$

Moreover, $F _ { h } ( 0 ) = B _ { r } = V$ 

Equivalently, $\beta _ { i }$ is the breakpoint at which the largest maximizer changes from $B _ { i - 1 }$ to $B _ { i }$ as λ decreases. 

Proof. For each $S \subseteq V , Q _ { \lambda } ( S ) \ : = \ : \mu _ { h } ( S ) - \lambda | S |$ is an afine function of λ. Since there are finitely many vertex sets, the pointwise maximum of these functions has finitely many breakpoints and is afine between consecutive breakpoints. Hence $F _ { h } ( \lambda )$ is constant on every open interval containing no breakpoint. Lemma 1.12 implies that its distinct values, listed as λ decreases, are nested, yielding Equation (8). A strict inclusion introduces at least one new vertex, so $r \leq | V |$ 

If $\lambda > \operatorname* { m a x } _ { \mathcal { O } \neq S \subseteq V } d _ { h } ( S )$ , then $Q _ { \lambda } ( S ) < 0 = Q _ { \lambda } ( \emptyset )$ for every nonempty $S _ { ; }$ so the first set is $B _ { 0 } = \varnothing$ . At $\lambda = 0$ , clique count is monotone under vertex inclusion, and $V$ is the largest maximizer; hence $B _ { r } = V$ 

Let $\tau _ { i }$ be the parameter at which the largest maximizer changes from $B _ { i - 1 }$ to $B _ { i }$ . Immediately above $\tau _ { i }$ the former set is optimal, and immediately below $\tau _ { i }$ the latter set is optimal when $\tau _ { i } > 0 ;$ when $\tau _ { i } = 0$ , the latter set is $V$ and is optimal at zero. Continuity of the two afine objective functions therefore gives 

$$
\mu_ {h} (B _ {i}) - \tau_ {i} | B _ {i} | = \mu_ {h} (B _ {i - 1}) - \tau_ {i} | B _ {i - 1} |.
$$

Since $\left| B _ { i } \right| > \left| B _ { i - 1 } \right| .$ , rearranging shows that $\tau _ { i } = \beta _ { i }$ as defined in Equation (9). 

Distinct transitions are encountered at strictly decreasing parameter values. Indeed, if two alleged consecutive changes occurred at the same parameter, the largest-maximizer rule at that parameter would select the largest of the tied sets, and the intermediate set would never be a distinct value of $F _ { h }$ . Consequently $\beta _ { 1 } > \cdots > \beta _ { r } \geq 0$ 

It remains to identify $F _ { h }$ at a breakpoint $\beta _ { i } \ > \ 0$ Pick any $\lambda ^ { - }$ with ma $\{ 0 , \beta _ { i + 1 } \} < \lambda ^ { - } < \beta _ { i } ;$ on this open interval between consecutive breakpoints the largest maximizer is $B _ { i }$ . The pointwise maximum of the finitely many afine functions $\lambda \mapsto Q _ { \lambda } ( S )$ is continuous in $\lambda ;$ approaching $\beta _ { i }$ from below along values where $B _ { i }$ is optimal shows that $B _ { i }$ is still optimal at $\lambda = \beta _ { i } .$ , so $B _ { i } \subseteq F _ { h } ( \beta _ { i } )$ because $F _ { h } ( \beta _ { i } )$ is the union of all maximizers at $\beta _ { i }$ . Conversely, Lemma 1.12 applied to $\lambda ^ { - } < \beta _ { i }$ gives $F _ { h } ( \beta _ { i } ) \subseteq F _ { h } ( \lambda ^ { - } ) = B _ { i }$ . Hence $F _ { h } ( \beta _ { i } ) = B _ { i }$ : at the upper endpoint $\lambda = \beta _ { i }$ the rule selects $B _ { i } ,$ , and by the same argument at the lower endpoint $\lambda = \beta _ { i + 1 }$ it selects $B _ { i + 1 }$ . There is no breakpoint in between. This proves Equation (10), with $\lambda = 0$ handled by the already proved identity $F _ { h } ( 0 ) = V$ and with the case $i = 0$ read of from $Q _ { \lambda } ( S ) < 0 = Q _ { \lambda } ( \emptyset )$ for all nonempty $S$ whenever $\lambda > \beta _ { 1 }$ : indeed, if some nonempty S had $d _ { h } ( S ) \geq \lambda > \beta _ { 1 }$ , then $Q _ { \beta _ { 1 } } ( S ) > 0$ would hold, whereas max<sub>T</sub> $Q _ { \beta _ { 1 } } ( T ) = Q _ { \beta _ { 1 } } ( B _ { 1 } ) = Q _ { \beta _ { 1 } } ( \emptyset ) = 0$ □ 

## 1.4 Divide-and-conquer separation and leaf extraction

For two chain sets $X \subsetneq Y$ , define their outer h-clique density by 

$$
d _ {h} (Y, X) := \frac {\mu_ {h} (Y) - \mu_ {h} (X)}{| Y | - | X |}.\tag{11}
$$

It counts every newly completed h-clique exactly once, including cliques whose vertices lie on both sides of the boundary of $X$ . 

Lemma 1.15 (Exact divide-and-conquer separator). Let $X = B _ { i }$ and $Y = B _ { j }$ for $0 \leq i < j \leq r$ , and set 

$$
\lambda := d _ {h} (Y, X), \qquad Z := F _ {h} (\lambda).
$$

Then the following statements hold. 

1. $I f j = i + 1$ , then $Z = Y$ 

2. $I f j > i + 1$ , then $Z = B _ { \ell }$ for some $i < \ell < j ,$ equivalently, $X \subsetneq Z \subsetneq Y$ 

Thus $Z = Y$ if and only if no principal-chain set lies strictly between X and $Y$ . 

Proof. Let $n _ { t } : = | B _ { t } | - | B _ { t - 1 } | > 0$ . By Equation (9), 

$$
\mu_ {h} (B _ {t}) - \mu_ {h} (B _ {t - 1}) = \beta_ {t} n _ {t}.
$$

Telescoping therefore gives 

$$
d _ {h} (B _ {j}, B _ {i}) = \frac {\sum_ {t = i + 1} ^ {j} \beta_ {t} n _ {t}}{\sum_ {t = i + 1} ^ {j} n _ {t}},\tag{12}
$$

which is a weighted average of $\beta _ { i + 1 } , \ldots , \beta _ { j }$ 

If $j = i + 1$ , Equation (12) gives $\lambda = \beta _ { j }$ , and the breakpoint convention in Theorem 1.14 yields $F _ { h } ( \lambda ) = B _ { j } = Y$ 

If $j > i + 1$ , strict decrease of the $\beta _ { t }$ values implies 

$$
\beta_ {j} <   \lambda <   \beta_ {i + 1}.
$$

By Equation (10), $F _ { h } ( \lambda ) = B _ { \ell }$ for an index satisfying $i < \ell < j$ 

Call an LhCDS born at layer i if i is the smallest index for which it is a connected component of $G [ B _ { i } ]$ 

Theorem 1.16 (Layer-wise extraction of LhCDSes). For each $i \in \{ 1 , \ldots , r \}$ ， the LhCDSes born at layer i are exactly the connected components W $o f G [ B _ { i } \rangle$ $B _ { i - 1 } ]$ satisfying 

$$
E (W, B _ {i - 1}) = \varnothing .\tag{13}
$$

Every such W satisfies 

$$
\eta_ {h} (W) = d _ {h} (W) = \beta_ {i}.\tag{14}
$$

Consequently, all LhCDSes born in the same layer have the same density, and layers enumerate LhCDSes in strictly decreasing density order. 

Proof. Let W be a connected component of $G [ B _ { i } \ \backslash \ B _ { i - 1 } ]$ satisfying Equation (13). Then W has no edge to any vertex of $B _ { i } \setminus W ,$ , so it is a connected component of $G [ B _ { i } ]$ . By Theorem 1.13, W is maximal h-clique $\beta _ { i } .$ -compact. (Theorem 1.13 is applied at a parameter whose largest maximizer is $B _ { i } \colon$ at $\lambda = \beta _ { i }$ when $\beta _ { i } > 0$ , using $F _ { h } ( \beta _ { i } ) = B _ { i }$ from Equation (10), and at $\lambda = 0$ when $i = r$ and $\beta _ { r } = 0$ , using $F _ { h } ( 0 ) = B _ { r }$ . These cases are exhaustive because $\beta _ { i } > \beta _ { r } \geq 0$ for every $i < r . )$ ) 

No proper hierarchy node $M \subsetneq W$ can be maximal at a level $\gamma \leq \beta _ { i } ,$ because W is itself h-clique γ-compact and would contradict the maximality of M. Nor can a hierarchy node $M \subsetneq W$ be maximal at a level $\gamma > \beta _ { i }$ . By Equation (10) in Theorem 1.14, 

$$
F _ {h} (\gamma) \subseteq B _ {i - 1}.
$$

By Theorem 1.13, M is a connected component of $G [ F _ { h } ( \gamma ) ]$ , and hence $M \subseteq$ $B _ { i - 1 }$ . This contradicts $M \subseteq W$ and $W \cap B _ { i - 1 } = \emptyset$ . Hence W is a leaf of the compactness hierarchy and is an LhCDS by Theorem 1.10. Moreover, i is the smallest index for which W is a connected component of $G [ B _ { m } ]$ : for $m \ < \ i .$ every connected component of $G [ B _ { m } ]$ is contained in $B _ { m } \subseteq B _ { i - 1 }$ , whereas W ∩ $B _ { i - 1 } = \emptyset$ . Hence W is born at layer i. 

Since W is h-clique β<sub>i</sub>-compact, $\eta _ { h } ( W ) \geq \beta _ { i }$ . If $\eta _ { h } ( W ) > \beta _ { i }$ , choose λ<sup>′</sup> with $\beta _ { i } < \lambda ^ { \prime } \leq \eta _ { h } ( W )$ and extend W to a maximal h-clique λ<sup>′</sup>-compact set M. By Equation (10) in Theorem 1.14, $F _ { h } ( \lambda ^ { \prime } ) \subseteq B _ { i - 1 }$ , while Theorem 1.13 gives $M \subseteq F _ { h } ( \lambda ^ { \prime } )$ . Thus $W \subseteq M \subseteq B _ { i - 1 }$ , contradicting $W \cap B _ { i - 1 } = \emptyset$ . Therefore $\eta _ { h } ( W ) = \beta _ { i }$ . Because W is an LhCDS, $\eta _ { h } ( W ) = d _ { h } ( W )$ , proving Equation (14). 

For the converse, let S be an LhCDS. By Theorem 1.10, S is a leaf node of the hierarchy. Choose the smallest i for which S is a connected component of $G [ B _ { i } ] ;$ such an i exists by Theorem 1.13. If S intersected $B _ { i - 1 }$ , it would contain a connected component of $G [ B _ { i - 1 } ]$ . That component is a hierarchy node by Theorem 1.13 and is a proper subset of S by the minimality of $i ,$ contradicting that S is a leaf. Thus $S \cap B _ { i - 1 } = \emptyset$ . Because S is a connected component of $G [ B _ { i } ]$ , it is a connected component of $G [ B _ { i } \setminus B _ { i - 1 } ]$ and has no edge to $B _ { i - 1 }$ 

Finally, $\beta _ { 1 } > \cdots > \beta _ { r }$ by Theorem 1.14, so the layer order is the strict density order. □ 

(The use of ordinary edges in Equation (13) is suficient: connectivity in Definition 1.1 is ordinary graph connectivity, and any h-clique crossing from $W$ to $B _ { i - 1 }$ necessarily contains at least one crossing edge. 

In the next theorem, candidate verification means directly testing a reported set against all deletion subsets, self-denseness, or maximal compactness. Connected-component construction and the layer adjacency filter are structural extraction operations.) 

Theorem 1.17 (Correctness of candidate-verification-free divide-and-conquer). Assume that every oracle call returns the exact largest maximizer $F _ { h } ( \lambda )$ . Consider the following recursive procedure on two principal-chain sets $X \subsetneq Y$ 

1. Set $\lambda  d _ { h } ( Y , X )$ and $Z \gets F _ { h } ( \lambda )$ 

2. If $Z = Y$ , visit, in the fixed tie-breaking order $\prec ,$ every connected component W of $G [ Y \backslash X ]$ with $E ( W , X ) = \emptyset$ , emitting the components one at a time. 

3. If $Z \neq Y$ , recurse first on (X, Z) and then on $( Z , Y )$ 

Starting from $( \varnothing , V )$ , the procedure reports every LhCDS exactly once. If emission is stopped after min $\{ k , q \}$ outputs (or when $k > q )$ , the reported subgraphs are top-k LhCDSes (under the convention stated above). 

Proof. We first record the invariant that every call receives a pair of principalchain sets $X = B _ { i } \subsetneq Y = B _ { j }$ with $0 \leq i < j \leq r .$ The initial pair $( \varnothing , V ) =$ $( B _ { 0 } , B _ { r } )$ satisfies it, and whenever it holds, Lemma 1.15 shows that $Z = F _ { h } ( \boldsymbol { \lambda } )$ is again a chain set with $X \subsetneq Z \subseteq Y$ , so both children $( X , Z )$ and $( Z , Y )$ of a nonterminal call satisfy the invariant as well. In particular, $X \subsetneq F _ { h } ( \lambda ) \subseteq Y$ holds at every call (exactly as the assumption of Section 1.5 mentioned below). 

By Lemma 1.15, every nonterminal call splits one contiguous principal-chain interval into two strictly smaller contiguous intervals; a terminal call corresponds to two consecutive chain sets. Therefore the recursion partitions the entire chain into its consecutive pairs $( B _ { i - 1 } , B _ { i } )$ . 

At a terminal pair, Theorem 1.16 shows that the reported components are exactly the LhCDSes born in that layer. The left recursive interval contains only smaller layer indices than the right interval. Since the critical densities are strictly decreasing, a left-first traversal outputs layers (LhCDSes) in nonincreasing density order. Within a layer all densities are equal, and the fixed order ≺ gives the stipulated tie-breaking order. Stopping after min $\{ k , q \}$ outputs is consequently exact. If need a tie-inclusive answer, we finish the terminal layer in which the kth output occurs. The terminal test consists only of connected-component construction and the adjacency check $E ( W , X ) = \emptyset ;$ LhCDS correctness follows. □ 

Corollary 1.18 (Number of parametric-oracle calls). If the full chain has r nonempty increments, the complete recursion invokes the $F _ { h }$ oracle at most $2 r - 1 \leq 2 | V | - 1$ times. A top-k execution may terminate earlier, although this bound alone does not imply an output-sensitive running time. 

Proof. At every nonterminal call, Lemma 1.15 gives $X \subsetneq Z \subsetneq Y$ , so both child intervals are strictly smaller than the parent interval and the recursion terminates. Its recursion tree is a binary tree in which every internal node has exactly two children; with one leaf for each of the r consecutive chain intervals it therefore has exactly $r - 1$ internal nodes, and a complete run makes exactly $2 r - 1$ oracle calls. □ 

## 1.5 An exact integer-capacity oracle for $F _ { h } ( \lambda )$

The hierarchy theorem is independent of how $F _ { h } ( \lambda )$ is computed. For completeness, we give an exact maximum-closure construction that (i) works for arbitrary h, (ii) restricts computation to any certified interval, and (iii) implements the largest-maximizer tie-break in a single integer-capacity minimum cut. 

Assume that $X , Y \subseteq V$ are known vertex sets satisfying 

$$
X \subsetneq F _ {h} (\lambda) \subseteq Y,
$$

and write $\lambda = a / b$ with coprime integers $a \geq 0$ and $b > 0$ . Let $N : = | Y \backslash X |$ . For each h-clique $C \in \Psi _ { h } ( Y )$ with $C \not \subseteq X$ , define its nonempty residual footprint 

$$
R _ {C} := C \setminus X \subseteq Y \setminus X.
$$

Equal residual footprints may be aggregated. Let 

$$
w (R) := | \{C \in \Psi_ {h} (Y): C \setminus X = R \} |.
$$

For $S \subseteq Y \setminus X$ 9 

$$
\mu_ {h} (X \cup S) - \mu_ {h} (X) = \sum_ {\varnothing \neq R \subseteq Y \setminus X} w (R)   \mathbf {1} [ R \subseteq S ].\tag{15}
$$

In every divide-and-conquer call, $\lambda = d _ { h } ( Y , X )$ is rational and Lemma 1.15 guarantees $X \subsetneq F _ { h } ( \lambda ) \subseteq Y$ . Thus the interval assumption above is automatic for every oracle call; the case $\lambda = 0$ is handled separately below. 

Theorem 1.19 (One-cut exact oracle with lexicographic tie-breaking). Under the interval and rationality assumptions above, suppose $a > 0 ,$ and set $L : =$ $N + 1$ . Construct a directed closure network containing one node $p _ { R } \ f o r$ every residual footprint with $w ( R ) > 0$ and one node for every vertex $v \in Y \setminus X$ Assign node weights 

$$
\omega (p _ {R}) := L b   w (R), \qquad \omega (v) := 1 - L a.
$$

Let 

$$
M _ {\infty} := 1 + \sum_ {R} L b w (R) + N (L a - 1).
$$

For every $v \in R ,$ add an implication arc $p _ { R }  v$ of capacity $M _ { \infty }$ . Convert the maximum-weight closure instance into an s–t cut by adding $s  p _ { R }$ with capacity $L b w ( R )$ , adding $v  t$ with capacity $L a - 1$ , and using the implication capacities just defined. Let $S ^ { * }$ be the vertex nodes on the source side of a minimum cut. Then 

$$
F _ {h} (\lambda) = X \cup S ^ {*}.
$$

For $a = 0$ , the largest maximizer in the interval is ${ \mathit { Y } } ,$ so no cut is needed. 

Proof. A positive numerator gives $a \ge 1$ , while $N \geq 1$ and hence $L \ge 2 ;$ in particular, every stated finite capacity is a nonnegative integer. The value $M _ { \infty }$ is larger than the sum of all source and sink capacities, so no minimum cut crosses an implication arc. Its source side is therefore closed: it may contain $p _ { R }$ only if it contains every vertex in R. Since $\omega ( p _ { R } ) > 0$ , once all vertices of R are selected, an optimal closure also selects $p _ { R }$ . Therefore the closure weight induced by a selected vertex set $S \subseteq Y \setminus X$ is 

$$
\begin{array}{c} W (S) = L b \sum_ {R} w (R) \mathbf {1} [ R \subseteq S ] + (1 - L a) | S | \\ = L \Big (b \big (\mu_ {h} (X \cup S) - \mu_ {h} (X) \big) - a | S | \Big) + | S |, \end{array}
$$

where Equation (15) is used in the second line. The expression in parentheses is the integer-scaled primary objective $Q _ { \lambda } ( X \cup S )$ up to a constant independent of S. Any two distinct primary values difer by at least one. Since $L = N + 1$ and the secondary term |S| lies in $[ 0 , N ]$ , maximizing $W ( S )$ first maximizes the primary objective and, among primary maximizers, maximizes |S|. 

By Lemma 1.11, primary maximizers are closed under union. Hence their union is the unique inclusion-wise largest maximizer and also the unique one of maximum cardinality. Thus the selected set is exactly the largest restricted maximizer. In particular the maximizer of $W$ is unique, and since the source side of every minimum cut is a maximum-weight closure, every minimum cut has the same source side; the set $S ^ { * }$ is therefore well-defined. Because $F _ { h } ( \lambda )$ is feasible in the interval $[ X , Y ]$ , that restricted largest maximizer equals the global $F _ { h } ( \lambda )$ : every restricted maximizer attains the global optimum value, hence is a global maximizer and is contained in $F _ { h } ( \lambda )$ , while $F _ { h } ( \lambda )$ itself lies in the interval. The standard maximum-closure/minimum-cut reduction proves that the source side of a minimum cut returns this set. If $a = 0$ , clique count is monotone and the largest-maximizer rule returns all of $Y ;$ moreover, $\lambda = 0$ together with the interval assumption $F _ { h } ( 0 ) \subseteq Y$ and the identity $F _ { h } ( 0 ) = V$ from Theorem 1.14 forces $Y = V$ , so returning Y coincides with the global $F _ { h } ( 0 )$ □ 

Corollary 1.20 (Polynomial implementability for fixed $h )$ . Let $n : = | V |$ and let P be the number of distinct positive-weight residual footprints in one oracle call. The closure network has $N + P + 2$ nodes and at most 

$$
N + P + \sum_ {R} | R | \leq N + (h + 1) P
$$

arcs. For fixed $h ,$ its footprints and weights can be constructed by enumerating at most ${ \binom { n } { h } } \ = \ O ( n ^ { h } )$ possible $h { - } c l i q u e s .$ , and the capacities used by the divide-and-conquer queries have polynomial bit length. Consequently, together with Corollary 1.18, the complete exact discovery procedure runs in polynomial time using any polynomial-time minimum-cut algorithm. This is a worst-case solvability statement, not an output-sensitive bound or a claim of practical scalability. 

Proof. Each positive residual footprint contributes one source arc and at most h implication arcs, and each interval vertex contributes one sink arc. In the divideand-conquer procedure, every queried $\lambda$ is a ratio of an integer clique-count diference and a positive integer vertex-count diference. The numerators, denominators, aggregated weights, and the scaling factor $L \leq n + 1$ therefore have polynomial bit length for fixed h. Clique enumeration, network construction, minimum cut, connected components, and adjacency checks are all polynomial, and there are at most $2 n - 1$ oracle calls. □ 

## 1.6 Safe high-density reduction

Definition 1.21 $( ( t , \Psi _ { h } ) – \mathrm { c o r e } )$ . For an integer $t \geq 0$ , the $( t , \Psi _ { h } ) \mathrm { - c o r e }$ of G is the inclusion-wise largest induced subgraph in which every vertex belongs to at least t h-cliques of that induced subgraph; denote its vertex set by $\mathrm { c o r e } _ { t , \Psi _ { h } } ( G )$ It is unique because this property is preserved when two qualifying vertex sets are replaced by their union. 

Lemma 1.22 (Clique-core containment). Every h-clique λ-compact set is contained in the $( \left\lceil \lambda \right\rceil , \Psi _ { h } )$ -core of G. In particular, for $\lambda > 0 , F _ { h } ( \lambda )$ is contained in that core. 

Proof. For any vertex v of an h-clique λ-compact set $S ,$ applying Equation (2) to $U = \{ v \}$ shows that the number of h-cliques of $G [ S ]$ containing v is at least $\lambda ,$ and hence at least ⌈λ⌉. Thus G[S] is contained in the maximal induced subgraph with this property. The claim for $F _ { h } ( \lambda )$ follows component-wise from Theorem 1.13. □ 

The $( t , \Psi _ { h } )$ -cores are nested as t increases. Hence, more precisely, if $\lambda _ { 0 } > 0$ is a certified lower bound and an oracle query satisfies $\lambda \geq \lambda _ { 0 }$ , then 

$$
F _ {h} (\lambda) \subseteq \operatorname{core} _ {\lceil \lambda \rceil , \Psi_ {h}} (G) \subseteq \operatorname{core} _ {\lceil \lambda_ {0} \rceil , \Psi_ {h}} (G).
$$

Thus that query may be restricted safely to the latter core. 

The target set $F _ { h } ( \lambda )$ lies in the core. The lower endpoint $X = B _ { i }$ is either empty or equals $F _ { h } ( \beta _ { i } )$ with $\beta _ { i } > \lambda \ge \lambda _ { 0 }$ (Equation (12) gives $\lambda \le \beta _ { i + 1 } < \beta _ { i } )$ ， so Lemma 1.22 places X inside cor $\mathsf { \Pi } ^ { * } \lceil \lambda _ { 0 } \rceil , \Psi _ { h } \left( G \right)$ as well. 

Set 

$$
Y ^ {\prime} := Y \cap \operatorname{core} _ {\lceil \lambda_ {0} \rceil , \Psi_ {h}} (G).
$$

Hence the restricted instance satisfies 

$$
X \subsetneq F _ {h} (\lambda) \subseteq Y ^ {\prime},
$$

and Theorem 1.19 applies with upper endpoint $Y ^ { \prime }$ . The set $Y ^ { \prime }$ need not itself be a principal-chain set, because the theorem requires only the certified interval containment displayed above. 

## 1.7 Main consequence

Theorem 1.23 (Candidate-verification-free solvability of top-k LhCDS discovery). Under Definitions 1.1–1.3, all distinct maximal h-clique λ-compact subgraphs over all $\lambda \geq 0$ form a laminar hierarchy whose leaves are exactly the LhCDSes. The principal chain induced by the largest maximizers of $\mu _ { h } ( S ) - \lambda | S |$ can be explored by the exact separator $\lambda = d _ { h } ( Y , X )$ . Consequently, the top-k LhCDSes can be returned exactly under the stated tie-breaking convention, without candidate verification, by a left-first divide-and-conquer traversal using the exact oracle of Theorem 1.19. For fixed h this is a finite polynomial-time algorithm. Cross-boundary h-cliques require no additional “boundary-safe” assumption: they are already included in $\mu _ { h }$ and contribute only nonnegative terms in the union-closure and parametric-supermodularity arguments. 

Proof. The laminar hierarchy follows from Lemma 1.8 and Theorem 1.9; its leaf characterization follows from Theorem 1.10. The parametric chain and its equivalence to maximal compact components follow from Theorems 1.13 and 1.14. Lemma 1.15 gives an exact recursive split; Theorem 1.16 identifies the leaves and orders them by density. The correctness and top-k stopping rule then follow from Theorem 1.17; exact implementability follows from Theorem 1.19 and Corollary 1.20. The treatment of cross-boundary cliques is clear from Lemma 1.8, Lemma 1.11, and Equation (11). □ 