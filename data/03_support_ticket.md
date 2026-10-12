# Support Ticket ACME-184 (October 7)
Severity: High. Status: Open. Owner: Ravi Patel.
In staging, the assistant occasionally includes a patient name in the diagnostic trace sent to the observability provider. Reproduced in 2 of 50 tests.
Mitigation proposed: pre-logging PHI scrubber and regression suite. Fix is not yet deployed or validated. This is a launch blocker until verified by security.
