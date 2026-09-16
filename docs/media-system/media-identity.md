---
status: active
last_verified: 2026-09-16
primary_evidence:
  - AE 2025 EAMedia / ImporterHost / MediaFoundation / VideoFrame runtime surfaces
  - AE 2025 BEE MediaCore bridge symbols
  - DynamicLinkMedia runtime surfaces
  - Premiere 26 importer and PPix cache contracts as cross-host comparison
---
# Media Identity: Asset, Content State, Request, and Frame

Media identity in After Effects is layered. A file path, project item, importer instance, decoded frame, cache entry, and rendered layer are not interchangeable identities even when they ultimately refer to the same visible footage.

## Identity layers
A practical model separates at least six coordinates:

1. **Asset/document identity** — which logical external media object is being referenced.
2. **Content/version state** — whether the bytes, metadata, or interpretation of that asset changed.
3. **Importer/runtime identity** — one host-side source/import instance and its transient lifetime.
4. **Media request identity** — stream, time/sample range, decode quality, pixel/color interpretation, ROI, and cancellation generation.
5. **Decoded-frame identity** — the resulting MediaCore `IVideoFrame` representation and its residency.
6. **AE render identity** — layer/effect/render-context state after the media frame enters BEE/RG evaluation.

Local `EAMedia` and `DynamicLinkMedia::BaseMediaInfo` surfaces expose separate `DocumentID`, `ContentState`, runtime GUID/hash state, stream enumeration, and asynchronous request functions. Their separation is evidence against modeling AE media with one universal GUID.

## Content state is not a path
A stable pathname does not imply stable media content. Importer and shared-media contracts expose explicit source-staleness/content-state concepts, while frame-cache contracts add preferences, decode quality, format, and color interpretation to the request identity.

This gives two independent questions: **is this still the same logical asset?** and **is this still the same content/version of that asset?** A relink, growing file, XMP change, proxy change, or external rewrite can preserve one coordinate while changing another.

## Request identity precedes compositing identity
`MediaFoundation` exposes `DecodeRequest`, `IdentifiedDecodeRequest`, decode queues, asynchronous executors, and CPU/I/O cancellation. `MF::FrameFormat` carries pixel format, bounds, pixel aspect ratio, field type, render quality, color space, and stream format.

AE 2025 also exposes `BEE_LayerMCVideoSource::GetIdentifierForSourceVideo(time, FrameFormat, BinaryData)`. This is direct evidence that source-video identity is parameterized before downstream BEE/RG compositing. A downstream effect edit can therefore invalidate AE render identity while leaving the source decode request reusable.

Cancellation identity is a lifetime/control coordinate, not automatically content identity. An obsolete scrub request can be cancelled without making an already-decoded equivalent frame semantically invalid.

## Decoded frame identity and residency
`VideoFrame.dll` exposes GUID-keyed host/device/shared frame caches and bridges common `MF::IVideoFrame` objects into After Effects `PF_World` and Premiere-style `PPix` consumers. Keep **semantic frame identity** separate from **where that frame is resident**.

A frame can be evicted and later reconstructed without semantic change. Conversely, a resident frame can become unusable for a new request because format, color, quality, source content, or downstream render context changed.

## BEE is the handoff, not an identity collapse
`BEE_LayerMCMediaInfo` implements shared media-file/media-info interfaces and exposes document/content state while constructing `MF::ISource` streams. `BEE_LayerMCVideoSource` then performs time/format-sensitive source requests before the result enters ordinary BEE/RG rendering.

The useful chain is:

`asset/document -> content state -> importer/source -> time+FrameFormat request -> IVideoFrame -> BEE/RG render request -> output/cache receipt`.

Do not assume GUIDs or receipts at adjacent arrows are bit-identical. The evidence supports a chain of related identity responsibilities, not one serialized master key.

## Dynamic Link adds transport/session identity
Dynamic Link preserves media-level `DocumentID` / `ContentState` while also exposing `RuntimeGuid`, request futures, cancellation, connection-status fulfillment, and wait operations. This adds a transport/session coordinate that can change independently of source content.

A serving AE restart can therefore replace runtime/request identity while preserving the linked composition's logical content. A remote project edit can change content state without requiring the downstream Premiere effect stack to become a different logical object.

## Cross-host comparison: Premiere PPix cache
Premiere's PPix cache makes a similar separation explicit. Import-frame identity includes importer instance, stream/frame, accepted formats, preferences, quality, and later color profile/space state; dependency registration separately controls retention. This is cross-host evidence for the invariant, not proof that AE uses the same implementation.

## Failure classes
- path treated as immutable content identity -> stale decode after external modification;
- persistent project-item ID used as frame identity -> reuse across changed media state;
- request/cancellation ID treated as content version -> unnecessary cache destruction;
- decode-frame GUID treated as BEE render GUID -> downstream effect/context invalidation is missed;
- format/color/quality omitted from frame equivalence -> semantically wrong reuse;
- residency miss interpreted as semantic change -> recomputation/eviction is misdiagnosed;
- Dynamic Link disconnect interpreted as source-content mutation -> transport and content failures are conflated.

## Reconstruction experiments
Use one source and mutate one coordinate at a time: external file bytes, XMP/content state, importer preference, decode quality, pixel/color format, comp/effect state, process restart, and Dynamic Link session restart. Record observable media IDs, request/trace activity, frame hashes, BEE/RG identity footprint, and cache reuse.

The strongest discriminator is a pair of edits with opposite boundaries: a pure downstream effect edit should change compositing identity without requiring a different source frame; a pure source-content edit should invalidate media-derived identity even when composition topology is unchanged.

## Unknown frontier
Still unresolved are the exact mapping from AE project footage IDs to MediaCore `DocumentID`, construction of `IdentifiedDecodeRequest` keys, which frame caches are shared across Adobe applications/processes, whether media GUIDs survive every process restart, and the exact handoff from VideoFrame residency into BEE/RG cache-node identity.

Cross-links: `runtime-architecture.md`, `../state-model/object-identity.md`, `../cache-system/state-identity.md`, `../interop/overview.md`, `../host-integration/premiere-pro/ppix-cache.md`, `../../research/findings/F-MEDIA-001-mediacore-identity-decode-frame-bridge.md`, and `../../research/findings/F-MEDIA-002-bee-mediacore-layer-source-bridge.md`.