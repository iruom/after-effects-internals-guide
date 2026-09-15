---
status: active
last_verified: 2026-09-15
evidence: Adobe-described 13.5 rearchitecture + SDK threading/state behavior
---
# CC 2015 / 13.5 Re-architecture

Adobe described the CC 2015 interactive-performance work as requiring a complete re-architecture. For AEIG, version 13.5 is therefore a hard boundary rather than just another feature release.

SDK behavior around this transition exposes a split between editable/UI-side state and render-side project copies/snapshots. Modern threading restrictions make that split observable from plug-in code.

A particularly strong clue is `PF_GetCurrentState()` behavior in `PF_Cmd_UPDATE_PARAMS_UI`: current headers say AE returns a randomized state in that context to avoid threading/deadlock problems. UI code is therefore deliberately prevented from synchronously relying on the real render-state query.

## Consequence
Pre-13.5 assumptions about pointer/handle longevity, sequence data and synchronous project/render access cannot be projected unchanged onto modern AE.

## Model
`editable project/UI state -> synchronization/flattening boundary -> render-side snapshot -> evaluation/render workers`.

The exact snapshot granularity remains an experiment target, but the architectural split itself is well supported.

All long-term version comparisons should mark whether evidence comes from before or after 13.5.## Concrete compatibility breaks
Adobe's 13.5 notes enumerate assumptions that stopped being safe: the render thread can no longer modify the project because it operates on its own local project copy; render-side sequence mutations no longer flow back to UI state; and UI-thread synchronous rendering should generally be avoided.

Operations that were always documented as context-restricted became stricter. Adobe specifically notes that `AEGP_RegisterWithAEGP()` outside `PF_Cmd_GLOBAL_SETUP`, which older hosts could tolerate, could now crash in 13.5.

This is a recurring AE compatibility lesson: **previous accidental tolerance is not a contract**.

## 13.5.1 audio regression evidence
The threading split also produced real regressions. Adobe documents that `AEGP_RenderNewItemSoundData()` behavior broke in 13.5 and was reworked/fixed in 13.5.1; inside `PF_Cmd_UPDATE_PARAMS_UI` it returns silence to avoid deadlock rather than performing the old synchronous behavior.

This is strong evidence that UI/render separation affected more than image rendering. Audio/materialization APIs also cross synchronization boundaries.

## New synchronization mechanisms
13.5 introduced `PF_Cmd_GET_FLATTENED_SEQUENCE_DATA` so AE could copy serialized instance state to the render project without destructively flattening the live UI copy. `PF_InFlag_PROJECT_IS_RENDER_ONLY` also lets resetup distinguish render-only instances that must treat the project as read-only.## Experiments and failure signatures
When reconstructing old plug-in behavior, test sequence-data-driven UI, click/drag invalidation, synchronous UI frame/audio access and project mutation separately. A failure only after 13.5 is evidence to inspect ownership/thread assumptions before blaming pixel code.

Record whether the effect instance is UI-capable or render-only, which selector/thread performs the operation, and whether the state was serialized before rendering.

## Unknown frontier
The SDK proves the architectural split but not the complete private snapshot implementation. Exact project-clone granularity, synchronization epochs and mapping into current BEE/TDB/RG objects remain separate runtime-research questions.

Do not back-project current MFR internals onto 13.5 merely because both use project/state separation.

## Cross-links
See `../architecture/project-vs-render-state.md`, `../mfr/state-ownership.md`, `../threading-system/overview.md`, `../ui-system/async-custom-ui-rendering.md`, and `../host-integration/cpp-sdk/state-api-evolution.md`.