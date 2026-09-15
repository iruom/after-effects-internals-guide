---
status: active
last_verified: 2026-09-15
---
# Guide Gap Matrix

The public C++ SDK Guide is the supported contract surface, but it is not treated as a complete inventory of the host. AEIG continuously compares it against distributed headers, historical headers, Adobe samples, runtime artifacts and independent reimplementations.

Legend: `yes` = directly represented; `partial` = only part of the concept is surfaced; `gap` = meaningful evidence exists elsewhere but the Guide does not expose the same detail.

| Concept | Guide 26.5 | Header 25.6 | Old Header | Adobe sample | Runtime/local | Reimplementation |
|---|---|---|---|---|---|---|
| Effect selectors / lifecycle | yes | yes | yes | yes | observable | aexlo/AexExecutor |
| SmartFX ROI / bounds | yes | yes | history | yes | observable | aexlo/AexExecutor |
| MFR sequence-data ownership | yes | yes | history | yes | prefs/logs | aexlo |
| Compute Cache | yes | yes | limited history | samples | indirect | partial |
| Render receipt / frame sufficiency | partial | yes | history | Artisan/AEGP | trace leads | partial |
| Hash/GUID construction | partial | yes | history | sparse | `MixHashGuid` trace | partial |
| Cache-key inclusion of AE build/effect version | yes | header context | history | — | behavior probe | — |
| `PF_ChannelType_DEPTHAA` | gap | yes | — | — | unknown | — |
| Private-header extension boundary | gap | yes (`AEGP_INTERNAL`) | historical clues | — | symbols/modules | — |
| Numeric PICA suite version mapping | abstracted | exact | exact history | indirect | actual requests | host emulators |
| Exact historical vtable layout | gap | current | exact | — | binary callers | host emulators |
| BEE / RG runtime vocabulary | gap | gap | gap | gap | Trace Database | — |
| Render-side project snapshot split | partial/history | selector contracts | history | some samples | runtime clues | emulators expose need |
| MediaCore boundary | partial | partial | history | AEIO | modules/logs | partial |
## How to use the matrix
A gap is not automatically an undocumented feature. It can be:
- a prose-documentation omission;
- ABI detail intentionally left to headers;
- historical compatibility support;
- renderer/host-specific behavior;
- Adobe-internal extension boundary;
- a stale or unused declaration;
- a false lead created by a third-party implementation.

Each gap should become a finding or hypothesis only after its strongest available source is inspected.

## Current high-value gaps
1. **Runtime evaluation vocabulary:** `BEE_*`, `RenderNode.RG_*`, `RenderTaskManager` and related local trace categories have no direct Guide ontology.
2. **Identity composition:** public hash/GUID/receipt APIs can be compared with runtime `MixHashGuid` and cache behavior.
3. **Historical ABI negotiation:** commercial plug-ins can request very old PICA suite versions even on modern hosts.
4. **Auxiliary image channels:** header-only or renderer-specific channel types may expose hidden intermediate buffers.
5. **Private/public build boundary:** distributed headers contain explicit internal-build include branches without distributing the private definitions.

The matrix should be regenerated conceptually for every major SDK release, rather than treated as a one-time audit.

## 26.5 Guide vs 25.6 distributed-header delta
The public Guide revision dated 2026-09-02 documents several surfaces absent from the local 25.6 header corpus:

| 26.5 Guide surface | Local 25.6 header result | Architectural relevance |
|---|---|---|
| `AEGP_CompSuite13` | absent; latest local is Suite12 / PICA 26 | parametric-mesh layer creation extends comp object model |
| `AEGP_StreamSuite7` | absent; latest local is Suite6 / PICA 11 | exposes layer-parameter render stage independently of layer ID |
| `AEGP_GuideSuite1/2` | absent | guides become first-class readable/writable project state |
| `AEGP_ItemViewSuite2` | absent; local has Suite1 / PICA 1 | guide visibility/snap/lock adds view-state control |

The absence check searched the complete local `Examples/Headers` tree for `AEGP_CompSuite13`, `AEGP_LayerParamStage`, `AEGP_GuideSuite`, and `AEGP_ItemViewSuite2` and found no matches.

This is a version delta, not an undocumented-host claim. It should remain separate from runtime-only gaps such as BEE/RG vocabulary.