---
status: active
last_verified: 2026-09-14
---
# Premiere PPix Cache: Identity, Dependencies, and Purge Protection

`PrSDKPPixCacheSuite` exposes unusually explicit cache-key and lifetime semantics that are useful when reconstructing Adobe's broader media/cache architecture.

## Import-frame cache identity
Frame cache operations identify an entry using importer instance, stream index and frame number, while retrieval also supplies acceptable frame formats. Later revisions add importer preferences, render quality and color profile/color-space identity.

A practical identity model is therefore closer to:
`K = H(importer instance, stream, frame, format contract, preferences, quality, color interpretation)`
than to a simple `(file, frame)` tuple.

## Named PPix cache
The suite also exposes GUID-addressed PPix entries. `AddNamedPPixToCache` is idempotent with respect to an existing identifier: if the GUID is already present, the supplied PPix is ignored and the caller keeps ownership.

This is a useful example of content/state identity being decoupled from storage ownership.

## Dependency registration pins cache entries
A client can register a dependency on a named PPix. While dependency count is non-zero, attempted expiry cannot flush the frame. Every successful registration must be matched by unregister.

Adobe's header explicitly describes a missing unregister as equivalent to a PPix memory leak. Cache dependency accounting is therefore a form of reference-counted retention, not merely a lookup optimization.
## Frame-derived dependency IDs
Later APIs can register dependency directly on a frame description and return the PPix identifier representing that configuration. The dependency call takes the same identity inputs used by frame-cache lookup, including formats/preferences and, in later revisions, quality and color-space/profile state.

This makes the returned identifier a useful observable fingerprint of host cache equivalence even when the actual hash construction is opaque.

## Cross-host implication
AE Compute Cache and render GUIDs solve a similar problem at different layers: identify render-relevant state, retain reusable work, and let memory pressure purge entries that are not actively depended upon. Do not assume identical implementations, but compare their invariants.

## Developer rules
- Never treat frame number alone as a cache key.
- Include all state that changes pixel interpretation, not only decoded bytes.
- Balance every cache dependency registration.
- Distinguish ownership of the supplied PPix from ownership of the cache entry.
- Test equivalent-state reuse after preferences/color/quality round trips.
## Version and failure boundary
Later PPix Cache revisions add more interpretation state such as render quality and color profile/space. That evolution demonstrates why a cache key correct for an older request contract can become incomplete after new semantic dimensions are introduced.

Failure patterns include dependency-count leaks that pin PPix indefinitely, keying only on frame/time while ignoring format/color policy, assuming idempotent insertion transfers ownership, and reusing a cached image after importer preferences/source interpretation change.

## AE comparison experiments
For equivalent media frames in AE, vary only decode quality, color interpretation and output pixel format while observing MediaCore identity/cache activity. Then compare memory pressure with active/expired consumers to test whether a separate retention/pin concept exists.

## Unknown frontier
The named PPix GUID algorithm and dependency-retention implementation are Premiere contracts; AE's BEE/MediaFoundation caches are not proven to reuse them. The value is the invariant separation of semantic identity, storage ownership, retention dependency and purge eligibility.

Related: `docs/cache-system/state-identity.md`, `docs/memory-system/runtime-architecture.md`, `docs/media-system/media-identity.md`, `docs/foundations/cross-host-triangulation.md`.
