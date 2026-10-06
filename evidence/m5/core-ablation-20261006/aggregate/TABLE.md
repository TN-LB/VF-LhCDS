# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require all three scheduled runs of that algorithm/case to complete and pass structural validation. Strict canonical output agreement is required for this ablation. Pair agreement is reported separately: timing a completed algorithm does not assert agreement with a timed-out counterpart. Censored measurements stay in runs.json/cells.json and never enter completion-time medians; no speedup is inferred for an unpaired cell.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-core-off | 3 / 3 | {'completed': 3} | 0.316864 [0.315234, 0.330907] | 49790976 [47316992, 54607872] | 3 / 3 |
| ca-grqc-h3-k5 | vf-core-safe | 3 / 3 | {'completed': 3} | 0.313924 [0.302518, 0.350243] | 47710208 [46563328, 51216384] | 3 / 3 |
| ca-grqc-h3-k10 | vf-core-off | 3 / 3 | {'completed': 3} | 0.887300 [0.885936, 0.889245] | 48119808 [47874048, 50544640] | 3 / 3 |
| ca-grqc-h3-k10 | vf-core-safe | 3 / 3 | {'completed': 3} | 0.890939 [0.886492, 0.917418] | 42418176 [40140800, 50184192] | 3 / 3 |
| ca-grqc-h3-k15 | vf-core-off | 3 / 3 | {'completed': 3} | 1.684735 [1.683410, 1.687738] | 48922624 [46809088, 49364992] | 3 / 3 |
| ca-grqc-h3-k15 | vf-core-safe | 3 / 3 | {'completed': 3} | 1.689759 [1.686944, 1.750608] | 46383104 [45219840, 49086464] | 3 / 3 |
| ca-grqc-h3-k20 | vf-core-off | 3 / 3 | {'completed': 3} | 2.686251 [2.685145, 2.733821] | 50479104 [49741824, 50642944] | 3 / 3 |
| ca-grqc-h3-k20 | vf-core-safe | 3 / 3 | {'completed': 3} | 2.690686 [2.688913, 2.745574] | 44924928 [42532864, 49463296] | 3 / 3 |
| ca-condmat-h3-k5 | vf-core-off | 3 / 3 | {'completed': 3} | 38.475664 [38.408034, 39.246395] | 154992640 [141508608, 163758080] | 3 / 3 |
| ca-condmat-h3-k5 | vf-core-safe | 3 / 3 | {'completed': 3} | 39.717360 [39.219348, 39.762930] | 136527872 [129318912, 141082624] | 3 / 3 |
| ca-condmat-h3-k10 | vf-core-off | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k10 | vf-core-safe | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k15 | vf-core-off | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k15 | vf-core-safe | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k20 | vf-core-off | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
| ca-condmat-h3-k20 | vf-core-safe | 3 / 3 | {'timeout': 3} | unavailable | unavailable | 0 / 3 |
