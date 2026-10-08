# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require every scheduled repetition of that algorithm/case to complete and pass validation. The required comparator is recorded per cell: main uses cutoff-tie agreement, core uses strict output, stop uses strict prefix agreement. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 0.346221 [0.341015, 0.350121] | 49283072 [33652736, 51838976] | 5 / 5 |
| ca-grqc-h3-k20 | vf-count-membership-core-safe | 5 / 5 | {'completed': 5} | 0.349207 [0.347236, 0.351431] | 33701888 [29179904, 46645248] | 5 / 5 |
| ca-grqc-h4-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 2.227008 [2.214073, 2.285430] | 313376768 [294207488, 365838336] | 5 / 5 |
| ca-grqc-h4-k20 | vf-count-membership-core-safe | 5 / 5 | {'completed': 5} | 2.228987 [2.180333, 2.232040] | 301760512 [267239424, 367230976] | 5 / 5 |
| ca-grqc-h5-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 14.667720 [14.409900, 15.212122] | 2011709440 [1997602816, 2253127680] | 5 / 5 |
| ca-grqc-h5-k20 | vf-count-membership-core-safe | 5 / 5 | {'completed': 5} | 14.322095 [14.274872, 14.617596] | 2008449024 [1709293568, 2087665664] | 5 / 5 |
| ca-condmat-h3-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 3.004335 [2.978667, 3.016944] | 145735680 [131317760, 150208512] | 5 / 5 |
| ca-condmat-h3-k20 | vf-count-membership-core-safe | 5 / 5 | {'completed': 5} | 4.516198 [4.471597, 4.603873] | 137920512 [126418944, 149209088] | 5 / 5 |
| ca-condmat-h4-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 5.032179 [4.927368, 5.099653] | 284016640 [275906560, 290488320] | 5 / 5 |
| ca-condmat-h4-k20 | vf-count-membership-core-safe | 5 / 5 | {'completed': 5} | 6.604414 [6.551126, 6.659555] | 277839872 [253231104, 286064640] | 5 / 5 |
| ca-condmat-h5-k20 | vf-count-membership-core-off | 5 / 5 | {'completed': 5} | 8.744677 [8.710525, 8.833273] | 499286016 [462880768, 535871488] | 5 / 5 |
| ca-condmat-h5-k20 | vf-count-membership-core-safe | 5 / 5 | {'completed': 5} | 10.193515 [10.040605, 10.240013] | 460292096 [455950336, 469254144] | 5 / 5 |
