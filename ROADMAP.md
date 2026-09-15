---
status: active
last_verified: 2026-09-15
target: AEIG-1.0
---
# AEIG Roadmap

## North-star goal
AEIG 1.0 is a versioned, evidence-graded reconstruction of After Effects as a complete software system. It does **not** claim access to Adobe source code. Its success criterion is predictive power: the model should explain and predict cache invalidation, render differences, ABI/compatibility failures, persistence behavior, temporal dependencies, threading hazards and important performance characteristics before a specific failure is directly observed.

The final knowledge graph should connect:
`Product behavior -> persistent/project state -> streams/dependencies -> evaluation/render requests -> identity/receipts -> render graph/work queues -> CPU/GPU/media execution -> caches/output`, with UI, scripting, plug-in APIs, files and diagnostics mapped as observation surfaces around that core.

## AEIG 1.0 definition of done
- Every domain in `datasets/aeig-domain-coverage.csv` is at least **L2 Contract-mapped**; no major visible AE subsystem remains only a placeholder.
- Core domains (evaluation, render-graph, cache, state/identity, plug-in host, observability) reach **L5 Experiment-backed** or higher.
- Temporal, image/ROI, expressions, MFR/threading, persistence, GPU/3D, color, text/vector and media reach at least **L3 Modelled**, with the most consequential paths at L4/L5.
- Important ABI and architecture transitions are mapped across multiple AE generations, not only the installed version.
- Major claims have explicit evidence class, version scope, contradictions and a falsification route.
- Reproducible datasets/probes exist for suite ABI, runtime-symbol archaeology, AEP/AEPX diffs, cache/identity experiments and trace/log capture.
- **API/Capability completeness gate:** every discoverable public, distributed-header-only, historical/deprecated, runtime-internal, diagnostic/hidden and cross-host API surface is inventoried with version/evidence scope; absence is recorded explicitly rather than silently omitted.
- API names are not treated as capabilities by themselves: host/context/thread/ownership/dependency/cache-safety constraints are mapped so AEIG can answer not only "does an API exist?" but "can this operation actually be done safely in this execution context?"
- At least several documented cases demonstrate a prediction made from AEIG and then confirmed by experiment, regression report or another independent evidence source.

## Milestone A — Atlas closure
Goal: eliminate blind spots before over-optimizing the render core.

1. Raise every L1 domain to L2: UI shell, audio, media, tracking, headless, interop, memory and remaining product domains.
2. Keep `product-system-atlas.md` bidirectional: visible feature -> internal domains, and subsystem -> affected product features.
3. Maintain a current Guide/Header gap matrix and installed-module inventory.
4. Add machine audits for Finding IDs, stale frontmatter, orphan docs, uncovered domains and broken cross-links.

**Exit condition:** no major product surface lacks an AEIG page, evidence route and concrete next experiment.

## Milestone B — Deep-core reconstruction
Priority chain:
`Evaluation -> Render Graph -> Cache -> State/Identity -> Temporal -> Image/ROI -> Expressions -> MFR/Threading -> GPU/3D -> Persistence`.

For each subsystem, reconstruct request identity, dependency registration, materialization, lifetime/residency, invalidation and version lineage. Continue adversarial ABI work against current Guide, distributed/old headers, Adobe samples, real plug-in requests, runtime artifacts and independent reimplementations.

High-value unresolved seams include render-receipt partial validity, StreamSuite7/effect-prefix lineage, PF_State-to-render-GUID boundaries, BEE/RG cache-node behavior, Object Matte/FastMask persistence, and exact suite-version negotiation.

**Exit condition:** the main render/evaluation model is internally consistent and supported by at least two independent evidence classes per core claim, with controlled experiments for unresolved alternatives.

## Milestone C — AE Observatory
Build controlled probes rather than relying on anecdotes: cache invalidation, temporal footprint, ROI/bounds, transform sampling, motion blur, alpha/numerics, CPU/GPU parity, sequence lifetime, undo identity, disk persistence, font/text identity, color conversion and headless determinism.

Prefer small orthogonal fixtures whose outputs can be hashed/diffed automatically. Preserve fixtures, environment metadata and raw outputs so results survive future AE releases.

**Exit condition:** key architecture claims can be reproduced or falsified from the repository without manual reverse-engineering each time.

## Milestone D — Version archaeology
Map when contracts and hidden requirements enter AE: suite generations/PICA integers, render receipts, SmartFX, disk playback/cache eras, CC2015 architecture changes, MFR, modern 3D, ML analysis and current 26.x surfaces.

Treat removed APIs and old headers as evidence of still-existing compatibility substrate. Record semantic drift separately from ABI drift.

**Exit condition:** important current behavior can be explained through a lineage, not only a snapshot.

## Milestone E — Predictive AEIG 1.0
Turn the reconstructed architecture into explicit invariants and predictions. Examples: which edit must invalidate which identity, which suite alias is unsafe, when a partial result can satisfy/continue a request, which state may be thread-local versus shared, and where CPU/GPU/color/media paths can diverge.

Maintain a prediction log: `model -> expected observation -> test/evidence -> confirmed/refuted -> model revision`.

**Exit condition:** AEIG has multiple successful out-of-sample predictions and clearly marks the remaining unknown frontier.

## Continuous workstreams
- **Public/current:** monitor Guide/release/fixed-issue changes and keep 26.x surfaces separated from local 25.6 headers.
- **SDK archaeology:** continuously mine comments, deprecated headers, samples, build artifacts and Premiere parallels.
- **Runtime archaeology:** inventory DLL exports/imports/dependencies, debug/trace databases, preferences, logs and crash symbols.
- **Persistence:** grow AEP/AEPX/FFX synthetic differential corpora.
- **Independent implementations:** use host emulators/parsers as adversarial specifications; catalogue semantic-success stubs and ABI aliases.
- **Repository quality:** unique Finding IDs, evidence/version frontmatter, reproducible probes, generated datasets and cross-links.

## Near-term queue
1. Execute the canonical `experiments/user-run/AEIG-1.0-L5` package once in a disposable full-host session; capture Receipt A/B, 1536 suite negotiations, RG/BEE/TDB/GUID traces, render-output delta and Scripting Reflection.
2. Promote `state-identity`, `cache`, `render-graph`, and `plugin-host` from L4 to L5 only if the raw captures satisfy their falsifiable acceptance gates.
3. Convert successful/failed user-run observations into Findings, prediction-log entries and version-scoped capability recipes.
4. Keep API completeness at zero unclassified surface gaps and zero unreviewed Guide/Header relation rows as new Guide/SDK releases arrive.
5. Continue historical SDK recovery for the 11.x -> 23.x gap and separate ABI drift, semantic drift and documentation drift.
6. Expand AEP/AEPX/FFX differential fixtures and persistence identity experiments beyond the 1.0 minimum.
7. After all 27 domain targets are met, run a repository-wide release audit: Findings, manifests, datasets, links, corpus hashes, prediction log and capability frontier.

This roadmap is deliberately evidence-driven: milestones advance when the model becomes more falsifiable and predictive, not when a predetermined number of pages has been written.
