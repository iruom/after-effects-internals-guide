from __future__ import annotations
import csv, re, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
SDK = Path(r"E:\Adobe_After_Effects_CC_2015_Panel_SDK")
OUT = ROOT / "datasets" / "ae-cc2015-panel-sdk-surface.csv"
DOC = ROOT / "docs" / "host-integration" / "cep" / "cc2015-panel-sdk.md"
rows=[]

def add(kind,path,name,value,evidence):
    rows.append({"kind":kind,"path":str(path.relative_to(SDK)),"name":name,
                 "value":value,"evidence":evidence})

for p in sorted(SDK.rglob("manifest.xml")):
    root=ET.parse(p).getroot()
    add("manifest",p,"ExtensionManifest.Version",root.attrib.get("Version",""),"distributed-sample")
    for h in root.findall(".//Host"):
        add("host-target",p,h.attrib.get("Name",""),h.attrib.get("Version",""),"distributed-sample")
    for r in root.findall(".//RequiredRuntime"):
        add("required-runtime",p,r.attrib.get("Name",""),r.attrib.get("Version",""),"distributed-sample")
    for tag in ["MainPath","ScriptPath","Type","Menu","AutoVisible"]:
        for n in root.findall(f".//{tag}"):
            add("manifest-field",p,tag,(n.text or "").strip(),"distributed-sample")
api_names=[
    "CSInterface","CSEvent","SystemPath","evalScript","dispatchEvent","addEventListener",
    "removeEventListener","getSystemPath","getHostEnvironment","getApplicationID",
    "requestOpenExtension","openURLInDefaultBrowser",
]
for p in sorted(SDK.rglob("*.js")):
    text=p.read_text(encoding="utf-8-sig",errors="ignore")
    for name in api_names:
        if re.search(rf"\b{re.escape(name)}\b",text):
            add("js-api",p,name,"present","distributed-sample")
for p in sorted(SDK.rglob("*.jsx")):
    text=p.read_text(encoding="utf-8-sig",errors="ignore")
    for name in sorted(set(re.findall(r"\bapp(?:\.[A-Za-z_]\w*)?",text))):
        add("extendscript-bridge",p,name,"present","distributed-sample")

OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["kind","path","name","value","evidence"])
    w.writeheader(); w.writerows(rows)
host_rows=[r for r in rows if r["kind"]=="host-target" and r["name"]=="AEFT"]
runtime_rows=[r for r in rows if r["kind"]=="required-runtime"]
js=sorted({r["name"] for r in rows if r["kind"]=="js-api"})
DOC.parent.mkdir(parents=True,exist_ok=True)
lines=[
    "---","status: active","last_verified: 2026-09-15",
    "evidence: local CC 2015 Panel SDK distributed samples + AE 2025 installed CEP substrate","---",
    "# CC 2015 Panel SDK lineage","",
    "The retained CC 2015 Panel SDK provides a historical third-party CEP/CSXS contract for After Effects.","",
    f"All {len(host_rows)} sample manifests target `AEFT` version `[13.0,15.9]` and declare CSXS 4.0.",
    "The standard route is HTML panel -> `CSInterface` -> `evalScript` -> ExtendScript/AE DOM.",
    f"Observed CSInterface/API vocabulary: {', '.join('`'+x+'`' for x in js)}.","",
    "AE 2025 still ships AEFT-targeted CSXS manifests at multiple runtime generations and native CEP/PlugPlug/Vulcan bridges.",
    "This supports architectural continuity of the CEP plane, not identity of Chromium/CEP internals across releases.","",
    "Machine inventory: `datasets/ae-cc2015-panel-sdk-surface.csv`.",
    "Modern comparison: `datasets/ae-2025-extension-substrates.csv`.",
]
DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("rows",len(rows),"AEFT manifests",len(host_rows),"JS API names",len(js))
print("wrote",OUT); print("wrote",DOC)
