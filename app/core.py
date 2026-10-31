import difflib
import hashlib
import re
import tempfile
from pathlib import Path
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base, database


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    text: Mapped[str]
    version: Mapped[int]
    active: Mapped[bool]
    digest: Mapped[str]


class Revision(Base):
    __tablename__ = "revisions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    document_id: Mapped[str]
    text: Mapped[str]
    diff: Mapped[str]


class Monitor:
    def __init__(self, url=None):
        self.engine, self.sessions = database(url)

    def update(self, did, text):
        digest = hashlib.sha256(text.encode()).hexdigest()
        with self.sessions.begin() as s:
            d = s.get(Document, did)
            if d and d.digest == digest and d.active:
                return {"changed": False, "version": d.version, "diff": ""}
            old = d.text if d else ""
            version = d.version + 1 if d else 1
            diff = "\n".join(
                difflib.unified_diff(
                    old.splitlines(),
                    text.splitlines(),
                    fromfile=f"{did}:v{version - 1}",
                    tofile=f"{did}:v{version}",
                    lineterm="",
                )
            )
            if d:
                d.text = text
                d.version = version
                d.digest = digest
                d.active = True
            else:
                s.add(Document(id=did, text=text, version=version, digest=digest, active=True))
            s.add(Revision(id=f"{did}:{version}", document_id=did, text=text, diff=diff))
            return dict(changed=True, version=version, diff=diff)

    def retire(self, did):
        with self.sessions.begin() as s:
            d = s.get(Document, did)
            if not d:
                raise ValueError("unknown document")
            d.active = False

    def search(self, query):
        tokens = set(re.findall(r"\w+", query.lower()))
        with self.sessions() as s:
            rows = []
            for d in s.scalars(select(Document).where(Document.active.is_(True))):
                score = len(tokens & set(re.findall(r"\w+", d.text.lower())))
                if score:
                    rows.append(dict(id=d.id, version=d.version, text=d.text, score=score))
            return sorted(rows, key=lambda r: (-r["score"], r["id"]))

    def history(self, did):
        with self.sessions() as s:
            return [
                dict(id=r.id, text=r.text, diff=r.diff)
                for r in s.scalars(select(Revision).where(Revision.document_id == did).order_by(Revision.id))
            ]


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        m = Monitor("sqlite:///" + str(Path(d) / "docs.sqlite"))
        m.update("policy", "Refund window: thirty days.")
        diff = m.update("policy", "Refund window: seven days.")
        current = m.search("refund")
        old = m.search("thirty")
        m.retire("policy")
        return dict(
            diff=diff,
            current=current,
            old_term_results=old,
            after_retirement=m.search("refund"),
            history=m.history("policy"),
        )


def evaluate(mode="fixture"):
    r = demo(mode)
    return dict(passed=not r["old_term_results"] and not r["after_retirement"], scenario=r)
