---
status: active
last_verified: 2026-09-15
---
# Plug-in Capability Frontier

This page tracks operations that plug-in developers commonly classify as "possible" or "impossible". AEIG replaces that binary with a versioned frontier: supported, supported only in a newer host, experimentally understood, observable through internal architecture, or reproducibly reachable only through unsupported/version-locked integration.

The machine-readable source is `datasets/ae-plugin-capability-frontier.csv`.

## Current rule
A capability is not promoted because an internal symbol exists. Promotion requires progressively stronger evidence about ABI, lifetime, host/context legality, dependency registration, cache safety and behavior under project mutation.

Current examples include formerly unavailable layer-parameter stage control becoming public in StreamSuite7, parametric-mesh creation in CompSuite13, and guide document/view state in the 26.5 APIs. By contrast RG node access, evaluated VectorArt and lower MediaCore source control remain internal observation surfaces until invocation safety is established.

## Why this matters
The practical target is to convert historical "cannot do this from a plug-in" cases into one of three useful outcomes: a newly discovered supported route; a precisely bounded unsupported route with reproducible risks; or a proof that the host currently exposes observation but not safe control. All three are more actionable than an undocumented assumption.

## Experiment-driven promotion
Every frontier row should have a concrete next experiment: acquire exact suite/version, exercise the capability under project mutation, verify thread/context legality, test invalidation/cache behavior and record failure modes. Observation without a promotion path remains `I1/I2` evidence rather than a usable capability.

A successful one-shot internal call is insufficient. To move an unsupported integration toward reproducible `I3`, AEIG requires exact host/build constraints, ownership/lifetime behavior, teardown, negative cases and evidence that the call does not corrupt project/cache state.

## Frontier regression
Supported capability can also move backward through deprecation, host-scope changes or current-product withdrawal. Therefore the frontier is versioned; "possible in AE" is never stored as an unscoped timeless boolean.

Related: `docs/reference/api-capability-atlas.md`, `docs/capability-recipes/suite-version-negotiation.md`, `docs/capability-recipes/observe-internals-safely.md`, `datasets/ae-plugin-capability-frontier.csv`.

## Completion criterion
A frontier entry is considered mature only when its current support class, host/version scope, ownership/thread/cache constraints and a reproducible confirmation or falsification path are all recorded.
