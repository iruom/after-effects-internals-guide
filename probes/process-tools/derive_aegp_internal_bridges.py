from __future__ import annotations
import csv, re
from pathlib import Path

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
SRC=ROOT/"datasets"/"ae-2025-runtime-export-atlas.csv"
OUT=ROOT/"datasets"/"ae-2025-aegp-internal-bridges.csv"
patterns={
 "collection-to-bee-spec": re.compile(r"AssignBEE@aegp@mee",re.I),
 "stream-handle-to-bee-spec": re.compile(r"GetStreamSpec@aegp@mee",re.I),
 "aegp-layerstream-to-tdb": re.compile(r"LayerStreamToBEEStream@aegp@mee",re.I),
 "tdb-to-aegp-layerstream": re.compile(r"BEEStreamToLayerStream@aegp@mee",re.I),
 "aegp-maskstream-to-tdb": re.compile(r"AEGPMaskStreamToBEEMaskStream@aegp@mee",re.I),
 "layer-param-id-bridge": re.compile(r"Convert(?:IDToLayerParam|LayerParamToID)@aegp@mee",re.I),
 "aegp-runtime-registration": re.compile(r"MEE_AEGP_|GetAEGPInternalID|G_aegp_internal_plugin_id",re.I),
}
rows=[]
for r in csv.DictReader(SRC.open(encoding="utf-8")):
    s=r.get("symbol","")
    for cat,rx in patterns.items():
        if rx.search(s):
            rows.append({"category":cat,"module":r["module_name"],"symbol":s,"evidence":"runtime-export"}); break
rows=sorted({tuple(r.values()):r for r in rows}.values(),key=lambda r:(r["category"],r["module"],r["symbol"]))
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["category","module","symbol","evidence"]); w.writeheader(); w.writerows(rows)
print("wrote",OUT,"rows",len(rows))
for r in rows: print(r["category"],"|",r["module"],"|",r["symbol"])
