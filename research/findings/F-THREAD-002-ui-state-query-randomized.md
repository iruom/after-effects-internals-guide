---
id: F-THREAD-002
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-THREAD-002 — UI-Context State Queries Are Deliberately Randomized

## Status
Confirmed from AE 25.6 `AE_EffectSuites.h`.

## Evidence
Adobe states that since AE 13.5, `PF_GetCurrentState()` returns a random state when called from `PF_Cmd_UPDATE_PARAMS_UI`, specifically to avoid threading deadlock problems. The same API behaves normally in other selectors.

## Interpretation
AE does not merely reject an unsafe query. It intentionally returns a value that cannot be relied on for equality/caching in that context. This suggests the real state query can cross a synchronization boundary that the UI selector must not enter.

The behavior was introduced with the 13.5 UI/render architecture split, matching other evidence that render-side state is no longer safely synchronously accessible from UI callbacks.