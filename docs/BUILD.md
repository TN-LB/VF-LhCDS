# M0 build and test instructions

Requires CMake >=3.16, a C++17 compiler, and Python >=3.10 with pytest >=7,<9.
There are no runtime third-party libraries, fetched CMake dependencies, Python
production bindings or test-framework libraries in M0. Arbitrary-precision
arithmetic is still required by D005 in M2; no numeric backend exists yet.

If `python`/pytest is unavailable, create a local environment and activate it:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Install CMake through the local toolchain if needed. For the recorded M0 run,
`.venv` was created with `--system-site-packages` to reuse installed pytest 8.4.2,
and CMake 4.4.3 was installed into that environment. It is tooling, not a linked
solver dependency. The exact run environment is in `evidence/m0/checks/environment.json`.

Required Debug checks, from the repository root with tools on PATH:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j2
ctest --test-dir build --output-on-failure
python -m pytest reference/tests -q
```

ASan and UBSan are enabled together, with errors non-recoverable:

```sh
cmake -S . -B build-sanitize -DCMAKE_BUILD_TYPE=Debug -DVFLHCDS_ENABLE_SANITIZERS=ON
cmake --build build-sanitize -j2
ctest --test-dir build-sanitize --output-on-failure
```

This instruments every compiled library/executable/test target and links the
sanitizer runtimes. GCC/Clang are supported for this option; other compilers fail
configuration explicitly. There is no parallel implementation or TSan profile.
Sanitizer runs exercise the skeleton only, not T16 or a numeric/solver campaign.

For other required profiles, use the same configure/build/test commands with
separate directories and `-DCMAKE_BUILD_TYPE=Release` or `RelWithDebInfo`.
Use a single-configuration generator (the default Makefiles generator is tested)
so `print-build-info` records the selected profile. No M0 performance claim uses
these builds. `-DBUILD_TESTING=OFF` omits Python discovery and all test targets.

Warnings are errors: GCC/Clang use `-Wall -Wextra -Wpedantic -Wconversion
-Wsign-conversion -Wshadow -Werror`; MSVC configuration uses `/W4 /WX /permissive-`
but is untested. M2 must handle the accepted `__int128` extension locally without
turning off project-wide strict warnings. M0 does not claim compiler portability
for a future numeric backend.

`m0_cpp_skeleton` checks library linkage and non-success of unavailable work.
`m0_cli_contract` checks actual process statuses, JSON and output preservation.
`m0_reference_skeleton` runs the independent import-isolation pytest check.
These do not complete any T01-T17 or M1+ task.
