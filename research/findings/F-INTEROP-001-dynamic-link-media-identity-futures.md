---
status: strongly-supported-local
last_verified: 2026-09-15
evidence: E2-L installed AE 2025 runtime
versions: AE 2025
---
# F-INTEROP-001 — Dynamic Link media preserves MediaCore identity and asynchronous request state

`DynamicLinkMedia.dll` is not merely an opaque IPC shim. Its `BaseMediaInfo` implements MediaCore/BE media interfaces and exposes `GetDocumentID`, `GetContentState`, `GetRuntimeGuid`, `GetHashInfo`, stream enumeration/source creation and cacheability state.

The module depends on `MediaFoundation.dll`, `VideoFrame.dll` and `ImporterHost.dll`, placing Dynamic Link media inside the same broad media object model as local imported footage.

## Asynchronous request boundary
The runtime exports `CreateRequestFuture`, `CancelRequest`, `TryCancelRequest`, `WaitForRuntimeGuid`, `WaitForXMP` and connection-status fulfillment paths. A Dynamic Link source therefore has explicit pending/request lifetime rather than behaving as a synchronous file read.

This helps separate three interop concerns: remote/project source identity, asynchronous transport/request state, and the common media/frame representation consumed after fulfillment.

## Important non-equivalence
`RuntimeGuid` should not be conflated with `DocumentID` or `ContentState`. Their separate accessors imply different roles even if some implementations may derive one from another. Likewise a request GUID used by Future/cancellation machinery is not automatically a media-version GUID.

## AEIG model
`remote/project source identity -> Dynamic Link request/future -> fulfilled MediaCore source/stream -> IVideoFrame/media consumer`, with DocumentID/ContentState surviving as media-level identity coordinates.

## Next experiments
Trace a Dynamic Link comp while changing only source project content, only AE-side downstream effects, and only transport/session state. Compare request IDs, media identity, frame-cache reuse and reconnection behavior. This would distinguish content invalidation from connection/request invalidation.

Runtime evidence is preserved by `datasets/ae-2025-media-pipeline-symbols.csv`.
