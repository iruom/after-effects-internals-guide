---
status: active
last_verified: 2026-09-16
evidence: current PF world/color contracts + Premiere host differences + GPU/video-frame bridge archaeology
---
# Pixel Formats, Layout, and Residency

Pixel format in After Effects is part of the render contract, not just storage metadata. Correct code must keep **numeric representation, channel layout, row stride, alpha interpretation, color semantics and residency** as separate dimensions.

A useful decomposition is:

```text
component representation (8 / 16 / float)
        x channel order/layout
        x rowbytes/alignment
        x alpha association
        x color-space/transfer interpretation
        x CPU/GPU/media residency
```

Changing one axis does not imply the others changed.

## PF_EffectWorld basics

After Effects exposes `PF_EffectWorld` / `PF_LayerDef` as the Effect API image container. Public formats include ARGB32 (8-bpc), ARGB64 (16-bpc) and ARGB128 (32-bpc float). Input and output worlds of one render have matching depth and will not exceed what the effect advertised support for.
## Rowbytes is authoritative

Never compute the next scanline from `width * sizeof(pixel)` alone. `rowbytes` may include padding, input and output worlds of identical dimensions may have different rowbytes, and subregions can inherit alignment that does not match SIMD assumptions.

Adobe explicitly warns that PF worlds are not guaranteed to be 16-byte aligned. Code that blindly casts the base pointer into a vector type can fail only on particular ROIs, hosts or allocator layouts.

The safe pattern is row-by-row addressing from the base pointer using `rowbytes`, then x-offset using the correct pixel type for the verified format.

Writing beyond the requested/world region is especially dangerous because adjacent memory may belong to cached image buffers owned by AE.

## Pixel pointer abstraction

The SDK strongly discourages arbitrary casting of `PF_PixelPtr`. Use the provided pixel-data accessors or `PF_WorldSuite` format query so the code fails safely when the world is not the expected depth.

This is future-proofing as well as type safety: opaque pointer representation is not a promise that every host/version will preserve one C struct layout forever.
## 16-bpc is not ordinary full-range uint16

AE's traditional 16-bpc UI/value conventions use the 0-32768 scale rather than treating 65535 as canonical white. Code that assumes a generic unsigned-16 normalization can therefore introduce gain errors or inconsistent conversions.

Do not derive numerical white/black constants yourself when a host callback/suite provides them. This becomes even more important in Premiere-native formats where RGB/YUV layout and legal ranges can differ.

32-bpc float introduces a different semantic class: values can be outside 0-1, including negative and over-range components. Clamping merely because the destination type is float destroys HDR/intermediate information.

## Alpha association is independent

Premultiplication is an interpretation/operation, not implied solely by component depth. AE supplies premultiply/unpremultiply utilities for 8/16/float worlds. Hidden RGB under zero alpha can be semantically significant; see `alpha-zero-rgb.md`.

A conversion pipeline should state explicitly whether it changes component depth, alpha association, color space or all three. Silent combined conversions make numerical debugging almost impossible.
## GPU worlds and residency

During GPU Smart Render, `PF_LayerDef` keeps geometry/format metadata while the CPU `data` pointer is null. Pixel storage is device-side and must be accessed through the GPU/device contract rather than by falling back to CPU pointer assumptions.

This is a strong example of format versus residency: a render request can keep the same logical dimensions/depth while changing where the pixels live and how they are accessed.

Local AE runtime surfaces also bridge PF worlds, GPU frames and MediaFoundation `IVideoFrame` objects. Those bridges are evidence of shared frame representations and transfer paths, not permission for third-party code to call private conversion exports.

## Cross-host warning: Premiere formats

Premiere can host AE effects but supports additional native pixel formats such as BGRA and YUV, with different render scheduling and checkout behavior. Adobe explicitly warns that AE utility functions are not automatically generalized to all Premiere-native formats.

Therefore host capability must be negotiated rather than inferred from an AE build that happened to work. A plug-in supporting multiple hosts should branch on the actual host/pixel-format contract and test each path independently.
