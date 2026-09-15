---
id: F-STATE-003
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-STATE-003 — Render validity is historically tracked by project timestamp plus time interval

**Evidence:** E0-L  
**Version:** AEGP Render Suite 2+, frozen from AE 6.5 lineage  
**Confidence:** High for the historical contract

Legacy Render Suite exposes a project render timestamp that increments when project changes affect rendering. `AEGP_HasItemChangedSinceTimestamp` then asks whether an item's video changed over a specific start-time/duration interval since that timestamp.

## Internal implication
Historical AE render invalidation was time-local rather than only whole-item dirty state. The API contract explicitly separates edit generation from the temporal interval whose output is being validated.

Possible abstraction:
`changed = Changed(item, [t0,t1), edit_generation)`.

## Modern relevance
Do not assume the exact data structure survives unchanged. Compare this contract with PF_State time ranges, Smart/Wide Time, current Render GUIDs, BEE cache traces and controlled edit-locality experiments.