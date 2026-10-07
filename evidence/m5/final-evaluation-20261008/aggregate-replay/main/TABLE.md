# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require every scheduled repetition of that algorithm/case to complete and pass validation. The required comparator is recorded per cell: main uses cutoff-tie agreement, core uses strict output, stop uses strict prefix agreement. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.239972 [0.230970, 0.262398] | 47120384 [45924352, 51134464] | 5 / 5 |
| ca-grqc-h3-k5 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 0.123710 [0.107986, 0.138914] | 30457856 [28131328, 32915456] | 5 / 5 |
| ca-grqc-h3-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.281676 [0.277680, 0.290482] | 47890432 [42844160, 51904512] | 5 / 5 |
| ca-grqc-h3-k10 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 0.132012 [0.127936, 0.138175] | 31293440 [27770880, 32178176] | 5 / 5 |
| ca-grqc-h3-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.324443 [0.319071, 0.352019] | 49807360 [45318144, 51757056] | 5 / 5 |
| ca-grqc-h3-k15 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 0.167906 [0.164799, 0.171142] | 32456704 [30375936, 33079296] | 5 / 5 |
| ca-grqc-h3-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.352457 [0.341774, 0.375172] | 48758784 [44171264, 54018048] | 5 / 5 |
| ca-grqc-h3-k20 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 0.183275 [0.182677, 0.184716] | 30883840 [30408704, 32309248] | 5 / 5 |
| ca-grqc-h4-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.914563 [1.874468, 2.026346] | 312672256 [303611904, 314818560] | 5 / 5 |
| ca-grqc-h4-k5 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 1.142424 [1.128401, 1.216507] | 297435136 [283181056, 301711360] | 5 / 5 |
| ca-grqc-h4-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.210457 [2.164972, 2.222296] | 305217536 [290193408, 318078976] | 5 / 5 |
| ca-grqc-h4-k10 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 1.135908 [1.109225, 1.214802] | 289488896 [284573696, 297598976] | 5 / 5 |
| ca-grqc-h4-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.293797 [2.218613, 2.337687] | 312967168 [298418176, 332283904] | 5 / 5 |
| ca-grqc-h4-k15 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 1.159046 [1.123760, 1.191947] | 293912576 [288178176, 297943040] | 5 / 5 |
| ca-grqc-h4-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.305021 [2.222465, 2.357350] | 307134464 [302432256, 309624832] | 5 / 5 |
| ca-grqc-h4-k20 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 1.162128 [1.153931, 1.267323] | 294486016 [280002560, 296435712] | 5 / 5 |
| ca-grqc-h5-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 13.106416 [12.872999, 13.385155] | 2059239424 [1939046400, 2143567872] | 5 / 5 |
| ca-grqc-h5-k5 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 9.919946 [9.709802, 10.195736] | 2173075456 [1964490752, 2453422080] | 5 / 5 |
| ca-grqc-h5-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.223643 [14.140348, 14.298751] | 2125185024 [1986707456, 2197340160] | 5 / 5 |
| ca-grqc-h5-k10 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 9.909919 [9.688215, 10.163659] | 2317123584 [1836826624, 2371354624] | 5 / 5 |
| ca-grqc-h5-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.494997 [14.367642, 14.528819] | 2135900160 [2040938496, 2163752960] | 5 / 5 |
| ca-grqc-h5-k15 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 9.920566 [9.683732, 10.348472] | 2237956096 [1752121344, 2431401984] | 5 / 5 |
| ca-grqc-h5-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.457536 [14.288860, 14.556922] | 2218901504 [2149924864, 2271166464] | 5 / 5 |
| ca-grqc-h5-k20 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 9.713126 [9.559613, 9.889138] | 2333376512 [2172420096, 2462007296] | 5 / 5 |
| ca-condmat-h3-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.600805 [1.562959, 1.612777] | 144015360 [129630208, 163086336] | 5 / 5 |
| ca-condmat-h3-k5 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 2.761199 [2.730057, 2.773414] | 171589632 [168607744, 177111040] | 5 / 5 |
| ca-condmat-h3-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.434332 [2.402943, 2.447578] | 132726784 [124518400, 140918784] | 5 / 5 |
| ca-condmat-h3-k10 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 4.920391 [4.896550, 5.003017] | 195280896 [184696832, 207585280] | 5 / 5 |
| ca-condmat-h3-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.982934 [2.942965, 3.036123] | 146341888 [141344768, 159662080] | 5 / 5 |
| ca-condmat-h3-k15 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 5.769325 [5.766312, 5.801950] | 199688192 [179126272, 210845696] | 5 / 5 |
| ca-condmat-h3-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.042262 [2.981430, 3.134164] | 151306240 [134381568, 155385856] | 5 / 5 |
| ca-condmat-h3-k20 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 5.922652 [5.836124, 6.036552] | 193069056 [185335808, 204750848] | 5 / 5 |
| ca-condmat-h4-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.952309 [1.917813, 1.972311] | 286654464 [283344896, 305545216] | 5 / 5 |
| ca-condmat-h4-k5 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 1.596234 [1.577837, 1.634913] | 251969536 [220397568, 263979008] | 5 / 5 |
| ca-condmat-h4-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.266568 [3.256626, 3.299872] | 276021248 [249266176, 289472512] | 5 / 5 |
| ca-condmat-h4-k10 | ippv-seven-patches | 5 / 5 | {'completed': 5} | 3.686611 [3.671361, 3.730209] | 313081856 [300793856, 316981248] | 5 / 5 |
| ca-condmat-h4-k15 | vf-count-membership-core-off | 1 / 5 | {'completed': 1} | unavailable | unavailable | 0 / 1 |
| ca-condmat-h4-k15 | ippv-seven-patches | 1 / 5 | {'completed': 1} | unavailable | unavailable | 0 / 1 |
| ca-condmat-h4-k20 | vf-count-membership-core-off | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h4-k20 | ippv-seven-patches | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k5 | vf-count-membership-core-off | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k5 | ippv-seven-patches | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k10 | vf-count-membership-core-off | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k10 | ippv-seven-patches | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k15 | vf-count-membership-core-off | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k15 | ippv-seven-patches | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k20 | vf-count-membership-core-off | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h5-k20 | ippv-seven-patches | 0 / 5 | {} | unavailable | unavailable | 0 / 0 |
