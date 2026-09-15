from pathlib import Path
import csv
import hashlib
import re

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
RUN = ROOT / "experiments" / "observatory" / "runs" / "EXP-CORE-001"
DATA = ROOT / "datasets"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def kv_file(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            out[key.strip()] = value.strip()
    return out


def png_hashes(label: str) -> dict[str, str]:
    folder = RUN / f"png-{label}"
    return {p.name: sha256(p) for p in sorted(folder.glob("*.png"))}
def sample_extent(label: str) -> dict[str, object]:
    path = RUN / f"samples-{label}.tsv"
    with path.open("r", encoding="utf-8-sig", errors="replace") as f:
        first = f.readline().strip()
        start_ns = int(first.split("=", 1)[1])
        f.readline()
        lo = None
        hi = None
        rows = 0
        modules = {}
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            elapsed = int(parts[0])
            lo = elapsed if lo is None else min(lo, elapsed)
            hi = elapsed if hi is None else max(hi, elapsed)
            rows += 1
            modules[parts[3]] = modules.get(parts[3], 0) + 1
    return {
        "start_unix_ns": start_ns,
        "sample_min_us": lo,
        "sample_max_us": hi,
        "sample_rows": rows,
        "modules": modules,
    }


def pass_window(label: str, start_ns: int) -> tuple[float, float]:
    meta = kv_file(RUN / f"pass-{label}.txt")
    begin_ns = int(meta["begin"]) * 1_000_000
    end_ns = int(meta["end"]) * 1_000_000
    return (begin_ns - start_ns) / 1000.0, (end_ns - start_ns) / 1000.0
hashes = {label: png_hashes(label) for label in "ABC"}
all_frames = sorted(set().union(*(set(v) for v in hashes.values())))
with (DATA / "exp-core-001-frame-diff.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["frame", "sha_a", "sha_b", "sha_c", "a_eq_b", "b_eq_c", "a_eq_c"])
    for frame in all_frames:
        a = hashes["A"].get(frame, "")
        b = hashes["B"].get(frame, "")
        c = hashes["C"].get(frame, "")
        w.writerow([frame, a, b, c, a == b and bool(a), b == c and bool(b), a == c and bool(a)])

sampler_rows = []
for label in "ABC":
    info = sample_extent(label)
    begin_us, end_us = pass_window(label, info["start_unix_ns"])
    max_us = info["sample_max_us"] or 0
    overlap = not (max_us < begin_us or (info["sample_min_us"] or 0) > end_us)
    sampler_rows.append({
        "pass": label,
        "sample_rows": info["sample_rows"],
        "sample_min_us": info["sample_min_us"],
        "sample_max_us": info["sample_max_us"],
        "render_begin_us": round(begin_us, 3),
        "render_end_us": round(end_us, 3),
        "render_duration_us": round(end_us - begin_us, 3),
        "sampler_overlaps_render": overlap,
        "gap_sample_end_to_render_begin_us": round(begin_us - max_us, 3),
    })
with (DATA / "exp-core-001-sampler-audit.csv").open("w", newline="", encoding="utf-8") as f:
    fields = list(sampler_rows[0].keys())
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(sampler_rows)

same_ab = sum(1 for frame in all_frames if hashes["A"].get(frame) == hashes["B"].get(frame))
same_bc = sum(1 for frame in all_frames if hashes["B"].get(frame) == hashes["C"].get(frame))
same_ac = sum(1 for frame in all_frames if hashes["A"].get(frame) == hashes["C"].get(frame))
print(f"frames={len(all_frames)} A=B:{same_ab} B=C:{same_bc} A=C:{same_ac}")
for row in sampler_rows:
    print(
        f"pass {row['pass']}: samples={row['sample_rows']} "
        f"sample_end={row['sample_max_us']}us render_begin={row['render_begin_us']}us "
        f"overlap={row['sampler_overlaps_render']} gap={row['gap_sample_end_to_render_begin_us']}us"
    )
print("wrote datasets/exp-core-001-frame-diff.csv")
print("wrote datasets/exp-core-001-sampler-audit.csv")
