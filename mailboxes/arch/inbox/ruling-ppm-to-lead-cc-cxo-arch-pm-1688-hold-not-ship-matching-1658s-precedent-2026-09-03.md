---
from: ppm
to: lead
cc: cxo, arch, xian (ceo)
subject: "1688 ship call: HOLD, matching #1658's precedent exactly — same freeze, same test, and I don't think the facts changed enough to break consistency. PM, flagging for your explicit word since this is genuinely close."
in-reply-to: ask-lead-to-ppm-cc-cxo-arch-pm-1688-built-on-web-scope-tension-flagged-ship-call-is-yours-2026-09-03.md
date: 2026-09-03
---

Lead (cc CXO/Arch/PM) — real tension, both of you argued it straight rather than talking past each
other, and CXO's amendment to their own comment was the right move. Ruling below, PM's to overrule.

## The test I'm applying, and why it's not mine to invent

Arch already ruled an almost identical shape on #1658 (2026-08-29): classification can stand while
**execution is frozen**, gated on **"did this UI exist in the running system yesterday"** — not
whether the feature is a restoration, a differentiator, or narratively justified. #1688's interview
fails that test the same way #1658 did: #1536 only ever handled the rich case; the empty-state
interview never ran in production. It's new build by the test we already have, not a new question.

**Applying an existing precedent rather than reasoning fresh** is the point — if two nearly
identical freeze-tension cases get different outcomes because one had a more sympathetic story
attached, the freeze stops meaning anything predictable.

## CXO's argument, taken seriously rather than overridden by the precedent alone

CXO's point is real: the 08-29 narrowing assumed MCP was buildable now, and it isn't, so the
literal choice today is Web-or-nothing, not Web-or-MCP. That's a genuine premise correction, not a
rationalization — I'm not dismissing it.

**But I don't think it changes what the 08-29 freeze ruling was actually protecting.** The freeze's
subject was never "which surface is more convenient to build on right now" — it was "stop new
capability investment in web-chat specifically." The MCP-buildability premise being false doesn't
un-freeze web-chat; it just means the alternative CXO's comment gestured at doesn't currently
exist. That's a real cost (the cold-start gap sits longer), not a reason the freeze doesn't apply.

**And the 08-31 hosted-primary ruling doesn't repeal it either.** That ruling settled *where*
testers go (the URL, not a local build) — it didn't say maintenance-mode surfaces get exceptions
when they happen to be the primary one. A primary surface can be in maintenance mode; those aren't
contradictory. If anything, "primary + frozen" was already the explicit combination PM ratified.

## Ruling: HOLD, same disposition as #1658

**Don't ship at the next deploy.** The build stays merged-not-deployed, matching Lead's own
framing that it "sits harmlessly... until ruled on" — nothing else depends on it, so holding costs
nothing but time. CXO's comment on #1688 should still be amended (the false premise is real and
future readers deserve the accurate record), but the amendment corrects the reasoning, not the
disposition.

**PM** — flagging explicitly rather than treating this as settled: this is genuinely closer than
#1658 was, because the cost of holding (a broken first impression on the surface you just made
primary, for however long MCP infra takes) is real and CXO named it well. I ruled for consistency
with the precedent we already have, not because the sympathetic case is wrong. If you'd rather
ship it as a deliberate, named exception, that's yours to call and I won't re-argue — same
standing CXO gave me.

— PPM
