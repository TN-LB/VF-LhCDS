# Decision Log

Use statuses: `proposed`, `accepted`, `rejected`, `superseded`, `needs-theory-clarification`.

| ID | Decision | Status | Rationale / evidence | Consequences |
|---|---|---|---|---|
| D001 | The proof file is the primary semantic authority | accepted | Prevents accidental import of edge-only or candidate-verification semantics | Conflicts trigger document/code correction |
| D002 | Build an independent Python exhaustive reference before production optimization | accepted | Needed for definition-level truth | Adds a second implementation path |
| D003 | Production solver uses C++17+ and CMake | proposed | Compatible with graph baselines and performance work | Confirm available compiler/hardware |
| D004 | Correctness decisions use exact rational/integer arithmetic only | accepted | Required by breakpoints, tie behavior, and capacities | No float epsilon logic |
| D005 | Initial production flow backend is deterministic Dinic with checked `unsigned __int128` capacities | proposed | Simple, inspectable first implementation | Must fail closed on overflow; benchmark alternatives later |
| D006 | Canonical subset order is lexicographic order of sorted original vertex-ID vectors | proposed | Gives deterministic fixed-k behavior | Confirm it matches intended paper convention |
| D007 | Canonical set ownership format is sorted internal vertex vector plus reusable membership markers | proposed | Avoids one dense bitset per recursion node | Profile before changing |
| D008 | Implement both materialized and streaming clique backend interfaces | proposed | Clique count can dominate either memory or repeated work | Materialized backend may be first complete path |
| D009 | Initial correct solver has no heuristic pruning | accepted | Keeps theorem-to-code path clean | Optimization begins after correctness tag |
| D010 | Safe h-clique-core reduction is the first structural pruning optimization | proposed | Explicitly supported by theory | Requires reduced-vs-full oracle differential tests |
| D011 | Baseline comparison is stratified by `h` | accepted | LDScvx is h=2 and LTDScvx is h=3 | No misleading general-h aggregation |
| D012 | Public `s01bvral/DCLDS` requires provenance review before novelty/SOTA claims | accepted | Its stated topic overlaps directly | May become baseline, related work, or own prior code |
| D013 | Final experiments report both end-to-end and solver-only time | proposed | Separates enumeration/I/O and core algorithm cost | Baseline timing scope must be audited |
| D014 | Fixed-cardinality top-k is default; kth-density tie-inclusive mode is optional and explicit | proposed | Matches proof draft's top-k convention | Wrappers need tie-aware validation |
| D015 | Isolated vertices are preserved or removed according to one documented policy | needs-theory-clarification | Zero-density LhCDS behavior can be affected | Decide before canonical preprocessing is frozen |
| D016 | Supported practical `h` range is explicit rather than silently accepting arbitrary huge `h` | proposed | Footprint key and clique enumeration depend on it | CLI rejects unsupported values clearly |

## Questions requiring owner confirmation

1. Is lexicographic vertex-set order acceptable for the fixed total order used to break density ties?
2. Should normalized graphs preserve isolated vertices present in the declared vertex count?
3. Is the first target only cliques, or should the code architecture immediately support general patterns?
4. Which final hardware environment and memory budget will be used?
5. Is the public DCLDS repository related to this project?
6. Is exact arbitrary-size integer support required, or is checked 128-bit capacity with explicit rejection acceptable for the experimental implementation?
7. Should `h=2` be a first-class supported mode in the proposed code or only a validation specialization?
