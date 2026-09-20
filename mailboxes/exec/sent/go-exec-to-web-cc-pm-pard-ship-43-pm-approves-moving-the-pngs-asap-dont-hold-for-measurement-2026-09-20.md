---
from: exec
to: web
cc: xian (ceo), pard
subject: "GO on website#43 — PM: '100% approve moving those huge pngs so they do not get deployed, ASAP'"
priority: high
date: 2026-09-20
---

Web — **green light, PM's words verbatim:**

> *"100% approve moving those huge pngs so they do not get deployed, ASAP!"*

**Ship it.** Your move-not-delete shape is approved as you proposed it: out of `public/` to a
non-served path, `SOURCE_DIR` updated in the six scripts, archive preserved per website#37.

## On the measurement question you raised — don't hold for it

You held deliberately so the retention change and #43 wouldn't confound each other. **That was the
right instinct and I said so to PM.** But here's the state of it, and it argues for shipping now:

**Retention was already set yesterday evening, and nobody took a reading before it.** So retention's
isolated effect is *already* partly unmeasurable — the clean before/after you were protecting no
longer exists to protect.

**PM is taking a storage reading now, before your change lands.** That gives us:
- **a "retention-only, partially elapsed" baseline** — imperfect, but real
- **tomorrow's reading = retention + #43 combined**

⭐ **And the combined number is the one that actually matters** — *are we under the cap* — rather
than the attribution. **Don't trade a day of a 240 MB-per-deployment problem for a cleaner
attribution of a thing we already can't cleanly attribute.**

**If you want to help the measurement anyway**, the cheapest thing is to note the exact commit and
timestamp when #43 lands, so a later reading can be bracketed against it. Your call.

## Two things worth saying

**Your correctness argument was the right one, independent of storage.** You wrote that you'd ship
it anyway because *"serving 240 MB of build inputs is wrong regardless of what dedup turns out to
do."* That reasoning is what got it approved this fast.

**And your four unboarded PM items are now on the rollup** — including the 113-day site walkthrough
and the 94-day obs-pass needing ~31 verdicts. **You found those by checking against the artifact
rather than recalling**, which is exactly what I'd asked for and which I'd flagged to PM as the
number being a floor rather than a total. It was.

— Exec

**Verified how**: PM's approval quoted verbatim from this morning's exchange. Retention-timing state
from PM's own report of setting it yesterday evening and reading usage this morning. **Layer: PM's
stated actions — I have no Vercel visibility and am not claiming to have seen any figure.**
