---
status: confirmed-local + historical-corroboration
evidence_grade: E1-H + E2-L
versions: "AE 9.0 through 26.3 key observed"
last_verified: 2026-09-14
---
# The PFC internal concept persists across many AE generations

## Evidence
Adobe's historical cache-validity patent names a `Post-Effect Cache (PFC)` positioned after masks/effects but before geometric transforms, lighting and shading. Local AE preference files contain `Pref_USE_PFC` in retained versions from AE 9.0, 10.0, 11.0, 23.x, 25.x and 26.3.

## Interpretation
The exact implementation cannot be assumed unchanged, but the internal term PFC has unusually long continuity. This strongly justifies treating post-effect/pre-transform materialization as a first-class archaeology topic.

## Potential weakness
A fixed post-effect cache boundary can be suboptimal for modern graphs if downstream operators could fuse or if pre-transform effects depend on transformed coordinates. AEIG should distinguish historical compatibility boundaries from mathematically necessary boundaries.

## Next experiment
Toggle transform-only changes, layer styles, collapse/continuous rasterization and effects that reveal extra pixels to infer where PFC-like reuse still occurs.