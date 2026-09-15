---
id: F-ABI-015
status: confirmed-current-corpus
confidence: high
evidence: [E0-G, E0-H]
version_scope: "current C++ Guide 26.5 versus SDK 25.6 + retained pre-25.6 + CS6 header corpora"
last_verified: 2026-09-15
---
# F-ABI-015 — Guide presence, spelling, and host scope are independent from distributed ABI

AEIG's complete Guide/Header relation review found multiple distinct reasons for a current Guide identifier to lack an exact distributed-header identifier. They must not be collapsed into "new API".

Confirmed classes include documentation aliases/truncations, explicit Guide signatures absent from all inventoried headers, historical removed calls, cross-host Premiere-only additions, and plain Guide vocabulary with no C identifier claim.

Examples:
- `AEGP_GetProjectProjectByIndex` is a Guide signature typo; SDK 25.6 defines `AEGP_GetProjectByIndex`.
- `AEGP_GetNthLayerIndexToRender` appears under the Guide's `AEGP_GetCompRenderTime` row; SDK 25.6 defines `AEGP_GetCompRenderTime` and separately `AEGP_GetNthLayerContextToRender`.
- `AEGP_GetIndProject` is a Guide row label for project-by-index behavior, not the distributed function spelling.
- `AEGP_GetNewMaskOpacity` remains documented beside the generalized `AEGP_GetNewMaskStream`; the distributed 25.6 StreamSuite exposes the generalized mask-stream accessor.
- `PF_HasParamChanged` is explicitly documented as removed/no longer supported; old headers retain an obsolete slot rather than a current contract.
- `AE_Effect_Description`, `AE_Effect_Search_Keywords`, and `PF_REGISTER_EFFECT_EXT3` are documented in the shared Guide but explicitly scoped to Premiere Pro Beta 27.0 rather than After Effects.

## Consequence
An AE host or compatibility layer must not synthesize ABI from documentation spelling alone. Each surface requires separate `host_scope`, `distribution_presence`, `historical_status`, and exact suite/version evidence.

Machine sources: `datasets/ae-api-completeness-classification.csv` and `datasets/ae-api-guide-relation-classification.csv`.
Status pages: `docs/reference/api-completeness-status.md` and `docs/reference/api-guide-relation-status.md`.
