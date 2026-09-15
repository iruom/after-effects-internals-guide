---
status: active
last_verified: 2026-09-16
evidence: AEGP_KeyframeSuite3 current contract + historical suite notes + point-coordinate compatibility history
---
# Keyframe API History and Coordinate Semantics

A keyframe in AE is not merely `(time, value)`. The public AEGP API exposes separate time coordinates, value dimensionality, temporal dimensionality, interpolation classes, spatial tangents, temporal ease, flags and batch-edit transactions.

## Zero keyframes does not mean constant
`AEGP_GetStreamNumKFs()` returns `AEGP_NumKF_NO_DATA` when the stream has no keyframe-accessible value domain. A return value of zero is different: the stream is keyframe-able but currently has no authored keys.

Adobe explicitly warns that zero keyframes still does **not** prove a constant stream because an expression can drive the value. Keep these states separate:
- no keyframe data domain;
- keyframe-able stream with zero authored keys;
- keyed stream;
- effective time variation caused by expressions/derived state.

`AEGP_IsStreamTimevarying()` is therefore semantically different from "number of keyframes > 0".

## Layer time versus composition time
Keyframe insertion and time queries accept `AEGP_LTimeMode`, allowing layer-time or composition-time coordinates. This matters for stretched, offset and time-remapped layers.

Never persist a bare numeric key time without its coordinate system. A robust record is `(time value/scale, time mode, owning layer/stream)`.

## Value dimensionality is not temporal dimensionality
`AEGP_GetStreamValueDimensionality()` and `AEGP_GetStreamTemporalDimensionality()` are separate APIs. Temporal ease indexing uses temporal dimensionality, not blindly the number of stored components.

This matters for property types whose displayed/value representation and temporal interpolation degrees of freedom differ. Code that loops ease dimensions using value dimensionality can read/write the wrong dimensions.

## Interpolation is a capability mask
`AEGP_GetValidInterpolations()` returns which interpolation families are legal for a stream: NONE, LINEAR, BEZIER, HOLD, CUSTOM or ANY. Do not assume every property accepts spatial Bezier or every keyed property accepts the same temporal modes.

The host owns the legality of interpolation for the stream type.

## Spatial tangents have coordinate semantics
`AEGP_GetNewKeyframeSpatialTangents()` returns owned `AEGP_StreamValue2` tangent values that must be disposed. The setter does not adopt caller-owned values.

Historical compatibility note: in `AEGP_KeyframeSuite2` and earlier, spatial tangent values for effect point-control streams and Anchor Point were wrong because they were not multiplied by layer size. The later suite corrected this.

This is a concrete example of an ABI-compatible-looking API whose numerical coordinate semantics changed between suite generations.

## Temporal ease units are not UI units
`AEGP_GetKeyframeTemporalEase()` indexes dimensions from `0` to `temporal_dimensionality - 1`. The Guide notes that returned ease values must be multiplied by layer height to match values displayed in the AE UI.

This is precisely the kind of host-coordinate conversion that must be preserved in tooling: raw SDK values and UI presentation values are not necessarily identical units.

## Point controls have their own historical coordinate transition
Effect point controls have another compatibility history. Prior to API specification 12.1 / AE 4.0, default point values used a normalized 0..100-style convention; modern hosts return point values in absolute layer pixels for newer API versions. Older plug-ins can retain the old behavior through their declared API version.

Buffer expansion adds yet another coordinate offset: `pre_effect_source_origin_x/y` shifts point coordinates as upstream effects expand the world. An animated expansion can make a non-animated point's effective coordinate move from frame to frame.

Therefore `point value == one immutable layer-space coordinate` is unsafe without accounting for API generation and upstream buffer origin.

## Batch insertion is a transaction
`AEGP_StartAddKeyframes()` returns a batch/cookie used by `AEGP_AddKeyframes()` and `AEGP_SetAddKeyframe()`, then `AEGP_EndAddKeyframes(addB)` commits or abandons the accumulated edit.

This avoids treating every single inserted key as an independent undo/database mutation. The pattern matches a broader AEGP convention: begin/end APIs bracket operations where AE must preserve coherent state around multiple edits.

For bulk editors, this is preferable to repeated standalone insertion when the entire change is conceptually one user action.

## Handle invalidation after mutation
AEGP references are short-lived. The Guide explicitly notes that adding a keyframe to a stream invalidates references to that stream. A batch editor should therefore not assume pre-edit `AEGP_StreamRefH`/related refs remain valid after the transaction.

A safe workflow is:
1. acquire stream and metadata;
2. perform the documented keyframe transaction;
3. finish/commit;
4. release stale refs;
5. reacquire before further structural inspection.

## Flags and interpolation state
Keyframe flags independently encode temporal/spatial continuity, auto-Bezier and related behavior. A value/tangent dump without flags is incomplete for reconstructing interpolation semantics.

Likewise, identical keyframe values/times can produce different motion because spatial tangents, temporal ease and interpolation flags differ.

## Version-sensitive failure patterns
- use pre-fix tangent semantics with newer suite -> scale error on Anchor Point/point controls;
- compare raw ease values directly to UI values -> apparent mismatch by host coordinate scale;
- assume API point coordinates are version-invariant -> wrong defaults for legacy plug-ins;
- cache point values across animated upstream expansion without origin correction -> drifting geometry;
- retain stream refs across key insertion -> invalid opaque handle;
- infer constant value from zero keys -> miss expression-driven variation;
- iterate temporal ease using value dimensionality -> wrong dimension indexing.

## Reconstruction experiments
Build a fixture matrix covering Position, Anchor Point, effect Point Control, Scale, Rotation, Color and a property with custom interpolation.

For each stream record:
- value dimensionality and temporal dimensionality;
- valid interpolation mask;
- key times in LayerTime and CompTime;
- key values;
- spatial in/out tangents where supported;
- temporal ease per temporal dimension;
- keyframe flags;
- pre/post-expression evaluated values.

Then repeat on retained SDK/host generations where available. A versioned corpus can distinguish genuine interpolation changes from coordinate/unit changes in the API layer.

## Unknown frontier
The public API describes authored keyframe semantics but not all internal interpolation machinery. Still unresolved:
- exact current numerical implementation of spatial Bezier/arc-length evaluation;
- how interpolation caches are keyed/rebuilt after tangent/ease edits;
- relationship between roving-keyframe timing solve and AEGP temporal ease representation;
- whether every derived property materializes a conventional keyframe object internally;
- how keyframe mutations propagate into TDB stream identity and BEE render GUIDs.

Related: `docs/animation-system/spatial-interpolation.md`, `docs/state-model/streams-properties.md`, `docs/temporal-system/time-model.md`, `docs/evaluation/dirty-invalidation.md`.
