---
status: active
last_verified: 2026-09-15
---
# Independent Reimplementation Triangulation

AEIG uses independent reimplementations as executable hypotheses, not authorities. Their value is that they must turn guessed contracts into concrete byte layouts, call sequences, ownership rules and fallback behavior.

## Three complementary boundaries
1. **Persistence readers/writers** observe what AE serializes (`.aep`, `.ffx`).
2. **Plug-in-side ABI clones** reproduce the structures and callbacks an effect binary expects from the SDK.
3. **Host-side emulators** attempt to load a real `.aex` and therefore expose what a host must supply for the plug-in to survive.

These boundaries should not be collapsed. Persistence layout does not prove runtime class layout; a plug-in ABI clone does not prove host implementation; a host emulator can work while simplifying behavior AE implements more richly.

## Current fixed external snapshots
- `boltframe/aftereffects-aep-parser` @ `cdc61856c1dbe035f5a6754c61864a30cd3756b6`
- `ePi5131/aex` @ `09090f34fb68cfb877cdbf3ec8db6982da1ecf8b`
- `potistudio/aexlo` @ `61bf0c1846c6eb843102ba18404d88033de46383`
- `mathi-vignesh/after-defects` @ `e89cf70b3775d689cb9df9072dfd7e6be0f410ce`

Snapshots live under `research/external-sources/` so future upstream changes can be diffed rather than silently replacing evidence.
## Promotion rule
A third-party observation is promoted only when its scope is explicit. Preferred labels are:
- **implementation fact**: what this repository actually does;
- **fixture fact**: what a supplied real file/test demonstrates;
- **cross-source agreement**: two independent implementations infer the same structure;
- **AE-confirmed behavior**: controlled AE or Adobe primary evidence agrees;
- **hypothesis**: plausible internal interpretation still awaiting falsification.

## Contradictions are first-class data
Do not normalize disagreements away. Example: an external project's README may describe one project-version field while its current parser reads a different location. Preserve both statements, identify which commit implements which assumption, and test real files.

Likewise, `aex` reproduces much of `PF_InData` and `PF_OutData`, but its current `PF_MAX_EFFECT_MSG_LEN` is 31 while the AE 25.6 distributed header defines 255. That mismatch changes `PF_OutData` layout and is evidence against treating the project as a current complete ABI specification.

## Why failures are valuable
When a host emulator needs to copy a plug-in-owned string immediately, initialize an entire checkout structure, preserve a world for callback lifetime, or wait for GPU completion before readback, each repair identifies a contract that a type declaration alone did not communicate strongly enough.
