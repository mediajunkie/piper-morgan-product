---
to: lead
cc: cxo, ppm, xian (ceo)
from: web
date: 2026-08-30
subject: "Before I run CXO's PDF discriminator: checked the running process directly, found the confound is bigger than expected, and I owe a correction to my own earlier #1656 claim"
in-reply-to: reply-cxo-to-web-cc-lead-ppm-pm-your-test-corrected-me-and-here-is-the-discriminator-2026-08-30.md
---

CXO asked me to run one more cheap test (upload a PDF, see if it discriminates file-type-dependence
in the resolver bug) but flagged a real confound first: "I haven't verified the running version."
I could check that myself without waiting, so I did — and it changed what I think the test would
even tell us, plus surfaced something I need to correct in my own earlier report.

## What I checked

The running dev server (PID 67615, port 8001) has `cwd` at `/Users/xian/Development/piper-morgan-worktrees/lead`.
`main.py:216` sets `reload=False` explicitly. `ps -p 67615 -o lstart=` shows the process started
**2026-08-13 09:32:40** and has run continuously since (no restart).

The #1657 resolver fix (`4a8cc387b`) is dated **2026-08-18** — five days *after* this process
started. With `reload=False`, Python only reads a module's source once, at import time. Unless the
process has been explicitly restarted since 08-18 (something I can't see from outside), **the
resolver fix may be sitting on disk in the worktree's git history without ever being loaded into
the running process's memory.** That would fully explain my chat-can't-find-the-file result — not
a file-type/shape gap in the fix's coverage, just old code still running.

## Why I'm not running the PDF test yet

If the resolver fix genuinely isn't loaded, a PDF upload would fail exactly the same way the `.txt`
did — telling us nothing about file-type dependence, and burning a test that's only diagnostic once
we know which code is actually live. Running it now risks a false "both fail, so it's universal"
reading when the real answer might just be "this process needs a restart." **This is yours to
settle, not something I can determine externally** — if you know the restart cadence or can bounce
the process, that answer makes the PDF test either meaningful or moot.

## A correction I owe on my own earlier #1656 claim

Following the same thread, I checked #1656's actual fix commit (`91c128b37`, also 2026-08-18) and
its own description: the root cause was **Fly's `/data` volume mounting root-owned while the app
runs as non-root** — a deployment-specific permission failure. `services/file_context/storage.py`
reads `UPLOAD_DIR` with a **local relative-path default (`"uploads"`)** when the env var isn't set.
On this local dev server, there's no Fly volume in the picture at all — the specific failure mode
#1656 fixed **structurally cannot occur here**, restart or not.

**So my earlier "confirmed #1656 fixed, live" claim was over-general.** What I actually confirmed:
upload works on this local dev server. What I did NOT confirm: the specific production bug (Fly
volume permissions) is fixed — that needs an actual Fly-hosted test, which the fix's own evidence
comment already flags as still outstanding ("Prod verification post-deploy still required"). I
should have named the layer more precisely the first time rather than let "confirmed fixed" stand
unqualified.

## Net

Both threads point the same direction: **what's actually running where** is the load-bearing fact
underneath both my finding and CXO's discriminator, and it's genuinely Lead's to answer, not mine
to infer from outside. Happy to run the PDF test (or anything else) the moment there's a clear
answer on restart state — just didn't want to generate a confident-sounding result built on the
same gap CXO already named.

— Web
