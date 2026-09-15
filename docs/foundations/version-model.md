---
status: active
last_verified: 2026-09-15
---
# Version Model

AEIG records **versioned behavior**, not one timeless "After Effects internals" diagram. Public APIs, binary layouts, cache policy and extension planes evolve at different rates.

## Important eras currently mapped
- **AE 9 / CS4**: retained Debug/Trace profiles begin the local hidden-vocabulary lineage.
- **CS6 / AE 11**: historical SDK corpus provides a concrete pre-modern ABI baseline; examples include the old 32-thread ceiling and compile-time transfer-mode gates.
- **CC 2015 / AE 13.5**: SDK history describes the major render architecture split with render-side project copies/synchronization.
- **SmartFX / Global Performance Cache era**: explicit PreRender/Render separation, render-state comparison and cache-aware dependency APIs become central.
- **MFR era**: frame-level concurrency changes sequence-data/threading assumptions and resource admission.
- **23.x–25.x**: modern BEE/TDB/RG/GPU/MediaCore traces and binaries form the main local runtime archaeology corpus.
- **25.2+ disk playback transition / 26.x compressed cache era**: disk-cache policy and playback architecture change again.
- **26.5 Guide**: CompSuite13 parametric meshes, StreamSuite7 layer stage, GuideSuite and ItemViewSuite2 exceed the local 25.6 distributed headers.

## Separate version axes
Track at least: product version, **Effect API version/subversion**, **AEGP API version**, public Guide version, distributed SDK/header version, suite generation, PICA selector, binary build, host scope (AE vs Premiere), and experiment environment.

The official Guide preserves a product→Effect API→AEGP API lineage through AE 22.0, while individual suites continue to evolve through their own generation/PICA coordinates. These axes must not be collapsed into one monotonic version number.

A newer C table generation does not imply a larger PICA integer; `PFAppSuite` demonstrates a reset from selector 7 to 1.

## Archaeology rule
When an identifier disappears, classify whether the capability was removed, renamed, folded, ungated, re-scoped or had a reserved ABI value repurposed. Name absence alone is not capability absence.

Every Finding should state its version scope, and every private/runtime claim should carry the exact binary/profile generation that exposed it.

## Current release anchor
As of 2026-09-16 the current public After Effects release is 26.5 (September 2026). AEIG uses that only as a product-release anchor. It does **not** mean the locally retained 25.6 SDK, the public Guide, every suite generation and every installed binary surface are all "version 26.5" in the same sense.

## Version tuple
For precise findings record a tuple rather than one number:

`(product_version, build_number, platform/arch, host_scope, PF_API, AEGP_API, suite_name+selector, SDK/header_snapshot, Guide_snapshot, binary_hash, experiment_date)`.

Not every field applies to every observation, but omitting the relevant axis makes historical claims ambiguous.

## Compatibility versus implementation change
A stable public suite selector can survive internal rewrites. Conversely, a new suite generation can add capability without replacing old tables. A preference/debug key can persist while its implementation changes, and a private symbol can disappear because of refactoring rather than capability removal.

Therefore "same name" is not implementation identity and "new name" is not necessarily new semantics.

## Release notes and fixed issues as version evidence
Fixed/known issues provide behavioral boundary markers. Examples in 26.x include Object Matte/aerender failure, text-style cache invalidation, compressed disk-cache incompatibility, Advanced 3D render-order/crash fixes and cache-purge hangs.

These establish that a behavior differed across versions; they usually do **not** identify the exact private class or root cause. AEIG records the observed behavior first and treats architectural interpretation separately.

## Failure patterns
- gate suite use only on product version instead of acquiring the capability;
- call a private symbol from another build because the product major version matches;
- compare Debug Database keys without recording stable/beta channel and exact profile version;
- describe a historical bug as current behavior after it was fixed;
- treat a modern Help-page statement as valid for CS6-era behavior;
- infer removal when a symbol/key disappears without testing behavior.

## Version-differential experiment
Run the same minimal fixture across retained host versions with identical project/media assets. Capture public capability availability, suite acquisition matrix, output hashes, trace/debug vocabulary, module/binary hashes and performance/state behavior.

Classify each difference as: public API addition/removal, behavior change behind stable API, performance/policy change, bug/regression, renamed/private implementation, or unresolved.

## Unknown frontier
AEIG still has sparse local coverage for many releases between CS6/CC2014 and the 23.x+ retained runtime corpus. Exact first-introduction versions for many private BEE/TDB/RG concepts remain lower/upper bounds rather than precise dates.

Related: `docs/archaeology/timeline.md`, `docs/archaeology/pf-api-version-lineage.md`, `docs/reference/version-matrix.md`, `datasets/ae-debug-trace-lineage.csv`.
