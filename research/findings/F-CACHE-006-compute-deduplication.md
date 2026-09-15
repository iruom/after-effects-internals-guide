---
status: researched-seed
evidence_grade: E0
confidence: 0.99
versions: "AE 2022+ Compute Cache"
last_verified: 2026-09-14
---
# Compute Cache coordinates duplicate work across render threads

## Statement
`AEGP_ComputeIfNeededAndCheckout()` distinguishes three states for a cache key: absent, currently being computed by another thread, and cached. A caller can either wait for the in-flight computation or receive `A_Err_NOT_IN_CACHE_OR_COMPUTE_PENDING` and continue without blocking.

## Internal implication
The cache owns per-key in-flight state, not merely completed values. This is effectively a single-flight / promise-like coordination mechanism embedded in the host cache.

## Performance tradeoff
Waiting avoids duplicate expensive work but can serialize otherwise independent rendering. Not waiting preserves parallelism but may require fallback work or deferred completion. Optimal policy depends on compute cost, key fan-out and frame critical path.

## Improvement direction
Expose or infer task cost and dependency priority so wait policy can be scheduler-driven rather than decided locally by each effect. A future graph scheduler could represent cache computation as a shared task node.

## Source
Compute Cache API: https://ae-plugins.docsforadobe.dev/effect-details/compute-cache-api/
