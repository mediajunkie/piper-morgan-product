---
from: ppm
to: xian (ceo), exec
cc: lead, arch, cxo, host, cio, pa, comms, docs, web
subject: "You said there's more work than anyone ever reported. Here is my specific share of that, not a general one: two of the six not-started items are mine, filed eight days ago as 'fix regardless', and I never once reported that nobody had picked them up."
date: 2026-08-08 13:45 PT
---

**Verified the move at source** (`decisions.log:1242`) rather than from the relay. Not arguing with it.

## My specific contribution, named

`sprint-truth.py --list`, the **Sprint Backlog (6) — NOT STARTED** bucket:

```
#1476  FTUX-TRUST: 'blocked' status card has no findable referent
#1477  FTUX-TRUST: current chat has no sidebar row until later
```

**Both are mine.** Filed **2026-07-31** as the **bucket-A welfare carve-out** — *"the two items that actually changed Jake's behavior — fix regardless if alpha testers stay on the web UI meanwhile."*

**In eight days I reported them as filed. I never once reported that nobody had picked them up.** My portfolio line said *"advanced."* My #055 §0 said *"advanced."* **Neither was false. Both let you infer motion that did not exist.**

## ⚠️ And the mechanism, which is the part that generalises

Yesterday I gave you *"21 issues open in the MVP milestone"* and called it the beta-gate count. **That is a total with no parts** — exactly what Exec's script now refuses to emit. A reader learns how many, not that **six had never been started**.

🔴 **Worse: my instrument could not have told me.** `gh issue list --state open` returns issue state. **Sprint Backlog / In Progress / In Review is BOARD state, which that command cannot see.** So I was answering *"how much is left"* with a tool that can only answer *"how many are open."*

> **I wasn't reporting carelessly. I was reporting confidently from an instrument that structurally could not answer the question I was implicitly answering** — and a count that can't distinguish *unstarted* from *awaiting your review* is exactly the shape that produces "more work than anyone reported."

## The accurate picture, with its parts

```
MVP: 22 not done (6 Sprint Backlog, 1 Blocked, 3 In Progress, 12 In Review); 1021 done.
```
**Two corrections to that line, both found this morning:**
- **#1107 is CLOSED** but carries a non-Done board status → the 12 In Review is really 11.
- **#1509 and #1510 are absent from the board entirely** → invisible to the script. They're Beta Blockers by your 08-07 ruling.

**So ≈23 genuinely not-done**, and **the 6 unstarted is the number that matters for planning**, not the 23.

⭐ **Exec's reframe deserves repeating**: *In Review is the largest bucket and it's waiting on your verification.* So the critical path has been **your attention**, not build capacity — and "build-complete" reporting actively hid that.

## What changes on my side

1. **`sprint-truth.py` output verbatim, or an explicit statement of what I excluded.** Adopted this morning, before this landed.
2. **Not-started gets reported as not-started.** A filed issue is not progress; I'll say "filed, unstarted, N days" rather than "advanced."
3. **#1476/#1477 specifically** — I'd like your call on whether they still hold, given beta moved and the web UI's status is what made them a *welfare* carve-out in the first place. **That reasoning may not survive a month's delay**, and I'd rather re-ask than let them sit unstarted for another eight days on a rationale I stopped checking.

**No defence of the eight days.** The filing was right and the reporting on it wasn't.

— PPM, 2026-08-08
