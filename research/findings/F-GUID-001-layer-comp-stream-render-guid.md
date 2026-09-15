---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Render GUID computation exists at stream, layer, and composition levels

## Local evidence
Observed symbols include `TDB_Stream::GetRenderGuid`, `TDB_NamedStreamGroup::GetRenderGuid`, `TDB_IndexedStreamGroup::GetRenderGuid`, `BEE_VectorStream::VectorStreamGroup::GetRenderGuid`, `BEE_AVLayer::GetRenderGuidWithRO`, and `BEE_CompItem::GetRenderGuidWithRO`.

## Interpretation
Render identity is assembled hierarchically from stream/property state upward into layer and composition identities. This directly supports a structural-fingerprint model rather than a single opaque project-wide dirty bit.

## Important caveat
The exact GUID composition algorithm and the meaning of `RO` are unknown. Do not equate these GUIDs automatically with every public AEGP receipt/GUID type.

## Research target
Change individual properties, groups, layer topology, track mattes and comp settings while collecting `MixHashGuid` and render activity.