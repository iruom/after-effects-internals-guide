---
status: active
last_verified: 2026-09-14
---
# GUIDs and Receipts

AE exposes several related but not yet proven-identical identity mechanisms: `AEGP_GUID`, Compute Cache keys, frame receipts, render receipts, receipt GUIDs, `PF_State`, GUID dependency mixing and runtime `GetRenderGuid` symbols.

## Public hash surface
`AEGP_HashSuite1` can create a GUID from bytes and mix additional bytes into an existing GUID. Compute Cache also defines its key as `AEGP_GUID` and requires all render-relevant inputs to participate without hashing rendered pixels.

## Render receipts
Canvas APIs can generate receipts for a layer after only the first N effects. Receipt validation can separately check geometry and can return `VALID_BUT_INCOMPLETE`, proving that reuse state is not only a whole-frame true/false flag.

## Frame receipts
AEGP frame checkout returns an opaque frame receipt. It can expose a read-only world, rendered region and receipt GUID, tying image ownership, partial spatial validity and identity together.

## Runtime evidence
Crash traces expose `TDB_Stream::GetRenderGuid`, stream-group GUID generation, `BEE_AVLayer::GetRenderGuidWithRO`, `BEE_CompItem::GetRenderGuidWithRO`, `BEE_Layer::MixInGuidForTransform`, `BEE_CheckoutReceipt` and `MixHashGuid`.

## Working hypothesis
AE builds hierarchical structural fingerprints from render-relevant state fragments and uses receipts as scoped proofs that a previously materialized result is reusable under a current context. Exact equivalence between all GUID/state domains remains unproven and must be tested.
## Receipt evolution and partial completeness
The legacy Canvas/Render surfaces show two distinct receipt concepts evolving in parallel. Canvas render receipts can describe a layer with only the first N effects rendered; frame receipts bind a checked-out image world to a rendered region and, in later Render Suite generations, a GUID.

Canvas receipt validation returns three states: `INVALID`, `VALID`, and `VALID_BUT_INCOMPLETE`. This is evidence for a reuse model where state can be semantically compatible yet insufficient for the full requested stage.

The `num_effects` dimension was added to receipt checking in AE 7.0, making effect-stack prefix part of receipt validity rather than merely an execution argument.

## Historical frame-receipt progression
Render Suite 1 (AE 5.5.1 era) already exposed frame checkout, read-only receipt world, rendered region, and render-option sufficiency. Version 2 (AE 6.5) added project render timestamps, time-range change queries, speculative worthwhileness tests and external-frame cache check-in. By the version frozen in AE 11.0, the receipt could expose a GUID.

This sequence is useful evidence for how AE's cache identity surface became progressively more explicit without proving that the current internal implementation is unchanged.