# AE Observatory

AE Observatory is the controlled-experiment layer of AEIG. Narrative experiment notes remain useful, but every experiment intended to promote a domain to L5 should also have a machine-readable manifest under `experiments/observatory/manifests/`.

## Lifecycle
`planned -> runnable -> observed -> replicated`.

- **planned**: question and discriminating hypotheses exist.
- **runnable**: fixture, procedure, capture channels and environment requirements are concrete.
- **observed**: raw outputs are preserved and hashed; a conclusion records which hypothesis survived.
- **replicated**: the observation was repeated on another run/version/machine or with an independent capture route.

## L5 rule
A domain is not experiment-backed merely because an experiment document exists. For AEIG roadmap purposes, an experiment contributes to L5 only when its manifest is `observed` or `replicated`, records environment/version, preserves raw-output references/hashes, and states a falsifiable conclusion.

This makes coverage promotion auditable and prevents documentation depth from being mistaken for experimental evidence.
