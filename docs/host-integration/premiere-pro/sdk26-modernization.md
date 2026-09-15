---
status: active
last_verified: 2026-09-14
---
# Premiere 26 SDK Modernization Clues

The Premiere 26.0 distribution exposes evolution that is useful for judging what Adobe considers a modern render contract.

`PrSDKAcceleratedRender.h` preserves request generations rather than replacing the ABI. Successive versions add caption format, final output pixel format, output color space, export LUT and hardware-resident-frame support.

The header contains explicit conversion helpers from older render-request layouts to newer layouts, supplying invalid/default values for fields that did not exist previously. Compatibility is therefore implemented as structured request up-conversion.

Render initiation is asynchronous and request-ID based. Cancellation is a first-class selector. Optional render-session start/finish selectors provide a lifetime larger than an individual frame.

The latest renderer contract can advertise support for hardware-resident output, showing that the logical frame result no longer necessarily implies host-readable CPU pixels.

## Contrast with AE
AE's Effect API also accumulates suite/selector generations, but much of the older compatibility history is split among old headers and host-specific flags. Premiere's explicit request structs make semantic growth easier to inspect.

## Improvement lens
AEIG should record not only old AE behavior but where a newer contract could move state out of ambient context and into explicit immutable request descriptors, capability flags and typed result handles.

## What to test against AE
Use Premiere's explicit request growth as a checklist for AE Render Options/Frame Receipt reconstruction: output color interpretation, hardware residency, session lifetime, cancellation generation and immutable request descriptors.

A discriminating experiment is to change one request dimension that older Premiere request generations could not express and observe how new-generation conversion/defaulting behaves. Then ask whether AE has an equivalent ambient/default field or an explicit versioned surface.

## Unknown frontier
The comparison does not prove Adobe plans to redesign AE around Premiere request structs. It only demonstrates one current Adobe host's solution to ABI growth. Exact shared MediaCore types below the host-specific request layers remain to be mapped.

Related: `docs/foundations/cross-host-triangulation.md`, `docs/render-graph/render-request-sufficiency.md`, `docs/foundations/version-model.md`.
