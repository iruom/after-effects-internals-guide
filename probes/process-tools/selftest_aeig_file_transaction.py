from pathlib import Path
import tempfile
from aeig_file_transaction import FileTransaction, atomic_write_text, recover_file_transaction

checks=[]
def check(name, ok):
    checks.append((name,bool(ok))); print("PASS" if ok else "FAIL",name)

with tempfile.TemporaryDirectory() as td:
    root=Path(td); a=root/"a.txt"; b=root/"b.txt"
    a.write_text("old-a",encoding="utf-8")
    try:
        with FileTransaction([a,b]):
            atomic_write_text(a,"new-a")
            atomic_write_text(b,"new-b")
            raise RuntimeError("synthetic failure")
    except RuntimeError:
        pass
    check("rollback-restores-existing",a.read_text(encoding="utf-8")=="old-a")
    check("rollback-removes-new",not b.exists())

    with FileTransaction([a,b]):
        atomic_write_text(a,"commit-a")
        atomic_write_text(b,"commit-b")
    check("commit-existing",a.read_text(encoding="utf-8")=="commit-a")
    check("commit-new",b.read_text(encoding="utf-8")=="commit-b")

    journal=root/"pending-journal"; c=root/"c.txt"
    tx=FileTransaction([a,c],journal_dir=journal); tx.__enter__()
    atomic_write_text(a,"crash-a"); atomic_write_text(c,"crash-c")
    recovery=recover_file_transaction(journal)
    check("crash-recovery-status",recovery["status"]=="rolled-back" and recovery["restored"]==2)
    check("crash-recovery-restores-existing",a.read_text(encoding="utf-8")=="commit-a")
    check("crash-recovery-removes-new",not c.exists())
    check("crash-recovery-cleans-journal",not journal.exists())

    with FileTransaction([a,c],journal_dir=journal):
        atomic_write_text(a,"journal-commit-a"); atomic_write_text(c,"journal-commit-c")
    check("journal-commit-existing",a.read_text(encoding="utf-8")=="journal-commit-a")
    check("journal-commit-new",c.read_text(encoding="utf-8")=="journal-commit-c")
    check("journal-commit-cleans-journal",not journal.exists())

passed=all(ok for _,ok in checks)
print("AEIG FILE TRANSACTION SELFTEST:","PASS" if passed else "FAIL")
raise SystemExit(0 if passed else 2)
