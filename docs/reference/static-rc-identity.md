---
status: generated
last_verified: 2026-09-16
---
# Static RC Identity

AEIG 1.0 の operator run 前 Static RC は、`datasets/aeig-static-rc-manifest.csv` に列挙された **56 artifacts** で固定されている。

Canonical fingerprint:

`406B70458F0D808891879AFAD610981C518ED7D7BADCC9C7720ACB31C6F64433`

算出規則は manifest 行を `path / role / bytes / sha256` で canonical serialization し、UTF-8列へ SHA-256 を適用する。

このfingerprintは個々のartifact hashの代替ではなく、RC全体のsummary identityである。`verify_aeig_static_rc.py` は各artifact、prediction lock、aggregate fingerprintをすべてfail-closedで検証する。

## Prediction lock

Prospective predictions は **7件**。観測後にstatus/evidenceは変化できるが、immutable予測本文は `datasets/aeig-prediction-lock.csv` で固定されている。
