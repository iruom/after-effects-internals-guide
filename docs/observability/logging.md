---
status: active
last_verified: 2026-09-15
evidence: local logs + replicated dvacore trace experiment + runtime inventories
---
# Logging and Tracing

AEIG treats logs as versioned evidence artifacts, not as prose diagnostics to quote selectively.

Important classes include Plugin Loading logs, aerender/headless logs, crash/stack logs, UXP/CEP logs, Debug Database, Trace Database and experiment-generated capture files.

Each preserved artifact should record host version, path/provenance, capture conditions and whether the file is mutable user state or immutable copied evidence.

## Interpretation rules
- Plugin Loading logs describe loader decisions, not necessarily runtime use after load.
- Crash symbols expose call-path vocabulary but do not establish supported APIs.
- Debug/Trace databases expose subsystem names and controls; category presence does not prove a feature is active in every run.
- Experiment logs are strongest when tied to a deterministic fixture and raw-output hashes.

`EXP-OBS-002` demonstrated that dvacore trace thresholds are live runtime policy rather than inert files. The canonical L5 package extends this by capturing selected BEE/TDB/RG categories only during a controlled render window.

## Privacy rule
Do not copy unrelated project names, user paths or private content into the research corpus. Preserve only the minimum evidence necessary to reproduce the claim.

See `trace-database.md`, `debug-database.md`, and `docs/reference/corpus-coverage-status.md`.## Unknown frontier and observer effect
A logging category name can survive after implementation changes, and absence can mean disabled threshold, alternate backend or uninstrumented path rather than feature absence. AEIG never treats silence as proof that a subsystem did not run without a positive control showing the capture path itself works.

Verbose logging can also perturb timing, I/O and race behavior. Performance conclusions therefore require an uninstrumented control run plus a minimally instrumented reproduction.

When a log string is used as evidence, preserve the raw artifact/hash and scope the claim to the exact host build and capture configuration. Cross-version string equality is lineage evidence, not proof of identical code.
## Correlation window
Prefer short, explicitly bracketed capture windows around one deterministic action. Long whole-session logs increase false correlations and make subsystem ownership harder to infer. Pair timestamps with process/thread ID and output hashes whenever the source permits it.

Related methodology: `docs/observability/process-tracing.md`, `docs/capability-recipes/observe-internals-safely.md`, `docs/foundations/evidence-model.md`.
