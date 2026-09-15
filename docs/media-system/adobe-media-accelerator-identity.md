---
status: active
last_verified: 2026-09-16
evidence: Premiere Media Accelerator/importer contracts + local AE 2025 ImporterHost/MediaCore runtime surfaces
---
# Adobe Media Accelerator Identity Pattern

Adobe's importer/media infrastructure exposes a useful two-axis identity model: **stable document/asset identity** and **mutable content-state identity**. This is stronger than using file path or modification time as the only cache key.

Premiere's Media Accelerator Suite accepts a Document ID and Content State GUID when registering/finding derived-media artifacts. The importer contract also exposes `imQueryContentState`: if the clip's semantic content has not changed, the importer should return the same content-state GUID.

A useful abstraction is:

`AssetIdentity = DocumentID`

`VersionIdentity = ContentState`

`DerivedArtifact = f(DocumentID, ContentState, artifact-key)`

The artifact key then distinguishes different accelerator/conform/analysis products derived from the same asset version.

## Why path alone is insufficient
One source can move without changing content, one path can be replaced with different content, and multi-file media can change through a subordinate file while the primary path remains unchanged. A path-only cache cannot represent all three cases correctly.

`imQueryContentState` was introduced specifically for streaming/folder-based/multi-file importers where checking only the main file's timestamp is insufficient.

## Validation, not just lookup
Premiere's Media Accelerator Suite evolved to include content-state validation when locating an existing accelerator. That matters because a database hit is not equivalent to a valid hit: the host must establish that the derived artifact still corresponds to the current content state.

This is the media-side analogue of AEIG's broader cache rule:

`identity -> lookup -> validity test -> residency/materialization`

Do not collapse those into one boolean called "cached".

## Local AE runtime evidence
AE 2025's installed `ImporterHost.dll` exposes MediaAccelerator-related interface/vtable vocabulary and an explicit `RegisterAcceleratorHandler` runtime export. The same local media inventory contains importer/module and MediaFoundation bridge surfaces.

That proves Media Accelerator-style substrate exists in the installed AE media runtime. It does **not** prove that After Effects exposes Premiere's public `PrSDKMediaAcceleratorSuite` to AE plug-ins or that every AE conform/cache database uses an identical schema.

## Interaction with downstream render identity
Source identity should remain separate from composition/render identity. An effect edit can invalidate BEE/RG output while the decoded source frame remains valid; a source-content change can invalidate media-derived artifacts even if layer/effect topology is unchanged.

A useful chain is:
`DocumentID + ContentState -> decode/derived-media identity -> frame residency -> BEE source-video identity -> composition/render GUID`.

## Failure modes
Watch for stale accelerator reuse after source replacement, unnecessary invalidation after path-only moves, multi-file media whose secondary resource changed, XMP/DocumentID duplication, offline-media transitions, and content-state implementations that hash only a subset of semantically relevant source files.

For an importer, a stable GUID is a correctness contract: returning the same content state after meaningful source change can poison every downstream derived cache that trusts it. Returning a new state for irrelevant changes destroys reuse and increases conform/decode work.

## Experiments
Use copied/moved/replaced media with controlled XMP, modification-time and byte changes. For folder media, mutate one subordinate file at a time. Record importer content state, accelerator/conform reuse, decoded-frame identity and downstream render-cache behavior independently.

## Evidence and unknown frontier
External contract evidence comes from the Premiere Pro C++ SDK importer/Media Accelerator documentation. Local evidence is `datasets/ae-2025-media-pipeline-symbols.csv`, where installed AE `ImporterHost.dll` exposes MediaAccelerator-related surfaces.

Related: `docs/media-system/runtime-architecture.md`, `docs/cache-system/state-identity.md`, `research/findings/F-MEDIA-001-mediacore-identity-decode-frame-bridge.md`, and `F-MEDIA-002-bee-mediacore-layer-source-bridge.md`.

The unresolved question is not whether Adobe uses content identity, but exactly how AE maps DocumentID/ContentState, XMP, source-video IDs and cache database keys in each media path and release. AEIG keeps that mapping open until differential evidence connects them.
