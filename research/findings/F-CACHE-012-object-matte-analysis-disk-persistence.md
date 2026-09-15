---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G
---
# F-CACHE-012 — Object Matte has a persistent analysis-result disk cache

After Effects 26.5 documents disk caching for propagated Object Matte results. The result can survive closing and reopening the project, reducing RAM pressure and avoiding repeated propagation on long clips.

## Architectural consequence
This is evidence for a cache class whose payload is not merely a final rendered frame. The cached object represents reusable analysis/propgation state consumed later by compositing.

## Open questions
- Is the cache keyed by project/item/layer identity, source media identity, selections, model version, propagation settings, or all of them?
- Does `Freeze` alter cache admission or only semantic mutability?
- Is the store shared with normal disk cache infrastructure or implemented as a separate namespace/format?
- What invalidates the cache after source relink, trim, time-remap, interpretation, color-management, or model-version changes?

## Historical precursor
AE 2024 dictionaries contain a Beta feature named EnableFreezeCache: when Freeze is run on propagated Roto Brush spans, cached propagation results are reused to improve performance. This predates Object Matte disk persistence and shows that propagation-result reuse was already treated as a distinct optimization domain.

The 2024 evidence should not be conflated with the 26.5 cross-session Object Matte disk cache. It does, however, support a lineage from in-session propagation-result reuse toward persistent analysis-result caching.
