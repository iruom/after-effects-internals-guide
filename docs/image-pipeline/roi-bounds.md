---
status: active
last_verified: 2026-09-14
---
# ROI and Bounds

SmartFX exposes separate request/result/max-result rectangles, making region algebra part of the host contract.

Local Debug Database also contains `AE.VectorBoundsCache`, showing that bounds computation itself may be cached in at least some paths.

Reconstruct functions of the form:
`input_region = F(output_request, parameters, time, transform, quality)`

Use impulses and boundary probes through Blur, Glow, Transform, Displacement, Convolution, Grow Bounds and nested comps.

## SmartFX bounds are a correctness contract
The SDK is unusually strict here. `max_result_rect` must describe the largest possible non-zero output for the node and must not vary with the particular current request. AE may request only bounds information with an empty request rectangle and may subsequently decide that no render is needed.

This implies a host phase that can reason about support/bounds separately from pixel production.

## Abstract-interpretation view
Treat bounds as a conservative abstract value over image support. Each operator implements a transfer function such as:
`B_out = G(B_in, parameters, time)`
and inverse demand propagation such as:
`R_in = F(R_out, parameters, time)`.

Overestimating `B_out` is safe but increases memory/cache/render work. Underestimating it is incorrect because the host will never request omitted pixels.

## Special cases to classify
- finite support expansion: box/convolution kernels;
- direction-dependent expansion: directional blur/shadow;
- inverse-transform demand: geometric transforms;
- map-dependent demand: displacement;
- potentially infinite support: Gaussian-like tails;
- explicit unknown/full-frame fallback.

The guide should measure which AE operations use exact, clipped, conservative or full-frame behavior rather than assuming a universal ROI algebra.

## Source
- https://ae-plugins.docsforadobe.dev/smartfx/smartfx/

## `PF_CheckoutResult` exposes collapse-aware reference dimensions
The AE 25.6 Header describes `ref_width` / `ref_height` as the original layer size before effects and without downsample factor, but explicitly says collapsed layers use the composition size.

This is a small but strong indication that collapse changes the semantic reference frame used by SmartFX checkouts. A renderer-promoted/collapsed layer cannot always use the source item's ordinary dimensions as its render-space reference dimensions.

## Result vs maximum support
`result_rect` is the support actually available for a specific checkout and may be empty. `max_result_rect` is the maximum possible support if the host requested all pixels, and the Header requires that it not vary as a function of the current request rectangle.

`PF_RenderOutputFlag_RETURNS_EXTRA_PIXELS` allows an effect to state that computing a larger region is effectively free, so the returned support may exceed the request. This separates **demand region**, **actual produced region**, and **intrinsic maximum support** as three distinct quantities.