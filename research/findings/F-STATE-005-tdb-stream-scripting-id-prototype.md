---
status: confirmed-local-feature-surface
last_verified: 2026-09-15
---
# F-STATE-005 — AE 2024/2025 carries a persistent Property/Stream ID scripting prototype

AE 2024 and AE 2025 localization dictionaries contain the Beta feature EnableTDBStreamScriptingIDs. Its description says a new ID scripting hook is added to Property objects so scripts can hold consistent references to specific streams; its display name describes persistent property IDs.

The current public Scripting Guide still documents reference invalidation when indexed property groups are rebuilt and does not expose a general Property.id/PropertyBase.id. By contrast, Item IDs and Layer IDs are publicly persistent across save/reload, while AEGP AEGP_GetUniqueStreamID is documented as session-unique.

## Architectural implication
AE's internal TDB stream model appears capable of a stronger property identity than the public scripting surface currently guarantees. This is consistent with runtime symbols such as TDB_Stream::GetRenderGuid, but persistent scripting identity and render GUID identity must not be assumed to be the same namespace.

## Research action
Track later Beta/stable builds for a Property-level ID API; compare AEP property records before/after effect reorder/duplication; instrument scripting references across group reconstruction; distinguish persistent object identity, session handles, and render-state identity.
