# Minimal dependencies

M2 adds only Boost headers for exact arbitrary-precision integer arithmetic. There
are no compiled Boost libraries, network fetches during CMake configuration,
Python production bindings or external test frameworks beyond pytest.

| Item | Pin / use | License / provenance |
|---|---|---|
| Boost | 1.86.0, `boost::multiprecision::cpp_int` | [Boost Software License 1.0](https://www.boost.org/LICENSE_1_0.txt) |
| Official archive | `boost_1_86_0.tar.bz2` | [Release metadata](https://archives.boost.io/release/1.86.0/source/boost_1_86_0.tar.bz2.json) |
| Archive SHA-256 | `1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b` | Verified before extraction |

Run `python scripts/fetch_boost.py` to fetch from the official Boost archive using
curl with TLS verification, verify the fixed checksum, and extract only `boost/`
and `LICENSE_1_0.txt` into ignored `.deps/boost_1_86_0/`. Header copyright/license
notices are retained. No global installation is performed. For an offline build,
provide the same verified header tree and set `-DVFLHCDS_BOOST_ROOT=/path/to/boost_1_86_0`.
The downloaded archive is about 120 MiB; it and extracted headers are not committed.
An existing archive with a wrong hash is rejected, not silently used.

The implementation uses the documented arbitrary-size signed cpp_int backend
([official documentation](https://www.boost.org/doc/libs/1_86_0/libs/multiprecision/doc/html/boost_multiprecision/tut/ints/cpp_int.html));
fixed-width flow uses native unsigned __int128 with local checked operations.
The Boost dependency implements arithmetic, not the clique/flow/oracle algorithms.
D012's baseline independence boundary remains unchanged.

Build tools: CMake >=3.16, GCC/Clang C++17 with native unsigned __int128 on a POSIX
system; Python >=3.10 and pytest >=7,<9 for testing. Fetching headers additionally
requires curl and Python tarfile. Exact tested tool versions and dependency fetch
attempts are in `evidence/m2/`.
