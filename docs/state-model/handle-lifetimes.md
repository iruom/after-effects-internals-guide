---
status: active
last_verified: 2026-09-14
---
# Opaque Handles Are Not Stable Identities

AEGP uses many opaque handle types, but opacity does not imply persistent identity or unlimited lifetime. AEIG tracks invalidation rules per handle family.

## Render Queue item handles
The old and current RQ Item suites explicitly state that **all** `AEGP_RQItemRefH` values are invalidated by any render-queue reorder, insertion, or removal: `DO NOT CACHE THEM`.

Output-module references carry a matching warning when output modules are reordered, added or removed.

This strongly suggests container-backed references whose validity depends on structural generation, not object identity independent of collection mutation.

## Receipts and checked-out worlds
Frame receipts own access to host-rendered read-only worlds. The world is not plug-in owned and remains tied to the receipt until `AEGP_CheckinFrame()`.

## Developer pattern
Store durable identifiers or reacquisition paths, not opaque references, across operations that can structurally mutate their owner collection. Treat each handle type as one of: durable object reference, collection-generation reference, render-context reference, checkout/receipt lifetime, or explicit owner-dispose resource.
## Project item handle vs item identity
Item APIs expose both `AEGP_ItemH` and a numeric `AEGP_GetItemID`. Treat these as different categories until experiments prove their persistence/equality rules. A handle is a host reference; an ID is an identity token exposed by the project model.

Project-created objects such as folders are explicitly allocated and owned by AE, unlike caller-owned StreamRefs and MemHandles.

## Current-time state is not render time
Old Item Suite comments explicitly state that `AEGP_GetItemCurrentTime` is not updated while rendering. It belongs to the item's interactive/native-timespace state, not to an active render request.

Render-time code must therefore use Render/Canvas context time rather than project-item current time. Mixing these domains is a direct snapshot-divergence bug class.

## Mutation blast radius
`AEGP_DeleteItem` removes the item from all compositions and is undoable. Any cached project-topology reference dependent on that item must be assumed invalid or stale across the mutation, even if an unrelated handle type remains numerically non-null.
## Borrowed frame worlds
`AEGP_GetReceiptWorld` returns a read-only world that is not owned by the plug-in. Its lifetime is tied to the frame receipt; `AEGP_CheckinFrame` releases that checkout. Never dispose or mutate the world directly.

The receipt is therefore both an identity/validity object and a lifetime token for borrowed image storage.

## GPU worlds: same type, different ownership
`PF_GPUDeviceSuite1::CreateGPUWorld` creates a plug-in-owned `PF_EffectWorld` that the caller must dispose. `DisposeGPUWorld` immediately invalidates it, and Adobe explicitly restricts disposal to worlds created by the plug-in.

A host-provided/checked-out GPU `PF_EffectWorld` may use the same C type while following a different ownership contract. Ownership must be tracked by origin, not inferred from handle type.

## Stable-looking UI time is snapshot state
Both Item and Layer suites historically mark their current-time getters as not updated while rendering. These handles remain usable, but the queried UI/project time is not the active render time. This is a semantic lifetime problem rather than pointer invalidation.
## Ownership is provenance, not C type
Legacy suite comments expose several distinct lifetime classes that share the same opaque-handle style:
- `GetNew*Stream`, duplicated StreamRefs, EffectRefs returned by lookup/apply, and MaskRefs are caller-disposable resources.
- Stream values may contain owned payload and require `DisposeStreamValue`, even though the value is returned as a struct.
- Input strings/collections marked `not adopted` remain caller-owned after setters return.
- RQItem and OutputModule refs are host-borrowed but become invalid when their owning collection is structurally mutated.

A generic wrapper should therefore encode acquisition provenance and release function, not infer ownership from the handle typedef.

## Thread-affinity is also part of lifetime
Legacy Canvas marks Artisan progress reporting as not thread-safe and restricted to render thread ID 0. Modern Utility Suite provides a complementary case: `CauseIdleRoutinesToBeCalled` itself is safe from a non-main thread, but the suite lookup used to obtain its function pointer is not thread-safe; Adobe tells callers to acquire/save the pointer on the main thread first.

A resource/callback capability can therefore have two affinities: acquisition affinity and invocation affinity. AEIG should track both separately.
