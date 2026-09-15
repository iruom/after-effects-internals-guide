---
status: seed
evidence_grade: E2-L
versions: "24.x-25.x observed"
last_verified: 2026-09-14
---
# Modern AE installation exposes distinct compute/render/GPU modules

## Statement
Local installation contains RendererCPU, RendererGPU, GPUKernels, GPUFoundation and newer AeCompute alongside OCIO/USD/ML modules. Names are clues, not proof of responsibility.

## Interpretation rule
Do not infer more than the evidence supports. Internal names are observation points, not automatically class or subsystem definitions.

## Next experiment
Correlate module load/stack activity with backend toggles and controlled renders.
