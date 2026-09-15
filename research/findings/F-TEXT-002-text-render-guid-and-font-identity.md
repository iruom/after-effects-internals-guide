---
status: confirmed-local
last_verified: 2026-09-15
evidence: AE-2025 TXT/TDB/BEE exports
---
# F-TEXT-002 — Text has its own render-identity layer below ordinary property streams

AE 2025 `TXT.dll` exposes `TXT_Doc::GetRenderGuid`, `GetRenderSeedGuid`, `SetRenderSeedGuid`, `InvalidateRenderGuid`, and `MixInToRenderGuid`.

Font objects independently expose `TXT_Font::AddMixinContribution(...MixHashGuidT<Murmur3MixerState>...)`, so font identity/attributes can contribute to text render identity without being reduced to a simple font-name string.

`TXT_Doc` also exposes style/paragraph sheets, glyph mapping, glyph metrics/bounds, reflow state, variable-font design vectors, missing/substituted-font state, and document resources.
BEE/TDB exports separately expose `BEE_TextDocumentStreamTraits`, `BEE_TextVariableFontAxisStreamTraits`, `ValidateCacheAtTime`, and `BEE_TextLayer::GetTxtDocRenderGuid`.

## Internal implication
The strongest current model is a layered identity path:
`property/stream state -> TXT document/font/glyph semantic state -> text render GUID -> BEE layer/render identity`.

This helps explain why visually meaningful text changes can require invalidation even when the mutation originates in expression style objects, font substitution, variable-font axes or text-layout state rather than a conventional scalar stream.

The exact composition order and whether glyph-layout caches are keyed directly by the same GUID remain unproven.
