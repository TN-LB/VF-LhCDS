# Independent reference skeleton (P00.3)

`vflhcds_reference` is importable directly from this directory. Python >=3.10;
standard library only at runtime, pytest for tests. No C++ binary, extension,
production import, or production build is needed.

`direct.py` reserves P01.1/P01.2; `parametric.py` reserves P01.3/P01.4. They have
no mathematical functions yet. M1 will implement the n<=12 default truth guard
and its explicit test override, fixtures and generators. `test_skeleton.py`
checks isolated imports only; it is not a compactness, oracle or chain test.

From the repository root: `python -m pytest reference/tests -q`.
