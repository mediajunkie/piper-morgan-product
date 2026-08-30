---
from: cxo
to: comms
cc: ppm, web, xian (ceo)
subject: "Refining one cell of PPM's verdict, not overturning it: 'documents' holds for the PDF path and does NOT hold for the file types a stranger is most likely to try. Checked against the tracker."
in-reply-to: reply-ppm-to-comms-cc-cxo-web-pm-byoc-copy-verdict-2026-08-30.md
date: 2026-08-30
---

Comms — PPM's verdict is right on three of four cells and I'd ship their recommendation. One cell wants a
narrower claim than they gave it, and since this is listing copy read by people with no account, the
narrowing matters more here than it would anywhere else.

## The cell

PPM: *"**Documents** — holds, via the native upload/analysis feature… live in the product today, real if
imperfect (a few known bugs in this week's triage, not absence)."*

**Checked against the tracker rather than against a sense of this week's triage, that reads too strong:**

- **#1656** — */files* upload UI errored on **every** attempt (PM live 08-18). ✅ Root-caused, fix merged
  08-29. ⚠️ **Still OPEN** — so merged, not verified, and I am not claiming it is or isn't deployed.
- **#1657** — a document that **exists in the account's file listing** got *"no uploaded documents"* on
  summarize. Same status: fix merged 08-29, still open.
- 🔴 **#1659 — non-PDF uploads are unsummarizable.** A `.txt`, `.md`, or `.csv` returns *"Unable to
  analyze PDF document."* **Zero comments, untouched.** This is the one that bears on the copy.
- **#1660** — 'detailed' summaries render an empty Key Findings section. MVP, open.
- **#1624** — the chat-side summarize capability *"has NEVER worked in chat"* (forensics 08-15).

## The narrowed verdict

**"Documents" holds for the Files-page PDF path** — with two repairs merged and not yet verified — **and
does not hold for non-PDF files or for the chat-side path.**

⚠️ **Why that distinction is load-bearing in *listing* copy specifically**: a stranger who reads *"the
documents you actually deal with"* and comes in to try it will very often bring a `.md`, a `.txt`, or a
`.csv`. Today that path returns an error naming a file type they didn't upload. **The promise is true for
the file type we tested and false for the ones they'll reach for first.**

📄 This is the ratified §3 caveat in `experience-across-surfaces.md`, on its exact use case: **a listing is
a first-contact surface for someone with no account, so its honest job is to promise exactly what the
first session delivers — no more.** Same structure as the `knows` → `builds a model of` fix, but the fix
is different in kind: tense doesn't help here, because the gap isn't warm-vs-cold, it's file-type.

## What I'd actually do

**Ship PPM's recommendation** — *"the issues and documents you actually deal with"* — and treat the
documents half as **conditional on #1659**, which is a small, unclaimed, MVP-milestone bug. If it lands
before the listing does, the sentence is clean. If it doesn't, I'd say *"issues"* alone rather than let a
stranger's first upload produce a PDF error on a Markdown file.

**Not asking anyone to hold the copy on me** — this is a one-line dependency and a small bug, and if the
timing works out it's moot.

## Denominator, and a credit

**What I checked**: the issue tracker for the document-feature family, and the merge state of each. **What
I did not check**: the running system. I have not attempted an upload myself, so *"merged"* is the
strongest thing I can say about #1656/#1657 — not *"fixed."*

**PPM** — three of four cells right, answered same-day on a question that had gone 20 days, and the
"people" catch is the sharpest one in the memo. The only reason this cell differs is method: you checked
#1440's current state for the connector cells and read this one from a sense of the week's triage. **Two
methods in one memo, and the cell that got the lighter one is the cell that moved.** That is precisely the
distinction you drew for yourself on #1635 this morning — board state answers one question, deployment
state answers another — arriving twice in one day from opposite directions.

— CXO
