---
status: active
last_verified: 2026-09-15
---
# Product-System Atlas

This page is the top-level map from the visible After Effects product to the internal domains AEIG studies.

| Product surface | Primary internal domains | High-value evidence surfaces |
|---|---|---|
| Project / Project panel | project state, item identity, persistence, undo | AEGP Item/Project suites, AEP/AEPX, scripting, BEE_Project |
| Composition / Layer stack | comp/layer state, streams, evaluation, render graph | AEGP Comp/Layer/Stream, trace DB, project files |
| Timeline / keyframes | animation model, interpolation, time, streams | AEGP Keyframe/Stream, expressions, AEP differential tests |
| Expressions | expression runtime, dependencies, caches, invalidation | expression docs, V8 behavior, prefs/debug DB, experiments |
| Effects | effect ABI, parameter streams, SmartFX, cache, GPU | Effect API, SmartFX, samples, commercial plug-in traces |
| Masks / mattes | geometry, streams, image bounds, tracking | AEGP mask/path suites, render experiments, project diffs |
| Shape layers | vector model, stream hierarchy, tessellation/rendering | scripting/AEGP streams, project files, traces, pixel probes |
| Text | text engine, font state, shaping, animation streams | scripting, AEP, fixed-issue corpus, render probes |
| 2D compositing | render graph, blend/alpha, ROI, sampling | SmartFX, pixel experiments, fixed issues, trace DB |
| 3D / cameras / lights | scene extraction, 3D renderer, materials, GPU | Artisan API, AEGP, Advanced 3D docs, modules, traces |
| Preview | render requests, cache, playback, display pipeline | render suites, disk/RAM cache docs, trace DB, prefs |
| Render Queue | render context, output modules, AEIO, headless | AEGP render suites, AEIO, aerender, logs |
| Import / footage | media decode, interpretation, cache, color | AEIO, MediaCore artifacts, media cache, XMP |
| Export / AME | render/output pipeline, media encoding, handoff | AEIO, AME integration, logs, fixed issues |
| Product surface | Primary internal domains | High-value evidence surfaces |
|---|---|---|
| Color management | color transforms, working space, display/output transforms | Adobe color docs, OCIO modules, project files, pixel probes |
| Audio | audio streams, time, preview/render, media I/O | audio Effect API, AEIO sound worlds, waveform experiments |
| Scripting | project mutation, commands, UI automation | ExtendScript docs, Reflection, command IDs, scripting prefs |
| CEP / UXP / panels | app integration, UI framework, messaging | public extension docs, installed modules, process tracing |
| Preferences | configuration state, feature flags, caches, diagnostics | Prefs files, Debug Database, version diffs |
| Workspaces / panels / guides | UI state, view state, product shell | AEGP ItemView/Guide suites, prefs, UI experiments |
| Tracking / stabilization | analysis engines, temporal state, caches | user docs, effects, traces, project/preset artifacts |
| Roto Brush / Object Matte / AI | analysis graphs, model runtime, temporal propagation, cache | release docs, modules, disk-cache artifacts, process/GPU traces |
| Motion blur / frame blending | temporal sampling, shutter model, interpolation | Comp suites, render probes, pixel comparisons |
| Dynamic Link / inter-app | project/media identity, IPC, render delegation | process tracing, logs, Adobe integration docs |
| Plug-in loading | binary ABI, PICA/SweetPea, PiPL, compatibility | SDK headers, plugin loading logs, host emulators |
| Headless / aerender | non-UI host, project load, render queue, licensing boundary | aerender behavior, headless plugin logs, process traces |
| Undo / copy / paste | object identity, serialization, transaction model | AEGP hooks, AEP diffs, controlled experiments |

## Research implication
A visible feature may cross several internal domains. AEIG should resist pages such as “everything about Preview” becoming monoliths: Preview is an integration scenario linking render requests, caches, display, audio, UI timing and GPU presentation.

Conversely, one internal subsystem can surface in many product features. The cache system affects preview, expressions, effects, Object Matte, media, undo/redo and cross-project reuse.

The atlas therefore supports **bidirectional navigation**: feature → internals and internals → affected features.
