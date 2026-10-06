# Separate phase diagnostic

This target links an existing matching Release `libvflhcds_lib.a`; it does not
rebuild or modify production. The caller must verify and record its library,
headers, compiler flags, executable and graph hashes before each diagnostic.
Use headers, compiler and Release flags matching that library. After the enumeration
API extension, use the new library below; rebuilding against the historical library
requires its saved historical headers. No dependency is added.

```sh
.venv/bin/cmake -S experiments/phase_probe -B build-m5-condmat-phase-probe -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS= -DCMAKE_CXX_COMPILER=/usr/bin/c++ -DVF_LIBRARY=/Users/nost/Documents/VF-LhCDS/build-m5-adjacency-release/libvflhcds_lib.a
.venv/bin/cmake --build build-m5-condmat-phase-probe -j2
build-m5-condmat-phase-probe/vflhcds_phase_probe GRAPH H K adjacency
```

Run the last command under the external timeout runner, as in the
[executed phase diagnostic](../../evidence/m5/phase-diagnostic-20261003/REPORT.md).
It uses basic semantics (core off, sorted footprints, automatic exact capacities).
Before and after parsing, indexing, solving and serialization it flushes a JSONL
marker to stderr, with a monotonic elapsed time. Normal stdout contains the same
solution JSONL as the production serializer. Stderr is a diagnostic schema, not
the production status contract. A timeout may leave only a prefix of markers;
that is phase evidence, not a successful or partially accepted algorithm result.

Instrumentation overhead and the separate executable make its time diagnostic
only. External validation runs after the native child and is never included in
phase timing. Two named tiny fixtures were checked for marker order, byte-identical
production output and independent definition agreement; this is not a substitute
for the full regression/sanitizer corpus when production code changes.

The optional fourth argument selects the existing `combinations|adjacency`
enumeration API. Omission retains combinations; diagnostics must explicitly
match the failed run's selector. The 2026-10-05 CA-CondMat diagnosis builds in
`build-m5-condmat-phase-probe`, preserving the historical probe binary. The
existing solver trace callback also flushes a `phase=query,event=end` marker
after each completed oracle query, with its index and recorded exact counters.
These query markers occur between solve begin/end; they do not enter semantic
output or production status. An unfinished query has no end marker, and such
absence does not by itself identify a particular inner flow operation.

[Executed D032 evidence](../../evidence/m5/condmat-phase-20261005/REPORT.md)
records two passing tiny output/query-counter checks with independent definition
validation. CA-CondMat parsing/indexing finish promptly, then 137 queries finish
before solving times out at the same 60-second limit. Production and the old
probe binary are preserved; diagnostic gaps are not standalone flow timings.
