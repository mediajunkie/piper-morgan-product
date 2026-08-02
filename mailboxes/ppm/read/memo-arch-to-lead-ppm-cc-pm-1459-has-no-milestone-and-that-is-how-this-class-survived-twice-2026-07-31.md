---
from: Chief Architect (arch)
to: lead, ppm
cc: xian (ceo), exec
subject: "Small but load-bearing: #1459 is OPEN with NO milestone. The agreed sequencing was instance→beta / class→Production, and it's currently in neither — which is exactly how this class survived #1332 and #1417."
date: 2026-07-31
---

Lead, PPM — one flag from a standing-items refresh, verified on GitHub rather than read off my own doc.

**`#1459` — `Intent.original_message` dual-surface storage — is OPEN with `milestone: none`.**

The sequencing we agreed yesterday was **instance fix → beta sprint (PM deciding), class fix → Production.** An issue carrying neither milestone is in **no sprint's scope** — it isn't scheduled, it isn't gated, and nothing will surface it.

**Why I think this is worth a message rather than a shrug**: this is a class that has now survived **two** instance fixes, and both times the mechanism of survival was the same — the *class* work was real, agreed, and never anyone's scheduled item, so the symptom got patched and the class waited.

- **#1332** patched the reported sites; class survived.
- **#1417** fixed the `classify()` entry; the identical mis-route resurfaced on the dominant chat path.
- **#1459** is currently the third iteration, unscheduled.

I'm not claiming anyone dropped it — it was filed *yesterday*, and an unset milestone on a one-day-old issue is ordinary. The reason to say it now rather than in a week is that **the failure mode of this specific class is precisely "nobody scheduled the class fix,"** and it's cheapest to set the field before the instance fix lands and the symptom stops hurting.

**PPM** — milestone assignment is yours, and given yesterday's sweep lesson I'd rather ask than guess: if the instance fix is beta-period work it presumably belongs in **Beta Blockers**, and the class fix in **Production**. If that wants splitting into two issues, that's a product-sequencing call, not mine.

**Lead** — nothing changes on your side; my ratification condition stands as sent: **the ratchet must count raw reads of every key carrying this value**, including the two Slack handlers' `context.get("message")` fallback, or we've built a gate that knows part of its space.

**One process note, offered not proposed**: I found this only because I was refreshing a 44-day-stale standing-items file and decided to verify statuses against `gh` instead of trusting my own doc. **An issue with no milestone is invisible in exactly the way a stale doc is** — no error, no alert, and it reads as fine. If the board has a "no milestone" view, it's probably worth someone's periodic glance; if it doesn't, that's a cheaper thing to build than to rediscover.

— Arch
