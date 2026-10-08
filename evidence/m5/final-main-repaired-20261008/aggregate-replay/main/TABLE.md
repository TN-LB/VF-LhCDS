# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require every scheduled repetition of that algorithm/case to complete and pass validation. The required comparator is recorded per cell: main uses cutoff-tie agreement, core uses strict output, stop uses strict prefix agreement. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.260179 [0.228050, 0.270892] | 52199424 [46710784, 55803904] | 5 / 5 |
| ca-grqc-h3-k5 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 0.116766 [0.109850, 0.123050] | 31752192 [30097408, 32014336] | 5 / 5 |
| ca-grqc-h3-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.291291 [0.280571, 0.320068] | 48906240 [44908544, 54820864] | 5 / 5 |
| ca-grqc-h3-k10 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 0.130094 [0.128033, 0.134627] | 28737536 [28704768, 30392320] | 5 / 5 |
| ca-grqc-h3-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.333358 [0.323588, 0.448516] | 54296576 [49872896, 55918592] | 5 / 5 |
| ca-grqc-h3-k15 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 0.171916 [0.162460, 0.208621] | 31342592 [26247168, 32882688] | 5 / 5 |
| ca-grqc-h3-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.347245 [0.341513, 0.350824] | 51986432 [49938432, 52543488] | 5 / 5 |
| ca-grqc-h3-k20 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 0.192330 [0.187348, 0.222351] | 32342016 [30621696, 33456128] | 5 / 5 |
| ca-grqc-h4-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.953241 [1.934252, 2.010056] | 303693824 [297926656, 318488576] | 5 / 5 |
| ca-grqc-h4-k5 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 1.244923 [1.206307, 1.267228] | 291389440 [282689536, 298663936] | 5 / 5 |
| ca-grqc-h4-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.162804 [2.134180, 2.190294] | 294600704 [289079296, 322174976] | 5 / 5 |
| ca-grqc-h4-k10 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 1.221018 [1.184371, 1.265057] | 284393472 [282165248, 298483712] | 5 / 5 |
| ca-grqc-h4-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.292136 [2.257714, 2.314453] | 312328192 [304758784, 325861376] | 5 / 5 |
| ca-grqc-h4-k15 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 1.218708 [1.200558, 1.250291] | 292847616 [282984448, 294879232] | 5 / 5 |
| ca-grqc-h4-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.329611 [2.286734, 2.339328] | 296402944 [281722880, 313704448] | 5 / 5 |
| ca-grqc-h4-k20 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 1.204879 [1.198004, 1.340088] | 294715392 [292208640, 297910272] | 5 / 5 |
| ca-grqc-h5-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 13.234607 [13.127972, 13.540851] | 2057863168 [1965735936, 2067103744] | 5 / 5 |
| ca-grqc-h5-k5 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 10.233439 [9.977978, 10.455711] | 2036580352 [1936719872, 2302197760] | 5 / 5 |
| ca-grqc-h5-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.467969 [14.441360, 15.977816] | 1982267392 [1901805568, 2074181632] | 5 / 5 |
| ca-grqc-h5-k10 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 10.360376 [10.220007, 10.658446] | 2126036992 [1920811008, 2167291904] | 5 / 5 |
| ca-grqc-h5-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.952384 [14.686493, 15.234344] | 2054733824 [1982709760, 2138882048] | 5 / 5 |
| ca-grqc-h5-k15 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 10.343736 [9.936399, 10.590790] | 2041675776 [1917304832, 2276605952] | 5 / 5 |
| ca-grqc-h5-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.843632 [14.798095, 14.961735] | 2077212672 [1983643648, 2145583104] | 5 / 5 |
| ca-grqc-h5-k20 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 10.162662 [9.989252, 10.450923] | 2143813632 [2080866304, 2307260416] | 5 / 5 |
| ca-condmat-h3-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.611873 [1.561063, 1.755882] | 144146432 [131940352, 145866752] | 5 / 5 |
| ca-condmat-h3-k5 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 3.062423 [3.031924, 3.088452] | 168509440 [160595968, 179699712] | 5 / 5 |
| ca-condmat-h3-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.506015 [2.444434, 2.589742] | 140902400 [123142144, 157564928] | 5 / 5 |
| ca-condmat-h3-k10 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 5.239991 [5.228296, 5.441529] | 199327744 [196575232, 210042880] | 5 / 5 |
| ca-condmat-h3-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.118217 [3.075182, 3.149941] | 144687104 [139476992, 166756352] | 5 / 5 |
| ca-condmat-h3-k15 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 6.207218 [6.082826, 6.579151] | 196608000 [191823872, 200065024] | 5 / 5 |
| ca-condmat-h3-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.119107 [3.048741, 3.205449] | 150470656 [138772480, 159154176] | 5 / 5 |
| ca-condmat-h3-k20 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 6.323642 [6.173087, 6.346204] | 207257600 [204668928, 210206720] | 5 / 5 |
| ca-condmat-h4-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 1.977284 [1.970315, 2.018353] | 293699584 [277151744, 303038464] | 5 / 5 |
| ca-condmat-h4-k5 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 1.668905 [1.649365, 1.711140] | 244252672 [241893376, 255836160] | 5 / 5 |
| ca-condmat-h4-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.397757 [3.379092, 3.411200] | 282132480 [275251200, 300630016] | 5 / 5 |
| ca-condmat-h4-k10 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 4.056361 [3.938601, 4.127479] | 306823168 [295878656, 320847872] | 5 / 5 |
| ca-condmat-h4-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 4.667451 [4.649892, 4.783245] | 277823488 [266747904, 298369024] | 5 / 5 |
| ca-condmat-h4-k15 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 6.134115 [6.089386, 6.236680] | 323387392 [309084160, 329826304] | 5 / 5 |
| ca-condmat-h4-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 5.160829 [5.082275, 5.183919] | 284688384 [270483456, 290619392] | 5 / 5 |
| ca-condmat-h4-k20 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 7.008117 [6.951435, 7.053949] | 306626560 [292323328, 327041024] | 5 / 5 |
| ca-condmat-h5-k5 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 4.010743 [3.939391, 4.053550] | 475807744 [456261632, 527761408] | 5 / 5 |
| ca-condmat-h5-k5 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 6.959792 [6.830489, 7.013300] | 451887104 [438419456, 463863808] | 5 / 5 |
| ca-condmat-h5-k10 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 6.162600 [6.083509, 6.422333] | 479920128 [476381184, 501415936] | 5 / 5 |
| ca-condmat-h5-k10 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 9.333925 [9.266196, 10.268779] | 481673216 [429916160, 486260736] | 5 / 5 |
| ca-condmat-h5-k15 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 8.585386 [8.434936, 9.320774] | 474284032 [461045760, 476610560] | 5 / 5 |
| ca-condmat-h5-k15 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 12.700630 [11.488667, 13.252943] | 454934528 [416284672, 492912640] | 5 / 5 |
| ca-condmat-h5-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 9.463668 [8.983904, 9.739818] | 482656256 [465731584, 492453888] | 5 / 5 |
| ca-condmat-h5-k20 | ippv-eight-patches | 5 / 5 | {'completed': 5} | 12.275369 [11.983067, 14.252367] | 477036544 [422150144, 492716032] | 5 / 5 |
