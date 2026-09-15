---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G 26.5
---
# F-RENDER-005 — A layer parameter has an explicit render-stage identity

AEGP_StreamSuite7 exposes the render stage of a `PF_Param_LAYER` independently from the selected source layer.

`AEGP_LayerParamStage_SOURCE` (0) samples source pixels before masks/effects. `ONLY_MASKS` (-2) applies masks but skips effects. `ALL_EFFECTS` (-1) applies masks and the full effect stack. Positive values 1..N render through effect N.

## Architectural consequence
A layer-valued parameter is not semantically just a Layer ID. Its render dependency can be modeled as `(source layer, render stage)` and therefore names a point inside the source layer's processing pipeline.

This directly aligns with historical effect-prefix Canvas receipts and layer render options (`upstream/downstream of effect`).

## Design consequence
Cache/dependency identity for layer parameters must include render stage. Treating two references to the same layer at different stages as identical would be incorrect.
