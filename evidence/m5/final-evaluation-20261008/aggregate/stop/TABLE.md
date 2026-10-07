# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require every scheduled repetition of that algorithm/case to complete and pass validation. The required comparator is recorded per cell: main uses cutoff-tie agreement, core uses strict output, stop uses strict prefix agreement. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.236101 [0.221208, 0.266567] | 45776896 [31309824, 54018048] | 5 / 5 |
| ca-grqc-h3-k5 | vf-count-membership-all | 5 / 5 | {'completed': 5} | 0.432088 [0.413339, 0.445326] | 39452672 [31309824, 50380800] | 5 / 5 |
| ca-grqc-h4-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.872192 [1.859450, 1.915131] | 329285632 [314015744, 337051648] | 5 / 5 |
| ca-grqc-h4-k5 | vf-count-membership-all | 5 / 5 | {'completed': 5} | 2.570042 [2.555303, 2.578593] | 319995904 [261357568, 336756736] | 5 / 5 |
| ca-grqc-h5-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 12.753801 [12.642515, 12.841396] | 2161950720 [1949827072, 2185822208] | 5 / 5 |
| ca-grqc-h5-k5 | vf-count-membership-all | 5 / 5 | {'completed': 5} | 16.083932 [15.949110, 16.238861] | 2166816768 [2000306176, 2189115392] | 5 / 5 |
| ca-condmat-h3-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.584342 [1.568993, 1.600200] | 147865600 [123043840, 158580736] | 5 / 5 |
| ca-condmat-h3-k5 | vf-count-membership-all | 5 / 5 | {'completed': 5} | 3.668926 [3.605421, 3.690666] | 148307968 [126779392, 154075136] | 5 / 5 |
| ca-condmat-h4-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.972400 [1.936983, 2.013581] | 288686080 [268795904, 305790976] | 5 / 5 |
| ca-condmat-h4-k5 | vf-count-membership-all | 5 / 5 | {'completed': 5} | 6.285132 [6.233971, 6.328772] | 275906560 [270827520, 301580288] | 5 / 5 |
| ca-condmat-h5-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.870560 [3.853869, 3.908190] | 477200384 [468680704, 497434624] | 5 / 5 |
| ca-condmat-h5-k5 | vf-count-membership-all | 5 / 5 | {'completed': 5} | 10.326776 [10.201782, 10.417804] | 503988224 [487735296, 542834688] | 5 / 5 |
