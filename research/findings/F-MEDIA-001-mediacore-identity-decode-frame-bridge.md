---
status: strongly-supported-local
last_verified: 2026-09-15
evidence: E2-L runtime symbols + E0/E1 AEIO/Premiere comparison
versions: AE 2025 runtime; AE 25.6 SDK comparison
---
# F-MEDIA-001 — MediaCore separates asset identity, decode scheduling and frame residency

The installed AE 2025 runtime exposes a multi-layer media path rather than one generic importer/cache subsystem.

## Asset and mutable-content identity
`EAMedia.dll` exports `GetMediaDocumentIDAndContentState(media, Guid&, Guid&)` and `GetXMPContentState`. `RenderableSourceIdentifier` has a GUID-valued hash and serialization cache. `DynamicLinkMedia::BaseMediaInfo` independently exposes `GetDocumentID()`, `GetContentState()`, `GetRuntimeGuid()` and hash/modification-state surfaces.

This locally corroborates the Adobe-wide identity pattern seen in Premiere's Media Accelerator API: a relatively stable document/asset identity can be separated from mutable content state.

AEIG must not assume these GUID values are bit-identical across EAMedia, Dynamic Link, Premiere Media Accelerator, BEE render GUIDs or VideoFrame caches without a controlled comparison.

## Import/decode layer
`ImporterHost.dll` exposes `FileImporter`, `Importer`, `ImporterFactory` and `ImporterModule`, including deferred-processing, media-analysis, metadata, trim and media-file interfaces. Importers add video/audio/data streams and can add decoded `IVideoFrame` objects to importer-side caches.

`MediaFoundation.dll` provides `DecodeRequest`, `DecodeQueue`, `IdentifiedDecodeRequest`, `IdentifiedDecodeQueue`, in-memory/filesystem `DataCache`, `DataCacheChain`, cache guards and managed disk-cache volumes. Decode requests expose CPU/I/O cancellation paths and queues are created over an asynchronous executor.

This is a materially different concurrency surface from legacy AEIO's frozen host-callback `AEIO_FunctionBlock4` contract.

## Frame-materialization layer
`VideoFrame.dll` maintains host/device and shared frame caches keyed by GUID, supports dependency registration on cached frames, and bridges the common `MF::IVideoFrame` representation into both After Effects `PF_World` and Premiere-style `PPix` objects. CPU/GPU video-frame conversion is part of the same layer.

A useful model is:
`media locator/file + DocumentID/ContentState -> importer/stream -> identified decode request/queue -> IVideoFrame -> GUID frame residency -> PF_World / PPix consumer`.

This path is adjacent to, but not equivalent to, BEE/RG compositing cache identity.

## Audio is a parallel branch
`ImporterHost` also exposes `ConformedAudioSourceFile` implementing async/source/file interfaces, with database, cancellation and render-request lifecycle functions. Media decode and audio conform therefore share host infrastructure without being the same payload/cache path.

## Reproduction and falsification
Run `probes/process-tools/inventory_media_pipeline_symbols.py` to regenerate `datasets/ae-2025-media-pipeline-symbols.csv`.

The model can be tested by tracing one footage request while independently changing file content, XMP/content state, decode quality/pixel format and comp/effect state. If media decode/frame-cache identities remain stable across pure downstream comp edits but change on media/content edits, that separates MediaCore residency from compositing cache identity.

Open questions: exact mapping from AE footage/item identity to MediaCore `DocumentID`; how `IdentifiedDecodeRequest` identity is constructed; which decode caches are shared across Adobe apps/processes; and where importer-side frame caches hand off to AE's BEE request system.
