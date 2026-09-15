---
status: active
last_verified: 2026-09-16
---
# Media System

After Effects media handling is not just "read a file into pixels". AEIG separates **asset identity, content/version state, decode-request identity, decoded-frame residency, and downstream composition/render identity** because those layers can invalidate independently.

A current runtime model supported by installed AE 2025 symbols is:

`locator/XMP -> DocumentID + ContentState -> ImporterHost streams -> MediaFoundation identified decode request/queue -> MF::IVideoFrame -> CPU/GPU/shared residency -> PF_World/PPix bridge -> BEE/RG consumer`

Legacy AEIO remains a public importer boundary alongside this shared MediaCore/MediaFoundation substrate. They represent overlapping integration eras, not one API with different names.

## Identity layers

**Asset identity** answers which source is being referred to. **Content state** answers whether the source's underlying content/version changed. **Decode request identity** additionally includes dimensions such as time, format, bounds, pixel aspect, field handling, quality and color representation. **Frame residency identity** answers whether an already-decoded frame exists in a reusable store. **BEE/RG identity** then adds composition/effect/render context.

This explains why an effect edit can invalidate composition output while a decoded source frame remains reusable, and why a source-file/content change can invalidate media-derived artifacts without changing layer topology.
## Request/materialization dimensions

Local `MF::FrameFormat` vocabulary includes pixel format, bounds, pixel aspect ratio, field type, render quality, color space and stream format. These are not merely labels added after decoding; they participate in what frame is requested/materialized.

Media decode also exposes explicit cancellation and queueing for general, CPU-processing and I/O phases. Scrubbing or rapidly changing requests can therefore abandon work below the composition renderer while leaving other media residency useful.

For developers, this means two frames at the same nominal source time are not necessarily interchangeable if requested format, quality, color or field semantics differ.

## BEE/MediaCore bridge

The handoff into AE is visible through BEE-side MediaCore-compatible objects such as `BEE_LayerMCMediaInfo` and `BEE_LayerMCVideoSource`. They carry project/layer context into source creation and asynchronous video/audio request surfaces rather than exposing only an anonymous decoded buffer.

The refined boundary is:

`BEE footage/layer -> BEE_LayerMCMediaInfo -> MF source -> BEE_LayerMCVideoSource -> source-video request identity -> IVideoFrame -> BEE/RG`

This is still an evidence-derived architecture model. Non-exported ownership, exact cache-key layouts and importer-selection policy remain private.

## AEIO coexistence

AEIO exposes the older host-driven importer contract with time/scale/required-region requests. MediaCore adds shared Adobe decode queues, frame objects, richer caching/residency and cross-host interop. When reproducing importer behavior, always identify which path the target media/version uses instead of assuming AEIO explains every current decode.
## Failure patterns

- **stale source state:** external content changes while an identity/version layer is not refreshed as expected;
- **format mismatch:** a decoded/resident frame is reused under incompatible color, field, quality or pixel-format requirements;
- **cancellation confusion:** abandoned preview/decode work is mistaken for a decoder failure;
- **residency vs render-cache confusion:** media remains decoded while downstream composition is correctly invalidated, or vice versa;
- **AEIO/MediaCore assumption:** a plug-in/debugger watches the wrong integration layer for the media type/version;
- **CPU/GPU bridge mismatch:** a frame conversion/residency transition changes precision, alpha or color semantics.

When debugging, record source/content identity, requested time/format/quality, decoder/importer path, residency location and downstream render identity separately. A single "frame cache hit" metric is not enough.

## Experiments

High-value fixtures include repeated same-time decode under different frame formats, source-file replacement without layer reconstruction, color-profile changes, field/pixel-aspect changes, aggressive scrubbing/cancellation, CPU/GPU residency transitions, still/sequence sources and AEIO-vs-built-in format comparisons.

Observe whether decode work, decoded frame GUID/residency and BEE/RG render work invalidate together or independently. Those deltas are more informative than timing alone.

## Version and unknown frontier

The concrete MediaCore chain is anchored in installed AE 2025 binary evidence. Legacy AEIO has much longer documented lineage. Exact importer routing and non-exported MediaCore internals can change between releases, so current symbol names must not be projected backward as universal architecture.

Control of MediaCore source/decode *below AEIO* remains an explicit capability boundary in `datasets/aeig-unknown-frontier.csv`; AEIG documents it for understanding and observability, not as a supported third-party invocation path.

Related material: `docs/media-system/runtime-architecture.md`, `docs/media-system/adobe-media-accelerator-identity.md`, `docs/host-integration/aeio/overview.md`, and `datasets/ae-2025-media-pipeline-symbols.csv`.
