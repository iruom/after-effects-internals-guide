from pathlib import Path
import json, os, shutil, tempfile


def atomic_write_bytes(path, data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=str(path.parent))
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    except Exception:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise


def atomic_write_text(path, text, encoding="utf-8"):
    atomic_write_bytes(path,text.encode(encoding))


def recover_file_transaction(journal_dir):
    journal=Path(journal_dir)
    if not journal.exists(): return {"status":"none","restored":0}
    meta_path=journal/"transaction.json"
    if not meta_path.exists():
        shutil.rmtree(journal,ignore_errors=True)
        return {"status":"discarded-unprepared","restored":0}
    meta=json.loads(meta_path.read_text(encoding="utf-8-sig"))
    state=meta.get("state")
    if state=="COMMITTED":
        shutil.rmtree(journal,ignore_errors=True)
        return {"status":"cleaned-committed","restored":0}
    if state!="PREPARED":
        raise RuntimeError(f"unknown transaction journal state: {state!r}")
    restored=0
    for item in meta.get("items",[]):
        path=Path(item["path"])
        if item.get("existed"):
            backup=journal/item["backup"]
            if not backup.exists():
                raise RuntimeError(f"missing transaction backup: {backup}")
            atomic_write_bytes(path,backup.read_bytes())
        else:
            path.unlink(missing_ok=True)
        restored+=1
    shutil.rmtree(journal,ignore_errors=True)
    return {"status":"rolled-back","restored":restored}


class FileTransaction:
    def __init__(self, paths, journal_dir=None):
        self.paths=[Path(p) for p in paths]
        self.journal=Path(journal_dir) if journal_dir else None
        self.recovery=recover_file_transaction(self.journal) if self.journal else {"status":"none","restored":0}
        self.before={p:(p.read_bytes() if p.exists() else None) for p in self.paths}
        self.done=False; self.prepared=False

    def _prepare_journal(self):
        if not self.journal: return
        self.journal.mkdir(parents=True,exist_ok=False)
        items=[]
        for i,(path,data) in enumerate(self.before.items()):
            backup=f"before-{i:03d}.bin"
            if data is not None: atomic_write_bytes(self.journal/backup,data)
            items.append({"path":str(path),"existed":data is not None,"backup":backup})
        meta={"schema":"AEIG-FILE-TRANSACTION-v1","state":"PREPARED","items":items}
        atomic_write_text(self.journal/"transaction.json",json.dumps(meta,indent=2)+"\n")
        self.prepared=True

    def commit(self):
        if self.done: return
        if self.journal and self.prepared:
            meta_path=self.journal/"transaction.json"
            meta=json.loads(meta_path.read_text(encoding="utf-8-sig"))
            meta["state"]="COMMITTED"
            atomic_write_text(meta_path,json.dumps(meta,indent=2)+"\n")
            shutil.rmtree(self.journal,ignore_errors=True)
        self.done=True

    def rollback(self):
        if self.done: return
        for path,data in self.before.items():
            if data is None: path.unlink(missing_ok=True)
            else: atomic_write_bytes(path,data)
        if self.journal: shutil.rmtree(self.journal,ignore_errors=True)
        self.done=True

    def __enter__(self):
        self._prepare_journal()
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False
