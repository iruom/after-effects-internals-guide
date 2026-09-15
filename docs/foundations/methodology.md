---
status: active
last_verified: 2026-09-14
---
# Methodology

Use four methods together: boundary reading of official APIs, artifact archaeology, black-box system identification, and version differential. The target is externally observable computational semantics, not guessed source code.

## Research intake channels
AEIG deliberately uses more than Internet documentation. A finding can begin from any of these channels:
- current/old SDK contracts and oddly specific warnings;
- Adobe patents, engineering posts and release-note regressions;
- local `Debug Database.txt`, `Trace Database.txt`, preferences and plug-in-loading logs;
- AEP/AEPX/FFX/PresetEffects differential analysis;
- crash reports, module names and process/file/GPU traces;
- first-party sample projects and behavior that implies hidden host contracts;
- third-party plug-in failures that expose verification assertions;
- controlled black-box probes and numerical fitting;
- mathematical reconstruction from impulse, temporal or geometric responses;
- cross-version changes and removed/obsolete APIs.

## Implementation-hole analysis
For every public API, ask what the host must secretly know in order to implement the contract. Examples: a receipt API implies state identity; precise ROI implies region transfer functions; undo-safe reuse implies versioned state rather than destructive invalidation; sequence flattening implies a serialization boundary.

Then ask where the contract leaks complexity or inefficiency: conservative bounds, false cache invalidation, duplicated per-thread sequence state, unstable handles, full-frame fallbacks, hidden coordinate conversions, excessive synchronization, non-composable special cases.

These are recorded separately as **observed AE behavior**, **inferred internal requirement**, and **possible better design**. Improvement proposals must never be presented as facts about AE.

## Stop condition for a subsystem
A subsystem is considered "closed enough" only when its core claims have at least two independent evidence paths or one direct reproducible experiment, version scope is known, contradictions are recorded, and remaining unknowns are stated as falsifiable hypotheses.

## Evidence chain used by AEIG
Prefer to move a claim through this chain where possible:

`public surface -> distributed SDK -> legacy SDK -> Adobe sample -> runtime artifact -> controlled experiment -> reconstructed model`

The chain is not mandatory, but every additional independent link raises confidence. A header comment can explain intent; a crash symbol can establish that a named runtime object exists; an experiment can establish actual behavior. None substitutes for the others.

## SDK distribution archaeology
The downloadable SDK is treated as a first-class primary corpus, not merely support material for the online Guide. Research includes current headers, old/deprecated suite definitions, internal-build conditionals, revision comments, example code, PiPL/resources, build files and utility code.

For every SDK discovery record separately:
1. literal contract or comment;
2. what hidden host state must exist to satisfy it;
3. matching runtime symbols/artifacts;
4. historical predecessor/successor APIs;
5. experiment that can distinguish competing internal models;
6. possible implementation weakness or cleaner design.

Never promote an internal-looking identifier into a semantic conclusion without an independent path. Preserve exact names, version numbers and comments as evidence, but keep reconstructed architecture explicitly separate.
## Independent-reimplementation triangulation
Use independent implementations as adversarial specifications. A parser, plug-in ABI clone, or host emulator reveals which details an outside implementer believed were necessary; its bugs reveal where that belief was incomplete.

Preferred loop:
1. freeze repository commit and record provenance;
2. extract the exact assumption from source, not only README prose;
3. compare with the current Adobe header/Guide;
4. compare with a second independent implementation where possible;
5. compare with local runtime artifacts or controlled AE behavior;
6. classify the result as agreement, contradiction, version drift, or unknown;
7. turn contradictions into experiments rather than choosing a favorite source.

Three especially useful directions are kept separate: persistence readers (`.aep/.ffx`), plug-in-side ABI reimplementations, and host-side Effect API emulators. Agreement across all three is unusually strong because they observe different boundaries of the same system.
