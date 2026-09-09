# Decision Log

Use statuses: `proposed`, `accepted`, `rejected`, `superseded`, `needs-theory-clarification`, `specified-in-revision`.

Revision note (2026-09-09): original accepted choices remain in force unless a
superseding row is explicit. `specified-in-revision` records this authorized plan
revision, not a fabricated earlier owner confirmation. M0 reviews these contracts;
only new unresolved semantic/experimental choices require a separate decision.

| ID | Decision | Status | Rationale / evidence | Consequences |
|---|---|---|---|---|
| D001 | The proof file is the primary semantic authority | accepted | Prevents accidental import of edge-only or candidate-verification semantics | Conflicts trigger document/code correction |
| D002 | Build an independent Python exhaustive reference before production optimization | accepted | Needed for definition-level truth | Adds a second implementation path |
| D003 | Production solver uses C++17+ and CMake | accepted | Compatible with graph baselines and performance work | Confirm available compiler/hardware |
| D004 | Correctness decisions use exact rational/integer arithmetic only | accepted | Required by breakpoints, tie behavior, and capacities | No float epsilon logic |
| D005 | Initial production flow backend is deterministic Dinic with checked `unsigned __int128` capacities | accepted | Simple, inspectable first implementation | Never continue after an unchecked overflow. If the fixed-width capacity bound is not provably safe, automatically use the arbitrary-precision exact backend; benchmark alternatives later |
| D006 | Canonical subset order is lexicographic order of sorted original vertex-ID vectors | accepted | Gives deterministic fixed-k behavior | Use this fixed project total order; any later change is an explicit output-policy revision |
| D007 | Canonical set ownership format is sorted internal vertex vector plus reusable membership markers | accepted | Avoids one dense bitset per recursion node | Profile before changing |
| D008 | Implement both materialized and streaming clique backend interfaces | superseded | Initial scope duplicated optional work and contradicted release gates | D016 requires only materialized storage for the first correctness release |
| D009 | Initial correct solver has no heuristic pruning | accepted | Keeps theorem-to-code path clean | Optimization begins after correctness tag |
| D010 | Safe h-clique-core reduction is the first structural pruning optimization | accepted | Explicitly supported by theory | Requires reduced-vs-full oracle differential tests |
| D011 | Baseline comparison is stratified by `h` | accepted | LDScvx is h=2 and LTDScvx is h=3 | No misleading general-h aggregation |
| D012 | Zhou et al. (PVLDB 2026, DCLDS) is confirmed as an independent parallel study with substantial overlap. Freeze the current theory, algorithm design, and implementation state before detailed comparison. DCLDS must be cited and treated as a primary related-work and experimental baseline. Its techniques must not be incorporated into this algorithm unless explicitly approved and documented | accepted | Preserves a clear boundary between independently developed work and later knowledge of the parallel study | - |
| D013 | Final experiments report both end-to-end and solver-only time | accepted | Separates enumeration/I/O and core algorithm cost | Baseline timing scope must be audited |
| D014 | Fixed-cardinality top-k is default; kth-density tie-inclusive mode is optional and explicit | accepted | Matches proof draft's top-k convention | Wrappers need tie-aware validation |
| D015 | Isolated vertices are preserved or removed according to one documented policy | superseded | This did not actually specify the policy and allowed a change to V | D017 preserves every declared vertex under the manuscript domain |


## Decisions specified in the 2026-09-09 revision

| ID | Decision | Status | Reason / effect |
|---|---|---|---|
| D016 | Materialized clique storage only for M3; streaming and its equivalence gate are deferred | specified-in-revision | One minimal complete path; supersedes D008 |
| D017 | Preserve all declared vertices, including isolates; no automatic positive-density-only filter | specified-in-revision | Defs. 1.1-1.3 include zero-density solutions; supersedes D015 |
| D018 | Public solver requires k>=1; --all is explicit; tie-inclusive mode is deferred | specified-in-revision | Matches the manuscript domain and keeps one initial output contract |
| D019 | Split largest_restricted from certified global_F; allow equality/empty outcomes outside separator queries | specified-in-revision | Audit clarification A supplies the non-strict closure argument |
| D020 | Chain endpoints and lambda remain original; only oracle upper bound is core-reduced | specified-in-revision | Lemma 1.22 does not make the reduced upper set a principal-chain set |
| D021 | Main proof ledger has separate argument and execution evidence; no test-only proof labels | specified-in-revision | Prevents circular/overstated acceptance claims |
| D022 | Independent reference chain uses the exact cardinality-line envelope | specified-in-revision | Covers outer breakpoints without production recursion |
| D023 | M3 does not depend on baseline availability or optional optimization | specified-in-revision | Separates mathematical implementation from empirical work |
| D024 | DCLDS gets an explicit primary-baseline task after the required snapshot boundary | specified-in-revision | Implements accepted D012; does not reopen independence or authorize technique import |
| D025 | External validation evidence and algorithm timing have explicitly separate scopes | specified-in-revision | Structural checks alone do not prove maximality; native candidate verification remains timed |
| D026 | Narrow owner-confirmation rule to new consequential choices, not already settled or theorem-forced details | specified-in-revision | Reduces avoidable implementation blocking while preserving scientific decisions |

## Still to freeze before final experiments, not before core implementation

Machine/compiler profile, exact dataset versions/checksums, final h/k grid,
timeout/memory budgets, worker-thread protocol, filesystem-cache policy, repeats,
seed manifest, and exclusions. Do not invent accepted values or claim baseline
commits/licenses/builds were verified merely from a paper or README.
