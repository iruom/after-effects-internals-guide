---
status: active
last_verified: 2026-09-14
---
# Compute Cache: Cached Computation as a Host-Scheduled Single-Flight System

AE's Compute Cache is substantially richer than a generic key/value cache. `AE_ComputeCacheSuite.h` exposes a host-managed computation registry whose cache entries have semantic keys, in-flight computation state, checkout receipts, memory-footprint metadata and host-controlled purge.

## Direct header evidence
A compute class has a globally unique class ID and four callbacks: `generate_key`, `compute`, `approx_size_value`, and `delete_compute_value`.

`generate_key` must be cheap and must hash every input required to identify the result. For layer-dependent computations Adobe explicitly points to `PF_GetCurrentState`; that state is a hash of render inputs, not rendered pixels, so constructing the key does not itself trigger a render.

The computed value may be non-flat. `approx_size_value` must return its total memory footprint, and the header explicitly states that this size is an input to the cache purging heuristic.
## The cache has an explicit in-flight state
`AEGP_ComputeIfNeededAndCheckout` distinguishes at least three operational states:

| State | do-not-wait | wait |
|---|---|---|
| no cached value | compute and checkout | compute and checkout |
| another thread is computing the same key | return `A_Err_NOT_IN_CACHE_OR_COMPUTE_PENDING` | wait, then checkout |
| cached | checkout | checkout |

This is single-flight de-duplication: one expensive computation may serve several render calls without each call independently performing the work.

## Multi-checkout is deliberately latency-hidden
Adobe's own header prescribes a pattern for a render that requires several expensive cached values: issue every checkout first with `wait_for_other_threadB=false`, then revisit only the pending values with a waiting checkout. This allows independent computations to begin before the caller blocks and avoids serializing expensive work.

That pattern is evidence for a broader AE design principle: dependency work should be exposed early enough for the host to overlap it rather than hidden behind a sequence of blocking calls.
## Polling and UI/render separation
`AEGP_CheckoutCached` never computes and never waits. The header gives the concrete example of a UI thread polling for a histogram produced on a render thread. Cache lookup is therefore also an asynchronous rendezvous surface between execution domains.

## Receipt lifetime
A successful checkout returns an opaque Compute Checkout Receipt. The caller obtains the value through the receipt and must check the receipt back in before returning to the host. The receipt is a lease/pin, not the semantic cache key itself.

## Registration lifetime participates in cache lifetime
Unregistering a compute class purges all values because the host would otherwise lose the class's deletion callback. Type-registration lifetime therefore bounds value lifetime.

## Architectural interpretation
Do not model this subsystem as `map<key,value>`. A closer public model is:

`semantic key -> {absent | in-flight | resident} -> checkout lease -> pressure-aware purge`

This should be compared with Frame Receipts and Canvas Render Receipts without assuming those three receipt types share an implementation.

## Source
Local AE 25.6 SDK: `Examples/Headers/AE_ComputeCacheSuite.h`.

## Failure modes and ownership traps
- incomplete `generate_key` inputs -> semantically wrong value reused;
- expensive key generation -> every lookup pays computation cost before the cache can help;
- underreported `approx_size_value` -> host purge policy underestimates pressure;
- leaked checkout receipt -> value remains pinned/leased longer than intended;
- double checkin or use after checkin -> lifetime/contract violation;
- unregister compute class while callers still assume entries exist -> class-wide cache invalidation;
- waiting serially for several independent keys -> destroys the latency-hiding pattern Adobe explicitly recommends.

A computed value can contain pointers/non-flat structures because the host uses the registered delete callback rather than assuming serialization. That also means Compute Cache is process/runtime cache, not persistence. Never store project-durable identity in the cached pointer itself.

## Key design
A key should represent semantic input state, implementation/schema version and any external dependency needed to reproduce the result. Prefer `PF_GetCurrentState`/host receipts for layer/parameter dependencies instead of hashing rendered pixels or opaque pointers.

If the computation depends on a large structure, hash a canonical semantic representation rather than raw struct bytes containing padding, addresses or uninitialized fields.

## Concurrency experiment
Request the same expensive key from several MFR render calls simultaneously. Measure whether only one `compute` callback executes while other callers receive pending/wait behavior. Then request independent keys together and compare serial versus issue-all-then-wait patterns.

Also apply memory pressure while holding/releasing checkout receipts to distinguish semantic cache hit from physical residency and pin lifetime.

## Relationship to other AE cache mechanisms
Compute Cache is explicit plug-in-defined derived-data caching. Frame cache/Render GUID, Canvas receipts, PF state receipts and Media/GPU caches solve different identity/lifetime problems. Similar words such as key, receipt and cache do not imply shared storage.

## Unknown frontier
The suite does not expose eviction priority formula, cache partitioning, cross-project sharing, or whether keys are namespaced by plug-in binary/build beyond the class ID. Runtime traces are required before making claims about implementation below the public contract.

Related: `F-CACHE-006-compute-deduplication.md`, `docs/mfr/state-ownership.md`, `docs/memory-system/runtime-architecture.md`, `docs/cache-system/state-identity.md`.
