cmake_minimum_required(VERSION 3.16)
project(vflhcds VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(CheckCXXSourceCompiles)
check_cxx_source_compiles("int main() { __extension__ typedef unsigned __int128 U; U x = 0; return static_cast<int>(x); }" VFLHCDS_HAS_UINT128)
if(NOT VFLHCDS_HAS_UINT128 OR NOT UNIX)
  message(FATAL_ERROR "M2 requires native unsigned __int128 and POSIX atomic file output (GCC/Clang on Unix)")
endif()
set(VFLHCDS_BOOST_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/.deps/boost_1_86_0" CACHE PATH "Boost headers root; see docs/BUILD.md")
if(NOT EXISTS "${VFLHCDS_BOOST_ROOT}/boost/multiprecision/cpp_int.hpp")
  message(FATAL_ERROR "Boost headers missing: run python scripts/fetch_boost.py or set VFLHCDS_BOOST_ROOT")
endif()
file(STRINGS "${VFLHCDS_BOOST_ROOT}/boost/version.hpp" VFLHCDS_BOOST_VERSION
  REGEX "^#define BOOST_VERSION [0-9]+$")
if(NOT VFLHCDS_BOOST_VERSION STREQUAL "#define BOOST_VERSION 108600")
  message(FATAL_ERROR "M2 pins Boost 1.86.0; use the documented verified headers")
endif()

option(VFLHCDS_ENABLE_SANITIZERS "Build with AddressSanitizer and UndefinedBehaviorSanitizer" OFF)
add_library(vflhcds_build_options INTERFACE)
if(CMAKE_CXX_COMPILER_ID MATCHES "^(AppleClang|Clang|GNU)$")
  target_compile_options(vflhcds_build_options INTERFACE
    -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -Werror)
elseif(MSVC)
  target_compile_options(vflhcds_build_options INTERFACE /W4 /WX /permissive-)
else()
  message(FATAL_ERROR "Strict warning configuration is required for this compiler")
endif()
if(VFLHCDS_ENABLE_SANITIZERS)
  if(NOT CMAKE_CXX_COMPILER_ID MATCHES "^(AppleClang|Clang|GNU)$")
    message(FATAL_ERROR "ASan+UBSan profile requires GCC or Clang")
  endif()
  target_compile_options(vflhcds_build_options INTERFACE
    -fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all)
  target_link_options(vflhcds_build_options INTERFACE
    -fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all)
endif()

configure_file(cmake/build_info.cpp.in generated/build_info.cpp @ONLY)
add_library(vflhcds_lib STATIC
  "${CMAKE_CURRENT_BINARY_DIR}/generated/build_info.cpp"
  src/cli/dispatch.cpp
  src/io/status.cpp
  src/core/exact.cpp
  src/core/graph.cpp
  src/clique/materialized.cpp
  src/oracle/closure.cpp
  src/telemetry/query.cpp
  src/io/graph.cpp
  src/io/solution.cpp
  src/solver/solver.cpp
  src/io/sha256.cpp)
add_library(vflhcds::lib ALIAS vflhcds_lib)
target_include_directories(vflhcds_lib PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_include_directories(vflhcds_lib SYSTEM PUBLIC "${VFLHCDS_BOOST_ROOT}")
target_link_libraries(vflhcds_lib PRIVATE vflhcds_build_options)
add_executable(vflhcds src/cli/main.cpp)
target_link_libraries(vflhcds PRIVATE vflhcds::lib vflhcds_build_options)

include(CTest)
if(BUILD_TESTING)
  find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)
  execute_process(COMMAND "${Python3_EXECUTABLE}" -m pytest --version
    RESULT_VARIABLE pytest_status OUTPUT_QUIET ERROR_QUIET)
  if(NOT pytest_status EQUAL 0)
    message(FATAL_ERROR "pytest is required for BUILD_TESTING; see docs/BUILD.md")
  endif()
  add_executable(vflhcds_skeleton_test tests/skeleton_test.cpp)
  target_link_libraries(vflhcds_skeleton_test PRIVATE vflhcds::lib vflhcds_build_options)
  add_test(NAME m0_cpp_skeleton COMMAND vflhcds_skeleton_test)
  add_executable(vflhcds_primitives_test tests/m2_primitives.cpp)
  target_link_libraries(vflhcds_primitives_test PRIVATE vflhcds::lib vflhcds_build_options)
  add_executable(vflhcds_m2_probe tests/m2_probe.cpp)
  target_link_libraries(vflhcds_m2_probe PRIVATE vflhcds::lib vflhcds_build_options)
  add_test(NAME m2_primitives COMMAND vflhcds_primitives_test)
  add_executable(vflhcds_solver_test tests/m3_solver.cpp)
  target_link_libraries(vflhcds_solver_test PRIVATE vflhcds::lib vflhcds_build_options)
  add_executable(vflhcds_m3_probe tests/m3_probe.cpp)
  target_link_libraries(vflhcds_m3_probe PRIVATE vflhcds::lib vflhcds_build_options)
  add_test(NAME m3_solver COMMAND vflhcds_solver_test)
  add_test(NAME m3_solver_smoke COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/validation/solver_campaign.py" --probe "$<TARGET_FILE:vflhcds_m3_probe>" --tier smoke)
  add_test(NAME m3_cli_contract COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/m3_cli.py" "$<TARGET_FILE:vflhcds>")
  add_test(NAME m3_failure_reducer COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/m3_harness.py")
  add_test(NAME m2_oracle_smoke
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/validation/oracle_campaign.py"
      --probe "$<TARGET_FILE:vflhcds_m2_probe>" --tier smoke)
  add_test(NAME m2_cli_contract
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/cli_smoke.py"
      "$<TARGET_FILE:vflhcds>")
  add_test(NAME m0_reference_skeleton
    COMMAND "${Python3_EXECUTABLE}" -m pytest reference/tests -q)
  set_tests_properties(m0_reference_skeleton PROPERTIES
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
endif()
