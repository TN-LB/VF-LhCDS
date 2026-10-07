# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require all three scheduled runs of that algorithm/case to complete and pass structural validation. Strict canonical output agreement is required for this ablation. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-count-sorted | 3 / 3 | {'completed': 3} | 0.349554 [0.342789, 0.533862] | 48349184 [45580288, 51281920] | 3 / 3 |
| ca-grqc-h3-k5 | vf-count-membership | 3 / 3 | {'completed': 3} | 0.250145 [0.230998, 0.597547] | 46694400 [45219840, 48578560] | 3 / 3 |
| ca-condmat-h3-k5 | vf-count-sorted | 3 / 3 | {'completed': 3} | 38.791546 [38.556403, 39.562047] | 149995520 [140427264, 150224896] | 3 / 3 |
| ca-condmat-h3-k5 | vf-count-membership | 3 / 3 | {'completed': 3} | 1.709334 [1.634339, 1.716649] | 141295616 [136855552, 155123712] | 3 / 3 |
