---
id: F-GUID-004
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-GUID-003 窶・AEGP exposes direct GUID/hash construction primitives

**Evidence:** E0-H  
**Version:** `AE_HashSuite.h`, frozen AE 17.5.1  
**Confidence:** High

`AEGP_HashSuite1` exposes `AEGP_CreateHashFromPtr` and `AEGP_HashMixInPtr`, operating on `AEGP_GUID`.

## Consequence
GUID/state construction is not merely an undocumented renderer detail: Adobe exposes a host-compatible mechanism for constructing and extending the same GUID-shaped identity domain used by Compute Cache and other render-state APIs.

This strengthens the model that render/cache identity is compositionally mixed from state fragments rather than derived from rendered pixels.

## Open question
Determine whether GUID mixing is algorithmically compatible with `AEGP_GetReceiptGuid`, `PF_State`, `I_MIX_GUID_DEPENDENCIES`, and the runtime `MixHashGuid` / `BEE_*GetRenderGuid*` symbols.
