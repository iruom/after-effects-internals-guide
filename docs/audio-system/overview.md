---
status: active
last_verified: 2026-09-16
---
# Audio System

Audio in After Effects is a parallel time-domain evaluation pipeline, not a small branch of image rendering. Source residency, prefetch, processor state, waveform analysis and playback-device buffering have separate lifetimes and invalidation rules.

Installed AE 2025 runtime evidence supports the working chain:

`imported/conformed source -> async audio source + prefetch/cache guards -> AudioRenderContext -> generator/processor graph -> mix/resample/time-scale/channel operations -> device/output`

Project-side BEE/TDB audio streams feed this world but are not the same objects as MediaFoundation residency or AudioRenderer processor state.

## State and identity layers

Keep at least five layers distinct:

1. **source/conformed media identity** — what underlying audio content is available;
2. **prefetched sample residency** — which time ranges/samples are ready for reuse;
3. **render/processor state** — gain, pan, effects, channel mapping, resampling/time-scale and mix topology;
4. **waveform/peak-analysis state** — UI/analysis artifacts that may outlive or be generated separately from rendered samples;
5. **device/playback buffering** — latency and hardware-facing state not equivalent to render identity.

A layer Audio Levels edit may invalidate mix/processor results while leaving source/conform data reusable. Regenerating a waveform does not prove the final mixed sample buffer was regenerated.
## Render context dimensions

`AudioRenderContext`/parameter vocabulary exposes dimensions such as requested time ranges, render mode/quality, latency, playback direction, looping and abort/cancellation policy. Preview, scrubbing and final render can therefore exercise different execution behavior even when source media and timeline values look identical.

This matters when diagnosing "audio differs only in preview" or "reverse/time-stretch behaves differently" reports: first compare the render context before blaming the source decoder or effect.

## Processing graph

Runtime symbols indicate generator/processor concepts for streams, clips, tracks, filters, faders, pans, sends and mixing, followed by resampling/time-scale/channel operations. AEIG treats this as a graph of time-domain processing responsibilities rather than assuming one monolithic audio callback.

BEE contains project-side audio stream/group vocabulary, but the exact object conversion from BEE/TDB property state into AudioRenderer generators is not yet proven. That boundary remains an explicit model frontier.

## Failure patterns

- **source-vs-processor invalidation confusion:** expensive conform/prefetch is blamed for a cheap mix-state change, or stale processing is blamed on source residency;
- **waveform proxy error:** waveform/peak data is treated as proof of final audio-render residency;
- **context mismatch:** preview latency/direction/quality differs from final-render context;
- **time-domain off-by-one:** sample/time conversion, loop endpoints or resampling boundaries produce discontinuities not visible in frame-based reasoning;
- **cancellation artifact:** rapid scrubbing abandons queued work and is misread as decode corruption;
- **device-path confusion:** hardware/output buffering is blamed for deterministic offline render differences, or vice versa.
