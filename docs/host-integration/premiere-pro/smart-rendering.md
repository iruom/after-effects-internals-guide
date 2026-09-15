---
status: active
last_verified: 2026-09-14
---
# Premiere Smart Rendering: Segment Reuse Instead of Pixel Recompute

Premiere's `PrSDKSmartRenderingSuite` uses the term Smart Rendering for a mechanism fundamentally different from AE SmartFX. It builds maps from timeline segments back to reusable source-media segments.

## Segment representation
`PrClipSegmentInfo` carries clip identity, timeline segment start/end, segment offset, clip start/end, source-media start/end and source path. The path is temporary callback-owned data and must be copied by the plug-in if retained.

This is a direct source-reuse map rather than a pixel ROI or effect pre-render contract.

## Multiple admissibility modes
The suite can build ordinary smart-render segment lists, lists that exclude preview files, ancillary-data maps, and color-managed segment lists. Pixel format, time base and—on color-managed paths—color-space ID participate in list construction.

The host therefore evaluates smart-render eligibility under an output interpretation, not solely by asking whether timeline media bytes exist.

## Importer/exporter handshake
The importer selector `imGetExtendedFormatInfo` exists specifically to provide extended format data to an associated exporter for match-source and/or smart rendering. Adobe warns that this information may be serialized into the project and that its UUID must change if the format-data extent or interpretation changes.

This is an explicit versioned serialization contract between source importer, project persistence and exporter reuse logic.
## Extended-format negotiation is bidirectional
`kExportInfo_SourceExtendedFormat` does not merely hand one importer blob to the exporter. The query record contains an exporter-supplied validation callback that classifies candidate source-format descriptions as acceptable, unacceptable, or no-comment; the host returns a final selected format.

The apparent flow is therefore:
`importer format description -> host candidate/query logic -> exporter validation -> selected reusable format`.

This makes Smart Rendering eligibility a negotiated compatibility problem, not a raw codec-name comparison.

## Compressed-frame importer path
The Importer selector table separately exposes `imGetFrameInfo`, optional `imGetCompressedFrame`, `imDisposeCompressedFrame`, and the ordinary decoded/rasterized `imImportImage` path. This is direct evidence that MediaCore can request compressed-frame materialization separately from raster image import.

The Smart Rendering segment-map API and compressed-frame selector are complementary evidence for a no-raster-recompute path, but the distributed SDK examples do not contain a complete end-to-end Smart Rendering implementation tying the two together. Keep that connection as a high-value reconstruction target rather than a proven call chain.

## Evidence gap to preserve
No example-project caller of `BuildSmartRenderSegmentList` and no example implementation of `imGetExtendedFormatInfo` was found in the inspected SDK corpus. The header contract is direct evidence; runtime ordering and compressed-byte transfer ownership still require tracing or a purpose-built importer/exporter probe.

## Version and failure boundary
Smart Rendering eligibility evolves with request/output interpretation. Adding color-management or extended-format fields means an older "source bytes are reusable" decision may no longer be sufficient for a newer export contract.

Failure classes include stale serialized extended-format metadata after importer changes, exporter/importer disagreement about admissible format, source-segment mapping errors at trims/timebase boundaries, and treating compressed-frame ownership/lifetime as decoded-frame ownership.

## Reconstruction experiments
Build a minimal importer/exporter pair that implements extended-format negotiation and one compressed-frame path. Change UUID/schema, output color space, time base and one source-format field independently, then observe project serialization and segment-list reuse.

For AE comparison, use the result only to ask where AE can avoid raster recompute through source/intermediate reuse; do not rename AE SmartFX behavior "Smart Rendering" based on Premiere terminology.

## Unknown frontier
The distributed Premiere SDK does not expose the full host call chain from segment list to compressed-frame export in one sample. AEIG has not proven an AE equivalent for source-segment bitstream reuse, nor that AE output modules share this exact negotiation substrate.

Related: `docs/foundations/cross-host-triangulation.md`, `docs/media-system/runtime-architecture.md`, `docs/render-graph/request-architecture-history.md`, `docs/persistence/sequence-data.md`.
