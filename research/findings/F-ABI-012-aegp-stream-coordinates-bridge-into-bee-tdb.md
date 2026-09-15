---
status: active
evidence_grade: strong-header-binary-correlation
versions: "SDK 25.6 + installed AE 2025 runtime"
last_verified: 2026-09-15
---
# AEGP stream coordinates bridge into BEE/TDB identities

## Confirmed observations
The distributed 25.6 header defines collection coordinates in public AEGP terms: a layer handle plus effect index for `AEGP_EffectCollectionItem`; layer/mask/effect variants for `AEGP_StreamCollectionItem`; and `AEGP_StreamRefH` as the stream handle carried by `AEGP_CollectionItemV2`.

Installed `MEE.dll` exports a family of conversion functions that place those public coordinates beside internal BEE/TDB types in the same ABI signatures:

- `AssignBEE(AEGP_EffectCollectionItem const*, BEE_EffectSpec*)`
- `AssignBEE(AEGP_StreamCollectionItem const*, BEE_StreamSpec*)`
- analogous mask, mask-vertex and keyframe conversions
- `GetStreamSpec(_AEGPp_Stream*, BEE_StreamSpec*)`
- `LayerStreamToBEEStream(BEE_Layer*, AEGP_LayerStream) -> TDB_StreamIDPath`
- `BEEStreamToLayerStream(TDB_StreamIDPath const&) -> AEGP_LayerStream`
- `AEGPMaskStreamToBEEMaskStream(AEGP_MaskStream) -> TDB_MatchName`
## Strongest justified model
AEGP selection/collection coordinates are not an unrelated public abstraction. At the MEE boundary, they are translated into BEE specs and TDB stream identity objects used by the host's internal model. This supports a cross-layer path of the form:

`AEGP layer/effect/stream coordinate -> MEE normalization -> BEE_*Spec / TDB_StreamIDPath -> render/dependency identity`

The last arrow remains a structural correlation, not a proven single call chain. Separate findings already show TDB render-GUID participation and BEE/RG cache graph integration.

## Important non-claims
This does **not** establish the private layout of `_AEGPp_Stream`, make BEE/TDB exports supported plug-in APIs, or prove that `AEGP_StreamRefH` can safely be dereferenced by third-party code. `GetStreamSpec` taking `_AEGPp_Stream*` is evidence about the host's internal representation boundary, not permission to bypass the opaque handle contract.

## Reproducibility
`probes/process-tools/derive_aegp_internal_bridges.py` regenerates `datasets/ae-2025-aegp-internal-bridges.csv` from the runtime export atlas. Current result: 24 bridge/registration rows.

## Next experiments
Correlate one selected layer property through AEGP CollectionSuite, StreamSuite persistent IDs/match names, TDB trace vocabulary and render-GUID changes. Test effect reorder and duplicate-match-name cases so index identity is not accidentally confused with persistent stream identity.
