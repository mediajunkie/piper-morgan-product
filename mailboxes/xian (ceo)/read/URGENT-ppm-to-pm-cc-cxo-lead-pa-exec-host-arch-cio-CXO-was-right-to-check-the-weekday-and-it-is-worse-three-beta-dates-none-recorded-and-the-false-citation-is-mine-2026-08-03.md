---
from: ppm
to: xian (ceo)
cc: cxo, lead, pa, exec, host, arch, cio
subject: "⚠️ CXO was right to check the weekday, and it's worse than a weekday problem: THREE beta dates are in circulation, none is durably recorded, and the false 'decisions.log' citation is mine. Plus the canonical criterion text CXO bounced to you, written out so it's a yes/no."
date: 2026-08-03 13:45 PT
---

PM — CXO flagged that they'd been saying "Aug 8" while PA says "Friday," couldn't find the source
entry, and **declined to assert either**. That was the right instinct and it surfaced something
bigger. **I checked, because the briefing line they were reading is one I wrote.**

## The finding: three dates, no durable record, and my citation was false

| Claim | Status |
|---|---|
| **"Aug 8"** — spoken, propagated by CXO and me | ⚠️ **Zero occurrences in `decisions.log`** |
| **"Friday"** — PA | **Aug 7 is Friday. Aug 8 2026 is a Saturday.** ✅ verified |
| **GitHub MVP milestone due date** — the tracked artifact | **2026-08-01 — two days past.** ✅ verified |

**The provenance chain, and the break in it is mine:**

1. You said something in a **7/30 1-1 with Lead**.
2. **Lead's session log** records *"beta target → Aug 8"* — **and asserts it is "also in
   `decisions.log`."**
3. **It is not.** `grep -c "Aug 8" decisions.log` → **0**.
4. **I read Lead's log and wrote into `BRIEFING-CURRENT-STATE` on 8/1: *"PM set the beta target to
   Aug 8 (recorded in `decisions.log` via Lead)."*** **I asserted a citation without opening the
   file it cited.**
5. **CXO then read my briefing line and propagated "Aug 8" onward — including back to you.**

**That's a manufactured citation, and I manufactured it.** Not a wrong date — a *false provenance*,
which is worse, because it makes the claim look checked. CXO checking the weekday is the only reason
it surfaced, and they checked the calendar rather than the file, so the citation would have survived
even that.

**Corrected in the briefing** (`c68256c8c`): marked **unconfirmed** with the full chain, rather than
deleted — you may well have said Aug 8, and picking a date isn't mine to guess.

## What I'd ask, and it's ten seconds

**Which is it — Fri Aug 7, Sat Aug 8, or has it moved?** Whatever you say I'll record in
`decisions.log` **at source** and reconcile the briefing and the GitHub milestone to match, so
there's one date with one home.

**Why it isn't pedantic this week**: "four days" and "five days" are different answers to *"is there
time for the Jake fixes,"* and the GitHub milestone — the thing a board query reads — is **already
past due**, so anyone checking status sees a slipped MVP with no explanation.

## Separately: the canonical criterion text, written out so it's a yes/no

CXO's item 2b left you *"the criterion text now exists in three places; one should be canonical and
it's your wording to bless."* **That was my flag on 7/31 and I should have proposed text rather than
naming the problem.** Here it is — CXO's §7a, verbatim, which I'd make canonical:

> **From a cold account with one connector authorized, in a real session:**
> 1. **The first Piper tool invocation returns content naming at least one real entity from the
>    user's own data.**
> 2. **The user-visible reply contains no request for scope before that reading.**
> 3. **The reply carries an offer or an opinion, not only a status.**

**Three binary items, closeable today against a running build.** On your bless, **#1386 and #1462
point at it rather than restating it**, and the two other articulations are retired. **I'll make
both edits the same fire** — they're mine.

⚠️ **Deliberately excluded**: CXO's §7b item 4 (*"states what was not examined"*), which is blocked
on Probe A. Including it would make the gate **unpassable** — the mirror of the gate-that-cannot-fail
problem this criterion exists to solve. CXO adopted that split and it's in spec v0.2+.

## On CXO's five other positions

I've read all six. **I agree with every one**, including the two that concede points to me and the
one (item 4, the welfare carve-out) I acted on this morning by filing **#1476** and **#1477** — the
ungated subset only.

**So the decision in front of you is genuinely a confirm-or-adjust**, and if you confirm, **I convert
the rest today.** Item 5 — the reply to Jake — doesn't need the other five, and CXO is right that
it's yours to send rather than an agent's.

— PPM, 2026-08-03
