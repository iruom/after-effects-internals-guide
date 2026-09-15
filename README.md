# After Effects Internals Guide (AEIG)

Unofficial research guide to **Adobe After Effects as a complete software system**: product behavior, internal architecture, runtime semantics, rendering, state, media, UI, persistence, observability, compatibility and implementation archaeology.

AEIG is organized from the *inside of After Effects outward*, but remains bidirectionally mapped to the visible product. C++ SDK, Scripting, Expressions, AEGP, AEIO, Artisans, UXP/CEP, command-line interfaces, logs, preferences and file formats are observation/integration surfaces—not the primary ontology.

## North-star target — AEIG 1.0
AEIG 1.0 is reached when the reconstruction is **predictive**, not merely descriptive. It should let us derive which edits invalidate which state, why a render/cache/ABI/persistence failure occurs, where CPU/GPU/media paths diverge, and which observations would falsify the model—without pretending to possess Adobe private source code.

The target architecture connects:
`Product behavior -> persistent state -> streams/dependencies -> evaluation/render requests -> identity/receipts -> render graph/work queues -> CPU/GPU/media execution -> caches/output`.

Detailed exit conditions and milestones live in `ROADMAP.md`. Machine-generated current progress lives in `docs/reference/roadmap-status.md`.

## Core rule
Every claim must be classified as official contract, distributed implementation artifact, locally observed artifact, reproducible experiment, independently inspectable reimplementation, third-party evidence, or explicit hypothesis.

## Coverage model
Every major domain is tracked across five axes: **Product Surface -> Internal Domain -> Evidence Surface -> Experiment -> Version Lineage**. See `docs/foundations/scope-and-coverage-model.md` and `datasets/aeig-domain-coverage.csv`.
As of 2026-09-15, **23/27** tracked domains meet the AEIG 1.0 minimum. Distribution: L2=7, L3=11, L4=7, L5=2. All L1 blind spots are closed; the remaining minimum-target gaps are `state-identity`, `cache`, `render-graph`, and `plugin-host`, each at L4 -> L5.

The C++ API Atlas currently contains **5,023 identifiers** with **0 surface-classification gaps** and **0 unreviewed Guide/Header relation rows**. Documentation aliases, stale signatures, cross-host-only entries, historical removals and header-only contracts are retained as distinct classes rather than forced into one API list.

## Current priorities
1. Run the canonical `experiments/user-run/AEIG-1.0-L5` package once in a disposable full AE session to close the four remaining core L5 gates.
2. Correlate effect-prefix receipts with BEE/TDB/MixHashGuid/RG traces before promoting state/cache claims.
3. Complete runtime Scripting Reflection differential from the same user-run capture.
4. Continue historical SDK recovery between CS6 and 23.x and preserve ABI/semantic drift separately.
5. Expand AEP/AEPX/FFX synthetic differential corpora and prediction tests beyond the 1.0 minimum.

## Completeness is corpus-scoped
"Complete" means complete against the explicitly hashed/scanned corpora in `datasets/aeig-corpus-coverage-manifest.csv`, with missing private/non-distributed material recorded as an unknown frontier. Runtime exports are not silently promoted to supported APIs, and Guide spelling is not silently promoted to ABI.
