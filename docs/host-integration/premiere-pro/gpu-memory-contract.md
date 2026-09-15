---
status: active
last_verified: 2026-09-14
---
# Premiere GPU and Memory Contract

Premiere's public MediaCore GPU suites expose lower-level device and allocation rules that the AE Effect GPU structs explicitly reference through `PrSDKGPUDeviceSuite` device indices.

## GPU frames are asynchronously live
The GPU Device Suite warns that all GPU frames may have outstanding asynchronous operations on the compute stream. Receiving a GPU PPix does not therefore imply that all producing GPU work has globally completed.

All GPU frames use a top-left origin. The public GPU image-processing formats are BGRA 16f and 32f device frames.

## Device-context ownership
General suite calls require exclusive device access. Full GPU plug-ins using the dedicated GPU-render entry point are already invoked with exclusive access held. CUDA implementations manage context push/pop on the calling thread.

This makes device context a thread-scoped execution resource, not a process-global invariant.

## Host-managed allocation
The header states that all device memory and all pinned host memory must be allocated through the GPU Device Suite. Device/host purge calls are reserved for emergency cases where memory cannot be allocated through that suite, such as external OpenGL allocations.

On DirectX, device allocation is represented by committed default-heap resources while host allocation uses upload-heap resources. CUDA/OpenCL map to their native device/host allocation primitives.
## Media memory manager
The Memory Manager can incorporate plug-in-owned purgeable blocks into host pressure management. A block has a size, purge callback, callback refcon and host ID.

`TouchBlock` raises an item's cache priority each time it is used, strongly resembling recency-based pressure heuristics. `RemoveBlock` removes an item manually but explicitly does not invoke its purge callback.

The purge callback may be called on any thread. Any destructor/release path reachable from it must therefore obey thread-safety and thread-affinity rules.

## Architectural implication for AE
Local AE Debug Database keys such as device/host pool factors, lazy host cache purge and GPU memory reserve are consistent with a centralized memory-pressure controller above backend-specific pools. Premiere's suite gives a public view of this style of contract, but exact AE pool policy remains to be measured.

## Developer rules
- Do not infer GPU completion merely from handle delivery.
- Do not bypass host GPU allocators for ordinary working memory.
- Treat purge callbacks as concurrent callbacks.
- Separate object removal from object destruction; they are not necessarily the same event.
- Record device index in every GPU cache/resource identity.
## Declarative dependencies and precompute
Premiere's dedicated GPU Filter contract asks the plug-in to enumerate render dependencies before `Render`. Dependencies may request another frame/time, transition input, field separation, or a host-side precompute phase.

A precompute dependency declares output pixel format, dimensions, PAR, field type and optional custom-data size. The host allocates the destination in pinned host memory; `Precompute` may run ahead of the final render; the host later uploads or converts the result into the GPU representation.

This cleanly separates dependency declaration, CPU-side preparatory materialization, transfer, and device execution.

The inspected SDK contains no concrete sample returning `PrGPUDependency_Precompute`; the contract is explicit but scheduling details must be measured.

## Contrast with AE SmartFX
Premiere GPU Filter dependencies are primarily declarative: enumerate what is required, then let the host schedule it. AE SmartFX discovers image dependencies through PreRender checkout calls, which are demand/checkout-oriented.

A generalized engine can support both: a static dependency declaration for maximum scheduling freedom, plus a controlled dynamic-checkout escape hatch for data-dependent requests.

## Version and failure boundary
This page is grounded in the inspected Premiere 26.0 SDK plus AE 25.6 shared-device references. Do not project exact allocator/pixel-format requirements into older Premiere or current AE without verifying the corresponding contract generation.

Failure classes include reading a GPU result before queue completion, using a stale device index after device change, bypassing host allocation and defeating pressure accounting, deadlocking exclusive-device access, and running thread-affine destruction from an arbitrary purge callback.

## Cross-host experiment
Implement equivalent no-op/copy GPU paths in AE and Premiere where supported. Record device index, allocation source, callback return, explicit synchronization point, CPU readback timing and memory-pressure behavior. A matching invariant is stronger than matching type names.

## Unknown frontier
Unresolved for AE: exact mapping from PF GPU world lifetime into GPUFoundation cache objects; whether AE exposes the same purge priority semantics; backend-specific fencing after effect callback return; extent of shared PrSDK device-suite implementation versus adapter-only compatibility.

Related: `docs/gpu-system/overview.md`, `docs/memory-system/runtime-architecture.md`, `docs/foundations/cross-host-triangulation.md`, `F-GPU-003-shared-mediacore-device-contract.md`, `F-GPU-004-return-is-not-gpu-completion.md`.
