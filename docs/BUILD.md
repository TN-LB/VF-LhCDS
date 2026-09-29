# Build and test instructions (through M3)

Requires CMake >=3.16, GCC/Clang C++17 with native unsigned __int128 on a POSIX
system, and Python >=3.10 with pytest >=7,<9 for testing. M2 uses header-only
Boost.Multiprecision 1.86.0. See [dependency pin/license](DEPENDENCIES.md). No
compiled Boost library or production Python dependency is introduced.

If needed, create and activate a local environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/fetch_boost.py
```

Install CMake through the local toolchain if needed. The recorded environment uses
Python 3.12.2, pytest 8.4.2, CMake 4.4.3 and AppleClang 17.0.0. Header download is an
explicit setup step, never a configure-time network action. An offline header
installation can be selected with `-DVFLHCDS_BOOST_ROOT=/path/to/boost_1_86_0`.

Required Debug checks, from the root with tools on PATH:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j2
ctest --test-dir build --output-on-failure
python -m pytest reference/tests -q
```

ASan and UBSan instrument all compiled targets and are non-recoverable:

```sh
cmake -S . -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DVFLHCDS_ENABLE_SANITIZERS=ON
cmake --build build-sanitize -j2
ctest --test-dir build-sanitize --output-on-failure
```

Use separate `build-release` / `build-relwithdebinfo` directories with build types
Release / RelWithDebInfo for the other required profiles. Use a single-configuration
generator so `print-build-info` records the profile. Strict warnings remain errors:
`-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -Werror`.
Only the native 128-bit typedef uses a localized extension. MSVC/no-128/non-POSIX
configurations fail explicitly; GCC/Linux support is intended but not yet tested.
No parallel code exists, so TSan is deferred. No performance claim uses these runs.

CTest contains nine tests: retained library argument checks; M2 primitives, oracle
smoke and CLI regressions; M3 solver, solver smoke, solve CLI and synthetic failure
reduction; and the 74 independent M1 pytest checks. The M0 reference
test name is historical. `-DBUILD_TESTING=OFF` omits Python discovery, test executables
and the exhaustive test-only probe; the production library still needs Boost.

Full M2 differential campaigns (each output directory must be new):

```sh
python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier exhaustive-small --output evidence/m2/new-exhaustive
python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier seeded --output evidence/m2/new-seeded
python validation/oracle_campaign.py --probe build/vflhcds_m2_probe --tier higher-h --output evidence/m2/new-higher-h
```

Repeat with the sanitizer probe to exercise those tiers under ASan/UBSan. The
seeded tier fixes seed 20260922 and 1,000 graph/h cases; these are correctness
fixtures, not benchmark parameters. Each campaign retains cases, compressed exact
query/result records, hashes and counts. `python scripts/run_m2_checks.py <new-dir>`
records all four profiles, both Debug/sanitizer campaigns and standalone pytest,
paper hashes and tool versions. See [M2 report](../evidence/m2/REPORT.md).


M3 solver campaigns compare complete results and every k prefix with independent
all-superset truth; they also check sealed chain-pair separators and relabeling:

```sh
python validation/solver_campaign.py --probe build/vflhcds_m3_probe --tier exhaustive-small --output evidence/m3/new-exhaustive
python validation/solver_campaign.py --probe build/vflhcds_m3_probe --tier seeded --output evidence/m3/new-seeded
python validation/solver_campaign.py --probe build-sanitize/vflhcds_m3_probe --tier higher-h --output evidence/m3/new-sanitized-higher
python scripts/run_m3_checks.py evidence/m3/new-full-checks
```

The full M3 driver executes all four tested profiles, production-only Release,
Debug/ASan+UBSan solver tiers, retained M2 oracle tiers, pytest and a real CLI
run followed by external reference validation. Seed 20260929 identifies M3
correctness fixtures; it is not a benchmark parameter. Logs/graphs/results are
saved, and existing evidence directories are never overwritten.

For a separately timed process with external definition checks:

```sh
python validation/run_solver.py --executable build/vflhcds --evidence evidence/m3/new-cli-run --check-reference -- solve --graph reference/fixtures/bridged_triangles.graph --h 3 --all
```

See [M3 API/measurement details](M3_IMPLEMENTATION.md) and
[executed M3 report](../evidence/m3/REPORT.md). The CLI version is 0.1.0 / stage M3.
