from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request
from pathlib import Path

REPO=Path(r"D:\Developer\After Effects Internals Guide")
DEST=REPO/"research"/"external-sources"/"ae-sdk-cs6"/"Headers"
META=REPO/"research"/"external-sources"/"ae-sdk-cs6"/"provenance.json"
API="https://api.github.com/repos/takahirome/AdobeScripts/contents/SDK/Adobe%20After%20Effects%20CS6%20Mac%20SDK/Examples/Headers?ref=master"

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"AEIG-research"})
    return json.loads(urllib.request.urlopen(req,timeout=30).read().decode("utf-8"))

def get_bytes(url):
    req=urllib.request.Request(url,headers={"User-Agent":"AEIG-research"})
    return urllib.request.urlopen(req,timeout=30).read()
def main():
    DEST.mkdir(parents=True,exist_ok=True)
    entries=get_json(API)
    manifest=[]
    for e in entries:
        if e.get("type")!="file" or not e["name"].lower().endswith((".h",".hpp")):
            continue
        data=get_bytes(e["download_url"])
        path=DEST/e["name"]
        path.write_bytes(data)
        manifest.append({"name":e["name"],"sha":e.get("sha",""),"sha256":hashlib.sha256(data).hexdigest(),"source":e["html_url"]})
    meta={
        "snapshot":"Adobe After Effects CS6 Mac SDK headers",
        "evidence_class":"third-party historical archive",
        "source_repository":"https://github.com/takahirome/AdobeScripts",
        "api_listing":API,
        "downloaded_utc":"2026-09-15",
        "files":manifest,
    }
    META.parent.mkdir(parents=True,exist_ok=True)
    META.write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print("downloaded",len(manifest),"headers to",DEST)
    print("wrote",META)

if __name__=="__main__": main()
