---
status: active
last_verified: 2026-09-15
---
# Scope and Coverage Model

AEIG studies **After Effects as a complete software system**, not only the C++ plug-in SDK and not only the render engine.

The repository therefore separates five orthogonal axes:

1. **Product surface** — what users can see or invoke: compositions, layers, effects, text, shapes, trackers, 3D, previews, render queue, UI panels, scripting, import/export, preferences.
2. **Internal domain** — the subsystem believed to implement that behavior: project state, streams, evaluation, render graph, cache, media, color, GPU, memory, UI, persistence, etc.
3. **Evidence surface** — where behavior can be observed: Guide, SDK headers, samples, scripting, expressions, AEGP, AEIO, Artisans, files, logs, preferences, modules, crash reports, patents, experiments.
4. **Experiment** — a controlled test capable of separating competing models.
5. **Version lineage** — when the behavior, ABI, file representation or architecture first appears, changes, disappears or forks.

No one axis is allowed to become the repository taxonomy by itself.

## Coverage rule
A subsystem is not considered well covered merely because its public API is documented. Mature coverage requires, where applicable:
- a user-visible entry point;
- a working internal model;
- at least one primary-source contract;
- at least one independent observation path;
- explicit version boundaries;
- known contradictions and open hypotheses;
- a falsifiable experiment plan.
## Domain completeness levels
Use the following state machine instead of a vague percentage:

| Level | Meaning |
|---|---|
| L0 Unmapped | domain exists but has no AEIG page |
| L1 Surface-mapped | user features and observation surfaces identified |
| L2 Contract-mapped | primary APIs/files/contracts indexed |
| L3 Modelled | coherent internal model with confidence labels |
| L4 Triangulated | model supported by independent evidence classes |
| L5 Experiment-backed | key behaviors reproduced or falsified experimentally |
| L6 Versioned | important transitions mapped across AE generations |
| L7 Predictive | model predicts previously unseen behavior/failure cases |

## Anti-bias rules
- Public SDK structure is an observation surface, not the ontology of AE.
- File names, DLL names, trace category names and private-looking symbols are clues, not semantic proof.
- A current feature page describes product behavior, not necessarily implementation.
- A third-party reimplementation can expose hidden contracts even when it fails.
- Historical documentation is not discarded: old contracts can remain active compatibility substrate decades later.
- Negative evidence matters: a feature absent from one surface but present in another is a research lead.

## Cross-link requirement
Every mature page should eventually answer four questions: **what invokes this, what state does it consume, what does it invalidate/produce, and how can we observe it?**
