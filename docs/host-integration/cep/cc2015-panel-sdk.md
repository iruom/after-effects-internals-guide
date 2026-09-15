---
status: active
last_verified: 2026-09-16
evidence: local CC 2015 Panel SDK distributed samples + Adobe CEP documentation + AE 2025 installed CEP substrate
---
# CC 2015 Panel SDK Lineage

The retained CC 2015 Panel SDK is valuable because it is a concrete Adobe-distributed snapshot of the third-party CEP/CSXS extension contract during the AE 13.x era. It provides historical evidence that is stronger than reconstructing old behavior from current binaries alone.

## Manifest contract
All four retained sample manifests target host ID `AEFT` over version range `[13.0,15.9]` and declare CSXS 4.0. This records three independent version dimensions:
- After Effects host range;
- CSXS/CEP manifest generation;
- panel implementation/runtime assumptions.

Do not collapse them into one "CC 2015 version" number.

## Standard execution route
The samples establish the familiar panel architecture:

`HTML/CEF panel -> CSInterface -> evalScript -> host ExtendScript engine -> AE DOM`

Observed panel-side vocabulary includes `CSEvent`, `CSInterface`, `SystemPath`, event registration/dispatch, `evalScript`, host-environment queries, extension opening and browser/file-system helpers.

The important architectural point is the bridge: panel JavaScript and host ExtendScript are separate execution contexts joined by CEP infrastructure.

## Continuity into modern AE
Installed AE 2025 still contains AEFT-targeted CSXS manifests and native CEP/PlugPlug/Vulcan substrate. This supports continuity of the extension plane across generations: AE has retained the infrastructure needed to host CEP-style extensions long after the CC 2015 samples were published.

Continuity does **not** mean the embedded Chromium/CEF build, Node integration, signing policy, CSInterface API level or private native bridge is identical. Those are separately versioned implementation details.

## What the historical samples prove
They are good evidence for:
- AE's public host identifier and manifest targeting model;
- HTML panel packaging and resource layout;
- `CSInterface`/`evalScript` as the host-DOM bridge;
- CSXS event-based communication;
- the fact that third-party panels were a supported extension plane.

They are not a complete inventory of every CEP native API, every hidden first-party service, or every modern security/runtime constraint.

## Developer pitfalls
Historical samples are particularly dangerous when copied without version review. Modern CEP builds may differ in CEF behavior, Node context policy, API-version availability, signing/debug configuration and web-platform behavior. Keep the architecture pattern, then verify the runtime-specific details against the target AE/CEP generation.

## Experiments and archaeology
For lineage work, compare the same minimal AEFT panel across retained CEP generations: manifest acceptance, CSInterface API version, `evalScript`, CSXS event round-trip, Node availability and startup/module logs. Record host/build/runtime separately so a browser-runtime regression is not mistaken for an AE DOM regression.

Static archaeology should diff manifest schemas, bundled bridge libraries and installed native imports before invoking undocumented services. First-party extension packaging is evidence of host capability, not permission for third-party use.

## Evidence and cross-links
Machine inventory: `datasets/ae-cc2015-panel-sdk-surface.csv`. Modern substrate comparison: `datasets/ae-2025-extension-substrates.csv`.

Related: `docs/host-integration/uxp-cep/cep-runtime.md`, `docs/capability-recipes/cep-vs-uxp-extension-plane.md`, and `docs/host-integration/uxp-cep/uxp-after-effects-status.md`.

## Unknown frontier
AEIG does not claim that every historical CEP API remains supported in current AE, nor that every installed first-party bridge is public. Exact CEP runtime/browser lineage and AE-specific private services remain version-scoped research subjects.
