---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G 26.5
---
# F-ABI-005 窶・Older Guide accessors become lossy when new guide semantics are used

AEGP_GuideSuite2 adds percentage positioning, per-guide color, and edge pinning while retaining the older base accessors.

Adobe documents that the base getter can return a percentage-position value in its numeric position output without indicating that the value is percentage-based. Color and pinned state are likewise unavailable through the base interface.

## Compatibility lesson
Backward-compatible API availability does not imply semantic completeness. A legacy accessor may continue to succeed while silently projecting a richer state into a lossy older representation.

AEIG should treat 'call still works' and 'call can faithfully round-trip current state' as separate compatibility properties.

