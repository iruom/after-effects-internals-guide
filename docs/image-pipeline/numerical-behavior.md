---
status: active
last_verified: 2026-09-16
evidence: Adobe bit-depth contract + PF pixel/world contracts + numerical probe methodology
---
# Numerical Behavior

After Effects' 8/16/32-bpc modes are not interchangeable storage widths. They expose different numerical domains, clipping behavior and precision.

## Nominal channel domains
Adobe documents:
- 8 bpc: nominal channel range `0..255`;
- 16 bpc: AE nominal white at `32768`, not a generic `65535` full-range assumption;
- 32 bpc: floating-point values, including finite values below 0 and above 1.

Therefore a generic `uint16 / 65535.0` conversion is not an AE-compatible 16-bpc model.

Use PF/AE conversion helpers and documented channel constants where possible instead of inventing scaling rules.

## 32-bpc float is semantic range, not just extra precision
Negative and over-range RGB can carry meaningful scene-linear/HDR information. Clamping to `[0,1]` at an intermediate stage can permanently alter later effects, color transforms, blurs and composites.
## Integer/float conversion is a policy boundary
Converting between depths can involve:
- scale/normalization;
- rounding mode;
- saturation/clamping;
- alpha handling;
- premultiplication/unpremultiplication;
- color-space transform before/after quantization.

Two conversions that both produce visually similar output can differ numerically enough to alter later thresholding, hashing or cache identity.

## Row/layout/residency are independent
Numerical interpretation must not be inferred from pointer type alone. Pixel depth, channel order, rowbytes, premultiplication and CPU/GPU residency are separate contract dimensions.

A GPU world may expose no CPU `data` pointer at all; a 16-bpc CPU world may include padding; a shared-media frame may use a different native channel layout before conversion into PF form.

## Floating-point adversarial corpus
For 32-bpc paths probe:
- `+0.0` and `-0.0`;
- values immediately below/above 0 and 1;
- subnormal/tiny finite values;
- large finite positive/negative values;
- negative/over-range RGB and alpha;
- NaN and ±Inf where the API accepts arbitrary float input.

NaN/Inf behavior is observational only; production effects should not rely on unspecified propagation.
## CPU/GPU equivalence levels
When comparing backends distinguish:
1. **bitwise identical**;
2. **numerically close within an explicit tolerance**;
3. **visually equivalent after display transform**;
4. **semantically equivalent for the downstream algorithm**.

A GPU path can be correct without being bitwise identical because of fused operations, precision, denormal handling or math-library differences. Conversely, visual similarity is insufficient for state hashing, thresholds or iterative algorithms.

## Interaction with alpha and color
A numerical difference may originate from the wrong subsystem if the test ignores:
- straight vs premultiplied representation;
- hidden RGB under zero alpha;
- working-space/linear-light transforms;
- output/display transforms;
- channel-format conversion.

Always run the numerical corpus alongside `alpha-zero-rgb` and controlled color-management fixtures.

## Failure modes
- treating AE 16-bpc as generic unsigned-16 full scale;
- clamping 32-bpc intermediate values to display range;
- assuming visually equal CPU/GPU results imply identical numerical behavior;
- hashing raw float bytes without defining NaN/-0 canonicalization;
- applying integer-style rounding to float render identity or cache keys;
- assuming all effects preserve negative/over-range values.

## Reproducibility matrix
For each effect/conversion/backend record input bit pattern, depth, rowbytes, color state, alpha interpretation, output bit pattern, absolute/relative error, clamp/sanitize events and backend.

Version the corpus by AE release and GPU/driver because backend numerical behavior can drift without any public API signature change.

## Unknown frontier
AEIG has not yet established universal host rules for NaN/Inf sanitation, denormal handling, rounding at every depth-conversion boundary or bitwise CPU/GPU determinism. Those remain experiment-scoped observations.

Cross-links: `pixel-formats.md`, `alpha-zero-rgb.md`, `../color-pipeline/overview.md`, `../gpu-system/overview.md`.