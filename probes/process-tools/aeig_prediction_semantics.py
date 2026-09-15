def all_true(mapping):
    return bool(mapping) and all(bool(v) for v in mapping.values())

def any_true(mapping):
    return bool(mapping) and any(bool(v) for v in mapping.values())

def pred004(prefix_ok):
    return "confirmed" if prefix_ok else "refuted"

def pred005(receipt_stable):
    return "confirmed" if receipt_stable else "refuted"

def pred006(target_groups_complete, target_present):
    if all_true(target_groups_complete): return "confirmed"
    if not any_true(target_present): return "refuted"
    return "inconclusive"

def pred007(identity_present, footprint_changed):
    if not all_true(identity_present): return "inconclusive"
    return "confirmed" if footprint_changed else "refuted"

def pred008(rg_cache_present, footprint_changed):
    if not all_true(rg_cache_present): return "inconclusive"
    return "confirmed" if footprint_changed else "refuted"
def pred009(plugin_complete, family_specific):
    if not plugin_complete: return "inconclusive"
    return "confirmed" if family_specific else "refuted"

def pred010(plugin_complete, family_specific):
    if not plugin_complete: return "inconclusive"
    return "confirmed" if family_specific else "refuted"
