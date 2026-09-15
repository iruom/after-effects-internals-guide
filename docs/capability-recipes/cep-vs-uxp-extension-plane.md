---
status: active
last_verified: 2026-09-16
---
# Choose CEP vs UXP for AE Extension UI

After Effects extension UI must be evaluated as a **host contract**, not merely as a choice of JavaScript framework. CEP and UXP use different runtime/bridge models, expose different host capabilities, and can have very different support status even when both runtimes are physically present in an Adobe installation.

## Confirmed third-party CEP route

The retained CC 2015 Panel SDK and installed modern AE substrate support the historical/continuing pattern:

`CSXS manifest targeting AEFT -> CEP/PlugPlug host -> HTML/JS -> CSInterface.evalScript -> ExtendScript -> AE host state`

The CC 2015 corpus contains four sample manifests targeting `AEFT` and exposes standard `CSInterface` operations such as `evalScript`, event dispatch/listening, host-environment queries and extension-to-extension routing. Modern installed artifacts still contain AEFT-targeted CSXS manifests plus CEP/PlugPlug/Vulcan infrastructure.

This establishes architectural continuity of the CEP extension plane; it does not imply identical Chromium, Node, CEP or security behavior across AE releases.

## Execution contexts are the important part

CEP is not one JavaScript VM. A panel can involve a browser/CEF context, a native CEP context, optional Node integration, and the host application's ExtendScript engine. `evalScript` crosses into the AE-specific scripting environment rather than making browser JavaScript itself part of the AE DOM.

That boundary has practical consequences: host mutation and many application operations ultimately enter a main-thread-sensitive environment. Long synchronous ExtendScript work can therefore make a panel appear frozen even if the HTML/JS side remains conceptually asynchronous.
## UXP runtime presence is not the same as a public AE contract

AE has shipped UXP/WebView2-related runtime activity and first-party UXP extension hosting. Local binary archaeology also shows AE-side imports for operations such as loading an extension by ID, creating/attaching a host view, sending events to JavaScript and exposing a client host API object.

Those facts prove a first-party/runtime integration surface. They do **not** by themselves prove that arbitrary third-party extensions receive an AE-specific public Host DOM, discovery path or supported packaging contract in the same release.

This distinction is central to AEIG: a shared `dvauxphost` module may contain third-party discovery machinery while AE's own import/use path exposes only a subset. Shared Adobe infrastructure is evidence of capability substrate, not automatic host enablement.

See `docs/host-integration/uxp-cep/uxp-after-effects-status.md` for the version-scoped support picture and `datasets/ae-2025-extension-substrates.csv` for local runtime evidence.

## Selection rule

For a production third-party AE panel, prefer the route whose **AE-specific public contract** is independently established for the target release. Runtime presence, beta access, another Adobe application's support status or a framework generator's target list are weaker evidence than an AE host contract.

A practical decision tree is:

1. Does the target AE version explicitly support the extension technology for third parties?
2. Does it expose the host operations your tool needs, not merely panel rendering?
3. Are packaging, signing/distribution and discovery documented for AE?
4. Can the required operation run safely through the host context/thread boundary?
5. If using a bridge to ExtendScript or native code, is that bridge itself supported and version-scoped?

If any of these are unknown, treat the missing piece as a deployment risk rather than assuming parity with Photoshop, Premiere or Media Encoder.
## Failure modes and developer traps

- **runtime-equals-support trap:** discovering UXP binaries or first-party panels does not prove a supported third-party AE API;
- **cross-host parity trap:** a UXP API documented for another Adobe host may not exist, or may have different semantics, in AE;
- **main-thread blocking:** a fast web UI can still stall when large synchronous work is pushed through `evalScript`;
- **context confusion:** browser, Node, native CEP and ExtendScript globals/permissions are different contexts;
- **serialization boundary:** values crossing a script bridge need deliberate encoding, error propagation and version-tolerant schemas;
- **lifetime mismatch:** UI lifecycle and AE project/object lifetime are not the same; cache host references conservatively;
- **silent fallback:** extension discovery failure, manifest-range mismatch or disabled runtime features can look like application logic failure.

## Architecture guidance

Keep UI, transport and AE-operation layers separable. Treat the panel as a client of an explicit host-operation protocol rather than scattering raw `evalScript` calls across UI components. This makes it possible to move an operation from CEP/ExtendScript to a future UXP Host DOM or native bridge without rewriting the entire panel.

For expensive operations, batch host work, return structured errors, and avoid assuming that asynchronous browser code makes the host-side work asynchronous. When native code is involved, document which side owns handles, files and callbacks and which thread each transition enters.

## Evidence and version boundary

The retained CC 2015 Panel SDK proves a historical distributed CEP contract for AEFT. Installed AE 2025 artifacts prove continued CEP substrate and first-party UXP infrastructure. General third-party AE UXP discovery/Host DOM remains an explicit capability frontier until target-release evidence closes it.

That frontier is tracked in `datasets/aeig-unknown-frontier.csv`; it should not be erased by optimistic framework support claims.

## Related material

- `docs/host-integration/uxp-cep/cep-runtime.md`
- `docs/host-integration/uxp-cep/uxp-after-effects-status.md`
- `docs/host-integration/cep/cc2015-panel-sdk.md`
- `datasets/ae-cc2015-panel-sdk-surface.csv`
- `datasets/ae-2025-extension-substrates.csv`

The long-term migration rule is simple: choose the modern surface when **After Effects itself** exposes the necessary third-party contract, but preserve a clean capability boundary so UI technology never becomes the ontology of the AE operation being performed.
