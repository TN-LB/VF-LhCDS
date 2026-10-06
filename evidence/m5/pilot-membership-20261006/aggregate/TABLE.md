# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require all three scheduled runs of that algorithm/case to complete and pass structural validation. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-adjacency-membership | 3 / 3 | {'completed': 3} | 0.516958 [0.516040, 0.565907] | 48513024 [48185344, 49872896] | 3 / 3 |
| ca-grqc-h3-k5 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.178408 [0.175774, 0.182534] | 31145984 [30113792, 31686656] | 3 / 3 |
| ca-grqc-h3-k10 | vf-adjacency-membership | 3 / 3 | {'completed': 3} | 1.449934 [1.444478, 1.450237] | 49250304 [47562752, 49971200] | 3 / 3 |
| ca-grqc-h3-k10 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.199315 [0.196222, 0.234662] | 30687232 [28164096, 30867456] | 3 / 3 |
| ca-grqc-h3-k15 | vf-adjacency-membership | 3 / 3 | {'completed': 3} | 2.809717 [2.756681, 2.832843] | 52428800 [45367296, 54673408] | 3 / 3 |
| ca-grqc-h3-k15 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.254034 [0.249765, 0.255264] | 29032448 [28360704, 30081024] | 3 / 3 |
| ca-grqc-h3-k20 | vf-adjacency-membership | 3 / 3 | {'completed': 3} | 4.404297 [4.381004, 4.449048] | 44728320 [44269568, 49184768] | 3 / 3 |
| ca-grqc-h3-k20 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.280171 [0.274367, 0.282414] | 30556160 [28491776, 32292864] | 3 / 3 |
| ca-condmat-h3-k5 | vf-adjacency-membership | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k5 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 4.219049 [4.198684, 4.294278] | 151928832 [125108224, 154353664] | 0 / 3 |
| ca-condmat-h3-k10 | vf-adjacency-membership | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k10 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 7.222165 [7.151765, 7.559391] | 172113920 [169279488, 204652544] | 0 / 3 |
| ca-condmat-h3-k15 | vf-adjacency-membership | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k15 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 8.484404 [8.419385, 8.496807] | 205881344 [199786496, 210583552] | 0 / 3 |
| ca-condmat-h3-k20 | vf-adjacency-membership | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k20 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 8.618505 [8.556651, 8.724470] | 208961536 [206127104, 211812352] | 0 / 3 |
