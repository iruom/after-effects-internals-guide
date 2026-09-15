---
status: confirmed-distributed-header-boundary
last_verified: 2026-09-15
evidence: AE 25.6 distributed headers
---
# F-ABI-011 — Distributed headers expose an Adobe-internal AEGP extension boundary

Multiple distributed 25.6 headers branch on `AEGP_INTERNAL` and include a non-distributed `AE_GeneralPlug_Private.h` for internal builds. Public builds instead receive opaque handles or reduced declarations.

The boundary appears in `AE_GeneralPlug.h`, `AE_ComputeCacheSuite.h`, `AE_HashSuite.h`, `AE_GeneralPlugPanels.h`, and `AE_IO.h`.

`AE_GeneralPlug.h` makes the split especially explicit: without `AEGP_INTERNAL`, Project, Item, Comp, Footage, Layer, Effect, Mask, Stream, RenderLayerContext, PersistentBlob, RenderReceipt, World, RenderOptions and other objects are represented as opaque handles.
## What this proves
It proves a private extension/definition boundary exists in Adobe's build and that the public handles intentionally hide host-owned structures. It does **not** reveal the private definitions or prove that guessing their layouts is safe.

The machine inventory is `datasets/ae-sdk-25.6-private-gates.csv`.

## Research direction
Correlate each opaque public handle with runtime BEE/TDB/RG symbols and debugger/trace vocabulary, but keep representation hypotheses distinct from the supported handle contract. The useful target is to recover semantics and capabilities without assuming the opaque handle is a raw pointer to any particular internal C++ object.

## Plug-in implication
Previously impossible operations may become understandable by locating the host subsystem behind an opaque handle, yet bypassing the public ownership boundary can invalidate thread/lifetime/cache invariants. Internal invocation should therefore require an I3 experiment-backed entry rather than being inferred from symbol names alone.
