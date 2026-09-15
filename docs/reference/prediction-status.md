---
status: generated
last_verified: 2026-09-16
---
# Prediction Status

Predictions: **10**. Prospective: **7**; locked before run: **7/7**; prospectively confirmed: **2**.

Modes: `{'retrospective-validation': 3, 'prospective': 7}`. Statuses: `{'confirmed': 5, 'pending': 5}`.

| ID | Mode | Domain | Experiment | Status | Prediction |
|---|---|---|---|---|---|
| `PRED-001` | retrospective-validation | `evaluation` | `EXP-CORE-001` | **confirmed** | Unchanged project state produces byte-identical output for every sampled frame. |
| `PRED-002` | retrospective-validation | `evaluation` | `EXP-CORE-001` | **confirmed** | Changing only the midpoint Blur keyframe changes interpolated dependent frames while preserving the unchanged t=0 endpoint. |
| `PRED-003` | retrospective-validation | `observability` | `EXP-OBS-002` | **confirmed** | TraceEnabled is bounded by both master and category trace thresholds. |
| `PRED-004` | prospective | `state-identity` | `EXP-CACHE-002` | **pending** | Within each pass, a generated effect prefix k<n returns VALID_BUT_INCOMPLETE while k>=n returns VALID. |
| `PRED-005` | prospective | `cache` | `EXP-CACHE-002` | **pending** | The abstract prefix-sufficiency relation remains unchanged after Blur 10->75 when topology/effect count are unchanged. |
| `PRED-006` | prospective | `render-graph` | `EXP-RG-001` | **pending** | BEE/RG/TDB/GUID target categories emit inside the real RenderTexture window. |
| `PRED-007` | prospective | `state-identity` | `EXP-RG-001` | **pending** | Changing only Blur state changes at least part of the MixHashGuid/TDB/evaluation trace footprint. |
| `PRED-008` | prospective | `render-graph` | `EXP-RG-001` | **pending** | Changing only Blur state changes at least part of the RG/cache/work-queue trace footprint. |
| `PRED-009` | prospective | `plugin-host` | `EXP-PLUGIN-001` | **confirmed** | Accepted PICA selector integers are scoped to suite name rather than one global monotonic generation namespace. |
| `PRED-010` | prospective | `plugin-host` | `EXP-PLUGIN-001` | **confirmed** | The runtime matrix cannot be safely represented by aliasing every family to one latest SDK 25.6 table. |

## Release rule
AEIG 1.0 requires the prospective predictions to be frozen before observation, at least three prospectively confirmed predictions, and no unresolved `pending`, `inconclusive`, or unknown result from the canonical L5 operator run. A refutation is acceptable only after the affected model is explicitly revised and the row is marked `refuted-revised`.
