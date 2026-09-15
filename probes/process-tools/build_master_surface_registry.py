from pathlib import Path
from datetime import date
import csv
from collections import Counter
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; OUT=DATA/"ae-master-surface-registry.csv"
STATUS=ROOT/"docs"/"reference"/"master-surface-registry.md"
FIELDS=['surface_class','support_class','host_scope','version','name','kind','container','source','evidence','contract_boundary','notes']
rows=[]
def add(**kw): rows.append({k:str(kw.get(k,'')) for k in FIELDS})
def read(fn):
    with (DATA/fn).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def cpp_support(v):
    return {
      'official-public-guide':'documented-public',
      'public-distributed':'distributed-public',
      'historical-compat-distributed':'distributed-historical-compat',
      'cross-host-distributed':'distributed-cross-host',
      'private-gate-reference':'private-boundary-reference',
      'thirdparty-historical-archive':'historical-thirdparty-snapshot',
    }.get(v,'inventory-only')
for r in read('ae-api-symbol-atlas.csv'):
    add(surface_class='native-cpp',support_class=cpp_support(r['visibility']),host_scope='After Effects/shared-host where noted',version=r['version'],name=r['symbol'],kind=r['kind'],container=r['container'],source=f"{r['source']}:{r['line']}",evidence=r['visibility'],contract_boundary='name/layout inventory; support depends on visibility+host scope',notes=r['notes'])
for r in read('ae-script-expression-api-atlas.csv'):
    cls='scripting' if r['surface']=='scripting-docs' else 'expressions'
    add(surface_class=cls,support_class='documented-public',host_scope='After Effects',version='current-docs',name=r['symbol'],kind=r['kind'],container=r['container'],source=r['source'],evidence=r['evidence'],contract_boundary='documented language/DOM surface; runtime reflection may differ')
for r in read('ae-2025-runtime-internal-surface.csv'):
    add(surface_class='runtime-internal-export',support_class='runtime-visible-unsupported',host_scope='After Effects installed build',version='AE 2025',name=r['symbol'],kind=r['category'],container=r['module_name'],source=r['module'],evidence=r['visibility'],contract_boundary='PE export visibility is not a third-party support contract',notes=r['forwarded_to'])
for r in read('ae-sdk-25.6-private-gates.csv'):
    add(surface_class='private-header-boundary',support_class='private-boundary-reference',host_scope='After Effects',version='25.6',name=r['gate'],kind=r['directive'],container=r['header'],source=f"{r['header']}:{r['line']}",evidence='distributed-header gate',contract_boundary='proves private extension boundary, not private layouts',notes=r['private_includes'] or r['opaque_public_types'])
for r in read('ae-2025-extension-substrates.csv'):
    if r['kind']=='pe-import':
        entry=r['entry'].strip()
        dumpbin_meta=('Dump of file','time date stamp','Import Address Table','Import Name Table','Index of first forwarder reference','Characteristics','Unload Import Name Table','Address of HMODULE','Bound Import Name Table')
        if not entry or any(token.lower() in entry.lower() for token in dumpbin_meta):
            continue
    cls='cep' if r['kind']=='cep-csxs-manifest' else 'uxp' if r['kind']=='uxp-manifest' else 'extension-native-bridge'
    support='manifest-declared-host-surface' if 'manifest' in r['kind'] else 'runtime-visible-bridge'
    if r['entry']:
        label=r['entry']; label_note=''
    else:
        label=f"{Path(r['path']).parent.name}:{r['host'] or 'shared'}"; label_note='search label derived from manifest directory + host because no UI entry point is declared'
    add(surface_class=cls,support_class=support,host_scope=r['host'] or 'shared Adobe host runtime',version=r['version'],name=label,kind=r['kind'],container=r['runtime'],source=r['path'],evidence=r['evidence'],contract_boundary='manifest/runtime evidence; third-party support depends on host contract',notes=label_note)
for r in read('ae-debug-trace-lineage.csv'):
    add(surface_class='diagnostic-observability',support_class='diagnostic-hidden',host_scope='After Effects',version=f"{r['first_seen']}..{r['last_seen']}",name=r['name'],kind=f"{r['channel']}:{r['kind']}",container='',source='Debug/Trace Database lineage',evidence=f"versions={r['version_count']}",contract_boundary='diagnostic vocabulary, not plug-in API',notes=r['value_default_variants'])
for r in read('ae-plugin-capability-frontier.csv'):
    add(surface_class='capability',support_class=r['status'],host_scope=r['host_scope'],version=r['min_version'],name=r['capability'],kind=r['maturity'],container='',source=r['public_route'],evidence=r['internal_evidence'],contract_boundary=r['context_constraints'],notes=f"cache={r['cache_dependency_safety']}; risk={r['risk']}; next={r['next_probe']}")
for r in read('ae-2025-headless-entrypoint.csv'):
    add(surface_class='headless-command-runtime',support_class='runtime-observed',host_scope='After Effects headless/controller',version='AE 2025',name=r['entry'],kind=r['relation'],container=r['source'],source='ae-2025-headless-entrypoint.csv',evidence='binary/runtime inventory',contract_boundary='entry/dependency surface; supported CLI semantics documented separately')
for r in read('ae-cc2015-panel-sdk-surface.csv'):
    add(surface_class='historical-cep',support_class='distributed-historical-public-sample',host_scope='AEFT/PPRO where manifest declares',version='CC 2015 / AE 13.x',name=r['name'],kind=r['kind'],container=r['path'],source='CC 2015 Panel SDK sample',evidence=r['evidence'],contract_boundary='historical CSXS/CEP sample contract',notes=r['value'])
for r in read('ae-suite-negotiation-matrix.csv'):
    suite_label=r['suite_macro_base'] or r['family']
    label_note='' if r['suite_macro_base'] else 'search label derived from family because no suite macro base exists for this compatibility row; '
    add(surface_class='suite-negotiation',support_class='distributed-public-contract',host_scope='After Effects/shared host where suite applies',version=r['generation'],name=suite_label,kind=r['family'],container=f"PICA={r['pica_version']}",source=r['source'],evidence='distributed header + structural comparison',contract_boundary=r['recommended_dispatch'],notes=f"{label_note}relation={r['pica_relation']}; prefix_safe={r['adjacent_prefix_safe']}; {r['header_comment']}")
rows.sort(key=lambda r:(r['surface_class'],r['name'],r['version'],r['source']))
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
by_surface=Counter(r['surface_class'] for r in rows); by_support=Counter(r['support_class'] for r in rows)
lines=['---','status: generated',f'last_verified: {date.today().isoformat()}','---','# Master Surface Registry','',
       'This registry normalizes discoverable AEIG API/capability/diagnostic surfaces without collapsing their support boundaries. Runtime exports and diagnostic names are not promoted to public API merely because they are visible.','',
       f'Total normalized rows: **{len(rows):,}**. Surface classes: **{len(by_surface)}**. Support classes: **{len(by_support)}**.','',
       '## By surface class','']
for k,v in by_surface.most_common(): lines.append(f'- `{k}`: **{v:,}**')
lines += ['','## By support class','']
for k,v in by_support.most_common(): lines.append(f'- `{k}`: **{v:,}**')
lines += ['','The machine-readable source is `datasets/ae-master-surface-registry.csv`. Capability maturity remains governed by `datasets/ae-plugin-capability-frontier.csv`; this registry is an inventory/index, not a support guarantee.']
STATUS.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('rows',len(rows),'surfaces',dict(by_surface)); print('wrote',OUT); print('wrote',STATUS)
