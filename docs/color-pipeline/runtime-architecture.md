---
status: active
last_verified: 2026-09-16
evidence: current ICC/OCIO color-management contracts + local ColorSpaceConverter/COR/OCIOWrapper/GPU runtime surfaces
---
# Runtime Color Architecture

AE's installed modules expose a color system that crosses application, MediaCore/DVA and GPU boundaries.

## Observed modules
- `ColorSpaceConverter.dll`: generic frame conversion, transfer functions, matrix conversions, ICC/model-space adapters, scripting color objects, CPU/GPU frame utilities.
- `COR.dll`: ACE profile/transform wrappers and conversion between ACE and DVA color representations.
- `OCIOWrapper.dll`: OCIO config discovery/validation and CPU/GPU CDL, File Transform, Look and color-space conversion.

All three use shared `dvamediatypes` color/pixel vocabulary; the conversion modules also meet `MediaFoundation`, and GPU paths use `GPUFoundation` device abstractions.
## Provisional dataflow
`source tags/profile -> shared ColorSpace description -> transform provider (ACE/ICC or OCIO) -> CPU/GPU frame converter -> working/render/display target`

The exact AE call path remains to be traced. In particular, do not infer that every effect receives MediaCore `IVideoFrame` objects; the Effect API still exposes PF worlds. A conversion boundary must therefore exist between some media/display surfaces and AE's effect/render image representation.

## Important distinctions exposed by symbols
`DVADisplayColorSpaceToEquivalentSceneColorSpace` makes display-referred versus scene-referred representation explicit. `DVAColorSpaceToEquivalentLinearColorSpace` and signal↔linear functions show that linearization is represented as a transform over a color-space description rather than simply a global project boolean.

`GetSignalValueForGraphicsWhiteLevel`, peak-luminance accessors and gamut/dynamic-range comparison indicate that HDR behavior has dimensions beyond primaries + transfer function alone.

## Next probes
Trace imports of `ColorSpaceConverter.dll` from BEE/PF/VideoRenderer/display modules; compare CPU and GPU conversion numerically; vary project working space, display color management, OCIO mode and HDR graphics-white settings while recording conversion GUIDs and cache behavior.

## Two public color-management engines
Current AE project settings expose at least two color-management engines:
- **Adobe Color Management**, based on ICC/profile workflows;
- **OCIO Color Management**, where OpenColorIO drives project color processing and ACES-style pipelines.

This is not just a UI label distinction. The project chooses different transform/configuration providers while the rest of AE still has to move image state through compositing, effects, preview, GPU and output paths.

A better runtime model is:

`source/native media state -> interpretation/input transform -> project working representation -> effect/composite operations -> view/display transform and/or output transform`.

The transform provider may be Adobe/ICC or OCIO, but the request still crosses common image/render boundaries.

## Working-space linearization versus linear blending
Current Help exposes two different concepts:
- **Linearize Working Color Space**: make project working-space operations occur in a linearized version of the chosen space;
- **Blend Colors Using 1.0 Gamma**: linearize layer blending behavior without being equivalent to a full linearized project working space.

Conflating these settings can produce incorrect reproduction experiments. Motion blur, resampling, antialiasing and blend modes can respond to linear-light processing even when other color operations follow a different path.

## Preserve RGB is semantic reinterpretation
`Preserve RGB` disables a normal color conversion for a footage/output item and preserves numeric RGB values instead of visual appearance. The same numbers are then interpreted in another color space/context.

This makes Preserve RGB especially useful for control-data images such as displacement maps, but dangerous if treated as "keep colors looking the same".

For cache/identity work, Preserve RGB belongs in the semantic request key because identical pixel numbers can acquire different meaning depending on the color-space interpretation.

## PF worlds meet shared color infrastructure at a boundary
Third-party PF effects still receive `PF_EffectWorld`/SmartFX worlds rather than a universal DVA `IVideoFrame`. Therefore AE must cross a representation boundary somewhere between source/media/display infrastructure and effect processing.

Questions to preserve separately:
- component format (8/16/32f);
- pixel/channel layout;
- linear/nonlinear encoding;
- color-space primaries/white point;
- scene/display-referred meaning;
- alpha interpretation;
- CPU/GPU residency;
- working/view/output transform state.

One conversion does not imply all of these dimensions changed.

## Failure modes and misleading equivalences
- A source profile assignment change can alter appearance without changing decoded source bytes.
- `Preserve RGB` can keep numeric values stable while intentionally changing their visual interpretation.
- Display Color Management changes viewer output, not project pixel data; a screenshot mismatch is therefore not automatically a render mismatch.
- Linearized working-space processing and gamma-1.0 layer blending are different state dimensions.
- CPU and GPU transforms that are visually indistinguishable may still differ numerically enough to affect deterministic tests or hashes.
- Converting an HDR/scene-referred signal through an insufficiently expressive integer path can clamp information even when the nominal color-space names match.

## Version and engine boundaries
AEIG records ICC/Adobe and OCIO as separate public project engines. Their existence is confirmed; exact internal ownership between `COR.dll`, `ColorSpaceConverter.dll`, `OCIOWrapper.dll`, MediaFoundation/DVA and BEE remains implementation evidence rather than public ABI.

A stable module name also does not prove invariant transform math across releases. OCIO configuration, bundled ACES version, ICC profile implementation, GPU backend and HDR policy can all change independently.

## Controlled experiment matrix
For one deterministic float image containing negative, in-range and over-range RGB values, vary exactly one dimension at a time: input interpretation, working space, engine (Adobe/OCIO), linearization, gamma-1.0 blending, display management, Preserve RGB, output profile and CPU/GPU path.

Record pre-effect and post-effect numeric samples where observable, rendered-file hashes, viewer-only differences, trace/module activity and output metadata. A strong result separates **data mutation** from **display-only transformation**.

## Unknown frontier
Still unresolved:
- exact PF-world ↔ shared DVA/MediaFoundation conversion boundary;
- whether every color transform contributes directly to BEE/TDB render identity or some are display-only state;
- current CPU/GPU transform equivalence tolerances;
- HDR graphics-white and peak-luminance participation in cache keys;
- ownership/lifetime of compiled ICC/OCIO transforms across project and device changes.

Related: `docs/color-pipeline/overview.md`, `docs/image-pipeline/numerical-behavior.md`, `docs/image-pipeline/pixel-formats.md`, `docs/gpu-system/overview.md`.
