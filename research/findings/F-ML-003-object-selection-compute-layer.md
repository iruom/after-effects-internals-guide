---
status: confirmed-local-symbols
last_verified: 2026-09-15
---
# F-ML-003 — AE 2025 exposes a higher-level DVACompute object-selection layer

`AeCompute.dll` in AE 2025 contains model keys plus symbol/string evidence for a higher-level object-selection pipeline, including:
- `SmartMaskingUtils`
- `DVACompute::DVAMLInferenceEngine`
- `DVACompute::ObjectSelectionWrapper`
- scripting-facing `ObjectSelectionObject`
- `DetectObjectsUsingMask`
- `PreSegmentationObject` / `UIPreSegmentationWrapper`
- `solax::object_selection::DeepLasso`
- `solax::ultimate_urm::ObjectMaskRefiner`
- model-factory registration paths.

AE 2024 has no `AeCompute.dll`. Its `dvamlprocessing.dll` already knows several relevant model keys, but not the higher-level wrapper symbols observed in AE 2025.
## Version-archaeology interpretation
A plausible sequence is:
1. shared DVAML model support and segmentation models exist first,
2. a higher-level DVACompute object-selection orchestration layer appears later,
3. product-facing selection/matte workflows expose selected pieces of that substrate afterward.

This is an architectural hypothesis, not a claim that `ObjectSelectionWrapper` is exactly the public Object Matte implementation.

## Research action
Compare AE 2025, 26.x/Beta and Premiere binaries for these symbols and model keys; capture runtime logging/model acquisition while invoking Object Matte/Object Mask; identify which model names are requested and whether analysis results serialize/cache identically across hosts.