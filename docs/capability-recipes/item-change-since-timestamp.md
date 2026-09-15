---
status: active
last_verified: 2026-09-16
evidence: historical/current AEGP Render Suite contract + AEIG state-identity model
---
# Ask Whether an Item Changed Since an Edit Generation

`AEGP_GetCurrentTimestamp()` and `AEGP_HasItemChangedSinceTimestamp()` answer a very specific question: whether render-relevant **video state for an item over a time interval** changed since a captured project timestamp.

They are useful for speculative/external renderers and project-derived caches, but they are not a universal cache-validity API.

## Timestamp semantics
The Render Suite documentation states that the project `AEGP_TimeStamp` is updated whenever an item is touched in a way that affects rendering. Capture it before doing expensive work, then later ask whether a target item's video changed over `[start_time, duration]` since that generation.

The interval matters. A change outside the queried time range need not make the answer useful for the range you care about, while temporal effects or time-dependent dependencies can make a seemingly local edit relevant across multiple frames.

## Important exclusion: audio
Adobe explicitly notes that `AEGP_HasItemChangedSinceTimestamp()` does **not** track audio changes. Never use a `false` video-change result to validate an audio render, waveform, conform state or mixed output.

## Speculative rendering pattern
The same Render Suite lineage pairs the timestamp query with `AEGP_IsItemWorthwhileToRender()`. Adobe recommends a speculative renderer check whether the frame is worthwhile **before** sending work out and check again when the result returns, before allocating/checking the rendered world back into AE.

That second check closes a race:

`timestamp T -> external render starts -> project changes -> old render completes`

Without revalidation, a result that was valid when scheduled can be stale when it arrives.

`AEGP_CheckinRenderedFrame()` then hands a rendered platform world to AE together with the render options/timestamp context. The host adopts the frame; ownership and lifetime therefore change at checkin.

## What an unchanged result does not prove
It does not prove that every external file, decoded-media state, GPU resource, plug-in-global cache, color-management environment, render-option handle or private cache node is reusable. It answers the documented item/video edit-generation question only.

If your derived state depends on anything outside that contract, add your own dependency identity rather than stretching timestamp semantics beyond what Adobe documents.

## Version and capability discipline
This API lives in historical Render Suite lineage, so acquire the exact suite generation supported by the running host. Do not assume that a symbol seen in one Guide snapshot means identical table layout or semantics in every AE generation.

## Failure modes and tests
Test edits that should and should not affect the queried interval: parameter changes, layer enable/disable, source replacement, time remap, upstream precomp edits and audio-only changes. Capture the timestamp, mutate one thing, and compare the API result with an independently hashed render.

For race testing, schedule speculative work, mutate after scheduling but before completion, and verify the second worthwhile/changed check prevents stale checkin.

## Evidence and cross-links
Primary evidence: AEGP Render Suite documentation for `AEGP_GetCurrentTimestamp`, `AEGP_HasItemChangedSinceTimestamp`, `AEGP_IsItemWorthwhileToRender` and `AEGP_CheckinRenderedFrame`.

Related: `docs/cache-system/state-identity.md`, `docs/evaluation/dirty-invalidation.md`, `docs/render-graph/render-tasks.md`, and receipt/GUID documentation.

## Unknown frontier
The public timestamp is an edit-generation abstraction. AEIG does not equate it with BEE Render GUIDs, receipt GUIDs, RG cache identity or project undo generation unless experiment explicitly connects those identities.
