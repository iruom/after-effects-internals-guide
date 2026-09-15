---
status: active
last_verified: 2026-09-16
evidence: Adobe Help motion-blur contract + Comp/Canvas SDK timing APIs
---
# Motion Blur as a Temporal Sampling Contract

AE motion blur is not just a post-process blur. It is a policy for evaluating render-relevant state over a shutter interval and combining multiple temporal samples.

This distinction immediately separates two kinds of motion:
- **AE-evaluated motion**: layer transforms, 3D/vector geometry and other state AE can sample at different times;
- **motion already inside source pixels**: live-action/object motion encoded within one footage frame.

Adobe explicitly notes that enabling layer/composition Motion Blur does not synthesize blur for motion that exists inside the layer's footage. Frame blending or an effect with its own motion estimation is a different subsystem.

## Public shutter state
Composition state exposes shutter angle and shutter phase. Adobe defines shutter angle as a fraction of a rotating 360° shutter and derives exposure from frame duration.

For example, 90° at 24 fps represents 25% of one frame duration, or an effective exposure of 1/96 second.
Shutter phase is a temporal offset relative to the frame boundary; it changes where the exposure interval sits around the nominal render time.

A simplified interval model is:

`shutter_duration = frame_duration * shutter_angle / 360`

`sample_interval = [frame_time + phase_offset, frame_time + phase_offset + shutter_duration]`

The exact endpoint convention and phase mapping must be measured rather than assumed from this simplification.

## SDK timing contract
Comp/Canvas APIs expose the actual shutter frame range for a requested composition time. Artisan query-time documentation also distinguishes **transform time** from **view time**; transform time feeds the shutter-range query, while view time is used for view-dependent layer/world transforms.

This is strong evidence that a renderer should consume host-provided temporal context rather than reconstructing motion blur from UI values alone.

`AEGP_RenderOptions` also carries frame time-step, documented as relevant to motion blur. The same project shutter settings can therefore participate in different concrete request coordinates.
## Sampling controls are bounds, not a universal fixed count
Adobe Help describes **Samples Per Frame** as the minimum sample count used when AE cannot determine an adaptive rate from layer motion; the same setting is used for 3D layers and shape layers. **Adaptive Sample Limit** is the maximum.

Therefore a fixed `N samples per frame` mental model is insufficient. A safer abstraction is:

`motion/renderer state -> choose sampling density within configured bounds -> evaluate temporal states -> integrate/composite`

The metric used to choose adaptive density is not publicly specified.

## Renderer and subsystem boundaries
Different systems can implement motion blur differently:
- transform/vector/3D sampling controlled by composition/renderer policy;
- effect-specific temporal sampling or accumulation;
- pixel-motion estimation effects;
- footage frame blending / optical-flow-like interpolation;
- renderer-specific geometry sampling.

Do not infer that all of these share one sample schedule or kernel.

## Failure modes
- treating shutter phase as a display-only offset;
- assuming Samples Per Frame is always the actual count;
- sampling source footage motion by simply evaluating more transform times;
- ignoring time remap when mapping comp shutter times into layer/source time;
- assuming CPU/GPU/3D renderer paths use identical adaptive subdivision;
- caching a temporally sampled result without including the effective shutter/request state in identity.

## Reconstruction experiment
Use analytically controlled geometry: a one-pixel/vector impulse moving at constant velocity, acceleration and a discontinuity. Vary angle, phase, frame rate, minimum samples and adaptive limit one axis at a time.

Measure output support/weights and repeat across 2D, shape, 3D, CPU/GPU and renderer variants. Non-integer frame times and asymmetric phases help distinguish centered, endpoint and stratified schedules.

## Unknown frontier
The exact sample positions, weighting kernel, adaptive-motion metric, renderer-specific subdivision rules and cache identity for temporally integrated results remain unproven.

Cross-links: `time-model.md`, `../render-graph/render-context.md`, `../evaluation/dirty-invalidation.md`, and `../three-d-system/overview.md`.