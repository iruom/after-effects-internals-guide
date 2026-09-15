---
id: F-GPU-003
status: confirmed-cross-header
last_verified: 2026-09-14
---
# AE and Premiere expose the same GPU device-management contract

## Observation
AE 25.6 `PF_GPUDeviceSuite1` and Premiere 26.0 `PrSDKGPUDeviceSuite` expose closely corresponding device records and operations: framework/device/context/queue handles, device enumeration, exclusive device access, device-memory allocation/purge, pinned-host allocation/purge, and GPU-resident image containers.

AE's Smart Render GPU structures also explicitly describe their `device_index` as intended for use with `PrSDKGPUDeviceSuite`.

## Strong shared semantics
Both headers state that ordinary device and pinned-host allocations must go through the host suite; purge is an emergency escape hatch for memory that cannot be allocated there. Both describe CUDA current-context push/pop on the calling thread when exclusive access is acquired.

## Confidence
High that AE Effect GPU execution is layered on a shared MediaCore-style GPU device substrate. Exact allocator implementation and pool policy remain host/version dependent.