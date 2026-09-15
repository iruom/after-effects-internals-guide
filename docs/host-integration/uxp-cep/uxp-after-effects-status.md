---
status: active
last_verified: 2026-09-16
evidence: Adobe UXP host-version tables + current UXP Hub + local AE runtime/extension substrate
---
# UXP in After Effects: Runtime Presence Is Not Public Host API

After Effects is a strong example of why AEIG separates **runtime substrate**, **first-party use**, and **public third-party extensibility contract**.

Older Adobe UXP version tables listed After Effects 22.x/23.0 among applications integrated with UXP 5.5-6.3. Local AE installations/logs also expose UXP/WebView-related runtime components and first-party extension activity.

That proves UXP infrastructure has existed in/around AE. It does **not** prove a supported public After Effects UXP DOM or generally loadable third-party panel contract for the current release.

## Current public boundary
As of September 2026, Adobe's current UXP Hub describes UXP as built into Photoshop, Premiere, InDesign and Media Encoder; After Effects is not listed in that current supported-host summary.

Adobe has meanwhile expanded Premiere UXP/Hybrid support and put Media Encoder UXP into public beta. This makes the absence of an equivalent current AE public host page meaningful, while still not proving what Adobe may ship later.## What may be inferred
Runtime binaries, manifests and first-party plug-ins can establish that the application contains or consumes UXP-related infrastructure. They may reveal loader versions, WebView/native bridge dependencies and internal capability vocabulary.

They cannot establish that an undocumented host object is stable, callable by third parties, Marketplace-supported, or compatible across releases.

Likewise, an old host-version table proves historical integration for those releases, not current public API continuity.

## Developer guidance
For production AE extensions, choose a plane with a current supported contract: C++ Effect/AEGP APIs, scripting/CEP where still appropriate, or another documented integration surface. Do not ship against a private UXP object merely because a first-party extension can see it.

If testing prerelease access, isolate it behind an adapter so the rest of the application does not depend on a provisional AE DOM.

## Comparison with Premiere/Media Encoder
Premiere 26.x now has documented UXP and Hybrid plug-in contracts. Media Encoder UXP is in public beta with a documented host API. These sibling hosts provide valuable design clues, but their DOM classes and lifecycle rules are not automatically AE APIs.## Experiments
For each AE release inventory UXP/WebView/native extension modules, first-party manifests and host IDs. Then test only documented loading routes. Record whether a candidate surface is visible to third-party developer tooling, requires beta entitlement, or exists only inside Adobe-signed/first-party contexts.

A falsification criterion for “public AE UXP support” is straightforward: Adobe must publish a current AE host contract/tooling route that a third-party plug-in can target without private entitlement. Runtime presence alone cannot satisfy it.

## Failure modes
The dangerous failure is accidental dependence on first-party-only infrastructure: a prototype works on one build or signed context, then fails distribution, loading or API access on another machine. Another failure is assuming sibling-host UXP DOM objects exist in AE because the platform layer is shared.

## Unknown frontier
AE's internal current UXP/first-party extension usage is not fully mapped, and future public support may change quickly. This page is intentionally date/version scoped and should be reverified whenever Adobe updates the UXP Hub or AE developer documentation.

Cross-links: `cep-runtime.md`, `../../capability-recipes/cep-vs-uxp-extension-plane.md`, `../cep/cc2015-panel-sdk.md`, and `../../product-shell/overview.md`.