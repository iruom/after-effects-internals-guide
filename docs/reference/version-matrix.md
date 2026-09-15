---
status: active
last_verified: 2026-09-15
---
# Version Matrix

AEIG records **first observed / documented evidence**, not assumed introduction dates. `≤` means the concept is proven to exist by that version and may be older.

| Era/version | Confirmed or strongly grounded transition | Evidence route |
|---|---|---|
| AE 9.0-era | SmartFX/time-cache and sequence-data compatibility preferences already present | preserved local prefs |
| AE 11 / CS6 | `MixHashGuid` trace vocabulary present; Global Performance Cache era | local Trace DB + Adobe docs |
| AE 12 | `AEGP_CompSuite10` frozen; PICA integer 21 | distributed Old Header |
| AE 13.5 / CC 2015 | major threading architecture; render thread uses local project copy; flattened sequence-data sync changes | SDK historical notes / Adobe material |
| AE 16.x | modern JavaScript expression engine era; `DEPTHAA` header annotation since 16.0 | expression docs + distributed header |
| 2021 SDK / AE 22 | Multi-Frame Rendering contract; render-time sequence-data ownership changes | SDK Guide/header |
| AE 23.x | modern `BEE_*`, `RenderNode.RG_*`, RenderTask traces observed in retained local trace DBs | local Trace DB lineage |
| AE 24.0 | `AEGP_CompSuite12` frozen with PICA integer 26 | 25.6 distributed header |
| AE 25.2 | Preview/Playback from Disk era; retained preference and public performance documentation | prefs + Adobe/Puget evidence |
| AE 26.0 | lossless compressed disk-cached frame playback generation | Adobe docs / known issues |
| AE 26.3 | Advanced 3D in-engine DOF; SVG/Illustrator native shape paste; updated Mask Tracker | current product docs |
| AE 26.5 | GuideSuite1/2, ItemViewSuite2 guide controls, CompSuite13 parametric mesh creation, StreamSuite7 layer-param render stage | current SDK Guide |
| AE 26.5 | Object Matte propagated result disk caching; Effect Controls modernization | current product docs |

## Reading the matrix correctly
A row is an evidence lower bound, not a release-note claim that the subsystem first appeared there. `first_seen=23.4` in a retained Debug Database means only that the current local corpus proves presence by 23.4.

Likewise, a current 26.5 Guide surface can postdate the locally retained 25.6 SDK distribution. Guide, header and installed binary evidence therefore have different clocks and must be recorded separately.

## Version-sensitive failure patterns
- same suite family, different selector/layout -> ABI mismatch;
- old project opened in a new host -> migration/view-state quirks;
- same public feature across releases -> internal cache/model/runtime may have changed;
- same debug key across versions -> concept continuity, not implementation identity;
- same effect binary under a newer host -> host scheduler/color/GPU semantics can still differ.

## Verification workflow
For every claimed transition, preserve at least one reproducible evidence route: header/SDK snapshot, Guide snapshot, binary/profile hash, fixed issue, experiment or project differential. When possible verify the version immediately before and after the claimed boundary.

Automated lineage datasets should report `first_observed`, `last_observed` and count rather than silently converting them into introduction/removal dates.

## Unknown gaps
AEIG still has weaker direct SDK/header coverage through parts of the 11.x→23.x period. Official Guide history, retained third-party SDK archives and binary/diagnostic lineage partially bridge the gap, but they do not turn missing releases into directly observed corpora.

The exact build where some private BEE/TDB/RG internals first appeared is also unknown; current retained traces provide only upper/lower observational bounds.

## Cross-links
See `docs/foundations/version-model.md`, `docs/archaeology/timeline.md`, `docs/host-integration/cpp-sdk/sdk-distribution-archaeology.md`, `docs/reference/bug-quirk-registry.md`, and `datasets/aeig-corpus-coverage-manifest.csv`.
