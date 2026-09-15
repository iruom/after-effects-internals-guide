from __future__ import annotations
import argparse, csv, re
from pathlib import Path

ASCII_RE = re.compile(rb"[ -~]{5,}")


def iter_ascii(data: bytes):
    for m in ASCII_RE.finditer(data):
        try:
            yield m.start(), m.group().decode("ascii")
        except UnicodeDecodeError:
            pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("binary")
    ap.add_argument("--keyword", action="append", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    path = Path(args.binary)
    data = path.read_bytes()
    needles = [k.lower() for k in args.keyword]

    rows = []
    for offset, text in iter_ascii(data):
        low = text.lower()
        hits = [k for k in needles if k in low]
        if hits:
            rows.append({
                "binary": path.name,
                "offset_dec": offset,
                "offset_hex": hex(offset),
                "keywords": "|".join(hits),
                "string": text,
            })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["binary", "offset_dec", "offset_hex", "keywords", "string"])
        w.writeheader()
        w.writerows(rows)
    print(f"matched {len(rows)} strings -> {out}")


if __name__ == "__main__":
    main()
