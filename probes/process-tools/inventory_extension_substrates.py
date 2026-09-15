from __future__ import annotations
import csv, json, re, subprocess, glob
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
AE=Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
COMMON=Path(r"C:\Program Files\Common Files\Adobe")
OUT=ROOT/"datasets"/"ae-2025-extension-substrates.csv"
rows=[]

def add(kind,path,host="",version="",runtime="",entry="",evidence=""):
    rows.append(dict(kind=kind,path=str(path),host=host,version=version,runtime=runtime,entry=entry,evidence=evidence))

def scan_csxs(base: Path):
    if not base.exists(): return
    for p in base.rglob("manifest.xml"):
        try: root=ET.parse(p).getroot()
        except Exception: continue
        req=root.find(".//RequiredRuntime")
        runtime="" if req is None else f"{req.get('Name','')} {req.get('Version','')}".strip()
        exts=[e.get("Id","") for e in root.findall(".//ExtensionList/Extension")]
        for h in root.findall(".//HostList/Host"):
            add("cep-csxs-manifest",p,h.get("Name",""),h.get("Version",""),runtime,";".join(exts),"manifest")
def scan_uxp(base: Path):
    if not base.exists(): return
    for p in base.rglob("manifest.json"):
        try: data=json.loads(p.read_text(encoding="utf-8",errors="ignore"))
        except Exception: continue
        hosts=data.get("host",[])
        if isinstance(hosts,dict): hosts=[hosts]
        eps=data.get("entryPoints",data.get("uiEntrypoints",[]))
        ep=";".join(str(x.get("type",x.get("id",""))) for x in eps if isinstance(x,dict))
        for h in hosts:
            if isinstance(h,dict):
                add("uxp-manifest",p,str(h.get("app","")),str(h.get("minVersion","")),str(data.get("manifestVersion","")),ep,"manifest")

candidates=glob.glob(r"C:\Program Files\Microsoft Visual Studio\2022\*\VC\Tools\MSVC\*\bin\Hostx64\x64\dumpbin.exe")
DUMPBIN=sorted(candidates)[-1] if candidates else None

def scan_imports(path: Path):
    if not DUMPBIN or not path.exists(): return
    text=subprocess.run([DUMPBIN,"/imports",str(path)],capture_output=True,text=True,errors="replace").stdout
    provider=""
    for raw in text.splitlines():
        line=raw.strip()
        if re.fullmatch(r"[A-Za-z0-9_.+-]+\.(?:dll|aex|prm)",line,re.I): provider=line
        low=(provider+" "+line).lower()
        if any(k in low for k in ("uxp","plugplug","csxs","vulcan","cep")):
            add("pe-import",path,provider,"","",line,"dumpbin")
scan_csxs(AE); scan_csxs(COMMON/"CEP"/"extensions")
scan_uxp(AE/"UXP"); scan_uxp(COMMON/"UXP"/"extensions")
for name in ("AfterFXLib.dll","AfterFX.exe","PlugPlug.dll","PlugPlugExternalObject.dll","csxsmanager.dll","dvauxphost.dll","dvauxpui.dll","dvavulcansupport.dll","VulcanControl.dll","VulcanMessage5.dll"):
    scan_imports(AE/name)
scan_imports(AE/"Plug-ins"/"Extensions"/"CEPManager.aex")

uniq={tuple(r.values()):r for r in rows}
rows=sorted(uniq.values(),key=lambda r:(r["kind"],r["path"],r["host"],r["entry"]))
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["kind","path","host","version","runtime","entry","evidence"]); w.writeheader(); w.writerows(rows)
print("wrote",OUT,"rows",len(rows))
for kind in sorted({r["kind"] for r in rows}): print(kind,sum(r["kind"]==kind for r in rows))
for r in rows:
    if r["kind"]!="pe-import" and r["host"].lower() in {"ae","aeft","aftereffects"}: print(r)
