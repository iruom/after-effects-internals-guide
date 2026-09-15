---
status: active
last_verified: 2026-09-15
---
# FastMask / Roto Brush Temporal-Memory Lineage

AE 2025 MLModels/model_metadata.json exposes three generations of segmentation/memory contracts useful for reconstructing Roto Brush/Object Selection internals. These are model-interface facts, not a claim that every public Object Matte operation uses each model.

## 2022 memory/query architecture
FastMaskMemoryInput512/1024 consumes (image, mask) and emits key and alue tensors. The paired FastMaskQueryInput512/1024 consumes the current image plus accumulated key/alue memory and emits a 2-channel mask. This is an explicit memory/query split.

At 512 resolution the memory encoder emits key[128,1024] and alue[256,1024]; the query path accepts larger accumulated memory key[128,2048], alue[256,2048]. The 1024 variants scale the spatial-memory lengths to 4096/8192.

## FastMask2 (2023-11-03)
The image encoder produces multi-scale features plus key, shrinkage, and selection. A separate mask encoder consumes image/features, last_mask, and recurrent sensory state, returning a memory alue and updated sensory state. The mask decoder consumes long-term memory_key, memory_shrinkage, memory_value, current-frame features, key/selection, sensory state and last mask, producing the new mask and next sensory state.

This exposes at least three distinct temporal state classes: long-term memory bank, short/recurrent sensory state, and explicit previous-mask state.

## FastMask3 (2024-11-18)
FastMask3 retains the image-encoder / mask-encoder / mask-decoder split but changes the interface. Encoder key and selection grow to 256×32×32. The decoder consumes memory_value[512,3072] but no longer declares separate memory_key or memory_shrinkage inputs. Multi-scale features are represented as conventional channel×height×width tensors.

The mask encoder still consumes last_mask and sensory, and the decoder still returns updated_sensory. Therefore recurrent local state remains explicit even though the long-term-memory interface changes.

FastMask3 models are registered under AdditionalMLModels with ccd-on-demand delivery, CoreML v6 and ONNX v17 variants, and CPU/GPU eligibility. FastMask2 and older FastMask memory/query models are registered under the bundled FastMask/Roto module.

## DeepLasso selection model
DeepLasso-20240605 is also ccd-on-demand. It consumes a 4×320×320 tensor and returns a 2×320×320 probability tensor. AeCompute.dll separately contains solax::object_selection::DeepLasso, giving independent linkage between the registry entry and the higher-level object-selection compute layer.

## Architectural consequences
Propagation cache identity must be versioned by more than source pixels: model generation, memory state, selection edits, time, render options and likely model delivery/runtime backend can all affect semantic results. Model residency is separate from propagated-result residency.

Do not serialize raw model-memory tensors as a supposedly timeless project semantic unless the model/version contract is also captured. FastMask2→3 proves that internal temporal-state shapes and meanings can change across model generations.

## Experiments
Capture model acquisition/runtime traces while starting selection versus propagation; perturb only one selection keyframe and observe temporal invalidation; compare FastMask2/3 selection on the same corpus if both paths can be activated; inspect whether cached analysis embeds a model version/schema marker.

## Host/API boundary
FastMask tensor contracts are internal model interfaces, not public Effect/AEGP APIs. The public product exposes Roto Brush/Object Matte controls and persisted project state; it does not expose raw memory-bank tensors or guarantee model file compatibility.

This matters for tools that try to "reuse AE's model": even when the model bytes can be located, preprocessing, tensor normalization, recurrent-state semantics, model-version pairing and postprocessing remain part of the private contract.

## Failure implications of the 2→3 interface change
FastMask2 and FastMask3 differ in long-term memory inputs and embedding sizes. Persisting raw recurrent/model state across model generations without a schema/version fence can therefore produce silent semantic corruption rather than a clean load error.

Likewise, an analysis-result cache must identify the model/runtime generation strongly enough that an old result is not reused after a semantic model upgrade unless Adobe explicitly defines compatibility.

## Temporal-memory experiments
Use a short clip with one controlled occlusion and one selection correction. Compare propagation after clearing only analysis results versus restarting the host/model runtime. If behavior differs with identical source/selection state, model/session-local recurrent state may be contributing beyond the persisted result cache.

If both FastMask2 and FastMask3 paths can be activated in a controlled environment, compare not only masks but invalidation footprint after editing one selection frame. A change in propagation horizon would expose different temporal-state semantics.

## Unknown frontier
Unresolved: which public workflows select FastMask2 versus FastMask3 in each AE release; serialization, if any, of sensory/memory state; exact preprocessing color/scale conventions; relationship between Roto Brush span state and model memory; whether Object Matte 26.5 shares any of these temporal-memory models.

Related: `docs/ai-analysis/ml-model-runtime.md`, `docs/ai-analysis/object-selection-pipeline.md`, `F-ML-002-fastmask-lineage.md`, `F-ML-004-preseg-guid-workqueue-cache.md`.
