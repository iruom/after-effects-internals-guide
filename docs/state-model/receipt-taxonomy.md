---
status: active
last_verified: 2026-09-14
---
# Receipt Taxonomy

AE exposes several opaque objects called "receipts" that must not be treated as one concept. Their public contracts reveal different layers of the rendering system.

## 1. Canvas Render Receipt — `AEGP_RenderReceiptH`
This receipt belongs to the Canvas/Artisan path. It is returned with rendered layer textures/results and later checked against a current render context and layer context.

AE 6.0 introduced `RenderTextureWithReceipt` with an unusually explicit comment: the receipt lets an Artisan determine whether a subsequent layer render can be skipped because the Artisan cached the previous result.

By AE 7.0 receipt checking gained `num_effects`, and `GenerateRenderReceipt` could manufacture a receipt "as if the first N effects have been rendered." This makes effect-stack stage/prefix part of validity.
Canvas receipt validation returns `INVALID`, `VALID`, or `VALID_BUT_INCOMPLETE`. The exact semantics of `VALID_BUT_INCOMPLETE` are not explained in the inspected current/legacy headers and remain an open reconstruction target. Do not silently equate it with a known effect-prefix rule until experimentally or historically confirmed.

The validation API also exposes a geometry-check dimension (`check_geometricsB`; an older suite used the less informative name `check_aceB`). This indicates that the receipt is a scoped proof over more than parameter values alone.

## 2. Frame Receipt — `AEGP_FrameReceiptH`
This receipt belongs to Render Suite checkout. It is returned by synchronous/async frame requests and acts as the lease on a materialized frame result.

The caller must `AEGP_CheckinFrame`. `AEGP_GetReceiptWorld` returns a read-only world that the plugin does not own, `AEGP_GetRenderedRegion` reports spatial materialization, and later suites expose a receipt GUID.

Frame Receipt success does not imply pixel storage exists: the 13.5 Async Manager explicitly says a successful request can return a receipt with no pixels/no world. Blank/no-materialization is therefore representable separately from request failure.
## 3. Compute Checkout Receipt — `AEGP_CCCheckoutReceiptP`
Compute Cache returns another opaque receipt after a keyed cached computation is checked out. It pins/accesses the cached compute value until `AEGP_CheckinComputeReceipt` and is independent of the frame-world receipt contract.

## Why this distinction matters
The three receipts map to different questions:

- Canvas Render Receipt: "is this previously rendered layer/stage context still reusable?"
- Frame Receipt: "what materialized frame result have I checked out, over what region, and what lease must I release?"
- Compute Checkout Receipt: "what cached non-frame computation have I pinned for this render call?"

A generic AEIG statement such as "the receipt is the cache key" is therefore incorrect. Identity, validity proof, materialization and lifetime lease are only partially co-located depending on the receipt domain.

## Sources
Local AE 25.6 SDK: `AE_GeneralPlug.h`, `AE_GeneralPlugOld.h`, `AE_ComputeCacheSuite.h`.

## Historical differential: why effect-prefix is the leading incomplete-status hypothesis
The AE 6.0 Canvas contract checks an old receipt against current render/layer context and a geometry flag, with no effect-count argument. Retained later headers explicitly annotate the 7.0 change as adding `num_effectsS` to `AEGP_CheckRenderReceipt`, alongside `AEGP_GenerateRenderReceipt`, which generates a receipt as if the first N effects had been rendered.

Therefore effect-prefix completion became an explicit receipt-validity dimension at that transition. This materially strengthens—but does not yet prove—the interpretation that `VALID_BUT_INCOMPLETE` means a reusable earlier stage that cannot directly satisfy the requested later stage.

The distinction maps naturally to AEIG's request/result algebra: `VALID` is a candidate for direct satisfaction, while `VALID_BUT_INCOMPLETE` is a candidate for `CanContinueFrom`. Keep this labeled as a hypothesis until the controlled prefix/status matrix in `experiments/canvas-receipt-prefix-status.md` is run.