---
status: active
last_verified: 2026-09-15
---
# Mining Fixed Issues for Internal Architecture

Adobe fixed-issue notes are a valuable secondary architecture surface. A bug description often names the boundary that failed even when the corresponding implementation is private.

## Method
For every useful issue record:
1. capture exact AE version and feature combination;
2. identify the state domains that should have remained distinct;
3. map the symptom to an AEIG failure class;
4. search SDK headers, traces and historical APIs for the same internal noun;
5. formulate a falsifiable causal model rather than treating the wording as proof of implementation.

## High-value 26.x examples
- Essential Property values leaked between precomp instances in the same Advanced 3D bin with Collapse Transformations: likely identity/context isolation failure.
- Object Matte inserted spurious `Set Stream Flags` undo steps: private analysis/UI code crossed a project-stream mutation/undo boundary.
- Mask Tracker failed when comp resolution was below Full: sampling or coordinate mapping depended incorrectly on preview/downsample state.
- Advanced 3D track-matte crashes: specialized dependency topology intersected the 3D renderer path incorrectly.
- `app.purge(ALL_CACHES)` semantics were aligned with the UI and `ALL_MEMORY_CACHES` added separately: public scripting now distinguishes all-cache purge from RAM-only purge.

These records are not root-cause proofs; they are highly targeted leads for SDK/runtime experiments.

## Bug/Quirk Registry as a reverse index
AEIG now keeps a curated `research/bug-quirks.csv` and generated `datasets/aeig-bug-quirk-registry.csv`. The registry is not a substitute for Findings; it is a symptom/version/source index that points back into architecture pages and evidence.

Each entry separates observed symptom from `architecture_boundary`, because the latter is the boundary to investigate rather than a claimed root cause. This prevents a fixed-issue sentence from being silently promoted into private implementation knowledge.

Useful classes include Adobe fixed/known issues, SDK contract warnings, historical ABI bugs, preserved compatibility quirks and SDK sample pitfalls. A bug can therefore teach either product behavior or plug-in-development constraints.

## Strong mining pattern
Prefer issues where changing exactly one state domain fixes/breaks behavior: resolution, renderer, cache purge target, project reopen, expression style, effect ordering, headless path or GPU backend. These symptoms are easier to turn into falsifiable boundary hypotheses than generic crashes.

For every mined issue ask whether the failure was about identity, validity, residency, coordinate conversion, lifetime, synchronization, capability negotiation or persistence. Multiple classes may remain plausible until tested.

## Negative evidence
A later fix only proves that the user-visible symptom changed in the stated release. It does not prove the old private implementation was replaced, nor that adjacent cases are fixed. Regression tests must preserve the original reproducer and add nearby perturbations.

## Current quality gate
The release/repository audit rebuilds and validates the Bug/Quirk Registry. Missing referenced docs/findings, duplicate IDs or malformed source metadata are treated as documentation-quality failures rather than silently ignored.

Related: `docs/reference/bug-quirk-registry.md`, `docs/foundations/evidence-model.md`, `docs/foundations/version-model.md`.
