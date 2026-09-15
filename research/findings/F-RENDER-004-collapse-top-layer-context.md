---
id: F-RENDER-004
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-RENDER-004 — Collapsed geometry separates render context from project-layer identity

**Evidence:** E0-H  
**Version:** `AEGP_CanvasSuite8`  
**Confidence:** High

`AEGP_GetTopLayerFromLayerContext` is documented to return the root-composition layer containing a layer context when collapsed geometrics are enabled; with collapse disabled it behaves like `AEGP_GetLayerFromLayerContext`.

## Internal implication
A render-layer context is not necessarily identical to the source project's immediate layer object. Collapse can preserve/promote an inner render context while associating it with a different top-level project layer.

This strongly supports graph-rewrite / layer-promotion models of Collapse Transformations and warns against modeling the renderer as a direct traversal of the project layer tree.

## Experiment
Compare nested-comp render GUIDs, ROI, transform sampling and cache reuse with collapse toggled while keeping visible output equivalent.