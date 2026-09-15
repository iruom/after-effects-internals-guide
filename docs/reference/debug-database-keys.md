---
status: reference-generated
last_verified: 2026-09-15
evidence: ae-debug-trace-lineage.csv
---
# Debug Database Keys

The machine-readable lineage dataset is the canonical source for hidden Debug Database vocabulary.

Current corpus summary:
- stable-channel unique debug keys: **678**;
- beta-channel unique debug keys: **407**;
- keys observed in both stable and beta: **391**;
- stable-only vocabulary in the retained corpus: **287**.

Each lineage row records `first_seen`, `last_seen`, version count and observed default/value variants. This allows AEIG to distinguish a one-build experiment from a long-lived internal control.

Debug keys are evidence of configurable internal vocabulary, not supported plug-in APIs. A key can be renamed, ignored, build-gated or semantically repurposed without compatibility guarantees.

High-value families include BEE/cache/evaluation controls, GPU/3D quality controls, MFR/read-ahead settings, expression caches, media/cache controls, AI-analysis features and logging/trace behavior.

Do not copy a key into production configuration merely because it is present. Prefer read-only archaeology or disposable-profile experiments.

Canonical data: `datasets/ae-debug-trace-lineage.csv` and `datasets/ae-debug-trace-vocabulary.csv`.

For version archaeology, compare `first_seen/last_seen` with public API introduction dates rather than assuming an internal key and a public feature appeared simultaneously.