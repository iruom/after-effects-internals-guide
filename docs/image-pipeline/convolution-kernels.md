---
status: active
last_verified: 2026-09-14
primary_evidence:
  - AE 25.6 SDK Headers/AE_EffectCB.h
  - public SDK Guide, Graphics Utility Suites
---
# Convolution Kernels: Exposed Surface vs Implemented Surface

AE's old `PF_WorldTransformSuite1::convolve()` accepts a surprisingly rich set of `PF_KernelFlags`, but the distributed header and Guide explicitly document that several advertised branches are not implemented.

This makes the kernel API a useful case study in the difference between **representable API state** and **actual host capability**.

## Implemented and non-implemented branches
The header says only `PF_KernelFlag_USE_LONG` is implemented for kernel coefficient storage. `USE_CHAR` and `USE_FIXED` remain defined but are not implemented.

`PF_KernelFlag_REPLICATE_BORDERS` is defined but ignored; transparent/alpha-zero borders are the effective implemented path.

`PF_KernelFlag_ALPHA_WEIGHT_CONVOLVE` is also defined but ignored; straight convolution is the implemented path.
## Why this matters for compatibility
A plug-in that assumes every declared flag is meaningful can silently produce the wrong algorithm while receiving no obvious API error. Compatibility testing must therefore distinguish:

- flag exists in the header;
- Guide documents the flag;
- host accepts the flag;
- host actually changes computation;
- behavior is stable across bpc/backend/version.

This is exactly the kind of API fossil that should be preserved in AEIG because mathematically superior behavior may be less AE-compatible than reproducing the effective ignored-flag semantics.

## Modern implementation opportunities
A new convolution engine can support typed floating kernels, explicit border modes, alpha-aware filtering, separable detection, SIMD/GPU dispatch and large-kernel FFT paths. These should be exposed as explicit semantics rather than dormant flags.

For AE compatibility modes, preserve the historical transparent-border and straight-convolution behavior separately from improved modes.

## Host contract details that affect implementation
`convolve()` accepts separate alpha/red/green/blue kernels, an arbitrary kernel size, kernel flags and an optional rectangle. Passing an area such as `extent_hint` limits work spatially; passing null/zero requests the whole image.

The source world must not also be the destination. Treat this as a real aliasing/lifetime constraint, not an optimization suggestion. If an algorithm conceptually works in-place, allocate a distinct output or intermediate world.

`NORMALIZED` and `CLAMP` are independent semantics: normalization changes effective kernel weight scaling, while clamping constrains output to the representable range of the destination data type. Neither should be inferred from the mathematical kernel alone.

Transparent-border behavior effectively samples outside the image as zero-alpha black. Because `REPLICATE_BORDERS` is ignored by the documented implementation, code that asks for replicated edges but does not implement them itself can silently receive different edge pixels.

## Extent and hidden-RGB interaction
Convolution expands spatial dependency beyond one input pixel. An effect using `extent_hint` must widen the required input region by the kernel radius or equivalent support footprint; otherwise edge pixels of the requested tile can be computed from missing samples.

Transparent zero-alpha borders also intersect AE's hidden-RGB rules. A mathematically straight convolution over premultiplied data is not the same as an alpha-aware reconstruction of straight color. Since the advertised alpha-weighted branch is not implemented, compatibility tests should preserve the effective historical behavior rather than assume the flag fixes premultiplication artifacts.

## Precision and backend testing
The public utility routine belongs to the PF world path. Do not assume identical rounding/clamping across 8-bpc, 16-bpc and 32-bpc float, or between this CPU utility and a custom GPU implementation.

For a compatibility implementation, test impulse images, constant fields, alpha-zero colored pixels, negative/over-range float values, odd/even kernel sizes and border-only fixtures. Compare interior pixels separately from edge pixels so border policy is not mistaken for coefficient precision.

## Failure modes
- request an ignored kernel flag and assume the host honored it;
- perform source==destination convolution despite the explicit prohibition;
- use the requested output rectangle without widening source dependency;
- normalize twice because both the kernel generator and host normalization are applied;
- compare only opaque RGB fixtures and miss premultiplication/alpha-zero divergence;
- port to GPU with different border or clamp semantics and call the result "equivalent".

## Unknown frontier
Still unresolved: exact arithmetic/rounding sequence of the current host implementation at each bpc, whether the utility path itself has changed internally across releases, and whether any modern AE subsystem still uses this public routine for built-in effects. Those questions require numerical probes and call-path/runtime tracing rather than inference from the suite name.

Related: `docs/image-pipeline/pixel-formats.md`, `docs/image-pipeline/alpha-zero-rgb.md`, `docs/image-pipeline/numerical-behavior.md`.
