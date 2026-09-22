# External validation boundary

No production solver/library target depends on this directory. Independent truth
lives in `reference/`.

M1 adds `reference_campaign.py`: finite reference-only definition/parametric
consistency checks and reproducible case/failure records. It imports only Python
standard library and the independent reference. It runs no production solver,
closure network, recursive extraction or external baseline. Production output
validation/differential harnesses (O12/P05.1) remain future work.
