---
status: active
last_verified: 2026-09-14
---
# Suite Versioning and Internal Versions

The AE-distributed `SPRuntme.h` exposes an internal `SPBasicFuncStruct` whose acquire/release callbacks accept both `apiVersion` and `internalVersion`.

This is a crucial distinction: public suite ABI versioning and host/runtime-internal implementation versioning are separate dimensions in the underlying Sweet Pea model.

## Public surface
Normal clients acquire a named suite and a public version through `SPBasicSuite::AcquireSuite()`.

## Internal surface
The internal callback signature is effectively:

`AcquireSuite(suiteList, name, apiVersion, internalVersion, outSuite)`

Therefore the runtime can distinguish two implementations that present the same public API version but differ in internal representation/behavior.

## AEGP suite archaeology
The deprecated `AEGP_SuiteHandler` shipped with AE 25.6 still enumerates many historical suite generations simultaneously. Examples include CompSuite 1 and 4-12, LayerSuite 1 and 3-9, RenderSuite 1-5, CanvasSuite 5-8, multiple Stream/Keyframe/Mask/ColorSettings generations and legacy ADM hooks.

This handler is not a canonical list of current best APIs; it is valuable because it preserves an ABI compatibility cross-section.

## Cross-host comparison
The Premiere 26 copy exposes 143 accessors; the AE 25.6 copy exposes those same 143 plus 11 newer/AE-specific accessors including CompSuite12, LayerSuite9, StreamSuite6, EffectSuite5 and newer iterate/color/light/keyframe suites. No Premiere-only AEGP handler accessor was found in this comparison.

## The suite registry is introspectable
`SPSuitesSuite` can enumerate the global suite list and retrieve each suite's provider plug-in, name, public API version, internal version, procedure table and current acquire count. This is much richer than the normal `SPBasicSuite` facade.

The internal version is therefore not merely an unused parameter in `SPRuntme.h`; it is stored as suite metadata and participates in `AddSuite`, `AcquireSuite`, `ReleaseSuite` and `FindSuite`.

Conceptually:

`Suite = { provider, name, apiVersion, internalVersion, procTable, acquireCount }`

The public `SPBasicSuite::AcquireSuite(name, version)` hides the suite-list and internal-version dimensions for ordinary clients.

## Reference-count semantics
Acquiring a suite increments its reference count; releasing decrements it and permits unload at zero. This is why helper correctness matters: suite acquisition is a lifetime operation, not a free dictionary lookup.
## A concrete SDK maintenance failure
The deprecated `AEGP_SuiteHandler` warns maintainers that adding a suite requires three synchronized edits: storage member, release path and accessor. In AE 25.6, `CompSuite12`, `ItemSuite9` and `LayerSuite9` have storage/accessors but do not appear in `ReleaseAllSuites()`.

Because `AcquireSuite()` increments a PICA reference count, accessing one of those versions through this helper can leave an unmatched suite reference until process/runtime teardown. The constructor zeroes the member table, so the observed problem is not an uninitialized pointer; it is a release/lifetime imbalance.

This is a strong reason not to use the old handler as new-code infrastructure even though it remains useful as an archaeological index.

## Why the RAII replacement matters
`AEFX_SuiteScoper<T>` acquires in construction and releases in destruction. The acquisition and release metadata live in one object, eliminating the three-site synchronization failure mode.

Developer lesson: ABI registries with reference-counted acquisition should be wrapped in ownership types. Manual "remember to update N switch tables" patterns become latent leaks as APIs evolve.