cmake_minimum_required(VERSION 3.16)
project(vflhcds VERSION 0.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

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
  src/io/status.cpp)
add_library(vflhcds::lib ALIAS vflhcds_lib)
target_include_directories(vflhcds_lib PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
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
  add_test(NAME m0_cli_contract
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/cli_smoke.py"
      "$<TARGET_FILE:vflhcds>")
  add_test(NAME m0_reference_skeleton
    COMMAND "${Python3_EXECUTABLE}" -m pytest reference/tests -q)
  set_tests_properties(m0_reference_skeleton PROPERTIES
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
endif()
