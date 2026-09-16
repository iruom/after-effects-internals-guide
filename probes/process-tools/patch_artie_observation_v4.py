from pathlib import Path
base=Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie")
# Apply after v3. Keep raw software count, but use the layer's real effect count when the Canvas API returns a negative sentinel.
p=base/'AEIGTraceCapture.h'; t=p.read_text(encoding='utf-8-sig')
old='g_aeig_trace.traceFd = _open_osfhandle((intptr_t)h, _O_APPEND | _O_TEXT);'
new='g_aeig_trace.traceFd = _open_osfhandle((intptr_t)h, _O_WRONLY | _O_APPEND | _O_TEXT);'
if old in t: t=t.replace(old,new,1)
elif new not in t: raise SystemExit('trace fd patch point missing')
p.write_text(t,encoding='utf-8')
p=base/'AEIGReceiptProbe.h'; t=p.read_text(encoding='utf-8-sig')
old='''    A_short num_effects = 0;\n    A_Err err = suites.CanvasSuite8()->AEGP_GetNumberOfSoftwareEffects(\n        render_contextH, layer_contextH, &num_effects);\n    AEIG_WriteReceiptRow("COUNT", num_effects, -99, -99, 0, -99, err);\n    if (err) return;\n\n    A_short capped = num_effects;'''
new='''    A_short software_effects = 0;\n    A_Err err = suites.CanvasSuite8()->AEGP_GetNumberOfSoftwareEffects(\n        render_contextH, layer_contextH, &software_effects);\n    AEIG_WriteReceiptRow("SOFTWARE_COUNT", software_effects, -99, -99, 0, -99, err);\n    AEGP_LayerH layerH = nullptr; A_long layer_effects = -1;\n    A_Err layer_err = suites.CanvasSuite5()->AEGP_GetLayerFromLayerContext(render_contextH, layer_contextH, &layerH);\n    if (!layer_err && layerH) layer_err = suites.EffectSuite5()->AEGP_GetLayerNumEffects(layerH, &layer_effects);\n    AEIG_WriteReceiptRow("LAYER_COUNT", layer_effects, -99, -99, 0, -99, layer_err);\n    if (err && layer_err) return;\n    A_short num_effects = software_effects >= 0 ? software_effects : (A_short)((layer_effects >= 0 && layer_effects < 32767) ? layer_effects : 0);\n    AEIG_WriteReceiptRow("COUNT", num_effects, -99, -99, 0, -99, 0);\n\n    A_short capped = num_effects;'''
if old in t: t=t.replace(old,new,1)
elif 'SOFTWARE_COUNT' not in t: raise SystemExit('receipt fallback patch point missing')
p.write_text(t,encoding='utf-8')
print('probe v4 patch present')
