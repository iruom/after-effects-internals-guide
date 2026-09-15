---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# A concrete internal Render Graph implementation is exposed by crash symbols

## Local evidence
Observed symbols include `RG_RenderNode`, `RG_CompositeNodeBase::Render`, `RG_CompositeNode::DoRender`, `RG_CacheNodeBase::Render`, `RG_XformNode::DoRender`, `RG_Traverser::PreRenderGraph`, `RG_Traverser::Execute`, and `RG_ExecuteGraph`.

Checkout-side symbols include `RGp_CheckoutResultImpl::GetWorld`, `GetOutputWorld`, `GetEffectWorld`, `CoerceBitDepth`, and `Release`.

## Consequence
AEIG may now treat a graph/traverser-based renderer as implementation evidence, not merely a conceptual model. Project/property streams and this render graph should remain separate until their construction mapping is measured.

## Next experiments
Capture graph-sensitive stacks/traces for one layer, effect chain, adjustment layer, track matte, precomp, Collapse Transformations, and 3D renderer transitions.