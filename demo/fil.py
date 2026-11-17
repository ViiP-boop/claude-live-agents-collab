# demo/fil.py
# ─────────────────────────────────────────────────────────────────────────────
# Le FIL — a tiny HTTP "thread" where Claude Code sessions post their current
# task so the whole mesh can read what everyone is doing, without being spammed.
#
# Pair it with the native SendMessage/ListAgents tools: messages for 1:1 action,
# FIL for 1:N awareness. Together they are the whole protocol used in OLYMPUS.
#
# Run:  pip install fastapi uvicorn && python demo/fil.py
# Then: POST /post, GET /view (see README in this folder).
# ─────────────────────────────────────────────────────────────────────────────
from fastapi import FastAPI
from pydantic import BaseModel
from time import time
from typing import Optional
import uvicorn

app = FastAPI(title="claude-live-agents-collab · le FIL (demo)")

# In-memory ring. Each entry = {"who": "agent-A", "what": "...", "when": epoch}.
FIL: list[dict] = []
MAX = 500


class Post(BaseModel):
    who: str          # session name (keep it human-readable)
    what: str         # one short line about the current task
    tag: Optional[str] = None  # optional label, e.g. "AGON" or "android"


@app.post("/post")
def post(p: Post):
    entry = {"who": p.who, "what": p.what, "tag": p.tag, "when": time()}
    FIL.append(entry)
    if len(FIL) > MAX:
        del FIL[0:len(FIL) - MAX]
    return {"ok": True, "n": len(FIL)}


@app.get("/view")
def view(who: Optional[str] = None, tag: Optional[str] = None, n: int = 20):
    """Return the last `n` entries, optionally filtered by `who` or `tag`.

    This is the 0-token read every session does on wake-up: it sees who is
    doing what, then chooses what (if anything) it needs to pull further.
    """
    rows = FIL
    if who:
        rows = [r for r in rows if r["who"] == who]
    if tag:
        rows = [r for r in rows if r.get("tag") == tag]
    return {"ok": True, "entries": rows[-n:]}


@app.get("/sante")
def sante():
    return {"ok": True, "app": "le FIL (demo)", "entries": len(FIL)}


if __name__ == "__main__":
    # Bind only to loopback: this is a trust-boundary. If you want other
    # machines of the mesh to reach it, put it behind Tailscale or similar.
    uvicorn.run(app, host="127.0.0.1", port=10001)
