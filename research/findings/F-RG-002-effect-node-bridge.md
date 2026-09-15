---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Effect plug-in nodes bridge into the internal Render Graph

## Local evidence
Stacks interleave `FLTp_Node::PreRender`, `FLTp_Node::Render`, and `FLTp_Node::CheckoutLayerRender` with `RGp_CheckoutResultImpl`, `RG_Traverser`, and `RG_CompositeNode` operations.

`FLT_FCSeqSpec::SuppressCacheHelper::ClearDependencyMap` appears directly below layer checkouts in several stacks.

## Interpretation
The effect host layer appears to project effect operations and their input checkouts into RG results while maintaining a dependency map/cache suppression helper. This is stronger than merely saying SmartFX is graph-aware.

## Open questions
Determine whether every classic effect receives an RG wrapper, how SmartFX differs from classic effects, and whether dependency maps are per-effect-instance, per-render, or per-sequence.