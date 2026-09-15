---
status: seed-map
last_verified: 2026-09-14
---
# Patent Archaeology Map

Adobe patents are not a specification of current AE, but some explicitly name After Effects and were authored by engineers later recognized for AE design/development. They are therefore valuable historical implementation evidence and experiment generators.

| Patent | Topic | AEIG use |
|---|---|---|
| US7103839B1 | cached-frame validity | interval lists, edit timestamps, collateral dependencies, pull validation |
| US6084597 | concatenated rendering | nested-comp promotion, delayed rasterization/sampling, transform fusion ancestry |
| US5917549A | pixel aspect transforms | coordinate metrics, PAR-aware sampling/transforms |
| US5872564 | controlling time | temporal resampling/frame blending ancestry |
| US6115051A | arc-length reparameterization | motion-path spatial interpolation / constant-speed semantics |
| US6809745B1 / US7446781B2 | 2D/3D compositing | mixed layer-stack / 3D compositing architecture |
| US5919249A | multiplexed output rendering | render settings, output pipelines, frame production |
| US7656406B1 | animated paint strokes | paint/stroke representation and temporal data |

## Interpretation rules
1. Prefer patents that explicitly mention After Effects or known AE team inventors.
2. Separate algorithm description from evidence that AE shipped exactly that algorithm.
3. Compare the patent with SDK behavior, current UI behavior, trace/debug vocabulary and project artifacts.
4. Treat changed behavior as architecture archaeology, not a contradiction.

## Primary index links
- https://patents.google.com/patent/US7103839B1
- https://patents.justia.com/patent/6084597
- https://patents.google.com/patent/US5917549A/en
- https://patents.justia.com/patent/5872564
- https://patents.google.com/patent/US6115051A/en
