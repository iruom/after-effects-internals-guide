---
status: active
last_verified: 2026-09-16
evidence: retained AE 25.6 Windows/macOS SDK archives + normalized header/identifier diff
---
# 25.6 Windows/macOS Header Parity

AEIG keeps **public header semantics** separate from platform packaging and runtime ABI. The retained AE 25.6 SDK archives provide a useful controlled comparison because both platform packages contain the same nominal SDK generation.

## Raw archive result
The Windows package contains 68 meaningful public headers. The macOS archive also resolves to 68 meaningful headers after excluding 68 AppleDouble `._*.h` metadata entries created by macOS archive/resource-fork packaging.

A raw byte comparison reports differences in 66/68 corresponding files. That does not mean the API differs: BOM/newline/text packaging alone is sufficient to make binary file hashes diverge.

## Normalized semantic result
After BOM/newline normalization, all 68 corresponding header texts are identical in the retained archives. A prefix-oriented identifier extraction produces 4,104 identifiers on each side with no Windows-only or macOS-only identifiers.

For AEIG's 25.6 public-header inventory, it is therefore justified to use one normalized API surface rather than duplicating thousands of rows by platform.

This is a corpus result for these retained archives, not a claim that Adobe guarantees all future platform headers to be identical.

## What header parity does not prove
Text-identical declarations do not imply identical binaries or host behavior. Platform differences can still exist in:
- calling convention and ABI details outside portable declarations;
- compiler/STL/layout assumptions in plug-in code;
- bundle/DLL loading and symbol resolution;
- resource/PiPL packaging;
- filesystem/path/Unicode behavior;
- signing, quarantine and hardened-runtime policy;
- GPU/backend and OS-framework behavior;
- sample project/build-system configuration.

Opaque handles are especially important here: identical typedefs can deliberately hide completely different private host representations.

## Build-system implication
Treat the shared header surface as one source-level contract, then maintain platform-specific build/packaging/test layers. Do not fork API wrappers merely because archive bytes differ, and do not remove platform validation merely because normalized headers match.

Cross-platform bugs should first be classified as declaration/API mismatch vs ABI/build/loader/resource/runtime mismatch. The parity dataset closes only the first class for this corpus.

## Reproduction method
The parity result should be reproducible from the retained archives: enumerate meaningful headers, remove archive metadata entries, normalize BOM/newlines for semantic text comparison, then compare identifier inventories separately from raw file hashes.

Keeping both raw and normalized results matters. Raw differences diagnose packaging/provenance; normalized equality supports one semantic surface. Collapsing those two measurements would either create false API differences or erase useful archive evidence.

## Version lineage
Repeat this test whenever a new distributed SDK or an original historical platform pair becomes available. A future platform-specific declaration is evidence worth preserving rather than normalizing away to maintain a convenient one-surface model.

## Evidence and cross-links
Datasets: `datasets/ae-sdk-25_6-platform-header-parity.csv` and `datasets/ae-sdk-25_6-platform-semantic-parity.csv`. Finding: `F-ABI-018-sdk25-windows-mac-header-parity.md`.

Related: suite ABI/versioning, SDK distribution archaeology, PiPL/resource packaging and version-model pages.

## Unknown frontier
Binary/sample/platform parity remains open. The current result establishes normalized **header** parity only; it is intentionally weaker than claiming Windows and macOS AE implement every declared contract identically.
