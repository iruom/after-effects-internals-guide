---
status: active
last_verified: 2026-09-15
---
# Render Nodes

The internal renderer is not only a conceptual graph: local crash symbols and installed exports expose concrete RG node and traversal types.

## Confirmed local surfaces
- `RG_RenderNode`
- `RG_CompositeNodeBase::Render`, `RG_CompositeNode::DoRender`
- `RG_CacheNodeBase::Render`, `CacheIsValid`, `IsValidCacheNodeData`, `ChildRequestHook`, `PreRender`
- `RG_XformNode::DoRender`
- `RG_Traverser::PreRenderGraph`, `RG_Traverser::Execute`, `RG_ExecuteGraph`
- checkout-result surfaces that expose output/effect worlds, bit-depth coercion and release

Effect-host stacks also interleave `FLTp_Node::PreRender`, `FLTp_Node::Render` and layer checkout with RG traversal/result objects. This is direct evidence that effect evaluation is projected into the internal render graph.

## Phase model
`request/dependency construction -> PreRenderGraph -> cache-node validation -> transform/composite/effect graph -> Execute/Render -> checkout/materialized world`.

The pre-render phase can compute bounds, dependencies and feasibility without executing the final pixel body. Public SmartFX behavior independently supports that separation.

## Identity boundary
A project item, layer or stream is **not** assumed to be an RG node. BEE render options/GUIDs and FLT effect nodes are bridge surfaces between persistent semantic objects and request-specific RG structures.

## Cache-node caution
`RG_CacheNodeBase` proves graph-local cache validation exists, but it does not prove one node equals one Global Performance Cache entry or one disk-cache artifact. Identity, validity and residency remain separate dimensions.

## Current experiment
`EXP-RG-001` captures `RenderNode.RG_CacheNodeBase` and `RenderNode.RG_XformNode` together with BEE/TDB/GUID categories for mutation passes A/B. The goal is phase/request correlation, not invocation of private RG methods.

Related findings: `F-RG-001`, `F-RG-002`, `F-RG-003`, `F-CACHE-015`.

## Effect-host bridge
Local crash stacks interleave `FLTp_Node::PreRender`, `FLTp_Node::Render` and `FLTp_Node::CheckoutLayerRender` with `RGp_CheckoutResultImpl`, `RG_Traverser` and `RG_CompositeNode` operations. `FLT_FCSeqSpec::SuppressCacheHelper::ClearDependencyMap` also appears near layer checkout paths.

This is stronger evidence than simply saying "effects participate in a graph": the effect-host layer appears to translate effect requests/checkouts into RG materialization while maintaining dependency/cache bookkeeping.

AEIG still does not assume every classic effect and every SmartFX effect map to identical private node classes.

## PreRender is a real graph phase
`RG_Traverser::PreRenderGraph` appears as a distinct runtime phase. Public SmartFX independently separates `PF_Cmd_SMART_PRE_RENDER` from pixel rendering, supports bounds/dependency planning and allows PreRender to occur without a later Render.

That supports a phase model:

`semantic request -> graph construction -> pre-render dependency/bounds/cache planning -> execution scheduling -> pixel/materialization -> checkout result`.

Dead branches can therefore be rejected or satisfied from cache before invoking final pixel bodies.

## Checkout result is another ownership boundary
`RGp_CheckoutResultImpl` surfaces expose world retrieval, output/effect-world distinctions, bit-depth coercion and release. A node/result pair should not be modeled as a permanently resident image: materialization and ownership/release are explicit phases.

This mirrors public checkout APIs where a receipt/reference can exist independently of long-lived pixel ownership.

## Failure patterns
- equate project layer/property objects with RG node identity -> stale topology assumptions;
- treat cache node as proof of one persistent disk/RAM entry -> confuse validity with residency;
- put dependency discovery only in pixel execution -> miss pre-render dead-branch/cycle planning;
- retain checkout worlds beyond their release contract -> lifetime bugs;
- infer graph structure solely from one crash stack -> overfit a request-specific execution path.

## Reconstruction experiment matrix
Trace the same semantic layer under one controlled topology change at a time: add/reorder one effect, enable adjustment-layer behavior, introduce track matte, precompose, toggle Collapse Transformations and switch 3D renderer.

Capture RG/BEE/TDB categories, receipt/render GUID changes, bounds/ROI and output hashes. Compare **graph-shape changes** against **semantic-state changes**; equal output pixels do not imply equal graph topology.

A second experiment should vary only request coordinates (ROI/downsample/world type) with project state frozen, testing which node/cache structures are request-specific.

## Version boundary
Concrete `RG_*` evidence currently comes from local 23.6/24.5-era crash symbols and installed runtime surfaces. Public SmartFX contracts corroborate the planning/execution split across later versions, but private class names and exact topology are not a supported ABI.

## Unknown frontier
Still unresolved: node taxonomy for masks/mattes/text/media/3D, graph construction ownership between BEE and RG, node lifetime/reuse across requests, exact relation between `RG_CacheNodeBase` keys and BEE Render GUIDs/Canvas receipts, and whether graph fragments survive across frame requests or are reconstructed from higher-level state.

Related: `F-RG-001`, `F-RG-002`, `F-RG-003`, `docs/render-graph/render-tasks.md`, `docs/render-graph/render-request-sufficiency.md`.
