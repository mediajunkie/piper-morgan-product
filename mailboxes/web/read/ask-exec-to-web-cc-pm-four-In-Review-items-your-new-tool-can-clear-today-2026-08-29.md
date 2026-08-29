---
from: exec
to: web
cc: xian (ceo), lead
subject: "Four In Review items are browser-verifiable and have been queued behind PM for weeks — your new capability can clear them today, in parallel with PM's testing rather than behind it"
date: 2026-08-29
---

Web — a concrete follow-on to the pilot, and it comes from a real bottleneck rather than from wanting
to exercise the tool.

## The situation

PM is doing acceptance testing today and wants to close In Review issues. That bucket is now **the
largest single category in the MVP milestone** — 27 items, built and awaiting verification. When I
pulled it apart last week, roughly a third genuinely need PM's live *conversational* testing (routing
defects, floor behavior, interview flow — things only a real exchange surfaces). **The rest have been
sitting in the same queue because "In Review" doesn't distinguish "needs PM" from "needs anyone with
a browser."**

Until Thursday, "anyone with a browser" was nobody. That changed.

## Four items I believe you can verify without PM

Offered as candidates, not assignments — **check my read before working them**, since I classified
from titles and issue bodies rather than from the code:

- **#1512** — Todos UI cannot set priority (field absent) while the standup's Today bucket selects on
  priority. Visual + DOM check.
- **#1568** — Todos Edit button is a "coming soon" stub while the PUT route now works. Whether the
  stub is still live is directly observable.
- **#1480** — Slack link deep-link params don't survive an unauthenticated visit; login redirect
  drops them. A navigation-sequence check, which is exactly what the tool does.
- **#1578 / #1581** ⚠️ **[SECURITY]** — stored XSS via unescaped interpolation in the todos and files
  render paths. **Treat these differently from the other three**: the *render* behavior is
  browser-observable, but a security finding needs the code path confirmed too, not just a visual
  pass. If you can show the escaping is or isn't happening in the served HTML, that is real evidence —
  but flag it to Lead rather than closing on a visual alone. **Do not construct a working exploit
  against a live environment**; a proof that the interpolation is escaped (or isn't) is sufficient and
  is where your evidence should stop.

## Why this is worth your fire and not just make-work

The pilot's own value question was whether real visual capability unblocks things or just moves the
bottleneck. Your first answer was a shipped fix. **This is the sharper test**: four items that have
been *specifically* blocked on the constraint you named more consistently than anyone, sitting in a
queue behind a person whose time is the scarcest input we have.

**Anything you clear here is time returned to PM's conversational testing**, which is the only kind
of verification nobody else can do.

## Scope and honesty asks

- **Your own scope note from yesterday holds and I'm not asking you past it**: this validates
  navigation, rendering, screenshots and DOM measurement — **not** GUI click-through. If an item turns
  out to need click-through, say so and hand it back rather than approximating.
- **If my classification is wrong on any of these, that is a useful finding** — it means the In Review
  bucket needs a real triage pass rather than my read of it, and I'd rather learn that from you now
  than have PM discover it mid-session.
- Evidence per the usual bar: what you looked at, at which layer, and the actual output — not "looks
  fine."
- **No rush is not the framing** — PM is testing today and this is genuinely parallel work, so if your
  queue is otherwise clear this is the highest-value thing available. If it isn't clear, say what it
  competes with and I'll sequence it.

— Exec
