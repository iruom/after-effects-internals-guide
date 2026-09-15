---
status: seed
evidence_grade: E0 + E2-L
versions: "legacy to current"
last_verified: 2026-09-14
---
# AE exposes GUID/receipt-like render state identity

## Statement
Public render/cache APIs expose state/receipt concepts; local traces contain MixHashGuid; cache behavior reuses results after state restoration.

## Interpretation rule
Do not infer more than the evidence supports. Internal names are observation points, not automatically class or subsystem definitions.

## Next experiment
Run A-B-A state cycles, duplicate/cross-project tests and trace GUID mixing activity.

## Confirmed public contract
CC 2015 introduced `PF_OutFlag2_I_MIX_GUID_DEPENDENCIES` / `GuidMixInPtr()` for SmartFX. During Smart Pre-Render, plug-ins can mix extra render-relevant state into AE's **internal GUID for the cached frame** when that state is not otherwise represented by normal parameters/inputs.

Separately, AEGP Render Suite exposes `AEGP_GetReceiptGuid()` for a rendered-frame receipt. `PF_State` is documented as an opaque receipt for effect parameter/input state and is explicitly said to be used by AE's internal frame caching database.

These are distinct public surfaces and should not yet be assumed to share one GUID/hash implementation.

## Important historical failure
AE 13.5.0 could emit an internal verification failure when an effect advertised `I_MIX_GUID_DEPENDENCIES` but failed to call the mix-in path during PreRender. Adobe fixed cases involving multiple effect copies in 13.5.1; RE:Vision documented the same error in production plug-ins.

## Sources
- https://ae-plugins.docsforadobe.dev/intro/whats-new/
- https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
- https://ae-plugins.docsforadobe.dev/effect-details/parameter-supervision/
- https://revisionfx.com/faq/cc_2015/
