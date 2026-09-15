---
status: strongly-supported-local
last_verified: 2026-09-15
evidence: E2-L installed AE 2025 runtime
versions: AE 2025
---
# F-AUDIO-001 — Audio uses a parallel render/prefetch pipeline with explicit time and cache state

AE 2025 ships a dedicated audio-render architecture rather than treating audio as image-render metadata. `AudioRenderer.dll` exposes `AudioRenderContextParameters`, renderer factories and generators/processors for streams, clips, tracks, groups, mixes, filters, faders, panners, sends, transitions, time scaling and resampling.

Render context state includes render mode/quality, loop and recording ranges, playback direction, latency, control interval, max sample frames, abort state and safety toggles for effects/faders/panners/sends.

## Temporal and prefetch behavior
Audio prefetch is explicit. `PrefetchRange`, `PrefetchRequestAccumulator`, `PrefetchAudio` and `PrefetchFromAudioGenerator` operate with `TickTime`, async Futures and MediaFoundation `CacheGuard` objects. Waveform generation is also asynchronous and returns a Future.

## Media/source boundary
`ImporterHost.dll` exposes `ConformedAudioSourceFile` as `IAsyncAudioSource`, `IAudioSource`, `IAudioSourceFile` and MediaFoundation source/file-owner interfaces. It has database, cancellation and render-request lifecycle functions. This makes audio conform/source residency a media-layer concern preceding composition audio processing.

`BEE.dll` separately exposes `BEE_AudioStreamGroup` and audio-level stream traits on the AE project/property side. The exact bridge from BEE stream values to AudioRenderer parameters remains open, but the two layers are independently visible.

## Working model
`media audio -> conform/async source -> prefetch/cache guards -> AudioRenderContext -> generator/processor graph -> mix/resample/time-scale -> device/output`, with BEE/TDB project streams supplying evaluated AE-side state.

Waveform/peak-data residency should not be assumed equivalent to rendered audio samples. `dvaaudiofile.dll` has an independent `PeakData` representation, while `AudioRenderer` exposes asynchronous waveform generation.

Reproduction: `probes/process-tools/inventory_audio_pipeline_symbols.py` -> `datasets/ae-2025-audio-pipeline-symbols.csv`.
