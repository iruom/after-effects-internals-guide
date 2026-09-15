---
status: active
last_verified: 2026-09-15
---
# Capability Recipes

This section starts from **what a plug-in wants to do**, not from which suite happens to contain a function.

Every recipe separates:
1. supported/public route;
2. minimum AE version and host scope;
3. valid execution context and lifetime;
4. dependency/cache consequences;
5. older-version fallback;
6. internal evidence that explains the feature;
7. shortcuts that are visible internally but are not safe contracts.

The machine source is `datasets/ae-plugin-capability-frontier.csv`. Runtime-internal exports are observation evidence unless a separate experiment proves a safe callable contract.

## Quick decision table

| Goal | Preferred route | Earliest mapped route | Status |
|---|---|---:|---|
| Render only part of an effect stack | `AEGP_StreamSuite7` stage (26.5) or LayerRenderOptions upstream/downstream | legacy LayerRenderOptions | supported/versioned |
| Continue/check a partial Artisan result | Canvas render receipts | AE 7-era prefix receipts | experimental semantics |
| Add non-parameter state to SmartFX cache identity | `GuidMixInPtr` + `PF_OutFlag2_I_MIX_GUID_DEPENDENCIES` | SmartFX era | supported/specialized |
| Ask whether an old render request is sufficient | `AEGP_IsRenderedFrameSufficient` | Render Options Suite lineage | supported |
| Create host-compatible hash/GUID state | `AEGP_HashSuite1` | 17.5.1-era frozen API | supported |
| Keep UI/automation outside render callbacks | ExtendScript / CEP plane | CEP era | supported extension plane |
| Observe RG/cache internals | Trace/Debug/exports, not private calls | current installed runtime | observe-only |
| Access BEE VectorArt or MediaCore internals directly | no supported route | internal-only | do not call by default |
| Use generic third-party UXP in AE | no current established contract | shared runtime exists | unknown/current |
