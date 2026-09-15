---
status: active
last_verified: 2026-09-16
evidence: Adobe Compute Cache API contract + MFR guidance + AEIG hash/state-identity model
---
# Deduplicate Expensive Computation Across Render Threads

Use `AEGP_ComputeCacheSuite1` when multiple render invocations may need the same expensive derived result and recomputing it independently would waste CPU/GPU time or memory. The API is designed as a thread-safe cache that can supplement or replace render-time mutable sequence state.

## Core route
`registered compute class + semantic key -> compute-if-needed -> checkout receipt -> value -> checkin`

The host owns cache coordination and eviction. Your plug-in owns key correctness, computation, size reporting and destruction of the cached value.

`AEGP_ClassRegister` associates a globally unique compute-class identifier with callback functions. Unregistering a class purges its entries and invokes `delete_compute_value`, so class lifetime is a real resource boundary rather than a namespace string only.

## Key correctness is the contract
`generate_key` must include every semantic input required by `compute`. If a parameter, layer state, source hash, mode flag, implementation version or other dependency can change the computed result, it must be represented in the key.

The inverse matters too: transient pointers, thread IDs, allocation order and mutable addresses should not enter the key unless they intentionally change result identity. They destroy reuse without adding correctness.

## Deduplication behavior
`AEGP_ComputeIfNeededAndCheckout()` can wait for another thread already computing the same entry or, with `wait_for_other_threadB=false`, return `A_Err_NOT_IN_CACHE_OR_COMPUTE_PENDING` instead of blocking behind that work.

That gives two legitimate scheduling policies:
- **must-have result**: wait/compute until a completed receipt is available;
- **opportunistic result**: avoid blocking if another thread owns the current computation and use a fallback/defer path.

Do not wrap the entire operation in a process-global mutex. The host cache already owns per-key coordination; a coarse plug-in lock serializes unrelated keys and can erase MFR gains.

## Receipts are lifetime tokens
A checkout receipt is not the cached value itself. Pass it to `AEGP_GetReceiptComputeValue()` to obtain the value pointer and always return the receipt with `AEGP_CheckinComputeReceipt()` before leaving the owning scope.

Double-checkin or use of an invalid receipt is a contract error; Adobe's implementation reports `A_Err_STRUCT` and can present an error dialog. Treat receipt ownership with the same rigor as a locked handle or checked-out frame.

## Memory accounting and eviction
`approx_size_value` feeds AE's cache-purging heuristic. Under-reporting can make the effect consume disproportionate memory; gross over-reporting can cause useful values to be purged too aggressively. Include subordinate allocations owned by the cached value, not only the top-level object size.

`delete_compute_value` must release every resource owned by the entry and must tolerate eviction driven by the host rather than by your effect's preferred schedule.

## MFR and persistence boundary
Compute Cache is especially valuable under MFR because many frame threads can converge on one expensive derived result without making render-time sequence data mutable. The cached value is **not** project persistence; it must be reproducible from durable inputs after reopening the project or restarting AE.

This makes it appropriate for things such as expensive lookup tables, analysis products, reusable geometry or other derived state whose validity can be expressed by a semantic key.

It is not automatically a rendered-frame cache. Reuse of a Compute Cache value does not prove a `PF_World`, render receipt, BEE render GUID or RG cache node remains valid for a different render request.

## Validation experiments
Instrument `generate_key`, `compute`, checkout/checkin and deletion. Issue identical requests concurrently and verify one computation serves multiple checkouts. Then vary one semantic dependency at a time and confirm a new key/value appears. Repeat under memory pressure to exercise host eviction and destruction.

For negative testing, deliberately omit one dependency from a development-only key and verify the resulting stale reuse is detectable. That demonstrates why key completeness is a correctness property, not merely a performance optimization.

## Evidence and cross-links
Primary contract: Adobe C++ SDK Guide `Compute Cache API` and MFR documentation. Related: `docs/capability-recipes/host-compatible-hash-state.md`, `docs/mfr/overview.md`, `docs/cache-system/state-identity.md`, `docs/persistence/sequence-data.md`.

## Unknown frontier
AEIG does not infer the private eviction algorithm, cache partition weights, exact concurrency primitive or relationship between Compute Cache storage and internal BEE/RG caches. Public behavior establishes a host-managed compute cache; internal unification beyond that remains an explicit unknown.
