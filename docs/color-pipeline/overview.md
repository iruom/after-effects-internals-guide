---
status: active
last_verified: 2026-09-16
evidence: Adobe Help color-management contract + AE 2025 ColorSpaceConverter/COR/OCIO runtime surfaces
---
# Color Pipeline

AE color processing must be modeled as a sequence of representation changes, not as one project-level “color management on/off” switch.

A useful high-level chain is:

`source interpretation -> working representation -> optional linearization -> effect/render processing -> display/view transform -> output transform/profile`

Each boundary can change numerical values while attempting to preserve appearance, or preserve numerical RGB while intentionally changing appearance semantics.

## Core dimensions
Keep these independent until a specific API binds them together:
- component depth / numeric representation;
- primaries/gamut;
- transfer function / signal encoding;
- scene-referred vs display-referred interpretation;
- linear vs nonlinear working representation;
- ICC/ACE vs OCIO transform provider;
- graphics white / peak-luminance / HDR metadata;
- CPU vs GPU transform backend;
- display/view transform vs file/output transform.
## Numerical domain matters
Adobe documents 8-bpc, 16-bpc and 32-bpc modes separately. 32-bpc uses floating point and can represent negative values and values greater than 1.0, so HDR/scene-linear workflows can carry energy outside the nominal display range.

Clamping those values early is a semantic change, not merely a precision reduction.

## Working space and linear light
Linear-light rendering is a transform policy layered on top of color-space identity. Adobe explicitly discourages linear-light output for most 8/16-bpc output and defaults output linearization to 32-bpc-oriented use.

Do not collapse:

`working-space name == transfer function == linearization == display transform`.

They can be configured/derived separately.

## Preserve RGB means preserve numbers, not appearance
Adobe's `Preserve RGB` output behavior prevents conversion from the working color space. This preserves channel numbers while potentially changing how those numbers should be interpreted/displayed.

That is a useful implementation distinction:
- color-managed path: transform values to preserve intended color appearance;
- preserve-RGB path: retain values and bypass that conversion boundary.
## Runtime implementation evidence
Installed AE 2025 binaries expose at least three cooperating layers:
- `ColorSpaceConverter.dll` — generic frame/color conversion with CPU/GPU utilities;
- `COR.dll` — ACE/ICC profile and transform bridging;
- `OCIOWrapper.dll` — OCIO configuration, looks and CPU/GPU transforms.

These modules share DVA/MediaFoundation color-space vocabulary and GPUFoundation device abstractions. Their coexistence argues against one monolithic AE-only color converter.

Private/runtime symbols also distinguish operations such as display-space ↔ scene-space conversion, signal ↔ linear conversion, graphics-white lookup and peak-luminance handling. That supports a richer color-state key than “profile name”.

## Effect API boundary
Effects still operate on PF worlds, while media/display/GPU infrastructure may operate on shared frame/color objects. Therefore there must be explicit representation boundaries between imported/shared media frames and effect-render worlds.

A plug-in should not assume that the numeric PF world it sees preserves source-file encoding or display-space values.

## Failure modes
- comparing pixel values from two renders without recording color-management state;
- treating 32-bpc over-range values as invalid and clamping them;
- applying a transfer function twice when a frame is already linear;
- confusing Preserve RGB with “preserve appearance”;
- assuming CPU and GPU transforms are bit-identical;
- using display-transformed pixels as if they were render/working-space pixels;
- ignoring premultiplication/alpha-zero RGB while diagnosing color differences.

## Experiments
Use synthetic ramps, primaries, negative/over-range float values and alpha-zero RGB. Vary one axis at a time: source profile/tag, project working space, linearization, OCIO mode, display management, output profile and CPU/GPU path.

Record numerical values before/after each observable boundary rather than judging only screenshots.

## Unknown frontier
The exact call graph between BEE/PF, ColorSpaceConverter, COR, OCIOWrapper, display surfaces and MediaFoundation is not fully reconstructed. Cache/GUID participation of color-transform state also remains to be measured.

Cross-links: `runtime-architecture.md`, `../image-pipeline/pixel-formats.md`, `../image-pipeline/numerical-behavior.md`, `../gpu-system/overview.md`, `F-COLOR-001`, `datasets/ae-2025-color-pipeline-symbols.csv`.