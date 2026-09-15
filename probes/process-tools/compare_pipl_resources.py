from pathlib import Path
import pefile, struct, binascii

def blobs(path):
    p=pefile.PE(str(path), fast_load=True)
    p.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
    out=[]
    for typ in p.DIRECTORY_ENTRY_RESOURCE.entries:
        name=typ.name.string.decode(errors='ignore') if typ.name else ''
        if name.upper()!='PIPL': continue
        for ent in typ.directory.entries:
            for lang in ent.directory.entries:
                d=lang.data.struct; off=p.get_offset_from_rva(d.OffsetToData)
                out.append(p.__data__[off:off+d.Size])
    return out

def props(b):
    n=struct.unpack_from('<I',b,6)[0]; pos=10; out=[]
    for _ in range(n):
        vendor=b[pos:pos+4][::-1].decode('latin1'); key=b[pos+4:pos+8][::-1].decode('latin1')
        pid,ln=struct.unpack_from('<II',b,pos+8); pos+=16
        val=b[pos:pos+ln]; pos+=ln
        out.append((vendor,key,pid,val))
    return out
paths=[
 ('old25-artie',Path(r'C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\Plug-ins\sdk_old\AEGP\Artie.aex')),
 ('new25-artie',Path(r'D:\Developer\After Effects Internals Guide\experiments\observatory\runs\EXP-CACHE-002\probe-build\AEGP\Artie.aex')),
 ('old25-twiddler',Path(r'C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\Plug-ins\sdk_old\AEGP\Text_Twiddler.aex')),
 ('new25-twiddler',Path(r'D:\Developer\After Effects Internals Guide\experiments\observatory\runs\EXP-CACHE-002\twiddler-build\AEGP\Text_Twiddler.aex')),
 ('ae26-fxconsole',Path(r'D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\VideoCopilot\FXConsole.aex')),
 ('ae26-labelmaker',Path(r'D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\Plugin Everything\Label Maker.aex')),
]
for label,p in paths:
    print('\n##',label,p)
    bs=blobs(p); print('blobs',len(bs),[len(x) for x in bs])
    for i,b in enumerate(bs):
        print('blob',i,'hex',binascii.hexlify(b).decode())
        for vendor,key,pid,val in props(b):
            printable=''.join(chr(x) if 32<=x<127 else '.' for x in val)
            print(f' {vendor}:{key} id={pid} len={len(val)} hex={val.hex()} ascii={printable}')
