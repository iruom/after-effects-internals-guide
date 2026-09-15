---
status: active
last_verified: 2026-09-14
---
# Internal Failure Model

AEIG troubleshooting should explain failures by violated internal contract rather than by symptom alone.

## Primary failure classes
1. **Identity / cache-key mismatch** — render-relevant state omitted from GUID/hash/receipt, or irrelevant state included and cache reuse collapses.
2. **Invalidation error** — dependency exists but dirty propagation or time-span tracking does not cover it.
3. **Lifetime error** — stale handle, suite pointer, world, stream reference, sequence payload or host-owned buffer outlives its valid context.
4. **Thread-affinity error** — main/UI-thread-only API is called from render/worker context, or host callback is entered while a conflicting plug-in lock is held.
5. **Snapshot divergence** — UI-project state and render-project/local-copy state disagree or synchronization is delayed/forced incorrectly.
6. **Render-context mismatch** — project-layer identity is confused with render-layer context, especially collapse, track matte, adjustment layer or nested compositions.
7. **Time-space mismatch** — comp, layer, source/media, segment or sequence time is substituted for another domain.
8. **Bounds / ROI under-request** — requested source region is insufficient for a spatial, temporal or transform dependency.
9. **Pixel semantic mismatch** — alpha/premultiplication, zero-alpha RGB, field order, color-space, bit depth or backend assumptions differ.
10. **ABI / suite-version mismatch** — wrong suite generation, old struct layout, frozen API, host-specific extension or accidental dependency on deprecated behavior.
11. **Ownership/refcount error** — host and plug-in disagree about who must dispose, retain, unregister or release a resource.
12. **Async staleness/cancellation error** — a completed result belongs to an obsolete request/state and is consumed or cached anyway.

Each troubleshooting page should identify the violated invariant, observable trace/log signature, minimal reproduction, confirmation probe, safe workaround and architectural fix.

## Triage order
Classify the failure before changing code. First ask whether the wrong semantic result was reused, the right result was invalidated too broadly, the right object was referenced after its lifetime, or the correct request was executed under the wrong context/time/backend.

Then reduce the reproducer by holding every other state axis fixed. AE bugs are often misdiagnosed because two domains change together: for example preview resolution plus tracker sampling, source layer plus render stage, or UI sequence state plus render snapshot generation.

## Observable signatures
- wrong pixels only after warm cache -> identity/invalidation suspect;
- crash after reorder/keyframe edit -> stale handle/lifetime suspect;
- UI freeze while render worker is active -> lock/thread-affinity suspect;
- fresh host passes but reused host fails -> process/global/module/cache lifetime suspect;
- CPU/GPU disagreement -> pixel/color/numeric/backend contract suspect;
- A→B→A does not recover reuse -> over-keying or hidden generation state;
- correct pixels but huge recomputation -> validity too conservative or residency/purge pressure.

## Bug Registry mapping
`datasets/aeig-bug-quirk-registry.csv` maps real Adobe issues and SDK hazards onto these boundary classes. Use it to find nearby historical failures before inventing a new causal theory.

## Confirmation standard
A failure model is promoted only after a discriminating test changes the predicted boundary while holding competing explanations fixed. Crash stacks, DLL names and fixed-issue wording are leads; they are not sufficient root-cause proof by themselves.

## Unknown frontier
Private scheduler policy, exact cache-key composition and internal object ownership remain partially opaque. In those areas, troubleshooting should end with explicit competing hypotheses and the next falsifying experiment rather than a confident narrative.

Related: `docs/foundations/evidence-model.md`, `docs/troubleshooting/fixed-issue-architecture-mining.md`, `docs/reference/bug-quirk-registry.md`, `docs/state-model/object-identity.md`, `docs/cache-system/state-identity.md`.
