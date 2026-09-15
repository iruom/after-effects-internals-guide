from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def flat_formats(model: dict) -> str:
    parts = []
    for f in model.get("available_formats", []):
        parts.append(f"{f.get('format')}:{f.get('variant')}:{f.get('supported_devices')}")
    return "|".join(parts)


def tensor_sig(items: list[dict]) -> str:
    out = []
    for x in items:
        shape = "x".join(str(v) for v in x.get("tensor_shape", []))
        out.append(f"{x.get('feature_name')}:{x.get('tensor_data_type')}[{shape}]")
    return "|".join(out)


def load_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def rows(registry: dict, label: str):
    for name, m in sorted(registry.items()):
        yield {
            "source": label,
            "model_key": name,
            "file_name": m.get("file_name", ""),
            "model_version": m.get("model_version", ""),
            "module_name": m.get("module_name", ""),
            "module_uuid": m.get("module_uuid", ""),
            "module_bundle_type": m.get("module_bundle_type", ""),
            "supports_batching": m.get("supports_batching", ""),
            "memory_consumption_mb": m.get("memory_consumption_mb", ""),
            "seconds_to_live": m.get("seconds_to_live", ""),
            "formats": flat_formats(m),
            "inputs": tensor_sig(m.get("model_inputs", [])),
            "outputs": tensor_sig(m.get("model_outputs", [])),
        }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", action="append", nargs=2, metavar=("LABEL", "PATH"), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    all_rows = []
    for label, raw_path in args.registry:
        all_rows.extend(rows(load_registry(Path(raw_path)), label))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(all_rows[0].keys()) if all_rows else []
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_rows)

    print(f"wrote {len(all_rows)} rows -> {out}")


if __name__ == "__main__":
    main()
