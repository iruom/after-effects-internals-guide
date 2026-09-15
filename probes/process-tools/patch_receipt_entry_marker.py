from pathlib import Path
p = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie\Artie.cpp")
t = p.read_text(encoding="utf-8-sig")
idx = t.find("EntryPointFunc(")
if idx < 0:
    raise SystemExit("entry not found")
brace = t.find("{", idx)
if brace < 0:
    raise SystemExit("brace not found")
marker = 'AEIG_WriteReceiptRow("ENTRY", -99, -99, -99, 0, -99, 0);'
if marker not in t[idx:idx+1200]:
    t = t[:brace+1] + "\n\t" + marker + t[brace+1:]
    p.write_text(t, encoding="utf-8")
print("patched", p)
