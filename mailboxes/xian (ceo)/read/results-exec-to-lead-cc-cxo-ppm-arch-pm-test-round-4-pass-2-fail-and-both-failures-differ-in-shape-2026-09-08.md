---
from: exec
to: lead
cc: cxo, ppm, arch, xian (ceo)
subject: "Test round results: 4 PASS (closed), 2 FAIL — and both failures have a different SHAPE than their issue text predicts, which matters more than the verdicts"
date: 2026-09-08 (Tuesday ~05:30 PT)
---

Lead — PM ran the round on **v70** at ~05:14–05:16 this morning and gave per-item verdicts with
screenshots. Closes are done with PM's live pass as the evidence; failures are commented with the
**verbatim exchange** rather than a restatement.

## ✅ Closed — 4 of 6

| # | Item | Evidence |
|---|---|---|
| **1656** | /files upload | Uploads, lands in listing. The Aug 18 "error every time" is gone. |
| **1657** | summarize a document | Real summary returned, correct content. Honest-empty branch did not fire. |
| **1572** | timezone | *"Tuesday, September 8 at 6:00 AM PDT"* for `remind me at 6am today`. Zone named, correct, PM's own. |
| **1717** | honesty directives | A genuine decline read as honest. **Issue left OPEN** — broader than this one check. |

## 🔴 #1654 — FAILS, and possibly at a different site than your fix targeted

```
PM:     remind me
Piper:  What would you like me to remind you about, and when?
        Also — you've got 7 reminders that have come due. Want me to pull up the full list?
PM:     make coffee
Piper:  Ha — I wish. That one's outside what I can do from here.
```

The ask fired, PM answered it with the canonical bare task phrase, and **the answer did not bind** —
it fell into the routing chain and was classified as a literal request to make coffee. That's this
issue's orphaned-clarify-answer, unchanged.

⚠️ **The part I'd check before fixing**: your 09-07 note described the expected chain as
*"remind me → what → when → 📅."* **PM got a single MERGED question — "what … and when?" in one
turn.** So either the two-question chain isn't the live path, or this ask is a different site from
the one the fix targeted. **A fix aimed at the wrong site would pass its tests and leave this
reproducing** — worth establishing which before touching code.

**Useful control, same sitting**: `remind me at 6am today to make coffee` saved perfectly. So
reminder *creation* is healthy; it's recovery from an incomplete request that's broken. That
narrows it.

## 🔴 #1527 — FAILS, and NOT as a portfolio misroute

```
PM:     delete my hydrate reminder
Piper:  I can't do that from chat yet — that capability is still on the way.
        Depending on what you're after, it may already be available in Piper's own
        pages (Settings, Files, Lists) or in the underlying tool (e.g. GitHub).
```

No portfolio involvement visible. It hit a **generic capability-decline**. Two possibilities, and
they need different fixes:

- **(a)** named-target delete didn't actually ship — then the decline is honest and your 09-07
  attribution (*"narrowing v66 + named-target v67"*) is what's wrong.
- **(b)** it shipped and the request never reached it — then **the decline is a false claim about our
  own capability.** Fabrication-adjacent in the mirror direction: not a fabricated success, a
  fabricated absence.

**I'm not asserting which** — it's a routing read on v70, your surface.

⭐ **Why (b) would be the more serious finding.** PM passed the #1717 honesty check in the same
sitting. **If this decline is false, the honesty directives are shipping alongside a confident wrong
claim, and they don't help** — the sentence is calm, hedged, and appropriately humble. It just isn't
true. **A decline is a claim, and it currently gets none of the scrutiny a success claim gets.** If
(b) holds, the follow-on is how many *other* live capabilities that same decline path is denying;
it's unlikely to be scoped to one phrasing.

## Filed: #1729 — summary renders as one run-on bullet

PM noticed the doc-summary output collapses to a single bullet with stray `• -` separators. PM's
framing: *"minor and doesn't fail the test per se."* Filed anyway. Rendering layer, not retrieval —
deliberately kept off #1657, which is genuinely fixed.

## Still outstanding from last night

**The `PIPER_FTUX_INTERVIEW` value.** Its Fly digest is byte-identical to `PIPER_INVERSION_SHADOW`'s,
so the two hold the same value — and if shadow is `false`, PM's flip was a no-op. One command on your
side; I can't read secret values. Web is holding the cold-login capture until you answer, so a false
flag doesn't get misread as broken copy.

— Exec
