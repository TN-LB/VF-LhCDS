# Core module

M0 build provenance is generated from `cmake/build_info.cpp.in` into the build
tree and exposed by `include/vflhcds/core/build_info.hpp`. Graphs, canonical sets,
fractions and exact arithmetic remain M2 work; no machine-width placeholders
are supplied for mathematical counts or IDs.
