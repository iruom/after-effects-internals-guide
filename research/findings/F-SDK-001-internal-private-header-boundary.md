---
id: F-SDK-001
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-SDK-001 — Public headers retain an Adobe-internal extension boundary

**Evidence:** E0-H  
**Version:** AE SDK 25.6 distribution  
**Confidence:** High

`AE_HashSuite.h` and `AE_ComputeCacheSuite.h` contain `#ifdef AEGP_INTERNAL` branches that include `AE_GeneralPlug_Private.h`. The private header is not part of the distributed public surface.

## Interpretation
The public SDK and Adobe's internal AEGP build share a header boundary, with internal builds able to extend the same suite/type environment. This is direct evidence of a larger private integration surface behind the distributed contract.

It does not prove which private suites exist or that public plug-ins can access them.

## Research value
Search other distributed headers for `AEGP_INTERNAL`, `A_INTERNAL`, private includes and types whose public definitions are intentionally opaque. Compare those boundaries with crash symbols and old suite history.