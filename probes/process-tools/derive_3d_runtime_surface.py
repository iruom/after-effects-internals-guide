from __future__ import annotations
import csv, re, subprocess
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
SRC = ROOT / "datasets" / "ae-2025-runtime-export-atlas.csv"
OUT = ROOT / "datasets" / "ae-2025-3d-runtime-surface.csv"
ADV = Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\Required\Advanced3D.aex")
DUMPBIN = Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\dumpbin.exe")
RULES = [
    ("ae3d-resource-cache", r"BEE_AE3D_.*(?:Cache|Cached|Guid|ResourceGuard|ResourceManager)"),
    ("ae3d-resource-types", r"BEE_AE3D_(?:BasicModel|MeshResource|TextureResource|BasicASMMaterial|ModelInfo|OverriddenModel)"),
    ("parametric-mesh", r"ParametricMesh|MeshOptionsStreamGroup"),
    ("camera-light", r"CameraLayer|CameraOptions|LightLayer|LightOptions|Light.*Stream"),
    ("material-streams", r"Material(?:Atom|Parade|Options|Projection|Scale|Override|Source)|ASM.*Material"),
    ("artisan-bridge", r"Artisan|PR_RenderContext|RenderTextureForArtisan|LayerCapsule"),
]

def classify(symbol: str) -> str:
    for cat, pat in RULES:
        if re.search(pat, symbol, re.I): return cat
    return "3d-other"

def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    out = []
    for row in rows:
        if row.get("module_name") not in {"BEE.dll", "AfterFXLib.dll", "RG.dll", "PF.dll"}:
            continue
        symbol = row.get("symbol", "")
        if not re.search(r"BEE_AE3D|Artisan|ParametricMesh|Camera|Light|Material|MeshOptions", symbol, re.I):
            continue
        item = dict(row); item["surface"] = "export"; item["three_d_category"] = classify(symbol)
        out.append(item)
    if ADV.exists() and DUMPBIN.exists():
        text = subprocess.check_output([str(DUMPBIN), "/imports", str(ADV)], text=True, errors="ignore")
        for line in text.splitlines():
            s = line.strip()
            if re.search(r"BEE_|PF_|PR_RenderContext|Artisan", s):
                out.append({"module":"Required\\Advanced3D.aex","module_name":"Advanced3D.aex","extension":".aex","ordinal":"","hint":"","rva":"","symbol":s,"forwarded_to":"","category":"3d","visibility":"runtime-import","surface":"import","three_d_category":classify(s)})
    out.sort(key=lambda r:(r["three_d_category"],r["module_name"],r["symbol"]))
    with OUT.open("w", newline="", encoding="utf-8") as f:
        fields = list(out[0].keys()); w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(out)
    from collections import Counter
    print("rows",len(out)); print(Counter(r["three_d_category"] for r in out))

if __name__ == "__main__": main()
