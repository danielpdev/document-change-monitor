from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.core import Monitor

app = FastAPI(title="document-change-monitor")


@lru_cache
def service():
    return Monitor()


def guarded(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except PermissionError as e:
        raise HTTPException(403, str(e)) from e
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


class Content(BaseModel):
    text: str = Field(min_length=1, max_length=100000)


@app.post("/api/documents/{did}")
def update_doc(did: str, b: Content):
    return guarded(service().update, did, b.text)


@app.post("/api/documents/{did}/retire")
def retire(did: str):
    guarded(service().retire, did)
    return {"retired": True}


@app.get("/api/search")
def search(q: str):
    return service().search(q)


@app.get("/api/documents/{did}/history")
def history(did: str):
    return service().history(did)
