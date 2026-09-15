---
status: strongly-supported-local
last_verified: 2026-09-15
evidence: E2-L installed AE 2025 runtime
versions: AE 2025
---
# F-MEDIA-002 — BEE layer sources directly implement shared MediaCore/BE media interfaces

The BEE/media boundary is not only an external call from the render graph into a separate decoder. AE 2025 exports concrete bridge classes inside `BEE.dll`.

`BEE_LayerMCMediaInfo` implements shared `BE::IMediaFile`, `BE::IMediaInfo` and `BE::IMediaMetaData`. It exposes `GetDocumentID`, `GetContentState`, modification/hash state, stream enumeration and `CreateSourceForStream(... -> MF::ISource)`.

`BEE_LayerMCVideoSource` implements `BE::IAsyncVideoSource`, `BE::IVideoSource`, audio-source interfaces, `MF::ISource`, `MF::IRenderableExtendedStillInfo` and `MF::ISmartRenderSegmentInfo`.

The bridge performs format/time-sensitive frame requests: `GetSourceVideo(time, FrameFormat, BinaryData)`, `GetVideo`, `GetVideoWithMatrix`, preferred-format selection, async I/O initiation/cancellation, still-range queries and smart-render-segment discovery.

`GetIdentifierForSourceVideo(time, FrameFormat, BinaryData)` is especially important: media-source request identity is explicitly parameterized by time and frame format before the result enters downstream BEE compositing.

## Refined model
`BEE footage/layer identity -> BEE_LayerMCMediaInfo -> shared media source/stream -> BEE_LayerMCVideoSource -> time+FrameFormat source identity -> IVideoFrame -> downstream BEE/RG render request`.

This makes the handoff bidirectional: BEE owns project/layer context while implementing the shared Adobe media interfaces required to obtain decoded source material.

## Smart-render caution
`DetermineSmartRenderSegmentsInRange` and still-range discovery indicate that source reuse can be interval/segment aware before ordinary compositing. Do not equate a media smart-render segment with an AE frame-cache receipt; they belong to different request layers.

Reproduction is included in the updated `inventory_media_pipeline_symbols.py` dataset, which now inventories BEE media bridge symbols as well.
