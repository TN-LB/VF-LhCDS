# Decision Log

Use statuses: `proposed`, `accepted`, `rejected`, `superseded`, `needs-theory-clarification`.

| ID | Decision | Status | Rationale / evidence | Consequences |
|---|---|---|---|---|
| D001 | The proof file is the primary semantic authority | accepted | Prevents accidental import of edge-only or candidate-verification semantics | Conflicts trigger document/code correction |
| D002 | Build an independent Python exhaustive reference before production optimization | accepted | Needed for definition-level truth | Adds a second implementation path |
| D003 | Production solver uses C++17+ and CMake | accepted | Compatible with graph baselines and performance work | Confirm available compiler/hardware |
| D004 | Correctness decisions use exact rational/integer arithmetic only | accepted | Required by breakpoints, tie behavior, and capacities | No float epsilon logic |
| D005 | Initial production flow backend is deterministic Dinic with checked `unsigned __int128` capacities | accepted | Simple, inspectable first implementation | Never continue after an unchecked overflow. If the fixed-width capacity bound is not provably safe, automatically use the arbitrary-precision exact backend.; benchmark alternatives later |
| D006 | Canonical subset order is lexicographic order of sorted original vertex-ID vectors | accepted | Gives deterministic fixed-k behavior | Confirm it matches intended paper convention |
| D007 | Canonical set ownership format is sorted internal vertex vector plus reusable membership markers | accepted | Avoids one dense bitset per recursion node | Profile before changing |
| D008 | Implement both materialized and streaming clique backend interfaces | accepted | Clique count can dominate either memory or repeated work | Materialized backend may be first complete path |
| D009 | Initial correct solver has no heuristic pruning | accepted | Keeps theorem-to-code path clean | Optimization begins after correctness tag |
| D010 | Safe h-clique-core reduction is the first structural pruning optimization | accepted | Explicitly supported by theory | Requires reduced-vs-full oracle differential tests |
| D011 | Baseline comparison is stratified by `h` | accepted | LDScvx is h=2 and LTDScvx is h=3 | No misleading general-h aggregation |
| D012 | Zhou et al. (PVLDB 2026, DCLDS) is confirmed as an independent parallel study with substantial overlap. Freeze the current theory, algorithm design, and implementation state before detailed comparison. DCLDS must be cited and treated as a primary related-work and experimental baseline. Its techniques must not be incorporated into this algorithm unless explicitly approved and documented | accepted | Preserves a clear boundary between independently developed work and later knowledge of the parallel study | - |
| D013 | Final experiments report both end-to-end and solver-only time | accepted | Separates enumeration/I/O and core algorithm cost | Baseline timing scope must be audited |
| D014 | Fixed-cardinality top-k is default; kth-density tie-inclusive mode is optional and explicit | accepted | Matches proof draft's top-k convention | Wrappers need tie-aware validation |
| D015 | Isolated vertices are preserved or removed according to one documented policy | accepted | Zero-density LhCDS behavior can be affected | Decide before canonical preprocessing is frozen |
