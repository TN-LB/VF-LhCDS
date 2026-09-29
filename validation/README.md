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
