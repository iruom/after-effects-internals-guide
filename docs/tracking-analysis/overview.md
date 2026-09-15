---
status: active
last_verified: 2026-09-15
---
# Tracking and Analysis

Tracking features are temporal analysis systems, not merely UI tools. AEIG will distinguish analysis state, user-visible keyframes, caches, source-frame requests and final render behavior.

## Scope
Mask Tracker; point/motion tracking; Warp Stabilizer-style analysis; camera tracking; motion estimation; feature propagation and related analysis effects.

## Questions
- What analysis results are persisted in the project versus external/cache storage?
- Which source-frame intervals are requested and how are edits invalidated?
- Is analysis state represented as ordinary streams, opaque effect state, auxiliary files, cache entries or combinations?
- How do analysis and render scheduling interact with MFR/work queues?
- Which tracking operations use shared Adobe media/GPU/ML infrastructure?

## Evidence surfaces
Project and preset diffs; effect/AEGP interfaces; disk/cache artifacts; process and GPU traces; fixed-issue history; controlled footage perturbation tests.

The updated Mask Tracker in AE 26.3 provides a current product surface for versioned analysis experiments.

## State/execution split
Installed AE 2025 evidence makes the classic Motion Tracker partially transparent: tracker groups and point data are addressable TDB-derived streams, including feature/search regions, attach point/offset and confidence. This gives AEIG a concrete project-state side of the tracker.

Analysis execution should remain separate in the model. Modern tracker preferences, source-resolution behavior and asynchronous analysis infrastructure can change how samples are computed without changing the semantic meaning of stored tracking coordinates.

Working model: `persistent tracker streams/config -> time/source/ROI analysis request -> transient analysis engine -> stream/keyframe updates -> downstream layer/mask use`.

See `F-TRACK-001`, `F-TRACK-002-motion-tracker-state-is-stream-addressable.md` and the persistence experiment queue.

## Current public execution boundaries
The 3D Camera Tracker explicitly performs analysis and solve work in a **background process** while the user continues editing. This makes process lifetime, cancellation and publication of solved camera/point state part of the feature architecture rather than an implementation detail.

The Mask Tracker is a different analysis plane. AE 26.3 introduced a substantially faster tracker and moved primary controls closer to the Timeline, but its semantic output remains mask/path state in the project. Analysis execution and persisted result state must therefore remain separate in AEIG.

## Resolution and coordinate invariants
Adobe fixed a 26.x Mask Tracker failure that occurred when composition resolution was below Full. This is direct symptom evidence that analysis-input sampling/resolution and stored semantic mask coordinates cross a conversion boundary.

A correct reconstruction should preserve full semantic coordinates while allowing the analysis engine to consume downsampled or preprocessed images. Preview/downsample policy is therefore not itself the tracker result identity.

## Background analysis publication model
A conservative shared model is:
`persistent tracker/mask/camera configuration -> source/time/ROI request -> background/transient analysis -> provisional analysis state -> project stream/keyframe/camera publication -> downstream render use`.

3D Camera Tracker additionally publishes solved scene/camera geometry; classic Motion Tracker publishes tracker-point/property data; Mask Tracker publishes mask-shape evolution. Do not assume these features share one solver or cache merely because all are called tracking.

## Failure classes and experiments
Separate failures into source-sampling/ROI errors, coordinate conversion errors, solver/model errors, cancellation/stale-publication errors, persistence errors and downstream application errors.

For each tracker run identical source footage under Full/Half/Quarter preview, fresh/reused host, warm/cold media cache and interrupted/restarted analysis. Record source request dimensions, process/module activity, final semantic coordinates, AEP/AEPX diffs and output hashes.

## Unknown frontier
Still unresolved: exact helper-process/IPC identity for modern 3D Camera Tracker analysis; whether Mask Tracker 26.3 uses a shared DVA tracking backend; cache/persistence format for intermediate camera solves; exact cancellation granularity; relationship between classic TDB tracker streams and modern Mask Tracker result storage.

Related: `F-TRACK-001`, `F-TRACK-002-motion-tracker-state-is-stream-addressable.md`, `docs/temporal-system/temporal-dependencies.md`, `docs/evaluation/work-queues.md`.
