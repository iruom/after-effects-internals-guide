---
status: confirmed
last_verified: 2026-09-14
evidence: distributed-header + public-guide
---
# F-CHANNEL-001 — `PF_ChannelType_DEPTHAA` exists in Header but not current Guide list

AE 25.6 `AE_Effect.h` defines `PF_ChannelType_DEPTHAA` and annotates it as present since AE 16.0 for 3D precomps in some Artisans.

The current public SDK Guide's Auxiliary Channel type list includes `DEPTH`, `NORMALS`, `OBJECTID`, `MOTIONVECTOR`, `BK_COLOR`, `TEXTURE`, `COVERAGE`, `NODE`, `MATERIAL`, `UNCLAMPED`, and `UNKNOWN`, but omits `DEPTHAA`.

This is a direct example of distributed SDK headers containing behaviorally relevant surface area not represented in the prose Guide.

## Implication
`DEPTHAA` should be treated as a renderer-specific auxiliary buffer class, not inferred to be universally available. The annotation links it specifically to 3D-precomp handling in some Artisan paths.

## Research action
Construct Classic/Advanced 3D precomp scenes and query both `DEPTH` and `DEPTHAA`, varying Collapse Transformations, resolution, motion blur, and renderer.