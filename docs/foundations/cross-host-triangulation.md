---
status: active
last_verified: 2026-09-16
---
# Cross-Host Triangulation

After Effects shares code, protocols and historical API ancestry with other Adobe hosts, but sibling-host behavior is never automatically an AE fact. Cross-host evidence is valuable only when the shared substrate and the host-specific divergence are both identified.

The method is:

```text
AE evidence gap
   -> identify shared Adobe primitive
   -> inspect better-documented sibling host
   -> separate substrate behavior from host policy
   -> predict an AE-side observation
   -> confirm/refute against AE artifact or experiment
```

This is particularly useful when Premiere exposes a public suite for a concept that appears only as internal/runtime vocabulary in AE.
## Evidence ladder

A cross-host transfer is strongest when several layers agree:
1. the same suite/API family or binary substrate is present in both hosts;
2. shared headers/types/ABI establish common ancestry;
3. runtime imports/exports show AE actually participates in the subsystem;
4. sibling-host documentation exposes semantics hidden in AE;
5. an AE-side trace, project differential or controlled experiment confirms the predicted behavior.

Without steps 1-3, a sibling API is only an analogy. Without step 5, the AE conclusion remains provisional.

## Premiere as a controlled contrast

Premiere Pro hosts much of the AE Effect API, but Adobe documents substantial differences in time values, render scheduling, field rendering, pixel formats, suite availability and multithreading. The same effect binary can therefore expose which behavior belongs to the shared API and which belongs to host policy.

Premiere's `appl_id` (`PrMr`) versus AE's `FXTC` is not merely a branding field; host-specific branches are often required because capability and scheduling differ even when the function signature is shared.
## High-value shared families

- **PICA / SweetPea suites**: suite negotiation/versioning is shared infrastructure, but each host exposes a different suite set.
- **AE Effect API in Premiere**: useful for host-difference testing; not evidence that Premiere render scheduling equals AE.
- **MediaCore / MediaFoundation**: importer/decode/frame identity is shared Adobe infrastructure; project integration remains host-specific.
- **GPU/device services**: shared device/pixel concepts can reveal residency rules while renderer policy differs.
- **CEP/CSXS / PlugPlug / Vulcan / UXP host substrate**: runtime presence can be shared even when public third-party host contracts differ.
- **Premiere-only public suites** such as Opaque Effect Data or Media Accelerator: strong design analogues where AE exposes related runtime objects, but not AE APIs.

## Failure modes in cross-host inference

The most dangerous mistake is semantic promotion by name: seeing the same `Guid`, `PPix`, suite family or module and assuming identical lifetime, thread or cache semantics. Another is version-number equivalence; Premiere's host version fields do not imply the same feature level as an AE release with a numerically similar API generation.

Adobe also warns that many suites are absent in Premiere even when equivalent macro functionality exists. Capability must therefore be tested by suite acquisition and host context, not by compiling against a header.

Cross-host evidence should always be labelled `corroborating`, `shared-substrate`, or `analogy` until AE-specific evidence promotes it.

## Experiments

Run the same minimal effect/plugin operation in AE and Premiere where the shared Effect API permits it. Record selector order, thread IDs, time values, pixel format, quality, checkout behavior and suite availability. Differences are as valuable as matches because they identify the host-policy boundary.

Cross-links: `evidence-model.md`, `methodology.md`, `../host-integration/premiere-pro/shared-effect-api.md`, `../host-integration/pica-sweetpea/runtime-architecture.md`, and `../media-system/runtime-architecture.md`.
