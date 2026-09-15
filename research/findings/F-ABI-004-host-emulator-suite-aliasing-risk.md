---
status: confirmed-as-reimplementation-risk
last_verified: 2026-09-15
evidence: E0-H + E2-R
---
# F-ABI-004 — Host emulators must not assume arbitrary Suite versions are aliases

Independent hosts often simplify PICA by returning one modern vtable for multiple requested versions. Adobe's distributed headers show this is unsafe unless each version family has been audited.

`PFAppSuite4` (PICA version 6) has 11 entries. `PFAppSuite5` (PICA version 7) inserts `PF_AppGetLanguage` at index 2, shifting every later slot. `PFAppSuite6` is a prefix extension of Suite5, but its published numeric version is reset to 1.

`PF_ParamUtilsSuite1` and Suite3 are also not prefix-compatible: obsolete state-change calls are replaced by the modern `PF_State` model, and the table shrinks from ten functions to nine.

## Reimplementation consequence
A host must dispatch on both Suite name and exact published version semantics. Returning a newer table for an older request can call the wrong function pointer even when every individual callback is valid.

## Independent-host comparison
AexExecutor ignored the requested version for several AEGP suites. `aexlo` is stricter, but still aliases selected version ranges when its authors believe the family is append-only. Each such alias must be checked against Adobe headers rather than trusted as a general PICA rule.
