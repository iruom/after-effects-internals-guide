---
status: active
last_verified: 2026-09-15
evidence: local PresetEffects.xml + CS6/modern schema comparison
---
# Pseudo Effects

Local `PresetEffects.xml` is direct evidence of an internal declarative parameter-schema mechanism used by pseudo effects/preset-defined controls.

The inline DTD/schema exposes constructs such as `Effect`, `Group`, Angle, Checkbox, Popup/Popup_UTF8, Color, Layer, Point/Point3D and Slider, together with `matchname`, `external_id`, range/display metadata and flags such as `CANNOT_TIME_VARY` and `INVISIBLE`.

CS6 versus modern files show schema evolution, including newer popup/string handling, Point3D and visibility-related attributes.

## What this proves
After Effects can materialize effect-like parameter trees from a data schema that is distinct from a compiled third-party PF effect binary.

## What it does not prove
`PresetEffects.xml` is not a supported public plug-in registration API, and schema tags must not be assumed to map 1:1 onto internal C++ classes.

## Research uses
Compare one pseudo effect across AEP/AEPX/FFX, track match-name persistence, inspect parameter ordering/flags and test how schema edits affect existing saved instances in disposable projects.

This surface is especially useful for understanding persistent property identity and preset compatibility because it exposes declarative structure that normal compiled effects hide behind PF parameter setup.

Related: `docs/persistence/ffx.md`, `docs/state-model/streams-properties.md`.## Failure modes
Schema experiments can fail in several distinct ways: AE may reject malformed XML, materialize a control tree but lose compatibility with saved instances, change parameter ordering, or load an existing project with defaults that no longer match the original schema.

A successful UI appearance is not enough to prove persistence compatibility. Verify AEP/AEPX reopen, FFX application, expression/property addressing and rendered output.

## Unknown frontier
`PresetEffects.xml` demonstrates a private declarative mechanism, but AEIG does not claim it is a supported authoring API or that all pseudo-effect state is defined by this file. First-party effects may have additional compiled/native behavior and internal registration paths.

The exact mapping among `external_id`, MatchName, saved property identity and current internal stream objects remains a controlled-reconstruction target.

Cross-version schema changes should be interpreted semantically first: a new XML attribute proves vocabulary expansion, not necessarily a new underlying C++ class.

Cross-links: `ffx.md`, `aep.md`, `aepx.md`, `../state-model/streams-properties.md`, and `../host-integration/cpp-sdk/sdk-distribution-archaeology.md`.