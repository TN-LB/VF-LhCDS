# Telemetry module

Exact query/event counters plus separately scoped native/external timing. M4
adds query-local core threshold, full-graph peeling counters and reduction time.
Original and reduced interval sizes stay distinct; all timing and backend details
are excluded from canonical semantic hashes. See docs/INTERFACE_CONTRACT.md.
