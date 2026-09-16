from pathlib import Path
p = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie\Artie.cpp")
t = p.read_text(encoding="utf-8-sig")
if "PROBE_LAYER_CONTEXTS" in t and "aeig_probe_contexts" in t:
    print("probe v3 already applied")
    raise SystemExit(0)
t = t.replace("\tbool\t\t\t\taeig_receipt_done\t= false;\n", "", 1)
old = '''\t\tif (item_flags & AEGP_ItemFlag_HAS_VIDEO){ \n\t\t\tif (!aeig_receipt_done) {\n\t\t\t\tAEIG_ArtisanStage("RECEIPT_PROBE_BEGIN", iL, err);\n\t\t\t\tAEIG_ProbeReceiptMatrix(in_dataP, render_contextH, layer_contexts.layer_contexts[iL]);\n\t\t\t\taeig_receipt_done = true;\n\t\t\t\tAEIG_ArtisanStage("RECEIPT_PROBE_END", iL, err);\n\t\t\t}\n\t\t\tERR(Artie_AddPolygonToScene(\tin_dataP,'''
new = '''\t\tif (item_flags & AEGP_ItemFlag_HAS_VIDEO){ \n\t\t\tERR(Artie_AddPolygonToScene(\tin_dataP,'''
assert old in t
t = t.replace(old, new, 1)
old = '''\tif (*cameraPH){\n\t\tERR2(Artie_DisposeCamera(in_dataP, *cameraPH));\n\t\t*cameraPH = NULL;\n\t}\n\treturn err;\n}\n\nstatic A_Err\nArtie_BuildCamera('''
new = '''\treturn err;\n}\n\nstatic A_Err\nArtie_BuildCamera('''
assert old in t
t = t.replace(old, new, 1)
old = '''\tAEGP_MemHandle\t\tsceneH\t\t= NULL;\n\tArtie_LayerContexts\tlayer_contexts;\n\n\tAEFX_CLR_STRUCT(layer_contexts);\n\n\tAEIG_ArtisanStage("RENDER_ENTER", 0, err);'''
new = '''\tAEGP_MemHandle\t\tsceneH\t\t= NULL;\n\tArtie_LayerContexts\tlayer_contexts;\n\tArtie_LayerContexts\taeig_probe_contexts;\n\tA_long\t\t\t\taeig_probe_layers = 0;\n\n\tAEFX_CLR_STRUCT(layer_contexts);\n\tAEFX_CLR_STRUCT(aeig_probe_contexts);\n\n\tAEIG_ArtisanStage("RENDER_ENTER", 0, err);'''
assert old in t
t = t.replace(old, new, 1)
old = '''\tconst bool aeig_trace_began = AEIG_BeginTraceCapture();\n\tAEIG_ArtisanStage("TRACE_BEGIN", aeig_trace_began ? 1 : 0, err);\n\tERR(Artie_BuildCamera(in_dataP, render_contextH, &cameraH));'''
new = '''\tconst bool aeig_trace_began = AEIG_BeginTraceCapture();\n\tAEIG_ArtisanStage("TRACE_BEGIN", aeig_trace_began ? 1 : 0, err);\n\tA_Err aeig_probe_err = Artie_CreateListOfLayerContexts(in_dataP, render_contextH, &aeig_probe_layers, &aeig_probe_contexts);\n\tAEIG_ArtisanStage("PROBE_LAYER_CONTEXTS", aeig_probe_layers, aeig_probe_err);\n\tif (!aeig_probe_err && aeig_probe_layers > 0 && aeig_probe_contexts.count > 0 && aeig_probe_contexts.layer_contexts[0]) {\n\t\tAEIG_ArtisanStage("RECEIPT_PROBE_BEGIN", 0, 0);\n\t\tAEIG_ProbeReceiptMatrix(in_dataP, render_contextH, aeig_probe_contexts.layer_contexts[0]);\n\t\tAEIG_ArtisanStage("RECEIPT_PROBE_END", 0, 0);\n\t}\n\tERR(Artie_BuildCamera(in_dataP, render_contextH, &cameraH));'''
assert old in t
t = t.replace(old, new, 1)
p.write_text(t, encoding="utf-8")
print("probe v3 patch applied")