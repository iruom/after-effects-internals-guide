---
status: active
last_verified: 2026-09-16
evidence: Adobe project-format contract + controlled local diffs + independent parser convergence
---
# AEP Binary Project Format

Adobe identifies `.aep` as the primary binary After Effects project format. AEIG treats it as a persistent **semantic graph serialization**, not a dump of BEE/TDB/RG runtime memory.

That distinction is fundamental: an on-disk object ID, an `AEGP_*H` handle, a BEE render GUID and an RG cache node can all refer to related concepts without being the same identity namespace.

## Container evidence
Independent/community readers used by AEIG converge on a big-endian RIFF/RIFX-style container with `Egg!` form identity in the studied corpus. One retained parser exposes nested four-byte chunks/lists, big-endian sizes and even-byte padding.

Names such as `idta`, `ldta`, `tdgp`, `tdmn`, `pard` and related parser labels are **descriptive reverse-engineering names**, not proven Adobe private class names.

Treat byte layout as version-scoped serialization evidence.
## Persistent object graph
Current parser evidence supports a project graph keyed by persistent numeric item IDs. Composition/layer records reference source items by ID rather than embedding an entire source object.

That matches the conceptual split visible in AEGP and scripting:

`project item identity -> composition -> layer identity -> source-item reference`

The exact numeric type codes or packed flags used by one parser are not promoted to stable Adobe ABI without controlled mutation across versions.

## Property persistence and MatchName
The strongest cross-boundary signal is hierarchical property persistence containing stable MatchName-like strings. Retained parser work reconstructs property groups corresponding to surfaces such as `ADBE Effect Parade`, text-property groups and nested effect parameter descriptors.

This strongly supports a persistent shape of:

`item graph -> ordered layers -> property groups -> stable MatchName identity -> typed property data`

That shape converges with AEGP Dynamic Stream / Stream APIs and scripting Match Names. The convergence is important; parser-specific chunk names are not.

## Persistent state beyond visible names
The binary model also exposes project-level semantic candidates such as expression-engine selection and project bit depth in the studied corpus. Layer records contain compact attribute state whose parser mappings include guide, 3D, adjustment, collapse, shy/lock, motion blur and effect/audio/video enablement.

Every packed-bit interpretation remains version-scoped until mutation-tested.
## Controlled-mutation protocol
A field interpretation should survive more than one accidental byte delta. AEIG's preferred loop is:

1. save a minimal baseline;
2. change exactly one semantic value;
3. save again in the same AE version;
4. diff structure and payload;
5. repeat with at least one additional value;
6. reopen both projects and verify the intended semantic survived;
7. repeat across another AE generation before calling an offset/layout stable.

High-value mutations include item/layer IDs, source replacement, layer reorder, effect reorder, MatchName/property changes, keyframes, expressions, sequence data, renderer choice, bit depth and color-management state.

## Failure modes
Raw binary differences can come from timestamps, generated IDs, save normalization, chunk relocation, alignment or version-upgrade rewriting. A single changed offset is therefore weak evidence.

Copy/paste, import-project and save-as operations may remap persistent IDs while preserving higher-level semantics. Never use an observed ID as a universal object key without testing those operations.

## Relation to runtime state
AEP persistence should be read as input to later runtime construction:

`AEP semantic graph -> project/TDB state -> synchronized render-side state -> BEE identity/work -> RG execution/cache`

The serialization may preserve enough information to reconstruct a project object while omitting every transient cache/scheduler/GPU handle.

## Unknown frontier
- exact versioned schemas for many chunks and encoded payloads;
- ID remapping rules across import/copy/save-as;
- opaque effect/plug-in payload ownership and compatibility behavior;
- normalization differences across historical AE releases;
- mapping between persistent property data and runtime TDB/BEE object construction.

Cross-links: `aep-binary-model.md`, `aepx.md`, `sequence-data.md`, `../state-model/handle-lifetimes.md`, and the versioned AEP mutation corpora.