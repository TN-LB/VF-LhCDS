# Proposed phase diagnosis — not executed

Static inspection found a concrete hypothesis: `MaterializedCliques` visits
every size-h vertex subset. For the preserved CA-GrQc input, n=5,242 and h=3,
that is 23,993,367,880 candidate triples for a complete index construction.
The CLI constructs this index before applying either M4 optimization. See
[the recorded source observation](static-observation.json). This describes
the code; it does not locate the timed-out processes in a measured phase.

Recommended next action: one bounded phase diagnostic, on the same normalized
graph and existing basic-mode semantics, with a 60-second process guard. Use a
separate diagnostic target to timestamp entry and completion of graph parsing,
materialized index construction, and solving. Phase markers must flush before
starting the next phase so timeout preserves the last reached boundary. Keep
its outputs separate from accepted algorithm timing/output evidence. Record
the diagnostic source, compiler flags, executable hash, native status and logs
before interpreting its result. No change to enumeration, closure, recursion,
tie rules or accepted solver output is included in this proposal.

If the constructor remains unfinished at timeout, record that observation and
prepare an independently designed clique-enumeration implementation change with
a preservation argument and output-equivalence test plan. Do not import DCLDS
techniques or silently replace the old measurements. No implementation repair
or enlarged runtime limit is authorized by this draft.

Alternative: choose the final experiment resource/scope policy first. This does
not resolve the current lack of a completed VF output on the shared real case.
The recommendation is phase diagnosis before choosing a larger timeout.

This is a proposal, not an executed run or approved final benchmark setting.
