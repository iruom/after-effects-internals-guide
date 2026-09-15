---
status: confirmed-public
last_verified: 2026-09-15
evidence: current-guide-26.5
---
# F-STREAM-003 — A Layer parameter now exposes render stage independently from layer identity

AEGP_StreamSuite7 (AE 26.5) exposes independent get/set of the render stage associated with a `PF_Param_LAYER` stream.

The parameter therefore contains at least two orthogonal semantic values:
1. the referenced source layer (`layer_id`), and
2. an `AEGP_LayerParamStage` describing where that layer is sampled in its render pipeline.

Published stages include:
- source pixels before masks/effects,
- masks applied with effects skipped,
- masks plus all effects,
- or a specific 1-based effect index N.

This publicly confirms that a layer reference is not sufficient to identify a sampled image.
## Internal-model implication
Model sampled-layer identity as something closer to:

`LayerSample = (LayerIdentity, Time, RenderStage, RenderContext, Quality/Representation)`

rather than as a bare Layer ID.

The stage model strongly aligns with older Canvas render receipts containing an effect-prefix depth and with LayerRenderOptions constructors for upstream/downstream effect states. It does not prove those APIs share one internal representation, but they expose the same conceptual boundary from different surfaces.

## Historical significance
AE 14.2 first exposed layer parameters that could include masks/effects. AE 26.5 makes the stage independently addressable through AEGP. This is a useful example of an internal concept gradually moving into the public API surface.