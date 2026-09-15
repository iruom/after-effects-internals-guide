from pathlib import Path
import csv, hashlib, json
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"
MAN=DATA/"aeig-static-rc-manifest.csv"
OUT=DATA/"aeig-static-rc-fingerprint.json"
DOC=ROOT/"docs"/"reference"/"static-rc-snapshot.md"

def rows(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def hash_lines(lines):
    h=hashlib.sha256()
    for line in lines:
        h.update(line.encode("utf-8")); h.update(b"\n")
    return h.hexdigest().upper()

m=rows(MAN)
canon=[f"{r['path']}\t{r['role']}\t{r['bytes']}\t{r['sha256'].upper()}" for r in sorted(m,key=lambda x:x['path'])]
fingerprint=hash_lines(canon)
api=rows(DATA/"ae-api-completeness-classification.csv")
master=rows(DATA/"ae-master-surface-registry.csv")
corpora=rows(DATA/"aeig-corpus-coverage-manifest.csv")
findings=rows(DATA/"finding-registry-audit.csv")
progress=rows(DATA/"aeig-roadmap-progress.csv")
met=sum(str(r.get("meets_1_0_target","")).lower() in {"true","1","yes"} for r in progress)
payload={
    "static_rc_fingerprint_sha256":fingerprint,
    "artifact_count":len(m),
    "api_identifiers":len(api),
    "master_surface_rows":len(master),
    "corpora":len(corpora),
    "findings":len(findings),
    "domain_targets_met":met,
    "domain_targets_total":len(progress),
}
OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
lines=["---","status: generated","last_verified: 2026-09-15","---","# AEIG 1.0 Static RC Snapshot","",f"Static RC fingerprint: `{fingerprint}`","",f"- Frozen artifacts: **{len(m)}**.",f"- C++ API identifiers: **{len(api)}**.",f"- Master Surface Registry rows: **{len(master)}**.",f"- Corpus entries: **{len(corpora)}**.",f"- Findings: **{len(findings)}**.",f"- Domain targets currently met: **{met}/{len(progress)}**.","","This fingerprint is derived from the sorted frozen-artifact manifest. It identifies the pre-operator static release candidate; mutable experiment outcomes are intentionally excluded."]
DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps(payload,indent=2))
print("wrote",OUT); print("wrote",DOC)
