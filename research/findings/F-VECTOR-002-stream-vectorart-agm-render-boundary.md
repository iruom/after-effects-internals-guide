---
status: strongly-supported-local
last_verified: 2026-09-15
evidence: E2-L + prior E0/E1 surface mapping
versions: AE 2025 installed runtime
---
# F-VECTOR-002 — Shape streams materialize into VectorArt before AGM/RG rasterization

AE 2025 `BEE.dll` exposes three distinguishable vector layers rather than one monolithic shape renderer.

## 1. Editable/evaluated stream layer
`BEE_VectorStream` contains concrete stream groups for Rect, Ellipse, PolyStar, Fill, Stroke, Gradient Fill/Stroke, Merge Paths, Offset Paths, Repeater, Trim, Twist, Roughen, Round Corners, Pucker/Bloat, Wiggler, Zigzag, transforms and 3D material options. These classes are constructed as TDB stream/group types and therefore belong to the property/evaluation side of the system.

## 2. Materialized vector-art layer
`BEE_VectorStream::PopulateVectorArt(...)` consumes `BEE_VectorLayer`, a `TDB_StreamIDPath`, time, abort state and optional `TDB_ParamBag`, producing a `BEE_VectorArt::Group`. `BEE_VectorLayer::GetVectorArt(...)` exposes the resulting group.

`BEE_VectorArt` has a separate object model: Group, Path, Graphic, GradientGraphic, SolidColorGraphic, Filter, StreamBasedFilter, StrokeData and OriginInfo. `OriginInfo` retains a `TDB_StreamIDPath`, preserving provenance from evaluated art back to stream identity.

## 3. AGM/RG materialization boundary
`BEE_VectorArt::Path` can be built from either `CAIMBezierPath` or `CAGMPath`. BEE imports `COR_NewAGMPort(PF_World, CAGMRasterPort)`, `COR_CombineAGMPaths`, `COR_PlayOutlines` and `TDL_VectorArt(CAGMPath, matrix, ...)`. `C_AGMDLTranslatePort` is constructed directly from a `PF_World` plus `BEE_IllusShapeTarget`.

`BEE_VectorLayer::Rasterize2DGraph(...)` returns an `RG_RenderNode`, while bounds are separately queried through `BEE_VectorArt::GetBounds(..., RenderExtentMode)` and `BEE_VectorLayer::GetSourceFloatRectHelper(...)`.

## Strongest justified model
`TDB/BEE VectorStream tree -> time-specific VectorArt materialization -> bounds/render-extent analysis -> AGM-facing path/display-list translation -> RG render node / PF_World materialization`.

This is stronger than saying "AE uses AGM for shapes": the runtime exposes explicit conversion boundaries and separate object models on both sides. It does **not** yet prove which exact operations are tessellated inside AGM, whether every shape-layer render takes this path, or where GPU acceleration begins.

## Reproduction
Run `probes/process-tools/inventory_vector_shape_symbols.py`. The generated `datasets/ae-2025-vector-shape-symbols.csv` preserves matching exports/imports/dependency edges from BEE, COR, drawbotagm, AdobeSVGAGM and AGM.

## Next discriminating experiments
- Animate one operator at a time and compare vector bounds/cache invalidation against pixel output changes.
- Hold frame concurrency constant while increasing single-frame shape complexity to isolate AGM/vector-domain threading from MFR.
- Compare native shape construction with SVG-to-native conversion while tracing `BEE_SVGToAGMDisplayListConverter`-adjacent behavior.
- Test whether operators that preserve path topology can reuse materialized VectorArt/bounds more narrowly than operators that change geometry.
