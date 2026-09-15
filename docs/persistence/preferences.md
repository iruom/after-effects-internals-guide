---
status: active
last_verified: 2026-09-16
evidence: current Adobe Preferences contract + AEGP Persisto sample + retained preference/debug lineage
---
# Preferences as Versioned Persistent Runtime Configuration

After Effects preferences are not one flat user-settings file. They form a version-scoped persistent configuration domain covering visible preferences, workspaces/shortcuts, migration state, diagnostic/debug settings and private feature/runtime knobs.

Adobe's current Help places preference files under a **version-specific After Effects directory** and explicitly supports migration from a previous version when the new version has no preference folder yet.

This makes preferences useful archaeological evidence, but not an implementation specification.

## Public lifecycle boundary
Current Adobe preference management can reset all preferences to defaults and also resets workspaces and the Debug Database. Some changes require an application restart. Adobe also warns that manually editing the files can cause crashes or unexpected behavior.

The operational model is therefore broader than `key -> UI checkbox`:

`versioned profile -> migration/default materialization -> application/runtime configuration -> session behavior -> persisted update`.## AEGP PersistentData bridge
Adobe's `AEGP/Persisto` sample obtains the application's persistent-data blob and accesses a real After Effects preference key (`Main Pref Section / Pref_DEFAULT_UNLABELED_ALPHA`). This demonstrates that AEGP persistent-data APIs can cross into AE's own preference domain rather than serving only plug-in-private storage.

The sample also documents a subtle behavior: a string-get operation can materialize a default when the key is absent. A nominal **read** can therefore change persistent state.

That matters for research tooling. Presence checks, reads, writes and default creation must be distinguished instead of assuming observation is side-effect free.

## Preference classes
AEIG separates at least:
- documented user preferences;
- workspace/keyboard/UI-layout state;
- plug-in or subsystem persistent state;
- private runtime/feature gates;
- Debug/Trace database controls;
- cache/playback/GPU/resource-policy knobs;
- migration/version compatibility state.

A key name establishes that a concept existed in that build. It does not prove that changing the key is supported, that the value is read in every session, or that the name still maps to the same implementation in later versions.## Research policy
Use disposable version-specific profiles. Record raw file/hash before and after access, AE build, key section/name, stored type, observed default, whether restart is required, and whether the key survives migration.

For each candidate key test separately:
1. absent vs present;
2. read-only observation vs read that creates a default;
3. supported UI mutation vs direct file mutation;
4. session-only effect vs restart-required effect;
5. current-version behavior vs migration from an older profile.

Never promote a hidden preference into recommended production practice solely because toggling it appears to work once.

## High-value lineages
Retained profiles expose long-running vocabulary around PFC/cache policy, SmartFX temporal behavior, expression caching/engine recycling, playback-from-disk, work queues, GPU memory pools, adaptive 3D and sequence-data lifecycle. These are research leads for subsystem history, not stable APIs.

## Failure modes
Preference experiments can contaminate future measurements through persistent state. Migration can carry an old behavior into a new build. Resetting preferences can simultaneously alter workspace/debug state, making a before/after comparison multi-variable unless the profile is isolated.

Cross-links: `../observability/debug-database.md`, `../cache-system/disk-cache.md`, `../expression-engine/caching.md`, `../product-shell/overview.md`, and `../archaeology/ae9-smartfx.md`.