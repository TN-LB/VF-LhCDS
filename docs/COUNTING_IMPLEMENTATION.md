# Exact membership clique counting

P12.1 profile follow-up; O01/O04/O08/O11/O12, T04-COUNT and T04-COUNT-CLI.
The frozen `fine-profile-20261007` CondMat query prefix measures 57.092156 s
inside `MaterializedCliques::count` out of 59.650414 s accounted solve time.
That is evidence for this one optimization, not a complete-run speedup claim.

`CliqueCounting::Sorted` retains the original `subset(clique, set)` loop.
`CliqueCounting::Membership` validates the same canonical internal vertex set,
builds the existing exact `Membership` marker array once for this call, and
increments the same `BigInt` result iff every vertex of each materialized clique
is marked. No clique is added, removed, reordered, approximated or cached.

For a validated set S and any stored clique C, `subset(C,S)` is true exactly when
every v in C belongs to S, exactly when every marker lookup is true. Therefore
each loop increments on the same cliques, so both exact sums equal mu_h(S).
The graph and clique index are immutable. Counts of chain points and emitted
components are consequently unchanged, as are endpoint densities, separator
parameters, branching, ordering, ties and fixed-k stopping. A new local marker
array on every call prevents state from leaking between unrelated sets.

Preconditions remain the original ones: sorted, unique, in-range internal IDs;
the unchanged constructor requires h>=2 and a supported enumeration. Count mode
is also validated before the h>n early return. Empty sets, no cliques, h>n,
isolates, large original IDs and repeated/different queries retain their behavior.
The accumulator stays arbitrary precision. Extra O(n) marker memory/allocation
is charged to the selected mode's time/RSS and can make very small calls slower.
Worst-case inclusion work changes from O(M(|S|+h)) to O(n+|S|+Mh), where M is
the stored clique count; no bound on recursive query count is changed.

The index's fourth constructor argument and CLI `--clique-count sorted|membership`
select the mode; **sorted remains the default**. The CLI accepts the option for
solve/oracle, rejects it for inspect-graph, and preserves all existing argument,
result and status conventions. Existing semantic hashes and counters are unchanged;
`cliques_scanned` continues to count footprint visits, not count-function visits.
The experiment manifest records this implementation switch as `counting`.

Before measuring: test both modes and both enumerators across subsets and invalid
sets; run CLI modes, zero/h>n and malformed-option cases; rerun the existing M2
and M4 independent-reference corpus through membership-counting test probes in
Debug/ASan+UBSan; compare every saved response against the previous sorted-count
corpus excluding only measured core time. Include real automatic big-integer flow
execution. Finite equality validates the implementation, not the theorem.

Then use the already planned two graphs, h=3,k=5, three repetitions per count
mode, randomized paired order with seed 20261003, one worker, 60-second limits,
no memory cap, uncontrolled cache, no warmups/retries. Use one new Release binary
for both modes and separate validators. Retain timeouts and stop other failures;
do not launch another optimization cycle based on these results. Exact pins and
executed evidence belong in `evidence/m5/counting-20261007/`.
