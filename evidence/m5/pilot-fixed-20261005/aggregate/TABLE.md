# All planned measurements

Native process wall time and peak RSS; separate external validation is excluded. Medians/min/max require three completed, tie-aware matching pairs. Censored measurements stay in runs.json/cells.json and never enter successful-run medians.

| Case | Algorithm | Recorded / planned | Status | Wall median [min, max] s | RSS median [min, max] bytes | Pairs matching |
|---|---|---:|---|---|---|---:|
| ca-grqc-h3-k5 | vf-adjacency-basic | 3 / 3 | {'completed': 3} | 1.191481 [1.191019, 1.192729] | 46252032 [45793280, 46858240] | 3 / 3 |
| ca-grqc-h3-k5 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.176961 [0.176261, 0.177558] | 30441472 [29933568, 31571968] | 3 / 3 |
| ca-grqc-h3-k10 | vf-adjacency-basic | 3 / 3 | {'completed': 3} | 5.316309 [5.214938, 5.553886] | 46186496 [40861696, 48398336] | 3 / 3 |
| ca-grqc-h3-k10 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.198185 [0.196546, 0.227762] | 30654464 [29540352, 32702464] | 3 / 3 |
| ca-grqc-h3-k15 | vf-adjacency-basic | 3 / 3 | {'completed': 3} | 10.452431 [10.369445, 10.479516] | 49020928 [47120384, 51986432] | 3 / 3 |
| ca-grqc-h3-k15 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.254021 [0.253945, 0.255390] | 31031296 [31014912, 32243712] | 3 / 3 |
| ca-grqc-h3-k20 | vf-adjacency-basic | 3 / 3 | {'completed': 3} | 18.082301 [17.965820, 18.198475] | 47169536 [43171840, 47169536] | 3 / 3 |
| ca-grqc-h3-k20 | ippv-seven-patches | 3 / 3 | {'completed': 3} | 0.317450 [0.280279, 0.326046] | 32849920 [31096832, 34996224] | 3 / 3 |
| ca-condmat-h3-k5 | vf-adjacency-basic | 1 / 3 | {'timeout': 1} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k5 | ippv-seven-patches | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k10 | vf-adjacency-basic | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k10 | ippv-seven-patches | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k15 | vf-adjacency-basic | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k15 | ippv-seven-patches | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k20 | vf-adjacency-basic | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
| ca-condmat-h3-k20 | ippv-seven-patches | 0 / 3 | {} | unavailable | unavailable | 0 / 0 |
