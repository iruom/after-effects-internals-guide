---
status: active
last_verified: 2026-09-14
---
# PICA / Sweet Pea Runtime Architecture

The distributed AE 25.6 SDK includes `SPRuntme.h`, which contains extensive `INTERNAL DOCS` describing the Sweet Pea/PICA host runtime. Treat this as primary distributed-header evidence, not as proof that every implementation detail is unchanged in current AE.

## Host/runtime split
PICA receives an `SPHostProcs` table from the host at initialization. That table includes host-provided external and internal allocators, startup/shutdown notification, assert/throw/debug traps, string-pool hooks, event filtering, plug-in list overrides, plug-in startup overrides, native plug-in access, and platform-specific link resolution / low-memory behavior.

The header explicitly distinguishes memory used by plug-ins from memory used by Sweet Pea itself. This implies that runtime infrastructure and client plug-ins can be accounted/allocated through separate policies.

## Global runtime registries
`SPRuntimeSuite` exposes references to the global string pool, suite list, file list, plug-in list, adapter list, host-proc table, plug-in folder and host executable. The runtime therefore has explicit registry objects rather than suite acquisition being a purely magical host callback.

## Lazy startup and plug-in caching
The internal comments describe a host override path where startup of an SP2 plug-in can be intercepted, cacheable PiPL information can be registered, and actual plug-in startup can be delayed until first use. This is a direct architectural clue for Adobe plug-in discovery/startup caching.

## Research implications
AEIG should model plug-in discovery, PiPL parsing, adapter selection, suite publication/acquisition, lazy startup and code unloading as a runtime subsystem distinct from the render graph itself.

## Plug-in access objects and code residency
`SPAccessSuite` makes code residency explicit. Acquiring a plug-in creates or increments a reference-counted `SPAccessRef`; releasing it decrements the count and allows unloading when it reaches zero. A plug-in may acquire itself to pin its code in memory.

This means a PICA plug-in object and its loaded code/access object are distinct concepts. The registry can remember metadata/globals even when the code module is unloaded.

PICA sends `Reload` before a plug-in is used after loading and `Unload` before code removal. The access message distinguishes startup, runtime reload, normal shutdown and terminal shutdown while references are still outstanding.

A plug-in exporting suites is expected to replace its function pointers with the permanent `SPBasicSuite::Undefined()` stub while unloaded and restore them on reload. That is a deliberate stale-function-pointer guard.
## Plug-in registry state
`SPPluginsSuite` exposes more than file/name lookup. A plug-in object carries property lists/PiPL-derived metadata, adapter identity and adapter-private data, host-private data, a `started` state, a `broken` state, shutdown behavior and a pointer to globals that PICA stores while the code module is unloaded.

`FindPluginProperty()` is lazy: if a property is absent, PICA can ask the plug-in to acquire/create it and then caches the result, including a null result. Property discovery is therefore potentially active and memoized rather than a passive read of static PiPL data.

The `broken` state is especially useful for failure modeling: the runtime has a first-class representation for a discovered plug-in that exists in the registry but has become unavailable because of an error condition.

## Adapter architecture
`SPAdaptersSuite` explicitly describes adapters as protocol translators between PICA and non-PICA plug-ins. An adapter scans the runtime file list, adds supported plug-ins to the global plug-in list, loads/calls them, and translates messages, data structures or API elements as needed.
PICA always has internal adapters for PICA itself and for the host application. The header explicitly says these internal adapters translate legacy function calls into currently supported PICA/application calls. That is direct evidence for a compatibility-translation layer inside the Adobe plug-in runtime.

Older first-generation adapter messages such as `Acquire Suite`/`Release Suite` are marked deprecated-but-internal, while newer adapters are expected to route most work through a generic `Send message` selector. This shows an architectural shift from many protocol-specific entry points toward a narrower message bridge.

## Runtime cache taxonomy
Do not confuse PICA code residency with image/frame caches. `SPCachesSuite` manages *loaded plug-ins* as memory-cache objects: PICA keeps plug-ins loaded, can flush unused ones, and lets adapters participate in deciding which modules to unload. `PF_CacheOnLoadSuite` adds another host-facing policy about whether an effect needs to be loaded from disk on every startup.

AEIG therefore distinguishes at least: code/module residency cache, suite/access reference lifetime, frame/result caches, compute caches, media caches and disk-persistent caches.

## Developer lesson
A robust plug-in host should separate metadata discovery, code loading, interface publication, resource context and instance state. PICA does this imperfectly but explicitly enough that many modern plugin-host design problems can be studied directly in the shipped headers.## Three distinct lifetime domains
SweetPea exposes at least three independently managed lifetimes:

1. **Code/module residency** — controlled by `SPAccessRef`, plug-in load/unload and `SPCachesSuite`.
2. **Suite publication/acquisition** — controlled by suite acquire counts and the provider's procedure table.
3. **Metadata/property lifetime** — controlled by property-list ownership, property refcounts and startup metadata caching.

Conflating these layers is a common source of stale-pointer reasoning errors. A plug-in's code can be unloadable even while a persistent plug-in metadata object still exists in PICA's registry.
## Module cache pressure
`SPCachesSuite` documents the default policy: PICA keeps loaded plug-ins resident until the application heap is filled, then unloads unused plug-ins. Hosts/adapters may trigger earlier flushing through `SPFlushCaches()`.

The adapter receives a flush callback and decides which managed plug-ins to unload. Therefore residency policy is not a single global LRU implementation exposed to clients; it is mediated by the adapter layer.

## Protective unload semantics
A suite-exporting plug-in is expected to replace exported procedure pointers with `SPBasicSuite::Undefined` before unload, then restore them on reload. This converts some stale-procedure use-after-unload failures into a defined error path.

### Diagnostic consequence
A crash in a suite function pointer is not necessarily a normal object-lifetime bug. It may indicate an Acquire/Release imbalance, a provider unloaded without replacing procedures, or code retaining a raw function table beyond its legal lifetime.
