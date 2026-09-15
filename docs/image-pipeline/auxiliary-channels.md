---
status: active
last_verified: 2026-09-14
---
# Auxiliary / Multi-Channel Image Data

AE exposes an old but unusually revealing side-channel system independent of the normal RGBA `PF_EffectWorld`. `PF_ChannelSuite1` is frozen in AE 5.0, showing that typed per-pixel auxiliary data has been part of the host architecture for decades.

## Known channel classes
The AE 25.6 distributed header names: Depth, anti-aliased Depth, Normals, Object ID, Motion Vector, Background Color, Texture, Coverage, Node, Material, Unclamped and Unknown.

`PF_ChannelType_DEPTHAA` is specifically annotated as introduced in AE 16.0 for 3D precomps in some Artisans. This is direct evidence that the legacy auxiliary-channel system continued evolving long after its original AE 5-era API froze.

## Data model
Each channel has a type, human-readable name, elementary data type and dimension. A normal can therefore be represented as a dimension-3 channel while a depth channel is dimension-1.
`PF_ChannelChunk` mirrors image storage: width, height, row bytes, data type, dimension, handle and locked pointer. Pixel size is `dimension * sizeof(data_type)`, so the system is a generic interleaved multi-plane raster container rather than a fixed set of structs.

## Temporal checkout
Channel data is checked out using `(what_time, duration, time_scale)` plus a requested data type. It must then be checked back in. The channel is therefore not merely metadata attached to a layer; it is a time-dependent renderable resource with host-managed lifetime.

The official `Checkout` sample demonstrates depth checkout from effect input parameter 0 and explicitly excludes Premiere because Premiere Pro/Elements do not support this suite.

## Architectural implication
RGBA pixels are only one product of AE's render ecosystem. Some 3D/render paths can expose auxiliary buffers carrying geometric or semantic information alongside color. This may explain old 3D-channel effects and provides a direct research surface for renderer materialization boundaries.
## Research priorities
- Determine which current Advanced 3D / Classic 3D paths still populate legacy channel types.
- Compare `DEPTH` and `DEPTHAA` numerically at 3D-precomp boundaries.
- Determine coordinate/sign conventions for Motion Vector and Normals.
- Test whether Object ID / Node / Material survive precomp, collapse transformations and effect application.
- Test whether `UNCLAMPED` represents an HDR/color-side buffer, a renderer-specific source, or legacy semantics.

## Developer tips
Always honor the returned `PF_ChannelDesc`; do not hard-code element width or vector dimension from channel type alone. Always check in a successful checkout, including error exits. Treat channel availability as host/render-path dependent rather than guaranteed by layer type.
## Guide/header coverage gap
The public Guide's current Auxiliary Channel list omits `PF_ChannelType_DEPTHAA`, while the distributed AE 25.6 header defines it and dates it to AE 16.0 for 3D precomps in some Artisans. Header and Guide must therefore be compared rather than treated as equivalent sources.

## Connection to AEIO
AEIO module flags separately expose `AEIO_MFlag_HAS_AUX_DATA` for file formats containing depth, normals, or other non-color per-pixel information. This strongly suggests an ingestion path where importer-provided non-color data can enter the host's auxiliary-data ecosystem.

The exact bridge from AEIO auxiliary payloads to `PF_ChannelSuite` should be traced in AEIO headers and samples rather than assumed.

## Cross-host boundary
Adobe's `Checkout` effect sample explicitly skips the Channel Suite when hosted by Premiere Pro/Elements because that host does not support it. This is useful cross-host evidence that auxiliary channels are an AE-specific host capability layered above the otherwise shared Effect API.

## AEIO source-side production path
AEIO exposes the matching source-side primitives: `AEIO_GetNumAuxChannels`, `AEIO_GetAuxChannelDesc`, `AEIO_DrawAuxChannel`, and `AEIO_FreeAuxChannel`. The description and payload types are the same `PF_ChannelDesc` / `PF_ChannelChunk` abstractions used by the Effect Channel Suite.

This is stronger than a naming coincidence: importer and effect surfaces share the same typed channel representation. A plausible host architecture is therefore `AEIO source auxiliary payload -> host channel object -> effect checkout`, although the exact internal handoff still requires runtime verification.

The stock AE 25.6 `SDK_IO` sample sets `AEIO_MFlag_HAS_AUX_DATA` but leaves the auxiliary callbacks unset in its zero-initialized function block. Treat that sample as an incomplete scaffold for this capability, not a complete reference implementation.

## Guide gap: `DEPTHAA`
The current public Guide enumerates the auxiliary types but omits `PF_ChannelType_DEPTHAA`; the distributed Header defines it and says it was added in AE 16.0 for 3D precomps in some Artisans. This is a concrete reason AEIG treats distributed Headers as an independent evidence layer rather than a mirror of the prose Guide.