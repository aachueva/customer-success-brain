# Load Test (October 9)
Owner: Ravi Patel. 100 concurrent users, 30-minute staging test.
p95 latency: 4.2 seconds, versus target under 3 seconds. Error rate: 0.8%, versus target under 1%.
Vector search contributes 1.4 seconds at p95. Suggested optimizations: caching, index tuning, and reducing retrieval payload. No production-equivalent retest yet.
