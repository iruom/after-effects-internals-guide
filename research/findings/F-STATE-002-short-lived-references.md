---
status: researched-seed
evidence_grade: E0
confidence: 0.99
versions: "current AEGP contract"
last_verified: 2026-09-14
---
# AEGP references are intentionally short-lived

## Statement
The AEGP data-type documentation warns that references to layers, streams and many other objects can be invalidated by user activity. Changes in object quantity can invalidate references; even adding a keyframe can invalidate a stream reference.

Adobe explicitly recommends acquiring information when needed and releasing/forgetting it quickly rather than caching handles between hook calls.

## Internal implication
The exposed handles behave more like transient views into mutable host-owned structures than stable object identities. This is consistent with container recreation and snapshot-oriented render state elsewhere in AE.

## Design lesson
Do not confuse handle identity with semantic object identity. A robust architecture should separate stable IDs from ephemeral views/iterators and make invalidation explicit in the type system where possible.

## Experiment
Hold references across keyframe insertion, effect insertion, group reorder, undo/redo and copy/paste while separately recording stable Item/Layer IDs and serialized project diffs.

## Source
AEGP Data Types, "Nasty, Brutish, and Short": https://ae-plugins.docsforadobe.dev/aegps/data-types/
