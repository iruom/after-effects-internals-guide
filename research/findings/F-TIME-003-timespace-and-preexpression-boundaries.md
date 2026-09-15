---
id: F-TIME-003
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-TIME-003 — Layer time, comp time and expression phase are explicit API boundaries

**Evidence:** E0-S / E0-H  
**Version:** AE 25.6 SDK `AEGP/ProjDumper` and Stream APIs  
**Confidence:** High

Adobe's ProjDumper requests layer in-point, duration and current time separately in `AEGP_LTimeMode_LayerTime` and `AEGP_LTimeMode_CompTime`. Stream value evaluation also takes `pre_expressionB`.

## Internal implication
AE's temporal model is not a single timeline scalar. At minimum, comp-space and layer-space time are distinct evaluation coordinates, and expression evaluation forms an explicit value-phase boundary.

A useful pipeline model is:
`comp time -> layer/source mapping -> keyframe/interpolation state -> pre-expression value -> expression -> post-expression value`.

## Next work
Add source-time, time-remap, stretch, nested comp, frame blending and motion-blur sampling to determine where each mapping occurs and which stages participate in cache identity.