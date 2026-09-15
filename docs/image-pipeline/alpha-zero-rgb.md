---
status: active
last_verified: 2026-09-16
evidence: SmartFX / PF_OutFlag2_REVEALS_ZERO_ALPHA contract + image-pipeline test design
---
# Alpha and Zero-Alpha RGB

A pixel with alpha zero is visually transparent at that stage, but its RGB components are not automatically semantically meaningless inside After Effects. Public effect contracts explicitly account for effects that can later reveal RGB hidden under zero alpha.

This matters for plug-ins because an optimization that discards RGB from transparent pixels can be locally invisible yet change a later blur, channel operation, matte, unpremultiply/premultiply round-trip or effect that modifies alpha.

## Public SDK contract

The Effect API exposes `PF_OutFlag2_REVEALS_ZERO_ALPHA` for effects that can reveal RGB data in pixels whose alpha is zero. The historical/current Guide describes Set Channels as an example and tells AE not to trim away those RGB values when determining the input extent.

The neighboring `PF_OutFlag2_DOESNT_NEED_EMPTY_PIXELS` optimization defines an "empty" pixel as zero alpha unless `PF_OutFlag2_REVEALS_ZERO_ALPHA` is set, in which case RGB must also be zero. This makes the distinction operational: zero alpha alone is not always enough for the host to treat a pixel as disposable.

For non-SmartFX rendering, the trimmed input origin is exposed through `pre_effect_source_origin`; an effect combining empty-pixel trimming with buffer expansion can even receive a null input when the source is completely empty. The Guide marks this particular trimming flag obsolete for SmartFX, so old-style and SmartFX paths must not be assumed identical.

## Why hidden RGB exists

Straight/unassociated color and premultiplied/associated color encode different semantics. In ideal premultiplied form, `C_p = A * C_s`; at `A = 0`, recovering `C_s` by division is undefined. Real pipelines therefore may preserve source RGB separately, sanitize it, reconstruct it from neighbors, or lose it at a conversion boundary.

AEIG treats that behavior as part of pixel semantics, not merely storage detail. Two buffers that composite identically over black can still produce different downstream results if one retains hidden RGB and the other zeros it.
## Operations that can expose the difference

The most diagnostic operations are those that move information between RGB and alpha or between neighboring pixels:

- channel mapping and Set Channels-like operations;
- blur, convolution, resampling and filtering near transparent edges;
- matte generation or alpha replacement after an earlier RGB operation;
- straight/premultiplied conversions;
- transforms and sampling where edge pixels participate in interpolation;
- CPU/GPU or host/video-frame format conversions that may sanitize transparent RGB;
- bit-depth changes where clamping/quantization can interact with hidden values.

A classic failure pattern is a colored fringe around a formerly transparent edge. The immediate cause may be incorrect premultiplication, but the deeper cause can be that hidden RGB was preserved, discarded or reconstructed at the wrong pipeline boundary.

## Canonical adversarial pixels

A useful fixture should include more than ordinary 8-bit legal colors:

- nonzero RGB with `A=0`;
- tiny positive alpha with large RGB;
- negative and above-1.0 float RGB;
- alpha below zero or above one where the pixel format permits it;
- transparent pixels adjacent to strongly colored opaque pixels;
- identical visible compositing results with intentionally different hidden RGB.

Run the same corpus through masks, effects, precomps, transforms, track mattes, multiple bit depths and CPU/GPU paths. Hash the raw channels as well as the composited appearance.

## Classification vocabulary

For each stage record whether zero-alpha RGB is:

- **preserved** exactly;
- **premultiplied** into zero;
- **clamped/sanitized**;
- **reconstructed** from another representation;
- **trimmed** from the requested extent;
- **undefined/unobserved** because the public contract does not guarantee it.

Do not collapse these into a single "transparent pixel" state.
## Plug-in implementation guidance

An effect that can reveal hidden RGB should declare the relevant public capability instead of assuming AE will retain an arbitrarily large transparent extent. Conversely, an effect that promises it does not need empty pixels must tolerate the smaller input bounds and the documented empty-input cases for the legacy path.

When writing SIMD/GPU code, avoid "alpha==0 => RGB=0" fast paths unless that behavior is explicitly part of the effect's contract. Such a shortcut can make CPU and GPU paths disagree even when both are numerically correct for the currently visible frame.

For convolution and resampling, decide explicitly whether filtering operates on straight color, premultiplied color or another working representation. A mathematically convenient choice is not automatically host-compatible; edge behavior must be validated against AE for the target pixel format and render path.

## Failure modes and debugging

If a plug-in shows halos, edge color contamination, CPU/GPU differences or a result that changes after adding an alpha-modifying effect downstream, inspect hidden RGB before assuming color management is responsible. Capture raw pixels before and after the suspect boundary and compare both associated and unassociated interpretations where meaningful.

Also separate **extent loss** from **channel-value loss**. `PF_OutFlag2_REVEALS_ZERO_ALPHA` can influence which pixels AE includes in an input extent; that is different from whether a buffer conversion preserves the RGB bits of a pixel already present in memory.

## Version and evidence boundary

The Effect API contract establishes that zero-alpha RGB can matter, but it does not prove one universal behavior across every modern SmartFX, GPU, media, 3D and internal compositing path. Those paths must be tested independently and version-scoped. Historical mask behavior and obsolete legacy optimization flags should not be projected onto a current SmartFX/GPU path without observation.

## Open experiments

AEIG should retain a cross-bit-depth corpus covering 8/16/32-bpc, straight/premultiplied conversions, mask boundaries, effect extents, transforms, track mattes and GPU-capable effects. The useful invariant is not "AE always preserves hidden RGB"; it is that **a developer must know at which boundary the current contract permits hidden RGB to affect later computation**.

Related pages: `docs/image-pipeline/sampling.md`, `docs/image-pipeline/pixel-formats.md`, `docs/color-pipeline/overview.md`, and `docs/host-integration/cpp-sdk/sample-pitfalls.md`.
