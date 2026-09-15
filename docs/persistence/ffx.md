---
status: active-hypothesis
last_verified: 2026-09-15
evidence: local preset/pseudo-effect schema + controlled-comparison plan
---
# FFX Preset Format

FFX is an important persistence boundary for reusable effect/property state, but AEIG does not assume that an FFX file is simply a serialized Effect Controls tree.

Local `PresetEffects.xml` proves that After Effects carries a parameter-schema vocabulary for pseudo effects/presets. The relationship between that schema, FFX payloads and ordinary plug-in parameter serialization still requires controlled mapping.

## Useful experiments
Apply the same FFX to multiple projects and versions, then compare:
- effect match names and ordering;
- parameter default/current values;
- animation/keyframe state;
- pseudo-effect schema identifiers;
- expression-bearing properties;
- hidden/invisible parameter behavior.

Use an FFX created from a one-effect baseline and vary one parameter at a time to identify stable versus incidental regions.

## Boundary rule
FFX persistence semantics should be compared with AEP/AEPX and `PresetEffects.xml`, but names/offsets from one surface must not be projected onto another without evidence.

Until its payload is reconstructed, FFX is a versioned persistence artifact rather than a supported low-level API.## Public semantic contract
Current Adobe Help confirms that an animation preset can package reusable layer-property configuration including effects, keyframes and expressions, and that `.ffx` files are transferable between computers.

That establishes **what presets can preserve**, not how those semantics are encoded internally.

A useful persistence model is therefore:

`selected property/effect state -> preset serialization -> target-layer resolution -> property/effect materialization`.

Target resolution is potentially semantic rather than offset-based: a preset must be applied into a new layer/project context where object IDs, handles and effect instances differ.

## Version and compatibility questions
Test presets across AE generations rather than assuming forward/backward identity. Distinguish “file loads”, “all properties resolve”, “expressions still reference the intended objects”, and “rendered output matches”. These are different compatibility levels.

Pseudo effects, removed/renamed effects, changed parameter schemas, localized display names and hidden properties are high-risk cases.## Failure modes
A preset can apply successfully yet bind differently because target property topology changed. Display-name-based inspection can also mislead where Match Names or hidden schema identifiers carry the stable identity.

Never edit binary regions based on one observed offset. Length changes, checksums, tables or versioned records can move unrelated data.

## Experimental reconstruction
Build a minimal corpus: one transform scalar, one animated scalar, one expression, one stock effect, one pseudo effect and one multi-effect stack. Save baseline plus one-variable mutations, then diff across versions and reapply into fresh projects.

Record semantic output after application in addition to binary diffs. A candidate field interpretation is stronger only when changing the inferred field produces the predicted property change after load.

## Unknown frontier
AEIG has not yet established a complete FFX record/container schema. Relationship to AEP property records and `PresetEffects.xml` is partially constrained by shared MatchName/property semantics but not proven byte-for-byte.

This page intentionally remains `active-hypothesis` until a repeatable parser/re-serializer or equivalent controlled format model exists.

Cross-links: `aep.md`, `aepx.md`, `pseudo-effects.md`, and `../state-model/streams-properties.md`.