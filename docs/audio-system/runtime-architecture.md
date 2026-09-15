---
status: active
last_verified: 2026-09-15
---
# Audio Runtime Architecture

Audio is a parallel time-domain pipeline with its own source residency, prefetch, processing graph and playback/output state.

```text
media importer / conformed audio source
        |
        v
IAsyncAudioSource / IAudioSourceFile
        |
        +--> MediaFoundation cache/prefetch guards
        |
        v
AudioRenderContext
(time ranges, quality, latency, direction, abort)
        |
        v
AudioGenerator / Processor graph
(stream, clip, track, mix, filter, fader, pan, send)
        |
        +--> resample / time scale / channel map
        |
        +--> waveform / peak-data analysis paths
        v
AudioSupport / device / output
```
## State separation
Do not collapse these into one audio cache:
- conformed/source media residency;
- prefetched sample/cache-guard residency;
- rendered/mixed audio-generator state;
- waveform/peak-analysis data;
- hardware/device playback buffering.

`AudioRenderContextParameters` also shows why preview and final render can differ even with the same source: render mode/quality, latency, playback direction, loop range and safety policy are explicit context dimensions.

## AE project-side state
BEE contains `BEE_AudioStreamGroup` and audio-level stream traits. These establish a project/property-side audio state graph, but the precise conversion into AudioRenderer generators/processors is not yet proven by symbol names alone.

## Experiments
- Hold source media constant and vary only layer Audio Levels/effect state; observe whether conform/prefetch remains reusable.
- Reverse playback, time-stretch and resample independently to distinguish source residency from processor-state invalidation.
- Compare waveform generation/cache updates with actual audio render requests.
- Trace scrubbing cancellation and prefetch ranges to determine horizon and granularity.

Primary local evidence: `datasets/ae-2025-audio-pipeline-symbols.csv` and `F-AUDIO-001`.

## Public request surfaces
`AEGP_RenderNewItemSoundData()` requests audio for an item over an explicit start time and duration in an explicit `AEGP_SoundDataFormat`. The returned `AEGP_SoundDataH` is caller-owned and may be null when no audio exists.

`AEGP_SoundDataFormat` separates sample rate, encoding, bytes/sample and channel count. `AEGP_SoundDataSuite` then exposes lock/unlock and sample-count access, giving audio its own host-owned buffer lifetime rather than pretending it is an image world.

At the importer boundary, `AEIO_GetSound()` additionally receives start time, duration, start sample/count and quality. `AEIO_SndQuality_APPROX` is documented for drawing the audio waveform, separate from LO/HI audio requests.

This is strong public evidence that **waveform analysis, source sample retrieval and final audio rendering are not one request class**.

## Time and format identity
An audio request key must at least consider source/content state, mapped time range, sample rate, channel layout and encoding/precision. Time stretch, reverse playback and nested comp mapping can alter which source samples are required without changing the source file itself.

Do not key reusable processed audio only by frame number: audio operates over continuous/rational ranges and sample counts that need not align to video frame boundaries.

## Waveform versus rendered sound
Waveform/peak data may use approximate-quality source reads and can have its own persistence/cache lifetime. A correct-looking waveform therefore does not prove final mix/render samples are available or bit-identical.

Likewise, purging peak/waveform data should not be assumed to invalidate conformed source audio or final rendered audio unless evidence shows a shared store.

## Failure modes
- assume waveform cache equals rendered-audio cache;
- ignore sample-rate/channel-layout changes when reusing processed state;
- map comp/video frame time directly to sample index with lossy floating-point conversion;
- treat reverse/time-stretched playback as a source-cache miss rather than processor-state change;
- keep locked SoundData samples across arbitrary host calls instead of respecting lock lifetime;
- attribute device-playback underrun to source decode when the failure is downstream buffering/scheduling.

## Controlled experiments
Use deterministic impulse/chirp audio and vary one dimension at a time: layer Audio Levels, time stretch, reverse, sample rate, channel count, effect state, preview quality and final output format.

Record AEIO/source reads, waveform/peak updates, local MediaFoundation prefetch ranges, processor-graph activity, SoundData sample hashes and device-output timing. Separate **source residency reuse** from **processed mix reuse**.

For temporal mapping, use rational `A_Time` boundaries and verify exact sample positions around video-frame edges. This can expose off-by-one/resampling behavior hidden by ordinary music material.

## Version boundary and unknowns
Public AEGP/AEIO audio APIs are long-lived, while local AudioRenderer/MediaFoundation surfaces represent newer internal infrastructure. AEIG does not assume a one-to-one adapter class between them.

Still unresolved: exact BEE audio-stream-to-AudioRenderer bridge, cache key composition for processed audio, waveform persistence format/lifetime, MFR interaction with audio-only dependencies, and cancellation semantics during scrub/prefetch.

Related: `docs/audio-system/overview.md`, `docs/media-system/runtime-architecture.md`, `docs/temporal-system/time-model.md`, `F-AUDIO-001`.
