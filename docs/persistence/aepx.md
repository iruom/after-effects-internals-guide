---
status: active
last_verified: 2026-09-16
evidence: Adobe Help project-type contract (2026) + controlled AEP/AEPX comparison methodology
---
# AEPX: XML Project Surface, Not a Complete Project Schema

AEPX is After Effects' text-based XML project representation. Adobe explicitly distinguishes it from the primary binary `.aep` format and recommends AEPX mainly as a saved copy / intermediate automation format rather than the canonical working representation.

That distinction matters for reverse engineering: **human-readable XML is an observation surface, not proof that every persisted semantic is represented as editable text**.

## What Adobe explicitly exposes
Current Adobe documentation says AEPX can expose editable text for at least:
- marker attributes, including comments and cue/chapter data;
- source-footage and proxy file paths;
- composition, footage, layer and folder names/comments.

But it also states that some project information remains hexadecimal-encoded binary data inside the XML document.
## Readable does not always mean authoritative
Adobe also documents an important trap: some strings such as workspace/view names are readable in AEPX but edits to those strings may not be honored when AE reopens the project.

Therefore classify each observed XML field as one of:
- editable semantic state;
- descriptive/redundant text;
- opaque or encoded payload;
- derived/defaulted value;
- compatibility/version metadata;
- currently unknown.

Do not infer write semantics from readability alone.

## Differential method
The strongest use of AEPX is paired differential analysis:

`baseline AEP/AEPX -> mutate exactly one semantic -> save both -> structural/text diff -> reload -> verify behavior`

A semantic that changes in readable AEPX **and** in a localized AEP region is substantially stronger evidence than one format alone.
## Identity rules
Names are not stable object identifiers. File paths are not media-content identity. XML ordering is not automatically render ordering. MatchName-like strings are more useful than localized display names but still must be mapped back to object/property identity experimentally.

Persistent identities observed in AEP/AEPX must also remain separate from:
- transient `AEGP_*H` handles;
- render receipts;
- BEE/TDB Render GUIDs;
- RG cache-node identity;
- GPU/media residency handles.

## Version and normalization behavior
AEPX was introduced long after the original AEP format (Adobe documents XML projects from the CS4 era onward). Save/reload may normalize ordering, generated names, defaults, whitespace and encoded payloads. A raw textual diff therefore needs semantic normalization before being treated as a format change.

## Failure modes and developer use
Useful automation targets are the fields Adobe explicitly treats as editable. Editing undocumented nodes can be ignored, normalized away, rejected on load or alter unrelated opaque state. Always validate an edit by reopening in the target AE version and comparing the resulting semantic state.

AEPX is excellent for archaeology and controlled automation; it is not a supported full-fidelity replacement for AE's project model.

## Open reconstruction targets
- map readable XML fields to AEP chunks and runtime object/property identities;
- classify every encoded payload by owning subsystem and version behavior;
- determine which default/derived values are omitted and reconstructed;
- identify normalization rules across 23.x-26.x and historical releases;
- distinguish project-semantic data from workspace/UI compatibility data.

Cross-links: `aep.md`, `aep-binary-model.md`, `sequence-data.md`, and the AEP/AEPX differential datasets.