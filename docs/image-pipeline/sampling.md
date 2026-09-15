---
status: active
last_verified: 2026-09-14
primary_evidence:
  - AE 25.6 SDK Headers/AE_EffectCB.h
---
# Sampling and Resampling Internals

Sampling in After Effects is not a single interpolation function. The distributed Effect API preserves an older host-managed sampling subsystem with explicit setup/teardown, quality-dependent callbacks, area sampling, batch-operation hooks, compositing state and motion-blur fields. This is useful both as historical implementation evidence and as a warning that visually equivalent transforms may travel through different sampling paths.

## Legacy host sampling contract
`PF_SampPB` contains source-world state, x/y sample radii, an explicitly supplied sample area, edge behavior, an `allow_asynch` field, motion-blur state, compositing mode, an optional per-pixel mask, legacy lookup-table pointers and reserved runtime storage.

The matching callbacks include `begin_sampling`, `subpixel_sample`, `area_sample`, `end_sampling`, plus an older batch-sampling path. `begin_sampling` is therefore a context-construction boundary, not merely a notification.

Adobe's header comments explicitly allow the host to use this setup phase to initialize platform acceleration, build scanline indices or otherwise precompute sampling state. The former batch path is described as an opportunity to remove repeated function-call overhead, pipeline requests into a DSP and reuse precomputed sample weights.
## Quality semantics
The old callbacks define high-quality subpixel sampling as an alpha-weighted interpolation of colors at non-integral coordinates. Low-quality sampling is explicitly nearest-neighbor. Area sampling likewise computes an alpha-weighted average over a non-integral axis-aligned rectangle in high quality and falls back to nearest-neighbor in low quality.

This does **not** prove that every modern AE transform still uses these callbacks. It does prove that the Effect API historically exposed quality as a selector over materially different sampling algorithms, rather than merely a tolerance value.

## Numerical ceiling in legacy area sampling
The header states that the old area sampler can average at most a 256x256-pixel region because of overflow limitations. This is a direct example of a mathematical constraint leaking from accumulator representation into visible API behavior.

For a modern implementation, the corresponding design question is accumulator precision and reduction strategy. Wider integer/floating accumulators, separable filtering, prefix-sum methods, SIMD reductions, tiled GPU reductions or compensated summation can remove the historical size ceiling, but may not reproduce legacy AE numerics bit-for-bit.

## Motion-blur clues
`PF_SampPB` also carries motion-blur state and was documented as supporting batch sampling/compositing for motion blur. This does not reveal the current shutter sampling schedule, but it establishes an older architecture in which repeated resampling positions could be prepared and processed as a group.

AEIG should therefore distinguish: host sampling callbacks, layer-transform sampling, Transform-effect sampling, continuously-rasterized vector sampling, 3D texture sampling, effect-owned sampling and GPU kernels. Equal-looking operations are not assumed to share kernels.
## Developer guidance
- Do not infer AE-compatible filtering from one resize test; probe fractional translation, minification, magnification, rotation and anisotropic scale separately.
- Test straight and premultiplied alpha independently. Historical callbacks describe alpha-weighted color operations, so hidden RGB and zero-alpha behavior can expose path differences.
- Compare CPU/GPU and 8/16/32-bpc paths independently; shared visual intent does not imply shared arithmetic.
- Treat old overflow limits and fixed-point fields as compatibility archaeology, not recommendations for new code.

## Reconstruction probes
Use one-pixel impulses, alternating Nyquist grids, subpixel ramps, transparent colored pixels and negative/>1 float values. For each path record support width, coefficient symmetry, normalization, edge extension, alpha treatment and backend variance.

For area/minification probes, vary footprint size across historical boundaries such as 128 and 256 pixels. A discontinuity would indicate retained legacy behavior; a smooth result would suggest replacement by a newer implementation.

## Open questions
Current AE may retain the old callback contract while routing many modern operations through unrelated CPU/GPU implementations. The exact relationship among `PF_UtilCallbacks`, internal RG transform nodes, GPU kernels and Advanced 3D texture filtering remains unresolved.## Abandoned edge modes
`PF_SampleEdgeBehav` preserves only the alpha-zero outside-image behavior. The same header contains commented-out `REPEAT` and `WRAP` enum values under `Sorry, not supported!`.

This is useful archaeology: edge extension was considered part of the sampling abstraction, but those alternate branches never became a supported host contract. Do not assume the existence of a named enum in historical source implies runtime implementation.

For compatibility probes, explicitly distinguish transparent-zero, clamp/replicate, wrap and mirror behavior. AE's legacy callback path should be expected to behave as zero-alpha unless another API documents otherwise.
