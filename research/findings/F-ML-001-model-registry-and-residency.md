---
status: confirmed-local-artifact
last_verified: 2026-09-15
---
# F-ML-001 — AE ships a policy-rich ML model registry separate from model residency

AE 2024/2025 contain `MLModels/model_metadata.json`. Entries carry model version, model file name, CoreML/ONNX variants, device policy, batching, memory/TTL hints, module UUID, bundle type, and tensor I/O signatures.

AE 2025 uses at least `bundled`, `ccd-on-demand`, `ccd-deferred`, and `local-dev` module bundle types.

This demonstrates that model identity/availability policy is represented separately from whether model bytes are resident in the application installation.

## Design implication
Model cache/residency should be analyzed separately from analysis-result caching. A model can be registered but non-resident; an analysis result can remain valid while the model itself is evicted or absent.