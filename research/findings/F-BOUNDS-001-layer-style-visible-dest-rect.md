---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Layer styles participate in explicit destination-bounds computation

## Local evidence
`BEE_LayerStyleNode::VisibleDestRect` appears in render stacks adjacent to RG render-node destruction/checkout paths.

## Interpretation
Layer styles have a bounds-aware render representation rather than being treated only as an unconstrained postprocess. `VisibleDestRect` is a concrete observation point for studying how shadow/glow/stroke-like styles expand or constrain destination bounds.

## Mathematical target
Infer `B_style = G(B_input, style_params, scale, transform, quality)` and determine whether multiple layer styles compose bounds analytically or fall back to conservative unions.

## Improvement question
Over-conservative bounds waste cache memory and render work; under-conservative bounds clip pixels. Measure how close AE's bounds are to the true nonzero support.