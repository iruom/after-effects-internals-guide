---
status: active
last_verified: 2026-09-14
---
# Premiere Cache Model as a Comparison Surface

Premiere exposes several cache mechanisms that are useful as sibling-host design evidence, not direct AE facts.

`PrSDKRenderCacheType.h` names imported-frame, imported-still, intermediate-frame, rendered-frame, rendered-still and persistent-prefetch cache classes. The render caller can select cache participation with a bitmask.

`PrSDKPPixCacheSuite` supports GUID-named pixel objects. Dependencies can be registered against a GUID so that the object cannot be flushed while the dependency count is nonzero. Failing to unregister is explicitly described as equivalent to a pixel-memory leak.

Frame-cache identities grew over SDK versions to include importer instance, stream, frame number, acceptable formats, importer preferences, quality, color profile and finally an opaque color-space identifier.

`PrSDKVideoSegmentRenderSuite` separately exposes functions that derive an identifier from the complete render request before the render is launched.

## AEIG relevance
These APIs reinforce a general Adobe design pattern: cache identity is a structured fingerprint of render semantics, while cache residency/lifetime is a separate policy layer.

Compare this with AE `PF_State`, `AEGP_GetReceiptGuid`, HashSuite GUID mixing, Compute Cache keys, effect/build cache versioning and local `MixHashGuid` traces.

Do not infer that AE uses Premiere's PPix cache or its exact key composition. The value is the shared architectural problem and Adobe's explicit solution in a sibling host.

## Named PPix cache semantics
`AddNamedPPixToCache()` uses a caller-supplied GUID as content identity. If an entry with that identifier already exists, the newly supplied PPix is ignored and remains owned by the caller. Adobe explicitly recommends retrieving the cached PPix afterward if duplicate computation is possible.

This is a subtle but important contract: cache insertion is not ownership transfer and not "last writer wins". The cache treats identity equality as stronger than producer identity.

## Dependency pinning is separate from identity
`RegisterDependencyOnNamedPPix()` can pin an object that is already cached *or one that may arrive later*. `ExpireNamedPPixFromCache()` cannot actually remove the frame while dependencies remain.

Residency therefore behaves like a reference-counted protection layer around a content-addressed object. A request can establish future dependency before the object exists.

This is analogous to pinning a promise/future's eventual value rather than merely retaining an existing buffer.
## Identity evolution across suite versions
The earliest frame-cache API keys mainly on importer instance, stream, frame number and acceptable formats. Later revisions add importer preferences, then color-profile information, render quality and finally an opaque color-space token.

That progression is an unusually clear record of cache-key bugs being prevented by expanding semantic identity. Whenever a newly introduced render dimension can change pixels, the cache contract must represent it or stale reuse becomes possible.

A useful abstract model is:

`FrameKey = H(importer, stream, frame, format-set, preferences, quality, color-semantics, ...)`

AEIG should compare this evolution with AE's `I_MIX_GUID_DEPENDENCIES`, effect/build version keying, time-dependent state and backend/color-space differences.

## Raw cache vs rendered frame cache
The PPix suite also exposes a per-importer raw cache keyed by a simple integer. That is a separate semantic layer from frame cache and named GUID cache. Adobe therefore does not treat all pixel memory as one cache namespace.

## Troubleshooting implications
A wrong-frame cache bug should be investigated as a missing semantic dimension before blaming "cache corruption". Conversely, gratuitously including disabled/irrelevant state reduces reuse and produces a performance bug rather than a correctness bug.