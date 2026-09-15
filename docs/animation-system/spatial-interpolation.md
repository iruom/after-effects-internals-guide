---
status: researched-seed
last_verified: 2026-09-16
evidence: Adobe patent US6115051A + current After Effects spatial/roving-keyframe behavior
---
# Spatial Interpolation and Arc-Length Parameterization

Spatial interpolation and temporal interpolation are separate parts of AE's animation model. Current After Effects exposes Linear, Bezier, Continuous Bezier and Auto Bezier spatial interpolation, while temporal interpolation controls how the property advances through time. Roving keyframes add another layer: their timeline positions are solved from surrounding keyframes to smooth the rate of motion rather than remaining fixed timestamps.

## Historical Adobe implementation model
Adobe patent `US6115051A`, filed in 1996, explicitly names After Effects and describes an arc-length reparameterization architecture for animation paths. It separates:

- a spatial curve `Q(u)` parameterized by a natural curve parameter `u`;
- an arc-length mapping `s = A(u)`;
- a one-dimensional motion graph `s = S(t)` describing traveled distance versus time.

Evaluation is therefore modeled as:

`time t -> traveled distance s=S(t) -> curve parameter u=A^-1(s) -> spatial value Q(u)`.

This explains why temporal speed control can be decoupled from uneven Bezier control-point spacing. The patent is strong historical implementation evidence, but **not proof that AE 26.x still uses the same numerical algorithm**.

## Approximation details in the historical design
The patent states that arc length generally requires numerical evaluation. One described implementation recursively subdivides the spline until the arc distance between samples drops below a threshold, accumulates `(u,s)` samples, and fits one or more differentiable Bezier curves to approximate `A` or `A^-1`.

That design exposes three different error sources that should not be collapsed:

1. approximation of geometric arc length along `Q(u)`;
2. approximation/interpolation of the `u <-> s` mapping;
3. temporal interpolation in `S(t)`.

A velocity artifact can therefore originate in geometry sampling even when the Graph Editor's temporal curve appears smooth.

## Current user-visible constraints
Current After Effects documentation still exposes separate spatial and temporal interpolation and documents Rove Across Time only for spatial properties. Roving keyframes are not fixed to a specific time; their timing changes with adjacent keyframes so that speed is smoothed across the range.

Current documentation also warns that Auto Bezier spatial interpolation can create unwanted back-and-forth or "boomerang" motion between equal-valued Position keyframes. This is useful evidence that spatial tangent construction has observable semantics distinct from temporal interpolation.

## Failure and compatibility traps
- Do not infer constant speed merely because a path is geometrically smooth.
- Do not infer current AE's numerical tolerance from the historical patent.
- Equal Position values do not guarantee a stationary path when spatial tangents overshoot.
- Roving changes keyframe timing; tests that compare only property values at authored keyframe times can miss the actual temporal redistribution.
- Separated dimensions no longer share one obvious Euclidean path, so the historical scalar arc-length model may not transfer directly.

## Modern reconstruction experiments
Use Position paths with analytically known geometry and deliberately pathological control-point spacing. For each fixture record exact keyframe values, spatial tangents, temporal ease, roving state and sampled positions/velocities.

High-value probes include:
- straight line with highly uneven Bezier handles;
- quarter-circle and S-curve approximations;
- equal-valued adjacent Position keys with Auto Bezier versus Linear/Hold;
- one roving key between fixed endpoints, then move one endpoint in space only;
- identical path geometry with different temporal ease;
- 2D versus 3D and separated-dimension variants.

Measure first- and second-derivative continuity and fit candidate `A(u)` approximations. A current implementation that materially disagrees with the historical recursive-subdivision/Bezier-fit error signature would falsify continuity with the patent-era algorithm.

## Unknown frontier
Still unproven for current AE:
- whether an explicit arc-length table or fit is persisted or rebuilt on demand;
- modern subdivision/integration tolerance;
- whether 3D distance is measured in layer, comp, world or another transformed space;
- interaction with pixel aspect and continuously rasterized/collapsed geometry;
- cache identity for spatial-path approximation data;
- exact relationship between roving-keyframe timing solve and spatial reparameterization.

Related: `F-ANIM-001`, `docs/temporal-system/time-model.md`, `docs/animation-system/keyframe-api-history.md`.
