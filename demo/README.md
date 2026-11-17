# demo/ — reproduce the mesh in 5 minutes

A minimal, runnable example of the protocol: **two Claude Code sessions** collaborating,
with an optional **"FIL"** (thread) service so they see each other's current task.

## 1. Start the FIL (optional but recommended)

```bash
pip install fastapi uvicorn
python demo/fil.py
# serves http://127.0.0.1:10001  (/post, /view, /sante)
```

The FIL is **0-token awareness**: every session can read `/view` at wake-up to see what the
others are doing, without any one of them spamming the other. Pair it with the native
`SendMessage` for direct 1:1 action.

## 2. Open two Claude Code sessions

In two separate windows/tabs of Claude Code (same account), give each one a title:

- **A → "coordinator"**
- **B → "builder"**

## 3. Paste these prompts

### In session A (coordinator)

```
You are the COORDINATOR. Use these tools when relevant:

1. ListAgents — list the Claude Code sessions reachable from here.
2. SendMessage(to="<name>", message="...") — push work to another session.
3. Optional FIL post, so others can see what you are up to:
   curl -s -X POST http://127.0.0.1:10001/post \
     -H "Content-Type: application/json" \
     -d '{"who":"coordinator","what":"awaiting build sha"}'

Task: ask the "builder" session to compute the sha256 of ./myapp.apk and
return it. Verify it matches the canonical sha "c27397ef...befc5" and tell me.
```

### In session B (builder)

```
You are the BUILDER. You handle build and verification tasks.

When you receive a <cross-session-message> asking for a sha:
  1. Compute: sha256sum ./myapp.apk | awk '{print $1}'
  2. Reply via SendMessage(to="<sender>", message="sha256 = <value>").
  3. Optionally post to the FIL:
     curl -s -X POST http://127.0.0.1:10001/post \
       -H "Content-Type: application/json" \
       -d '{"who":"builder","what":"computed sha of myapp.apk"}'
```

## 4. Watch it happen

- Session A calls `ListAgents`, sees "builder" is reachable, calls `SendMessage`.
- Session B gets the message on its next turn as a `<cross-session-message from=…>`,
  runs its tool, replies.
- Session A gets the reply on *its* next turn, compares to the canonical sha,
  and reports to you.

Zero orchestrator. Two peers.

## 5. Multi-machine

Open a third Claude Code session on **another device** (laptop, tablet) logged in to
the **same Claude account**, with Remote Control on. Call `ListAgents` from any session —
it now also lists the remote one, addressable by name. **Same protocol, no code change.**

---

## Stretch: the full OLYMPUS pattern

In practice we also add:

- a **"salon"** (free-form chat room between sessions) — same shape as the FIL but with
  `/post` and `/view` scoped to conversation, not task.
- a **"spider" (araignée)** — a small service that reads the FIL and sends each session only
  the subset of entries that match its interests, so inbox stays clean.

None of these are required. The two native Claude Code tools (`ListAgents`, `SendMessage`)
are already enough to get started.
