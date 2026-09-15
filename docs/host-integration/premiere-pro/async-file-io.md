---
status: active
last_verified: 2026-09-14
---
# Premiere Async File I/O as a Modern MediaCore Boundary

`PrSDKAsyncFileReaderSuite` exposes a small but revealing host-managed asynchronous file reader.

## Stable file handle, request tuples
A read is identified by file handle, byte offset, requested size and destination buffer. Cancellation uses the same tuple. This implies the host tracks outstanding reads as semantic requests rather than requiring a separate opaque request object.

## File staleness is a first-class result
`SDK_AsyncReadResult_FileIsStale` means the file changed on disk and must be reopened. The I/O contract therefore treats source mutation as a state-version violation, not merely as a generic read failure.

## Completion serialization
At open time, a caller may request `CompletionIsSingleThreaded`. The host can therefore decouple I/O concurrency from callback serialization: reads may proceed asynchronously while completion delivery is serialized.
## Failure-model relevance
This contract suggests a useful distinction for AEIG diagnostics:

- I/O failure: data could not be read.
- Stale-source failure: the request was valid when issued, but the external source identity/version changed before completion.
- Cancellation: work is no longer desired, without implying an error in the source.

These should not be collapsed into one generic error path.

## AE comparison
AEIO has older source/file lifecycle hooks and sparse-frame requests but does not expose this exact MediaCore reader contract. Compare it with AE media-cache/XMP source identity, importer refresh behavior and any asynchronous read traces before inferring shared implementation.

## Experiment transfer to AE
Externally modify a media file between request issue and completion while tracing importer/media cache behavior. Distinguish hard read failure from detected content staleness and from cancellation caused by an obsolete render request.

Repeat with completion serialization on/off in a purpose-built Premiere probe, then compare AE importer/media callbacks for observable callback ordering. Similar behavior is useful substrate evidence; differences localize host policy.

## Unknown frontier
AEIG has not proven AE's current import path directly uses this Premiere Async File Reader Suite. Exact file-staleness detection, reopen policy and callback serialization in AE MediaFoundation remain reconstruction targets.

Related: `docs/host-integration/aeio/overview.md`, `docs/media-system/media-identity.md`, `docs/media-system/runtime-architecture.md`, `docs/foundations/cross-host-triangulation.md`.
