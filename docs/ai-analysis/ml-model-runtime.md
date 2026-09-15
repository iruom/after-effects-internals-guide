---
status: active
last_verified: 2026-09-15
---
# ML Model Registry and Runtime Policy

AE 2024/2025 ship an `installed:MLModels/model_metadata.json` registry plus ONNX Runtime binaries. The registry exposes a cross-feature model-management layer rather than a single hard-coded AI feature.

Observed registry dimensions include:
- stable model key and `model_version`,
- model file name,
- CoreML/ONNX format and format variant,
- supported device class and device filters,
- batching capability,
- optional memory-consumption and seconds-to-live hints,
- module name/display name/UUID,
- module bundle type,
- full input/output tensor signatures.

This is direct local-artifact evidence of an Adobe model registry with policy metadata. It does not identify the exact AE feature that consumes every model.
## Distribution classes observed
AE 2025 uses at least four model residency/distribution classes:
- `bundled`: model module ships with the application.
- `ccd-on-demand`: declared in the registry but intended to be acquired on demand.
- `ccd-deferred`: registered for deferred Creative Cloud delivery.
- `local-dev`: development/local module class.

The registry therefore separates **model identity/availability metadata** from **local model residency**.

## Concrete example: FastMask lineage
The legacy/current Roto Brush-related `FastMask` module is explicitly named `DisplayName=Rotobrush`, has a stable module UUID, and its FastMask2 ONNX models are physically bundled in AE 2025.

The 2025 registry also declares a FastMask3 encoder/decoder/encoder trio under `AdditionalMLModels`, marked `ccd-on-demand` and private-beta display metadata. Do not equate FastMask3 with Object Matte without a consumer-side trace, but it is a high-priority lineage clue.
## Segmentation-oriented private/on-demand cluster
The 2025 `AdditionalMLModels` module contains names whose functional decomposition is suggestive:
- `PPYOLO` — object detection candidate,
- `InstanceMaskPrediction` — instance-mask prediction candidate,
- `UniversalRefinementModel` — segmentation/matte refinement candidate,
- `DeepLasso` — interactive selection candidate,
- `FastMask3*` — temporal mask propagation/state candidate.

This set resembles a detect → select/mask → refine → propagate toolchain, but the mapping to Object Matte remains a hypothesis until binary references, runtime logging, or controlled model acquisition connect the feature to these keys.

## Packaged model representation
Bundled FastMask model files use `.mlem`. Their leading bytes are not raw ONNX signatures, a 2 MB sample has near-maximal byte entropy, and ordinary ONNX/protobuf marker strings were absent in a passive inspection. Classify `.mlem` as an opaque Adobe model container. Do not call it encrypted without stronger evidence.
## Public API boundary
The installed model registry is an internal product artifact, not a documented third-party After Effects SDK for registering arbitrary inference models. Model keys, bundle types and `.mlem` containers may change without plug-in compatibility guarantees.

Third-party code should therefore use the registry as archaeology/observability evidence only. A product integration must not modify `model_metadata.json`, replace bundled model files or assume on-demand delivery endpoints are stable extension APIs.

## Runtime policy dimensions
Model **identity**, **delivery**, **residency**, **device eligibility**, **inference-session lifetime** and **analysis-result residency** are separate. A model may be registered but not downloaded; downloaded but not loaded; loaded on CPU versus GPU; evicted while a propagated matte remains reusable from disk.

TTL/memory hints in registry metadata are evidence of runtime residency policy, not proof of a specific eviction algorithm.

## Failure classes
- model registered but unavailable/download failed;
- device filter selects unsupported backend;
- model generation changes while stale analysis cache survives;
- tensor/schema mismatch between orchestration code and model version;
- model residency pressure mistaken for result-cache invalidation;
- cross-host shared technology assumed to have identical model keys/runtime policy.

Recent Object Matte launch/headless regressions are valuable integration evidence, but they do not establish which model-registration component failed.

## Experiments
On a disposable profile, record module/model files before and after invoking an on-demand-capable workflow, process/module loads, GPU/CPU activity, registry key requested where observable and resulting analysis cache artifacts. Repeat after host restart and cache purge to distinguish model download/residency from analysis-result persistence.

Compare AE versions with the same logical feature and diff normalized model registry entries by stable key, model_version, tensor signature, device policy and bundle type. Never infer model semantic equivalence from filename alone.

## Unknown frontier
Unresolved: `.mlem` container format; exact downloader/verification protocol; model-signature/cryptographic policy; residency eviction mechanism; whether Object Matte 26.5 uses FastMask3 or another declared cluster; how model version is mixed into persistent analysis-cache identity.

Related: `docs/ai-analysis/object-selection-pipeline.md`, `docs/ai-analysis/fastmask-lineage.md`, `F-ML-001-model-registry-and-residency.md`, `F-ML-003-object-selection-compute-layer.md`.
