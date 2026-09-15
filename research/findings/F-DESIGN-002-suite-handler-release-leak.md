---
id: F-DESIGN-002
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-DESIGN-002 — Deprecated Suite Handler Can Leak Acquired Suites

## Status
Confirmed from the distributed After Effects 25.6 SDK source.

## Evidence
`Util/AEGP_SuiteHandler.h` explicitly instructs maintainers to update three places when adding a suite version: member storage, `ReleaseAllSuites()`, and accessor boilerplate.

However `CompSuite12`, `ItemSuite9`, and `LayerSuite9` appear only in member declarations and accessors; none appears in `ReleaseAllSuites()`.

`SPBasicSuite::AcquireSuite()` increments a suite reference count. `ReleaseSuite()` decrements that count and unloads when it reaches zero. Therefore use of these accessors creates an acquisition/release imbalance in this deprecated helper.

The constructor zeroes the suite table with `AEFX_CLR_STRUCT`, so this is not an uninitialized-pointer bug; it is a lifetime/reference-count maintenance bug.
## Architectural lesson
The old handler encoded suite-version bookkeeping in three manually synchronized lists. The recommended `AEFX_SuiteScoper` instead couples acquisition and release in one RAII object, structurally eliminating this class of omission.

This is a useful example of SDK archaeology revealing not only host behavior but Adobe's own API-helper design evolution.

## Developer impact
Do not extend or copy the deprecated handler as a modern abstraction. Prefer scoped acquisition. If legacy code uses the new accessors repeatedly in short-lived handlers, audit suite reference counts and plug-in unload behavior.

## AEIG classification
Design debt; SDK helper defect; PICA lifetime; ABI/tooling archaeology.
