---
status: active
last_verified: 2026-09-15
evidence: GPU runtime inventory + trace/debug vocabulary
---
# GPU Tracing

GPU traces answer execution questions, not semantic correctness questions. AEIG therefore pairs GPU tracing with CPU/GPU parity fixtures and host-side render identity observations.

The installed runtime exposes GPUFoundation devices/queues, GPU frame upload/conversion, GPU renderer identifiers, memory-budget handling and GPU-capable PF world paths.

Useful external observation tools include GPUView/ETW and vendor profilers where available. Correlate dispatch and synchronization timestamps with AE trace markers rather than reading an isolated GPU timeline.

## Questions a trace can answer
- Was work submitted to a GPU backend?
- Was a frame uploaded/downloaded or kept device-resident?
- Where do long waits/fences occur?
- Did a backend/device change alter scheduling?

## Questions it cannot answer alone
A GPU dispatch does not prove the output matches CPU semantics, that the correct dependency identity was used, or that cache reuse was valid.

## Required companion data
Capture input/output hashes, pixel-format/world type, host renderer/device identity, relevant BEE/RG trace and CPU reference output.

See `docs/gpu-system/overview.md` and `datasets/ae-2025-gpu-execution-surface.csv`.## Version scope
GPU backends, device policy and renderer modules change across AE releases and OS/hardware. Record exact AE build, GPU model/driver, backend/framework, project renderer, effect path and whether the frame is CPU- or GPU-resident before comparing traces.

A trace collected on one adapter/backend is not representative evidence for another.

## Observer and failure effects
Vendor profilers, GPU validation layers and verbose tracing can serialize work, alter queue timing, increase memory pressure or disable optimizations. A trace run that becomes slower or changes residency may be measuring the instrumentation as much as AE.

Out-of-memory, device-reset and fallback behavior must be distinguished from ordinary synchronization stalls. If AE falls back to CPU, the absence of later GPU work is a result, not missing evidence.

## Unknown frontier
Runtime symbols establish GPUFoundation/frame/device boundaries but do not expose the complete scheduler or cache-coherency algorithm. Queue ownership, cross-device migration and exact render-GUID participation remain experiment targets.

Cross-check GPU traces against `../gpu-system/overview.md`, `../image-pipeline/numerical-behavior.md`, `../memory-system/runtime-architecture.md`, and BEE/RG host traces.