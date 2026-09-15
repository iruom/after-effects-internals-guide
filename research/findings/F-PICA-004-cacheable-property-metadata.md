---
id: F-PICA-004
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-PICA-004 — PICA properties can persist as startup metadata

**Evidence:** AE 25.6 distributed `SPProps.h` and `SPPlugs.h`.

PICA properties carry a `cacheable` bit. The distributed header states that stable properties may be cached by the application in the startup preferences file. Missing properties may trigger an `SP Properties / Acquire` message to the plug-in, after which PICA stores the returned property or a null result.

## Internal implication
PICA contains a persisted metadata-discovery cache in addition to code/module caching. Plug-in discovery can therefore be separated into file enumeration, property extraction/materialization and code startup.

## Confidence
High for the PICA contract. Current AE persistence format and invalidation rules remain to be verified.
