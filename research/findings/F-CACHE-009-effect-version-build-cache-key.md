---
status: confirmed-public
evidence_grade: E0
versions: "CS6+ Global Performance Cache documentation"
last_verified: 2026-09-14
---
# Effect version and AE build number participate in frame-cache identity

## Official evidence
Adobe's SDK Tips & Tricks states that a plug-in's effect version and the After Effects build number are part of the Global Performance Cache key. Updating the effect version prevents reuse of frames rendered by an older plug-in build.

## Architectural consequence
Cache identity includes implementation-version metadata in addition to project state. The cache therefore models semantic compatibility, not only visible parameter values.

## Design implication
A robust content-addressed cache should namespace results by implementation/kernel version, numerical mode, backend and ABI-affecting semantics. Otherwise bug fixes can resurrect stale but key-compatible pixels.

## Source
https://ae-plugins.docsforadobe.dev/effect-details/tips-tricks/