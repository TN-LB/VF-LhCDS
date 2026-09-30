# External validation boundary

No production solver/library target depends on this directory. Independent truth
lives in `reference/`.

M1 adds `reference_campaign.py`: finite reference-only definition/parametric
consistency checks and reproducible case/failure records. It imports only Python
standard library and the independent reference. It runs no production solver,
closure network, recursive extraction or external baseline. M2 adds `oracle_campaign.py`, which communicates with the C++ test-only probe and
uses the unchanged reference for expected counts, footprints and largest sets.
It retains exhaustive-small, seeded and higher-h results independently of timings.
Production solver output validation and end-to-end P05.1 remain M3 work.


M3 `solver_campaign.py` compares complete and fixed-k production output with
independent direct definitions and chain points, saving cases/results/traces and
original/minimized failures. `run_solver.py` measures child-process end-to-end time
and keeps optional direct-definition validation outside that measurement. These
are correctness/evidence tools; benchmark fairness and baseline adapters remain M5.

M4 `m4_campaign.py` reuses the M3 independent truth corpus with four implementation
modes, all-subset definition cores and exact footprint records. It retains every
mode response and stops after saving the original failure. `m4_profile.py` retains
all fixed local timing/RSS repetitions; it is not an M5 benchmark campaign.
