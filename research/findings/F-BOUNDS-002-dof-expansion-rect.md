---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Depth of field computes an explicit expansion rectangle

## Local evidence
A stack contains `PF_TransformWorld`, then repeated `BEE_ComputeDOFExpansionRect`, followed by RG checkout/cache-node activity.

## Interpretation
Depth-of-field rendering expands required spatial support before graph execution/cache consumption. This is direct evidence for a bounds-planning stage tied to optical blur extent.

## Mathematical research
Measure expansion against aperture, blur level, focal distance, depth discontinuity, downsample factor and comp resolution. Compare the measured rectangle with conservative circle-of-confusion bounds.

## Optimization opportunity
A single worst-case rectangle can waste work for spatially varying depth. A tiled/depth-binned support model could be substantially tighter if the current implementation is globally conservative.