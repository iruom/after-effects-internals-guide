---
status: generated
last_verified: 2026-09-16
---
# AEIG 1.0 Static RC Status

- Domain target: **24/27**.
- Frozen artifacts: **56**.
- Static RC SHA-256: `406B70458F0D808891879AFAD610981C518ED7D7BADCC9C7720ACB31C6F64433`.
- Master Surface Registry: **53728 rows**.
- Operator preflight: **BLOCKED**.
- Release blockers: **2**.

## Release blockers
- `domain-targets` — 24/27 domains meet target; unmet=state-identity,render-graph,cache
- `predictive-validation` — prospective=7 locked=7 confirmed=2 unresolved=5 refuted_unrevised=0

## Operator preflight
```text
PASS	ae-binary	D:\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe
PASS	canonical-aex	9768BC9B463F6377E1AE246303D6AEDD8BF11725E8D96034DF14E85F1AD9BE98
PASS	static-rc-manifest	frozen manifest present
BLOCK	not-running:afterfx.exe	running
PASS	not-running:afterfx.com	not running
PASS	not-running:aerender.exe	not running
PASS	probe-not-installed	D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\AEIG-Probes\AEIGReceiptArtie.aex
PASS	ae-version-26.3	26.3
PASS	no-unarchived-user-capture	stale=0
BLOCK	operator-session-issued	session=missing fingerprint=missing errors=['schema', 'session_id', 'issued_unix_ms', 'static_rc_fingerprint', 'canonical_aex_sha256']
PASS	static-rc-verification	AEIG static RC verification: PASS | artifacts 56 predictions 7 | fingerprint 406B70458F0D808891879AFAD610981C518ED7D7BADCC9C7720ACB31C6F64433
AEIG L5 OPERATOR PREFLIGHT: BLOCKED (2 blocker(s))
```

Static RC files are immutable for the operator run. Post-run result files and promotion state are intentionally mutable.
