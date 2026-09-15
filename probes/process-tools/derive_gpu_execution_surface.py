from __future__ import annotations
import csv, re
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
SRC = ROOT / "datasets" / "ae-2025-runtime-export-atlas.csv"
OUT = ROOT / "datasets" / "ae-2025-gpu-execution-surface.csv"
MODULES = {"PF.dll", "BEE.dll", "RG.dll", "GPU.dll", "RendererGPU.dll", "AfterFXLib.dll"}
RULES = [
    ("pf-gpu-frame-bridge", r"CreateGPUEffectWorld|GPUFrameToWorld|GPUFrameUpload|CreateFromIVideoFrame|CreateFromPFWorld|IsEffectWorldGPUBased|MapEffectWorldToPPix"),
    ("pf-device-selection", r"GetCurrentDevice|GetPrimaryMetalDevice|DeviceFrameworkToPFFramework|GetRendererID|SetRendererID|IsRendererGPU|IsEffectAEGPUSDKSupported|IsPixelFormatGPUSupported"),
    ("pf-gpu-memory", r"CanAllocateGPUFrame|PF_GetPixelDataFloatGPU|FreeUpSomeMemory|AllocationFailure"),
    ("gpu-queue-sync", r"CommandQueue|Fence|Semaphore|Wait|Synchron|Barrier|Event"),
    ("gpu-resource-cache", r"AssetCache|ResourceCache|TextureCache|DeviceCache|Purge|Residency|Pinned"),
    ("renderer-gpu", r"RendererGPU|GPURender|GPU_Render|Render.*GPU|GPU.*Render"),
]

def classify(symbol: str) -> str:
    for cat, pat in RULES:
        if re.search(pat, symbol, re.I):
            return cat
    return "gpu-other"

def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    out = []
    for row in rows:
        if row.get("module_name") not in MODULES:
            continue
        symbol = row.get("symbol", "")
        if not re.search(r"GPU|Device|CommandQueue|Fence|Semaphore|Pinned|Purge|Residency", symbol, re.I):
            continue
        item = dict(row)
        item["gpu_category"] = classify(symbol)
        out.append(item)
    out.sort(key=lambda r: (r["gpu_category"], r["module_name"], r["symbol"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        fields = list(out[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(out)
    from collections import Counter
    print("rows", len(out))
    print(Counter(r["gpu_category"] for r in out))

if __name__ == "__main__":
    main()
