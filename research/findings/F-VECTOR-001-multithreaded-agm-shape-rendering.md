---
status: confirmed-local-feature-surface
last_verified: 2026-09-15
---
# F-VECTOR-001 — AE exposes an AGM-specific multithreaded vector-shape render path

AE 2024 localization resources contain MultithreadedAGMShapeRendering, described as rendering vector shapes on multiple threads to improve performance.

## Architectural implication
Shape rendering has an identifiable AGM-backed execution path whose threading policy can be independently changed from general MFR/effect rendering. Do not assume a shape layer is rendered only by the same RG/effect scheduler used for raster effects.

## Research action
Find AGM-related modules/trace categories; compare shape-only render scaling with MFR on/off; vary repeater count, path complexity, strokes, gradients and merge paths; determine whether the multithreading is per-shape, per-tile, per-path, or command-buffer decomposition. Track CPU thread topology and cache behavior.

## Design lesson
Vector rasterization can expose its own internal work graph while still materializing into the shared compositing graph. Separate domain-specific parallelism from composition-level frame parallelism.
