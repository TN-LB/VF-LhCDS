# Claim-to-Code-to-Test Traceability

Update this table whenever theorem-dependent code changes. The exact theorem numbering should be synchronized with the final paper draft.

| Theory claim / invariant | Source section | Production module | Reference/test evidence | Status |
|---|---|---|---|---|
| LhCDS is a maximal h-clique `d_h(S)`-compact connected induced subgraph | Definitions 1.1–1.3 | output validator, reference checker | exhaustive definition tests | planned |
| Maximal compact subgraphs form a laminar hierarchy | hierarchy theorem | solver assumptions only | exhaustive nestedness tests | planned |
| Hierarchy leaves are exactly LhCDSes | leaf characterization | terminal extractor, solver | terminal-layer vs exhaustive LhCDS tests | planned |
| Components of `G[F_h(lambda)]` are maximal h-clique lambda-compact sets | parametric characterization | oracle/solver interface | exhaustive `F_h` and component tests | planned |
| Distinct `F_h(lambda)` sets form the principal chain | principal-chain theorem | interval recursion | exhaustive chain construction tests | planned |
| Outer-density query separates a nonconsecutive interval | set-separator theorem | `solver/divide_conquer` | consecutive/nonconsecutive interval tests | planned |
| Terminal components anti-adjacent to `X` are exactly the new leaves | layer extraction theorem | `solver/terminal_extractor` | terminal extraction differential tests | planned |
| Left-first recursion outputs nonincreasing density | top-k theorem | recursion/stack order | ranked end-to-end tests | planned |
| Full recursion uses at most `2r-1` oracle calls | complexity theorem | telemetry | exhaustive chain call-count test | planned |
| Residual-footprint identity reconstructs clique gain | oracle derivation | footprint aggregator | all-subset identity tests | planned |
| Closure network maximizes the scaled objective | exact oracle theorem | closure network, max flow | exhaustive objective/oracle tests | planned |
| `+|S|` tie term returns the largest maximizer | exact oracle theorem | capacity construction | dedicated tie tests | planned |
| h-clique core restriction is safe at certified threshold | core reduction theorem | clique core / reduced oracle | exhaustive reduced-vs-full oracle tests | planned |
| Fixed-k subset ordering is deterministic | top-k convention + project decision | top-k order, writer | duplicate-component tie tests | planned |
| No floating-point decision enters correctness path | engineering invariant | fraction, oracle, solver | static inspection + tests | planned |
| No capacity overflow is silent | engineering invariant | checked integer, flow | near-limit and failure tests | planned |

## Change protocol

When a row changes:

1. cite the exact proof paragraph or theorem name;
2. name the code symbol, not only a directory;
3. name deterministic and randomized tests;
4. record the commit implementing it;
5. set status to `verified` only after tests run in CI or the recorded environment.
