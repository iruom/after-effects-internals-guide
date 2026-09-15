from __future__ import annotations
import csv,re
from pathlib import Path
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
AE=Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
OUT=ROOT/"datasets"/"ae-2025-extension-loader-strings.csv"
FILES=[AE/"AfterFXLib.dll",AE/"dvauxphost.dll",AE/"dvauxpui.dll",AE/"csxsmanager.dll",AE/"PlugPlug.dll",AE/"PlugPlugExternalObject.dll",AE/"Plug-ins"/"Extensions"/"CEPManager.aex"]
KEY=re.compile(r"uxp|cep|csxs|plugplug|extension|plugin|manifest|developer|third.?party|3p|directory|folder|scan|load",re.I)

def strings(data:bytes):
    for m in re.finditer(rb"[ -~]{5,}",data):
        yield "ascii",m.start(),m.group().decode("ascii","ignore")
    for m in re.finditer(rb"(?:[ -~]\x00){5,}",data):
        yield "utf16le",m.start(),m.group().decode("utf-16le","ignore")
rows=[]
for p in FILES:
    if not p.exists(): continue
    data=p.read_bytes()
    for enc,off,s in strings(data):
        if KEY.search(s): rows.append({"module":p.name,"encoding":enc,"offset":off,"text":s[:1200]})
uniq={(r["module"],r["encoding"],r["offset"],r["text"]):r for r in rows}
rows=sorted(uniq.values(),key=lambda r:(r["module"],r["offset"]))
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["module","encoding","offset","text"]); w.writeheader(); w.writerows(rows)
print("wrote",OUT,"rows",len(rows))
for r in rows:
    t=r["text"]
    if re.search(r"manifest|developer|third.?party|3p|plugin.*(dir|path)|extension.*(dir|path)|uxp.*(dir|path)",t,re.I):
        print(r["module"],hex(int(r["offset"])),t[:600])
