---
status: active
last_verified: 2026-09-14
primary_evidence:
  - AE 25.6 SDK Headers/AE_IO.h
  - AE 25.6 SDK AEGP/IO sample
comparison_surface:
  - Premiere Pro 26.0 PrSDKAsyncImporter.h
  - Premiere Pro 26.0 PrSDKClipRenderSuite.h
---
# AEIO Architecture and Legacy I/O Contract

AEIO is an old but still revealing boundary between After Effects and media/file modules. `AEIO_FunctionBlock4` is explicitly frozen at AE 10, so its shape should be treated as a stable legacy contract rather than a model of modern MediaCore design.

## Function-block model
An AEIO module supplies a table of callbacks that AE invokes for import, sparse frame drawing, audio reads, output initialization, frame/audio writing, option serialization, user data, markers, auxiliary channels/files, idle processing, flush and source-file closure.

The contract is callback-oriented and host-driven: the module does not own the evaluation scheduler. AE calls into it with an `AEIO_InSpecH`/`AEIO_OutSpecH` and request records describing time, scale, region and interruption behavior.
## Sparse-frame / ROI semantics
`AEIO_DrawSparseFramePB` carries a `required_region`; an empty rectangle means the entire frame. The SDK sample explicitly checks whether the requested rectangle is nonzero and only works on that region when possible.

This is important historically: region-limited image requests existed at the I/O boundary independently of SmartFX. AE therefore has multiple region concepts across subsystems, and they must not be collapsed into one generic "ROI" without evidence.

`AEIO_MFlag_CANT_CLIP` tells the host that a module cannot accept worlds smaller than the requested dimensions. That flag is an explicit capability boundary between partial-region production and full-frame-only implementations.

## Time and frame-store semantics
Input modules can advertise `AEIO_MFlag_NO_TIME`, still/video/audio support, non-linear frame addition and other capabilities. `AEIO_DrawFramePB` includes render time, duration, frame blending, field request, rational scale and interrupt callbacks.

The interface therefore distinguishes media time, render duration, field semantics and requested spatial region at the importer boundary. These are separate dimensions of a media-frame request.
## Persistence boundary
AEIO options have explicit flatten/inflate callbacks. Treat this as a serialization boundary analogous in spirit to Effect sequence-data flattening: runtime pointers/handles are not persistence-safe and must be converted into portable data.

The sample returns `AEIO_Err_USE_DFLT_CALLBACK` for many optional operations, demonstrating that AEIO is partly a policy-negotiation surface: a module can delegate behavior back to the host instead of implementing every operation.

## Flush, idle and source lifetime
The output `Flush` callback is documented by the sample as the place to free temporary buffers retained for writing. Separate callbacks exist for `Idle` and `CloseSourceFiles`, meaning resource cleanup is not represented by a single destructor-like event.

Developer code should therefore assign ownership to specific lifecycle phases and avoid assuming that closing a file, disposing an input spec, flushing output buffers and module shutdown are interchangeable.

## Cross-host comparison: Premiere async importer
Premiere's Async Importer makes concurrency/lifetime rules explicit: most calls are reentrant, the async object must not retain a link to its creator importer, relevant state is copied, `flush` is a barrier, cancellation is a non-blocking hint and `close` may arrive while work is still executing.

Do not project those rules directly onto AEIO. Instead use them to expose what AEIO leaves implicit and to design probes around ownership, cancellation and concurrent access.
## Why AEIO is still valuable to study
Adobe now generally recommends a MediaCore/Premiere importer unless AE-specific AEIO behavior is required. That recommendation is itself architectural evidence: AEIO is a legacy AE-local host callback model, while MediaCore provides a shared cross-application importer substrate and importer-priority system.

AEIO remains useful because its boundaries are unusually explicit. It reveals what the host expects an importer/exporter to own versus what AE can supply through default callbacks.

## Input lifecycle as a state machine
A typical file import path is:

`VerifyFileImportable -> InitInSpecFromFile -> describe dimensions/depth/audio/alpha/options -> GetInSpecInfo -> DrawSparseFrame/GetSound -> project save FlattenOptions -> CloseSourceFiles/DisposeInSpec`.

These phases have different frequency and ownership. `AEIO_GetInSpecInfo()` may be called often during Project-panel refresh, so repeated allocation/decoding there is a performance bug even if functionally correct.

Options data belongs to the InSpec/OutSpec persistence boundary; runtime decoder/file handles do not.

## Pixel/audio contract
AEIO supplies video as `PF_EffectWorld` and audio through AE sound-world/data contracts. The public guide states AEIO works with uncompressed ARGB worlds at 8/16/32-float per channel; compression/decompression remains the module's responsibility.

This makes codec state, decoded image state and AE project interpretation three separate layers. A codec can decode identical bytes while interpretation/alpha/color metadata changes downstream rendering.

## Default-callback negotiation
Many hooks may return `AEIO_Err_USE_DFLT_CALLBACK`. This is not "unimplemented error"; it is explicit delegation to host policy. A minimal robust AEIO should implement only the behavior it truly owns and allow AE to handle supported default cases rather than partially reproducing host logic.

## Failure modes
- retain external pointers inside flattened options -> project reopen crash/corruption;
- treat `required_region` as advisory and always decode/copy full frame -> large performance penalty;
- assume `CloseSourceFiles` equals `DisposeInSpec` -> double-close or leaked persistent state;
- allocate heavily inside `GetInSpecInfo` -> Project-panel refresh stalls;
- forget field/time/rational-scale semantics -> wrong frames under nontrivial interpretation;
- use AEIO to replace a built-in MediaCore importer and expect priority arbitration -> wrong registration architecture.

## AEIO versus modern MediaCore
Local AE runtime evidence shows MediaFoundation/media caches, async source/prefetch and content-identity infrastructure that are not exposed through the frozen AEIO function block. AEIG therefore treats AEIO as one integration plane feeding a larger media subsystem, not as the complete modern media architecture.

Sibling Premiere async-importer contracts provide useful questions about cancellation, reentrancy and lifetime, but their exact concurrency guarantees must not be projected onto AEIO without AE-side evidence.

## Controlled probes
Implement a disposable AEIO fixture with deterministic synthetic frames. Vary only ROI, rational scale, time, field mode, alpha interpretation and options bytes. Log callback order, thread ID, region requested, project save/reopen behavior and close/dispose ordering.

A second fixture should compare equivalent AEIO and MediaCore import paths for the same synthetic media while tracing MediaFoundation cache activity and output hashes.

## Unknown frontier
Still unresolved: current internal adapter path from AEIO callbacks into MediaFoundation/BEE, thread-affinity guarantees for every AEIO callback in modern AE, how AEIO frame identity maps into media ContentState/render GUIDs, and which built-in formats still traverse AEIO versus MediaCore-only paths.

Related: `docs/media-system/runtime-architecture.md`, `docs/host-integration/premiere-pro/async-file-io.md`, `F-IO-001`.
