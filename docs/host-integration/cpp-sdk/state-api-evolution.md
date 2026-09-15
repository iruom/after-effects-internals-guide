---
status: active
last_verified: 2026-09-16
evidence: ParamUtils state APIs + wide-time contracts + 13.5 UI/render synchronization notes
---
# State API Evolution: From Conservative Dirty Checks to Dependency Receipts

AE's state APIs show a long evolution from broad invalidation toward more precise, host-computed dependency identity.

This history matters because obsolete APIs can remain ABI-compatible while becoming less precise and less efficient than the modern path.

## Compatibility can preserve correctness but lose reuse
The old Param Utils state functions remain for binary compatibility. Adobe deliberately renamed/de-emphasized obsolete source-level entry points so new builds move toward the newer state APIs.

Header comments describe the obsolete path as more conservative/inefficient. The compatibility goal is therefore not “same cache precision”; it is “old plug-ins still produce correct output”.

That is a useful general rule for AE archaeology:

`legacy API compatibility != modern scheduler/cache behavior`.
## Modern `PF_State` is an opaque dependency receipt
`PF_GetCurrentState()` captures host state for a selected parameter scope and optional time range; `PF_AreStatesIdentical()` compares such receipts.

The plug-in does not need to know the host's internal hash/layout. That lets AE change the implementation while preserving the semantic question: **would the selected dependency state render the same result?**

For automatic wide-time input, the queried state can include source-time dependencies needed to produce the requested interval. The receipt is therefore closer to a dependency closure than a simple memcpy of parameter values.

## Selector-specific safety boundary
Since the 13.5 UI/render architecture split, Adobe explicitly makes `PF_GetCurrentState()` return randomized/unreliable state from `PF_Cmd_UPDATE_PARAMS_UI` to avoid entering an unsafe synchronization/deadlock boundary.

This is stronger than “not recommended”: the host intentionally prevents callers from treating the result as valid identity in that context.

## Explicit extra state
When the host cannot infer every semantic dependency, modern APIs provide explicit escape hatches such as SmartFX GUID mixing or parameter/ARB change signaling. These are preferable to blind `FORCE_RERENDER` because they let old cache entries become reusable again when semantic state returns to a previous value.## Developer decision rule
Choose the narrowest host-state primitive that actually models the dependency:
- parameter/time dependency -> `PF_GetCurrentState()` / `PF_AreStatesIdentical()`;
- automatically discovered temporal checkout footprint -> wide-time dependency tracking;
- host-invisible semantic input -> GUID/state mix-in where the API permits it;
- ordinary user-visible parameter change -> parameter/ARB change signaling;
- emergency compatibility fallback -> forced rerender only when no semantic identity mechanism can represent the dependency.

The objective is not merely to trigger more renders. It is to let AE distinguish **same semantic state**, **different semantic state**, and **state that returned to a previous value**.

## Failure patterns
Broad invalidation can hide missing dependency declarations during development, then destroy cache reuse in production. Conversely, an underspecified state receipt or GUID mix can produce stale cached output that looks nondeterministic.

A second failure class is context misuse: state APIs that are valid in render/evaluation selectors may be unsafe or intentionally meaningless in UI callbacks. Treat selector context as part of the API contract.

## Experiments
Build one effect with two independent dependencies: a normal parameter and an external/hidden semantic value. Mutate each independently, undo/redo, move the requested time span, and compare callback counts plus frame reuse under precise state APIs versus `PF_OutFlag_FORCE_RERENDER`.

A useful falsification test is whether returning to an earlier semantic state can reuse an earlier cached frame. If it cannot, inspect whether the chosen invalidation path destroyed identity rather than describing it.

## Unknowns
Public `PF_State`, SmartFX GUID mixing, project render timestamps, Canvas receipts, TDB/BEE render GUIDs and RG cache-node identity are related by purpose but are not proven to be one internal representation. AEIG keeps them separate until controlled traces establish the mapping.

Cross-links: `../../evaluation/dirty-invalidation.md`, `../../cache-system/cache-architecture.md`, `../../render-graph/frame-checkout.md`, and `../../architecture/project-vs-render-state.md`.