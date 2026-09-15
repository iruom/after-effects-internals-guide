---
status: confirmed-local
last_verified: 2026-09-15
evidence: AE-2025 PE exports/imports
---
# F-COLOR-001 — ICC/ACE and OCIO converge on a shared ColorSpace / frame-conversion substrate

AE 2025 ships `ColorSpaceConverter.dll`, `COR.dll`, and `OCIOWrapper.dll` as separate modules, but their exported ABI vocabulary converges on shared MediaCore/DVA types rather than exposing isolated color systems.

`ColorSpaceConverter.dll` exports `ConvertFrame` paths over `MF::IVideoFrame`, `dvamediatypes::ColorSpace`, `PixelFormat`, and `ColorManagementSettings`, plus GPU frame conversion using `GF::Device` and a conversion-parameter GUID.

It also exposes signal↔linear transfer functions, RGB↔XYZ/YUV matrices, graphics-white handling, display→scene color-space mapping, ICC-equivalent model spaces, gamut/dynamic-range comparison, and scripting-facing color-space objects.
`OCIOWrapper.dll` separately exports CPU and GPU conversion, Look, File Transform and CDL paths, but again consumes `dvamediatypes::ColorSpace` / `PixelFormat` and `GF::Device`. Its dependencies include `dvamediatypes.dll`, `MediaFoundation.dll`, `GPUFoundation.dll` and `OCIOAPIProvider.dll`.

`COR.dll` bridges ACE profiles/transforms to DVA color-space/profile types and depends on `ColorSpaceConverter.dll` plus `ACEWrapper.dll`.

## Internal implication
A useful current model is not `ICC pipeline` versus `OCIO pipeline` as two complete render pipelines. Instead, ICC/ACE and OCIO are transform providers/adapters around a shared color-space/frame/device substrate.

This does not prove every AE composition pixel passes through `ColorSpaceConverter.dll`, nor that CPU/GPU results are always bit-identical. It does establish a reusable color-conversion layer shared with Adobe media infrastructure.

Machine-readable evidence: `datasets/ae-2025-color-pipeline-symbols.csv`.
Probe: `probes/process-tools/inventory_color_pipeline_symbols.py`.
