---
status: active
last_verified: 2026-09-15
---
# Object Matte / Object Selection Internals

Object Matte should be modeled as a learned temporal-analysis subsystem, not merely as a conventional pixel effect. AE 26.5 persists propagated Object Matte results to disk across project closure. Adobe states that earlier propagated frames lived only in memory; 26.5 can restore already-computed frames from disk and marks cached propagation spans in the timeline.

## Product-to-internal lineage
Local AE 2025 dictionaries already contain Beta feature strings for EnableRotoBrush4, EnableRotoLive, EnableRotoSelectionBrush, and an ObjectSelectionTool/PreSegmentationFailed error. The RotoBrush4 description explicitly describes automatic object selection before propagation.

Retained AE 26.0 and 26.3 Debug Databases contain DVACompute.ShouldUseObjectSelectionAsync = true; nearby entries include ML.MakeRenderableNodeVisualisation and DVASE.ORT.UseTensorRTRTXEPOnNVIDIAGPU. AE 26.3 Trace Database separately exposes RotoBrush4 and RotobrushSpanView. These names are direct local artifacts, but adjacency does not prove one fixed call chain.

## Current architecture hypothesis
Selection and propagation should be treated as separate phases: object selection/pre-segmentation produces an initial semantic region, temporal propagation extends/refines that state over time, and a persisted analysis cache stores propagation outputs. ShouldUseObjectSelectionAsync strongly suggests a host-managed asynchronous selection path.

Do not equate the analysis cache with Global Performance Cache. Object Matte results survive sessions even without Freeze in 26.5, while the user-facing workflow separately exposes Freeze as a semantic lock. This implies at least two concepts: computed analysis residency and frozen/committed matte state.

## Cross-host clue: Premiere Object Mask
Adobe states that AE Object Matte uses the same AI technology as Premiere Object Mask. Premiere documentation further says required AI models are downloaded the first time Object Masking is used. Treat a shared model/runtime delivery substrate as a testable hypothesis, not a fact about AE packaging.

A local Adobe-wide file scan found a separate MediaCore DepthONNX plug-in with multiple depth_anything_v2_small ONNX models. This is not evidence that Object Matte uses Depth Anything; it is evidence that Adobe already ships shared MediaCore plug-ins that package ONNX models independently from an individual host application.

## Failure-model implications
Object Matte bugs should be split into: model/runtime availability; asynchronous selection/pre-segmentation; temporal propagation; analysis-cache identity; cache persistence/I/O; render integration; and headless/aerender integration. Adobe fixed an aerender failure for comps containing Object Matte in 26.2.1 and a startup-error crash in the same release, proving that headless/render integration and initialization are independent failure surfaces.

## Experiments
1. Propagate without Freeze, close/reopen, and record cache files changed/created.
2. Change one selection keyframe and measure which cached temporal spans invalidate.
3. Change source footage interpretation, layer time remap, scale, comp resolution, project color space, and model/runtime version independently.
4. Compare Freeze versus un-frozen cached propagation at the filesystem and project-file level.
5. Compare interactive AE and aerender for identical frozen/unfrozen states.
6. Trace process module loads during first Object Matte use, then repeat offline after any model download.
7. Compare AE and Premiere model/cache roots without assuming shared file formats.

## Evidence discipline
DVACompute.ShouldUseObjectSelectionAsync is strong evidence for an asynchronous object-selection code path; it does not prove that every Object Matte operation runs asynchronously. DVASE.ORT.UseTensorRTRTXEPOnNVIDIAGPU proves an ORT/TensorRT execution option exists in the retained debug surface; it does not prove Object Matte selects that backend.
