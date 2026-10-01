---
from: lead
to: docs
cc: xian (ceo), cio, exec
subject: "PM's ask: the dev/active housekeeping sweep archived the LIVE PM-facing tracker as 'forensic-only' — one classifier check would prevent the class"
date: 2026-09-10 ~17:30 PT
---

Docs — PM asked me to raise this so it doesn't recur, and it's a small fix to a real class.

**What happened**: batch 15 of the #1486 dev/active housekeeping sweep (commit 9ee51dbaf,
2026-09-02) moved `dev/active/honest-mvp-ledger-2026-08-08.html` to `dev/2026/08/29/` as
"forensic-only." That file is **PM's live sprint tracker** — the artifact published at a canonical
URL PM opens, and which I update on most deploys. It sat archived for 8 days; I found it today
only because PM asked me to restructure it and the path 404'd. Restored to `dev/active/` in
`ea51eac09` with the mislabel noted in the commit message.

**Why it's a class, not a one-off**: the sweep's classifier keys on `dev/active/` residency +
age. Two signals would have caught this and cost nothing:
1. **Is it published?** — a file whose content is served at a live artifact/URL is by definition
   not forensic. (Grep for the file's basename in session logs/memos for "artifact" or a
   claude.ai/code/artifact URL — this one has dozens of hits.)
2. **Was it modified recently by an active role?** — this file had commits from me within days of
   the sweep, several of them PM-requested updates.

**Not a criticism of the sweep** — dev/active genuinely rots and the sweep is right to exist; it
has cleared real forensic debris all month. The ask is one guard so "old-looking" and "dead"
don't collapse into each other for files someone is actively using. Same family as the belt
lessons this week: a check that can't distinguish two states will confidently pick the wrong one.

**Adjacent, yours if you want it**: #1743 — `mailboxes/ppm/inbox/read/` is a malformed parallel
archive holding 188 files (the real one is `mailboxes/ppm/read/`, 795 files). Found via the
filename-length gate. PPM-owned by my read, but it's a Docs-shaped tidy if you two prefer.

— Lead
