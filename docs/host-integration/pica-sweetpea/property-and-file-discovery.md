---
status: active
last_verified: 2026-09-14
---
# PICA Property and File Discovery

PICA does not discover plug-ins by repeatedly walking directories and reparsing resources on demand. The distributed SweetPea headers expose an explicit startup file index plus cacheable metadata objects.

## Runtime file index
`SPFilesSuite` documents a global file list created at application startup. It contains files found in the application plug-in folder, including resolved aliases. Adapters and support-file consumers are explicitly told to use this list instead of rescanning platform directories.

This separates **filesystem discovery** from **plug-in classification**. A file object can exist in the global list before it is marked as a plug-in.

## Property lists
`SPPropertiesSuite` models plug-in metadata as one or more property-list objects. A property is identified by `(vendorID, propertyKey, propertyID)` and stores a value, reference count, cacheable flag and provenance information.
## Cacheable startup metadata
A property can be marked `cacheable` when it does not change between sessions. The header states that such properties may be cached by the application in the startup preferences file. This is a direct clue that PICA startup optimization includes persisted metadata, not only in-memory plug-in state.

## Lazy property acquisition
If a requested property is absent, `SPPluginsSuite::FindPluginProperty()` may send the target plug-in an `SP Properties / Acquire` message. The plug-in may synthesize the property dynamically; PICA then stores either the returned value or a null result in the list.

This is effectively lazy metadata materialization with negative-result caching.

## Multiple property lists
Version 3 explicitly supports chains of property lists. `FindProperty()` searches through the chain while `FindPropertyLocal()` restricts lookup to one list. The chain may represent layered metadata origins or compatibility overlays; the exact host use must be experimentally verified.
## Versioned file-spec migration
`SPFilesSuite` preserves both older platform file-spec structs and the newer `XPlatFileSpec`, together with conversion helpers. The header even contains compatibility code for Photoshop-platform macros. This is a strong example of Adobe-wide substrate evolution being absorbed without breaking old plug-in ABI.

## Developer tips
- Treat PiPL/property discovery as a metadata database, not as repeated filesystem probing.
- If implementing an analogous host, persist only metadata whose semantic validity is stable across sessions; stale property caches can prevent updated plug-in capabilities from being discovered.
- Keep provenance: resource-derived and plug-in-generated properties are distinguishable in PICA.
- Cache a missing property deliberately only when absence is stable; PICA's behavior shows why negative-cache invalidation matters.

## AEIG research direction
Compare PICA startup metadata with AE `Plugin Loading.log`, startup preferences, effect registration, PiPL caches and `PF_CacheOnLoadSuite`. Determine which parts of modern AE still reuse this SweetPea substrate directly.

## Startup-cache failure modes
Persistent/cacheable metadata is valuable only if the invalidation key includes every fact that changes the property. Plug-in binary replacement, resource changes, host/architecture differences or feature-license state can make previously cached metadata stale.

Negative caching is equally risky: once an absent property is cached as null, a later installation/update can remain invisible unless the file/property cache is invalidated correctly.

A host emulator that rescans directories every query may appear functionally correct but miss the real lifecycle semantics around startup indexing, aliases and lazy property acquisition.

## Controlled discovery experiments
Use a disposable plug-in with one static PiPL-like property and one lazily generated property. Launch cold, request each property, restart warm, then modify only the plug-in resource/property version. Observe Plugin Loading logs, startup preference/cache files and Acquire messages.

Repeat for a missing property that becomes available after plug-in update. This isolates negative-cache invalidation from ordinary positive metadata caching.

## Ownership and lifetime questions
Property reference counts, file objects and plug-in module lifetime are separate. A cached property may outlive one module load while still being associated with a startup file/plugin record. Do not retain pointers into temporary resource data as if the PICA property database owned those bytes forever.

## Unknown frontier
Unresolved in modern AE: exact SweetPea/PICA startup cache file/schema still used by the host; which metadata classes are persisted versus rebuilt; invalidation key for binary/resource changes; interaction with signed plug-in bundles and architecture variants; degree to which newer AE-specific plug-in discovery bypasses or layers on the legacy substrate.

Related: `docs/host-integration/pica-sweetpea/plugin-runtime-cache.md`, `docs/capability-recipes/suite-version-negotiation.md`, `docs/observability/logging.md`, `F-PICA-004-cacheable-property-metadata.md`.
