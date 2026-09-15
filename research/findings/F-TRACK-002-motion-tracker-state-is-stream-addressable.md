---
status: strongly-supported-local
last_verified: 2026-09-15
evidence: E2-L installed AE 2025 runtime + E0-G fixed-issue context
versions: AE 2025 runtime; AE 26.5 Mask Tracker behavior context
---
# F-TRACK-002 — Classic motion-tracker state is stream-addressable, while analysis execution is a separate layer

AE 2025 `AfterFXLib.dll` exports derived TDB match names for motion-tracker groups and individual tracker-point streams. The visible state includes feature center/size, search size/offset, attach point/offset and confidence.

This means at least the classic tracker exposes persistent/project-addressable state through the same broad stream system used by animation properties rather than storing the entire tracker result in one opaque analysis object.

Layer/UI code separately exposes tracker creation, current tracker selection, tracker type, point creation, region editing and application to layer state. Tracker UI state and stream state should therefore not be conflated with the temporary image-analysis engine that generates updates.

## Modern-analysis seam
The runtime also exposes preferences such as `GetEnableNewTrackingAlgorithm` and `GetEnableTrackerAutoPreprocessing`, while BEE has a generic WorkQueue analysis-job entry point and tracker-related feature flags. These are adjacency evidence only; they do not prove that every tracker runs through the BEE generic analysis job.

The 26.5 Mask Tracker fix for non-Full composition resolution provides a behavioral constraint: analysis-input resolution/coordinate conversion is an execution concern distinct from the semantic tracker coordinates stored in project state.

## Working model
`tracker UI/config streams -> analysis request over source/time/ROI/resolution -> transient tracker engine -> stream/keyframe updates + confidence -> downstream layer transform/mask use`.

## Next experiments
Diff AEP/AEPX while changing only feature/search regions, then while tracking one frame. Compare which state becomes ordinary stream/keyframe data versus opaque payload. Repeat the same tracking operation at Full/Half/Quarter resolution and verify that semantic coordinates remain invariant.
