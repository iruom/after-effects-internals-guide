---
status: active
last_verified: 2026-09-16
---
# Construct Host-Compatible Hash State

Use `AEGP_HashSuite1` when a public AE API asks you to construct an `AEGP_GUID`-shaped compute key. The suite gives plug-ins a host-provided hash accumulator; it does **not** mean that every internal AE render/cache GUID uses the same namespace or algorithm.

The documented Compute Cache route is:

`stable semantic seed -> AEGP_CreateHashFromPtr -> mix every result-changing input with AEGP_HashMixInPtr -> AEGP_CCComputeKey`

The `generate_key` callback must be unique within its registered Compute Cache class, and Adobe recommends making it globally unique across registered classes for future-proofing.

## What belongs in the key

Hash state that changes the computed value: normalized effect parameters, source/input identity supplied by the relevant public contract, algorithm/version selectors, color/pixel semantics when they alter results, and any explicit external dependency required by the cache class.

Do not mix raw addresses, temporary handles, allocation order, callback thread IDs or uninitialized struct padding merely because they are easy bytes to access. Those values can make a key nondeterministic across processes, machines or repeated renders without representing a semantic result change.

A useful mental rule is:

`same semantic computation -> same key; different semantic result -> different key`
## Byte-level determinism

`AEGP_HashMixInPtr` hashes the bytes you give it. That makes serialization discipline part of cache correctness.

Prefer fixed-width values and explicit canonicalization where representation can vary. Be cautious with C/C++ structs containing padding, enums whose size is compiler-dependent, floating-point NaN payloads, platform-width integers, locale-dependent strings and pointer-bearing containers. If a logical value has a canonical serialized representation, hash that representation rather than an incidental in-memory object layout.

Order also matters. Mixing `(A,B)` is not generally interchangeable with mixing `(B,A)`. Collections that are semantically unordered should be normalized before hashing; ordered effect stacks, layer lists or channel tuples should preserve meaningful order.

## SDK sample pitfall: `sizeof(pointer)` is not string length

The retained Adobe Compute Cache Guide sample declares `const char* hash_buffer = "Level2Histo"` and passes `sizeof(hash_buffer)` to `AEGP_CreateHashFromPtr`. In C/C++, `sizeof(hash_buffer)` is the size of the pointer, not the length of the pointed-to string.

That can still produce a deterministic seed from the first pointer-sized bytes of the string literal, so it is not automatically a cache failure. But developers should not copy the idiom when they intend to hash an entire C string. Use an explicit byte count such as the known literal size or another canonical length policy.

This is exactly the kind of SDK-example detail AEIG should preserve: sample code demonstrates an integration route, but it is not a substitute for understanding C/C++ object representation.

## Identity namespaces are separate

Do not assume an `AEGP_HashSuite1` result is bit-equivalent to SmartFX GUID dependency state, Canvas/render receipts, `PF_State`, frame receipt GUIDs, TDB stream GUIDs or internal BEE Render GUIDs.

Binary archaeology shows BEE using `MixHashGuidT<Murmur3MixerState>` and importing TDB render-GUID/value-at-time operations, but that only establishes related identity responsibilities. It does not establish a universal GUID format shared with `AEGP_HashSuite1`.
## Cache-correctness failure modes

- **under-keying:** an input that changes the result is omitted, so stale data can be reused;
- **over-keying:** irrelevant state is mixed in, destroying reuse and making the cache appear ineffective;
- **unstable representation:** padding, pointer values or nondeterministic ordering make equivalent requests hash differently;
- **version collision:** an algorithm changes while its key schema does not, allowing old/new results to share identity;
- **context omission:** result-changing host context such as format or mode is omitted when the cache class expects the plug-in to distinguish it.

When debugging, log a human-readable description of every semantic component before it is mixed. A final GUID alone tells you that two keys differ; it does not tell you **why**.

## Relationship to SmartFX and host invalidation

For SmartFX render identity, use the documented SmartFX GUID/dependency mechanism rather than assuming a generic Compute Cache hash automatically invalidates host render caches. Compute Cache keys identify entries in the registered Compute Cache class; host render identity has additional ownership and dependency rules.

Similarly, an AEGP hash is not permission to retain public handles indefinitely. Hash the stable semantic data or documented identity token, then obey the lifetime rules of the API that produced it.

## Recommended key schema

Treat the key as a versioned schema:

`class/domain tag + schema version + normalized semantic inputs + documented dependency identities`

Changing the implementation in a way that changes results should normally change the schema/version component. This makes cache invalidation intentional rather than an accidental consequence of compiler layout.

## Verification

A useful controlled test generates keys for identical inputs across repeated calls/processes, then varies exactly one semantic dimension at a time. Equivalent inputs should remain stable; each result-changing mutation should change the key; irrelevant mutations should not.

Related pages: `docs/cache-system/state-identity.md`, `docs/evaluation/bee.md`, and the Compute Cache capability recipes. Public API details remain grounded in the retained official Guide snapshot; internal identity relations remain evidence-graded and version-scoped.
