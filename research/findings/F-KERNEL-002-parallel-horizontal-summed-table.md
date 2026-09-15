---
status: confirmed-local-feature-surface
last_verified: 2026-09-15
---
# F-KERNEL-002 — CPU Camera Lens Blur / 3D DOF used a parallel horizontal summed-table optimization

AE 2024 localization resources contain ParallelHorizontalSummedTable, described as improving Camera Lens Blur and 3D Depth of Field performance, especially at small radii.

## Interpretation
The name strongly suggests a summed-area/prefix-sum family optimization with a horizontally parallelized construction/evaluation phase. The exact kernel, dimensional decomposition, precision and boundary handling are not established by the string alone.

## Why it matters
Performance varying specifically with blur radius is a clue to algorithm crossover points. A prefix/summed-table method has setup cost with favorable per-radius evaluation, while other direct/separable kernels may dominate at different radii. The Beta feature may represent a construction-stage parallelization rather than a new blur equation.

## Experiments
Benchmark Camera Lens Blur and CPU 3D DOF versus radius, image size and thread count across 23.x/24.x/25.x; look for slope/crossover changes. Use impulse, edge and HDR/negative-value inputs to test whether optimization changes numerical output or only speed.
