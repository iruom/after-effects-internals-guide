---
status: confirmed-local-artifact
last_verified: 2026-09-15
---
# F-ML-002 — FastMask2→FastMask3 transition is directly visible in Roto Brush

AE 2024 `Required/Roto Brush.aex` contains references to `FastMask2` but not `FastMask3`.

AE 2025 `Required/Roto Brush.aex` contains references to both `FastMask2` and `FastMask3`.

The registry identifies the older FastMask module as `DisplayName=Rotobrush`; bundled FastMask2 `.mlem` models are physically present in the AE 2025 install. FastMask3 entries are declared under `AdditionalMLModels` with `ccd-on-demand` delivery.

## Interpretation
FastMask3 is strongly connected to the Roto Brush lineage and was introduced as an optional/newer model path while FastMask2 remained available. This is stronger than inferring purpose from the model name alone.
## Model-interface diff
Registry inspection confirms that the older 2022 FastMask path explicitly separates memory-input and query-input networks using key/value banks. FastMask2 exposes image/mask encoders plus a decoder with memory_key, memory_shrinkage, memory_value, sensory, last_mask, key and selection. FastMask3 keeps recurrent sensory/last_mask but removes separate memory-key/shrinkage decoder inputs and increases key/selection embeddings.

A normalized snapshot of the relevant registry entries is stored at datasets/ae25.6-selection-model-registry.json.
