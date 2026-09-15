---
status: strong-cross-source
last_verified: 2026-09-15
evidence: E0-G + E2-R
---
# F-TEXT-001 — Text properties persist through the same Match Name property tree model

The public scripting reference exposes `ADBE Text Properties` as the Text-layer property root, with `ADBE Text Document`, path options, animators, selectors, and animator properties below it.

Independently, `aftereffects-aep-parser` snapshot `cdc61856c1dbe035f5a6754c61864a30cd3756b6` reconstructs the layer's `tdgp` tree and looks up the literal Match Name `ADBE Text Properties`; if found, it parses that node through the same generic property parser used for `ADBE Effect Parade`.

## Interpretation
At least part of text-layer persistence is integrated into AE's general hierarchical property model rather than being stored only in a completely separate text-specific object graph.

This does not prove the entire `TextDocument` payload is represented as ordinary scalar properties. Complex text/style data may still live in opaque or specialized payloads beneath the tree node.

## Next probe
Create one-variable AEP mutations for source text, paragraph/point text, font/style runs, animator selectors, and text-on-path. Diff `tdgp/tdmn` paths and opaque payload chunks separately.
