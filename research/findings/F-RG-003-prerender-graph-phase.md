---
status: confirmed-local + public-contract-corroboration
evidence_grade: E0 + E2-L
versions: "23.6/24.5-era logs; SmartFX current contract"
last_verified: 2026-09-14
---
# RG has an explicit pre-render graph phase

## Local evidence
Stacks show `FLTp_Node::PreRender` followed by RG checkout/bit-depth handling and `RG_Traverser::PreRenderGraph`, before layer/comp render-GUID computation.

## Public correlation
SmartFX separates `PF_Cmd_SMART_PRE_RENDER` from rendering, allows bounds-only requests, and explicitly permits PreRender with no corresponding Render.

## Interpretation
The internal graph has a metadata/dependency/bounds phase distinct from pixel execution. The graph can therefore decide that an output is unnecessary before invoking a render body.

## Design implication
Bounds, dependency acquisition and backend feasibility should be modeled as declarative planning, not hidden inside pixel execution. This creates opportunities for dead-branch elimination and better scheduling.