---
status: active
last_verified: 2026-09-15
---
# AI / Learned Analysis Systems

AEIG groups learned inference features by runtime behavior rather than marketing labels. Current examples include Object Matte and historically ML-assisted segmentation/propagation workflows such as Roto Brush.

## Questions
- Which models/runtimes are loaded, on which device backend, and at what granularity?
- What is inference input state versus temporal propagation state?
- Which results are persisted in the project, RAM cache, disk cache or separate analysis assets?
- What constitutes a cache key for propagated mattes?
- How does a source edit invalidate only affected temporal regions?
- How are model/runtime versions included in semantic identity to prevent stale results?

## Evidence surfaces
Release documentation; installed ML/runtime modules; process/module loads; GPU tracing; cache filesystem observation; project diffs; network-isolation tests; temporal perturbation experiments.

AE 26.5 explicitly adds disk caching for propagated Object Matte results that survives project closure, making this a new first-class persistence/cache research target.

Do not infer model architecture from DLL names alone. Runtime/module inventory is discovery evidence until correlated with behavior.

## Current reconstructed model
Evidence now supports a multi-residency analysis architecture rather than a single opaque AI effect:

`selection / pre-segmentation -> render-state-derived GUID -> async WorkQueue/Future -> model inference -> temporal propagation state -> reusable analysis result -> compositing/render consumption`.

Model residency, transient inference state, propagated-result residency and frozen/committed user state are separate concepts. AE 2025 local symbols establish GUID-keyed asynchronous pre-segmentation and model/runtime policy; AE 26.5 public behavior independently establishes cross-session persistence for propagated Object Matte results.

This cross-class agreement upgrades AI Analysis to a triangulated domain while preserving an important version boundary: the AE 25.x ObjectSelection/RotoBrush4 internals are predecessor/shared-substrate evidence, not automatically the exact 26.5 Object Matte implementation.
## Public workflow and state machine
Current Object Matte documentation exposes a useful semantic sequence:

`user selection / correction -> per-frame propagation -> review/refinement -> optional Freeze -> downstream matte/effect consumption`.

The propagated timeline state is not identical to the final committed/frozen state. In 26.5, propagated results can also be cached to disk and recovered after reopening the project, so transient analysis computation, reusable propagated results and user-committed matte state must be modeled separately.

Adobe states that Object Matte is built on the same AI technology as Premiere's Object Mask workflow. That is cross-host substrate evidence, not proof that the AE/Premiere project-state or cache implementations are identical.

## Public API boundary
AEIG's Master Surface Registry currently finds no general third-party Object Matte API contract; the capability is classified as internal observation / no-general-access. UI-visible effect/property state and public product behavior therefore must not be mistaken for a documented C++/scripting analysis API.

If a later SDK exposes such an API, this page must be versioned rather than retroactively assuming it existed in 26.x.## Bug history as boundary evidence
Adobe fixed several Object Matte failures in 26.2.1, including a launch-error crash and `aerender` failure on compositions containing Object Matte. In 26.5, an Undo-history issue that inserted spurious stream-flag steps was also fixed.

These facts show that the feature crosses application startup/runtime initialization, headless rendering and project undo/state-management boundaries. They do **not** by themselves reveal the root cause or private class ownership.

## Experiments
Use one short deterministic clip and change one axis at a time: initial selection, correction stroke, source-frame edit, effect parameter, timeline range, Freeze state, AE restart and disk-cache purge. Record which propagated frames invalidate, which survive restart and whether final compositing pixels change.

Run the same frozen/unfrozen project through interactive AE and aerender to distinguish analysis preparation from render-time consumption. Hash rendered output so a faster warm-cache run is not mistaken for different semantics.

For runtime-model research, monitor module/GPU residency only as secondary evidence; first verify the semantic state transition on the same fixture.

## Unknown frontier
The exact model files, inference runtime, propagated-result key, disk container and relation to predecessor Roto Brush/FastMask/ObjectSelection internals remain version-scoped unknowns. Local 25.x symbols constrain possible shared substrate but do not prove the exact 26.5 Object Matte implementation.

Cross-links: `../persistence/cache-formats.md`, `../archaeology/disk-playback-era.md`, `../memory-system/runtime-architecture.md`, `../observability/gpu-tracing.md`, and the Object Matte entries in `aeig-unknown-frontier.csv`.