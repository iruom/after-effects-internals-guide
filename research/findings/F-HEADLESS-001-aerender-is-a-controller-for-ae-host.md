---
status: confirmed-local-runtime
last_verified: 2026-09-15
evidence: E2-L aerender runtime help + PE dependency inventory
versions: aerender 25.6.4x3
---
# F-HEADLESS-001 — `aerender` is a controller/launcher for an AE host instance, not a separately linked render engine

The installed `aerender 25.6.4x3` help explicitly states that rendering can be performed by an already running instance of After Effects or by a newly invoked instance. By default it invokes a new AE instance; `-reuse` asks an already running AE instance to perform the render.

This makes the CLI boundary materially different from the simplistic model `aerender.exe -> independent headless renderer`. The render owner is an AE host instance whose lifetime can be created or reused by the controller.

PE dependencies reinforce this distinction. `AfterFX.exe` statically depends on `AfterFXLib.dll` and USER32, while the small `aerender.exe` front end has only OS/CRT/socket-style static dependencies and no direct `AfterFXLib.dll` dependency.

## Policy injection
CLI switches such as `-mem_usage` and `-mfr` alter memory-cache/total-memory limits and MFR/CPU policy of the requested render. `-close` controls project/save/host lifetime behavior; the help also notes a preference-writing difference for reuse versus newly launched invocations.

These options are evidence that headless rendering is a host-mode/policy surface over shared AE project/render infrastructure, even though UI services and startup/plugin behavior can still differ from an interactive session.

## Working model
`aerender CLI/controller -> {launch AE render host | reuse existing AE} -> project/render queue -> shared BEE/PF/media/GPU infrastructure -> output`.

The transport used between aerender and an existing AE instance is not established here. `WSOCK32.dll` is a static dependency, but that alone is insufficient to assert a protocol.

## Reproduction
Run `probes/process-tools/inventory_headless_entrypoint.py`. It records selected runtime-help statements, aerender version and PE dependency differences in `datasets/ae-2025-headless-entrypoint.csv`.

Next: compare module/plugin load lists, environment, cache use and output hashes between fresh aerender-hosted AE and interactive/reused AE.
