---
id: F-ABI-016
status: confirmed-historical-corpus
confidence: high
evidence: [E0-H]
version_scope: "CS6/11.0 -> CC2014/13.0 -> SDK 25.6 header corpora"
last_verified: 2026-09-15
---
# F-ABI-016 — CC2014 is a major transitional API surface, not a minor lineage point

A three-point raw/header inventory across CS6, CC2014 and SDK 25.6 finds 3,481 identifiers continuously present, 468 introduced by CC2014 and retained through 25.6, 7 transient CC2014-only identifiers, 5 identifiers present through CC2014 but absent from 25.6, and 417 identifiers introduced after CC2014.

Representative CS6→CC2014 additions include `AEGP_CanvasSuite8`, `AEGP_LayerRenderOptionsSuite1`, `AEGP_NewFromUpstreamOfEffect`, `AEGP_RenderAndCheckoutLayerFrame`, `AEGP_GetPluginPaths`, bicubic layer sampling, newer persistent-data surfaces, and the Drawbot family.

The transient CC2014-only set is mostly version/runtime glue such as `PF_AE131_PLUG_IN_VERSION/SUBVERS` and legacy SP/CFM helpers. The removed-after-CC2014 set includes older compatibility names such as `PF_ANSICallbacks`, `PF_App_Color_TLW_NEEDLE`, `PF_ExtendedSuiteTool_CAMERA_ORBIT`, `PF_MAX_THREADS`, and the formerly reserved render-output flag.

## Consequence
Do not interpolate directly from CS6 to modern 25.x when reconstructing feature introduction or ABI compatibility. CC2014 already contains several modern request, sampling, UI drawing and plug-in-path concepts, while also retaining compatibility names later folded, split or repurposed.

Machine evidence: `datasets/ae-sdk-lineage-cs6-cc2014-25_6.csv`, `datasets/ae-api-surface-deltas.csv`, and the pinned third-party archive under `research/external-sources/ae-sdk-cc2014`.