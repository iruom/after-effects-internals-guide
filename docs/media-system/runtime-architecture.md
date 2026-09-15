---
status: active
last_verified: 2026-09-15
---
# Media Runtime Architecture

AE ships both the legacy AEIO boundary and the shared Adobe MediaCore runtime. They should be modelled as overlapping integration eras, not collapsed into one importer API.

```text
file / media locator / XMP
        |
        +--> DocumentID + ContentState
        |
        v
ImporterHost
(FileImporter / ImporterModule / video-audio-data streams)
        |
        v
MediaFoundation
(IdentifiedDecodeRequest / DecodeQueue / DataCache)
        |
        v
MF::IVideoFrame
        |
        +--> VideoFrame GUID caches / CPU-GPU residency
        |
        +--> PF_World bridge (AE Effect/render side)
        +--> PPix bridge (Premiere/shared Adobe side)
```

## Identity layers
Keep at least four identities distinct until experiments prove equivalence:
1. **Asset identity** — DocumentID / locator identity.
2. **Content/version identity** — ContentState / XMP content state.
3. **Decode request identity** — identified decode requests, format/time/quality dependent work.
4. **Frame residency identity** — GUID-keyed `IVideoFrame` caches on host/device/shared stores.

Downstream BEE/RG frame identity is a fifth layer because composition/effect state can change without changing the underlying media decode.

## Request dimensions visible in the runtime
`MF::FrameFormat` contains pixel format, bounds, pixel aspect ratio, field type, render quality, color space and stream format. This makes format/color/quality part of media-frame materialization rather than metadata attached only after decode.

Decode work has explicit cancellation for generic, CPU-processing and I/O phases. This should inform experiments around scrubbing, rapid source changes and abandoned preview requests.

## AEIO coexistence
AEIO still exposes time/scale/required-region requests through the legacy host callback model. MediaCore adds asynchronous decode queues, shared frame objects, richer identity/cache services and Adobe-wide interop. Which importer route is chosen is therefore itself a version/format research dimension.

## Cross-links
- `docs/host-integration/aeio/overview.md`
- `docs/media-system/adobe-media-accelerator-identity.md`
- `research/findings/F-IO-001-aeio-vs-mediacore-async-boundary.md`
- `research/findings/F-MEDIA-001-mediacore-identity-decode-frame-bridge.md`
- `datasets/ae-2025-media-pipeline-symbols.csv`

## BEE bridge object refinement
The handoff into AE is now directly visible. `BEE_LayerMCMediaInfo` implements the shared BE media-info/file/metadata interfaces and can construct `MF::ISource` streams. `BEE_LayerMCVideoSource` then implements async video/audio/source interfaces inside `BEE.dll` itself.

This means BEE does not merely consume anonymous decoded pixels. It carries project/layer context through concrete MediaCore-compatible bridge objects. Source requests include time plus `MF::FrameFormat`, and BEE exposes a corresponding source-video identifier before downstream composition rendering.

Refined chain:
`BEE footage/layer -> BEE_LayerMCMediaInfo -> MF source -> BEE_LayerMCVideoSource -> source-video request identity -> IVideoFrame -> BEE/RG`.

Smart-render segments and still ranges exist on this media-source side and should remain distinct from BEE/RG checkout receipts and compositing cache sufficiency.

See `F-MEDIA-002-bee-mediacore-layer-source-bridge.md`; the media symbol dataset now includes BEE bridge surfaces.
