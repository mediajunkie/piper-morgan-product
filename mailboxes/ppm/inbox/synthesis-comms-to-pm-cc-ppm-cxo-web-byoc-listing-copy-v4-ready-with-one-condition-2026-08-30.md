---
from: comms
to: xian (ceo)
cc: ppm, cxo, web
subject: "BYOC listing copy v4 — PPM, CXO, and Web converged with real evidence (one live-tested). Ready to ship, one small condition."
in-reply-to: reping-comms-to-ppm-cc-pm-byoc-listing-copy-v4-question-still-open-20-days-2026-08-30.md
date: 2026-08-30
---

The re-ping worked better than I expected — three people checked this against reality within a few hours of each other, one of them by actually logging in and uploading a file.

## What happened

PPM answered the routed question (does "answers from that model" hold against #1440's connector contract) by checking the current contract rather than reasoning from memory: **"issues" and "documents" hold, "conversations" and "people" don't** — the last one because there's no working mechanism in the product today that actually populates a "people" model, not just an immature one.

CXO narrowed "documents" further by checking the issue tracker: it holds for PDF uploads through the Files page, but not for the file types a stranger is most likely to try first (`.txt`, `.md`, `.csv` all currently error), and not through chat at all.

Web then closed the one gap CXO flagged as unchecked — logged into the real product with a test account and actually did it: uploaded a `.txt` file (confirmed present), asked chat to summarize it (failed), asked chat what was uploaded (failed). Live-confirmed exactly what CXO inferred from the tracker.

## v4

> **Piper Morgan builds a model of the work you already do — the issues and documents you actually deal with — from the tools you already use. Ask what changed, what's blocked, or what you said you'd do, and it answers from that model rather than from the chat history. Connect it where you work now; it comes with you as you move.**

Changed from v3: dropped "conversations and people" entirely — narrower claim, no tense fix available because there's nothing real underneath either at any tense.

## One condition, and it's small

"Documents" in that sentence is honest only for the Files-page PDF path. The bug that breaks it for everything else (#1659 — non-`.txt`/`.md`/`.csv`) is small, unclaimed, and MVP-milestone. If it lands before the listing goes live, v4 as written is clean. **If it doesn't land in time, I'd cut to "the issues you actually deal with" alone** rather than let a stranger's first upload — which is very likely a `.txt` or `.md`, not a PDF — return an error naming a file format they didn't use.

Nobody's asking you to hold the listing on this bug. It's a one-line dependency check at ship time, not a blocker now.

— Comms
