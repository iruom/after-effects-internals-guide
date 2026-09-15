from pathlib import Path
import subprocess, csv, re
ROOT = Path(r"D:\Developer\After Effects Internals Guide")
AE = Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
DUMPBIN = Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\dumpbin.exe")
MODULES = ["ColorSpaceConverter.dll", "OCIOWrapper.dll", "COR.dll"]
TERMS = re.compile(r"Color|OCIO|ICC|ACE|Gamma|Linear|Transfer|Display|Scene|Luminance|ConvertFrame|RenderIntent", re.I)
rows=[]
for module in MODULES:
    p = AE / module
    exp = subprocess.run([str(DUMPBIN), "/exports", str(p)], capture_output=True, text=True, errors="replace").stdout
    for line in exp.splitlines():
        if TERMS.search(line): rows.append({"module":module,"relation":"export","entry":line.strip()})
    deps = subprocess.run([str(DUMPBIN), "/dependents", str(p)], capture_output=True, text=True, errors="replace").stdout
    for line in deps.splitlines():
        s=line.strip()
        if s.lower().endswith('.dll'):
            rows.append({"module":module,"relation":"depends","entry":s})
out = ROOT / "datasets" / "ae-2025-color-pipeline-symbols.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=["module","relation","entry"])
    w.writeheader(); w.writerows(rows)
print("wrote", out, "rows", len(rows))
for m in MODULES:
    print(m, sum(r['module']==m and r['relation']=='export' for r in rows), 'matched exports')
# Major AE consumers of the shared conversion modules.
for consumer in ["BEE.dll","PF.dll","VideoRenderer.dll","AfterFXLib.dll","aelib.dll","DisplaySurface.dll"]:
    p = AE / consumer
    deps = subprocess.run([str(DUMPBIN), "/dependents", str(p)], capture_output=True, text=True, errors="replace").stdout
    for line in deps.splitlines():
        s=line.strip()
        if s in {"ColorSpaceConverter.dll","OCIOWrapper.dll","COR.dll","ACEWrapper.dll","MediaFoundation.dll","VideoFrame.dll","GPUFoundation.dll","dvamediatypes.dll"}:
            rows.append({"module":consumer,"relation":"depends-color-substrate","entry":s})
# Rewrite after consumer inventory is added.
with out.open("w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=["module","relation","entry"])
    w.writeheader(); w.writerows(rows)
print("consumer edges", sum(r['relation']=='depends-color-substrate' for r in rows))
