---
id: F-PERSIST-001
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-PERSIST-001 — AEGP Persistent Data bridges into real AE preference keys

**Evidence:** E0-S  
**Version:** AE 25.6 SDK `AEGP/Persisto` sample  
**Confidence:** High

Adobe's `Persisto` sample gets the application persistent blob and accesses the literal preference section/key `Main Pref Section / Pref_DEFAULT_UNLABELED_ALPHA`.

The sample explicitly demonstrates temporarily changing this preference to suppress alpha-interpretation prompting, and warns developers to restore user settings afterward.

It also comments that `AEGP_GetString()` can set a default value when the key is absent.

## Internal implication
The PersistentDataSuite is not only plug-in-private storage; it reaches the application's persistent key/value preference domain. Getter semantics may include default materialization, so reads can have persistence side effects.

## Research direction
Map known Prefs.txt keys against PersistentDataSuite lookups in disposable profiles and classify read-only, default-materializing and mutable keys.