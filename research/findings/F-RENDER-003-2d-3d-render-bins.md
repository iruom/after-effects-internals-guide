---
id: F-RENDER-003
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-RENDER-003 — Composition rendering exposes explicit 2D/3D bins

**Evidence:** E0-H  
**Version:** `AEGP_CanvasSuite8`, frozen AE 12.0  
**Confidence:** High

Canvas exposes `AEGP_GetNumBinsToRender`, `AEGP_SetNthBin`, and `AEGP_GetBinType`. Bin type is explicitly `AEGP_BinType_2D` or `AEGP_BinType_3D`.

## Internal implication
At least in the Artisan contract, a composition render can be partitioned into ordered 2D and 3D regions rather than treated as a single homogeneous layer pass.

This gives a concrete basis for researching 2D/3D materialization boundaries, renderer handoff, transform-space changes and cache barriers.

## Next work
Construct mixed stacks of 2D, 3D, adjustment, matte and collapsed-precomp layers and infer where bin boundaries appear through render behavior, Artisan callbacks and runtime traces.