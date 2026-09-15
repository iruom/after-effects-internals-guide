---
id: F-GPU-004
status: confirmed-header-and-sample
last_verified: 2026-09-14
---
# GPU render callback return does not imply device completion

## Observation
Premiere's GPU Device Suite states that GPU frames may have outstanding asynchronous operations on the compute stream. The distributed Vignette sample follows this contract: OpenCL enqueues a kernel and returns without a queue finish; Metal commits a command buffer and returns without waiting for completion.

## Architectural implication
GPU PPix/world handoff is sequenced by the host's device queue/stream contract. CPU callback completion and GPU execution completion are distinct events.

## Developer consequence
Never use CPU callback return as a synchronization primitive for resources referenced by queued GPU work. Resource disposal/reuse must respect the host device/queue lifetime contract.

## AE relevance
AE exposes the same style of device/command-queue handles through `PF_GPUDeviceSuite1`, so CPU/GPU completion separation is a high-confidence cross-host inference to test directly in AE.