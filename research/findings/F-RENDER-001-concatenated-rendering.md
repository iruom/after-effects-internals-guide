---
status: researched-seed
evidence_grade: E1
confidence: 0.97
versions: "historical AE architecture; behavior family survives as collapse/continuous rasterization"
last_verified: 2026-09-14
---
# Concatenated rendering and delayed rasterization

## Statement
Adobe patent US6084597, explicitly describing After Effects, documents a method for delaying rendering of nested-composition source layers. A nested source layer can be **promoted** into the root composition so rasterization or image sampling is delayed until root-layer rendering.

The patent's baseline render order is source acquisition -> mask/clip -> image effects -> geometric transform -> blend. Concatenated rendering selectively removes a nested-composition rasterization barrier so transforms/sampling can be deferred.

## Why this matters
This is unusually direct historical evidence for the conceptual ancestry of Collapse Transformations / Continuous Rasterization. It also supports treating precomp flattening as graph rewriting rather than as a mere UI switch.

## Mathematical view
If two stages are linear coordinate transforms, delaying rasterization allows transform composition before sampling. But effects, masks, blend operations, 3D context and non-commutative operators create barriers where promotion cannot be naively fused.

## Improvement direction
Model flattening as explicit graph rewriting with typed barriers and transform fusion rules, rather than special-case precomp behavior.

## Sources
1. US6084597 summary: https://patents.justia.com/patent/6084597
2. JP family with After Effects reference: https://patents.google.com/patent/JP2008084329A/en
