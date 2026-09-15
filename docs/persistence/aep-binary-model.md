---
status: active
last_verified: 2026-09-15
---
# AEP Binary Model and Semantic Graph

## Scope
This chapter records reproducible structure exposed by independent AEP readers. Field names that originate in community parsers are descriptive hypotheses, not Adobe class names. Disk layout must not be equated with AE's in-memory object layout.

## Container layer
`boltframe/aftereffects-aep-parser` parses `.aep` as big-endian RIFF (`RIFX`) with form type `Egg!`. Chunks carry four-byte tags and big-endian sizes, with LIST-like nested containers and even-byte padding.

The parser recognizes recurring chunk tags including `Utf8`, `idta`, `cdta`, `fdta`, `ldta`, `tdgp`, `tdmn`, `pard` and `parT`. Names remain provisional until independently correlated.

## Project-level state
The parser finds an `ExEn` list and exposes its first block as the project's expression-engine string. It reads a project `nhed` structure containing a bits-per-channel value and maps observed values to 8/16/32-bpc modes.

This is important because expression-engine choice and project depth are persistent semantic state, not merely transient UI preferences.

## Item graph
Items are inserted into a map keyed by a persistent numeric ID. The root folder is treated specially with ID 0; non-root `idta` records provide an item type and ID.
Observed item-type codes in this parser are `0x01` folder, `0x04` composition and `0x07` footage. These numbers are parser discoveries, not public Adobe enum values.

Folder contents are reconstructed recursively from nested `Item` lists. Composition items parse dimensions, duration, framerate, background color and an ordered set of `Layr` lists. Footage items parse source dimensions, duration/framerate and selected source-type data.

## Layer source references
Within `ldta`, the parser reads a 32-bit `SourceID`. Layer sources are therefore represented on disk as ID references into the project item graph rather than as nested source objects.

For unnamed layers the parser resolves the displayed name from `project.Items[layer.SourceID]`, which is consistent with the conceptual distinction between layer identity and source-item identity exposed by AEGP/Scripting.

`ldta` also contains compact layer attribute bits. The parser has experimentally mapped bits for sampling mode, frame blending mode, guide, solo, 3D, adjustment-layer, collapse transformations, shy, lock, motion blur, effect/audio/video enablement and related state.

These bit assignments need controlled mutation verification across AE versions before being treated as stable ABI.

## Property and MatchName tree
The strongest semantic clue is the `tdgp`/`tdmn` hierarchy. The parser pairs `tdmn` values with following nested structures and uses the strings as Match Names.
A layer root `tdgp` can contain `ADBE Effect Parade` and `ADBE Text Properties`; effect groups then expose nested match names and `pard` parameter descriptors. `pard` bytes are interpreted into property kinds such as Boolean, OneD, TwoD, ThreeD, Color, Angle, LayerSelect, Select, Group and Custom.

Effect groups (`sspc` in this implementation) can contain a human-facing effect name plus a nested property tree. A `tdsn` value is used by this parser as a user-defined property label, with `-_0_/-` treated as a no-label sentinel.

The important architectural point is not the community names `tdgp/tdmn`; it is the independently reconstructed persistence shape:

`Project Item ID graph -> Composition Layer records -> Source Item ID references -> hierarchical property groups -> stable MatchName strings -> typed property descriptors`

That shape closely resembles the semantic model exposed through AEGP Stream/Dynamic Stream and Scripting Match Names. This cross-boundary agreement raises confidence that Match Names and hierarchical stream identity are part of AE's persistent semantic contract.

## Research constraints
AEP is not a memory dump. Chunk boundaries can be serialization-specific, IDs can be remapped during import/copy, and packed flags can change meaning by version. Every inferred offset must be scoped to a corpus and AE generation.

Next experiments: one-change project mutation, copy/paste identity, reorder-only diffs, precomp source replacement, effect reorder, hidden parameter labels, expression-engine switching, BPC switching and save/open across AE 11/24/25/26-era installations.
