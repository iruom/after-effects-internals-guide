---
status: active
last_verified: 2026-09-14
---
# GUID Mixing and Extra Render Dependencies

AE's SmartFX cache identity can be extended with plug-in-defined state through `GuidMixInPtr()`, gated by `PF_OutFlag2_I_MIX_GUID_DEPENDENCIES`.

This exists for render-relevant state that AE cannot infer from ordinary effect parameters or upstream image checkouts: custom UI state, sequence data, host queries, external state, or other dependencies invisible to the default dependency graph.

Conceptually:

`FrameGUID = H(AE-managed dependencies, plug-in supplied render-relevant bytes)`

The exact hash algorithm is intentionally opaque. What matters is the equivalence relation: if two render requests are semantically identical, they should mix identical dependency state; if output semantics differ, the mixed state should differ.
## SmartyPants exposes a subtle context bug
Adobe's `SmartyPants` sample mixes the composition background color into the frame GUID during Smart PreRender. The sample itself warns: `This doesn't handle the collapsed comp case`.

The reason is architectural: the effect obtains its project layer, asks for that layer's parent comp, and hashes that comp's background color. Under Collapse Transformations / collapsed geometrics, the effective render context can be promoted into a different root-comp context. Project parentage and render parentage are therefore not guaranteed to identify the same semantic environment.

This is a concrete example of a cache-key bug caused by using project topology where render-context topology is required.

### Developer rule
Do not hash ambient host state by navigating ordinary project objects unless that object identity is guaranteed to match the current render context. For collapsed/precomposed/renderer-mediated cases, prefer context-aware queries or explicitly test the mismatch.
## Under-mixing and over-mixing
Under-mixing causes false cache hits: two semantically different renders share the same GUID and stale pixels are reused. Over-mixing causes false cache misses: irrelevant state changes create new identities and destroy reuse.

A good dependency fingerprint should include only state that can change rendered output in the current mode. Adobe's header comments explicitly warn that mixing state even while the effect/functionality is disabled reduces cache efficiency.

This creates an optimization problem:

`maximize cache reuse subject to semantic correctness`.

The ideal cache key is therefore not a dump of all available state. It is a minimal sufficient fingerprint of output semantics.

## Local evidence
Retained AE trace databases contain `MixHashGuid`; local runtime crash/trace evidence also exposes Render-GUID functions at stream, layer and comp levels. These observations support a hierarchical identity model but do not reveal the hash implementation itself.
