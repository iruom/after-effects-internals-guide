---
status: active
last_verified: 2026-09-16
evidence: current PF outflag contracts + 13.5 render-state changes + SmartFX/cache guidance
---
# Performance Contracts and Escape Hatches

Many Effect API flags are semantic promises to the host. AE uses them to decide how much input to materialize, whether caches remain valid, what context fields matter and which optimization paths are legal.

A false promise can produce wrong pixels or crashes; an unnecessarily conservative promise can destroy reuse and parallelism.

## `PF_OutFlag_PIX_INDEPENDENT`
Declares that output pixels do not depend on neighboring input pixels. Adobe notes this can produce dramatic performance improvements because AE may restrict work to relevant pixels/fields.

It also changes assumptions elsewhere: some `PF_InData` fields and extent behavior are meaningful only with the declaration. Do not set it for blurs, convolutions, resampling or any effect whose output neighborhood depends on surrounding input.

## Empty-pixel trimming
`PF_OutFlag2_DOESNT_NEED_EMPTY_PIXELS` allows AE to trim transparent input regions. Combined with buffer expansion, a completely empty input can arrive as a **null input buffer**; the effect must handle that case.

`PF_OutFlag2_REVEALS_ZERO_ALPHA` changes what “empty” means because hidden RGB under zero alpha may become visible. These flags are therefore image-semantics declarations, not cosmetic optimizations.## Writable input and buffer expansion
`PF_OutFlag_I_WRITE_INPUT_BUFFER` can save an allocation by permitting input mutation, but Adobe explicitly notes that it invalidates pipeline caching optimizations. Prefer a dedicated temporary world unless profiling shows the allocation dominates and the cache trade-off is acceptable.

`PF_OutFlag_I_EXPAND_BUFFER` is another expensive legacy declaration; the Guide warns that it drastically reduces caching efficiency. Modern SmartFX should express bounds through PreRender/result rectangles rather than using old broad buffer-expansion semantics where possible.

## `PF_OutFlag_FORCE_RERENDER`
Forced rerender is a compatibility escape hatch, not a preferred dependency model. Since the 13.5 UI/render project split it can also trigger synchronization of sequence state into the render-side clone.

Adobe recommends precise semantic mechanisms such as `GuidMixInPtr()`, arbitrary-data change signaling or `PF_ChangeFlag_CHANGED_VALUE` where applicable. Those preserve identity so an Undo can return to a previously cached state; blind invalidation destroys that opportunity.

Historical caveat: Guide notes around AE 14.0 document a case where `PF_ChangeFlag_CHANGED_VALUE` for layer/path parameters did not trigger rerender and recommended setting the value through `AEGP_StreamSuite` instead. Such notes must remain version-scoped, not generalized forever.

## Other dependency declarations
`I_USE_SHUTTER_ANGLE`, audio-use flags, external-dependency flags, wide-time declarations, mask dependencies and SmartFX GUID mixing tell AE about inputs it cannot safely infer from ordinary parameter values alone.

Missing one can create stale reuse. Setting one unnecessarily can broaden dependency footprints and reduce cache hits.## Optimization workflow
First make the effect correct with full inputs and conservative identity. Then profile and tighten one contract at a time: pixel independence, temporal footprint, transparent-region handling, output bounds, GPU feasibility and shared derived computation.

For every optimization record callback count, input/output extents, checkout footprint, cache-hit behavior, peak memory and output hashes. Performance gains are invalid if they silently change semantics under masks, zero-alpha RGB, downsampling, fields, motion blur or Undo/Redo.

## Failure modes
Common failures are overclaiming pixel independence, dereferencing a null trimmed input, depending on input mutation that the host/caches do not expect, using FORCE_RERENDER to hide missing identity dependencies, and carrying legacy flags into SmartFX where the modern contract supersedes them.

## Unknowns
Public flags define what AE *may* optimize, not the exact internal heuristic chosen by every host version. BEE/RG traces can test whether a declaration changes graph/cache behavior, but an observed optimization is not itself a permanent API promise.

Cross-links: `../../image-pipeline/alpha-zero-rgb.md`, `../../evaluation/dirty-invalidation.md`, `../../render-graph/frame-checkout.md`, `../../mfr/state-ownership.md`, and `sample-pitfalls.md`.