---
status: researched-seed
evidence_grade: E1
confidence: 0.98
versions: "historical AE architecture"
last_verified: 2026-09-14
---
# Pixel-aspect-aware transforms are architectural, not cosmetic

## Statement
Adobe patent US5917549A explicitly names After Effects and treats source/destination pixel aspect ratio as part of image transformation mathematics. Non-square pixels alter the mapping between discrete pixel coordinates and displayed geometry.

## Internal implication
Pixel aspect ratio cannot safely be bolted onto only the viewer or final output. It may enter transform matrices, sampling coordinates, ROI inversion and bounds propagation depending on the operation.

## Research direction
Use anisotropic impulse/checker probes with PAR values such as 0.9, 1.0, 1.2 and legacy video ratios. Compare Transform, masks, effect coordinate parameters, motion blur and nested comps.

## Improvement direction
Represent image coordinates in an explicit physical/display metric separate from storage-index coordinates. Convert at defined graph boundaries rather than carrying hidden PAR correction factors through arbitrary operators.

## Source
Adobe patent US5917549A: https://patents.google.com/patent/US5917549A/en
