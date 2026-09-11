---
from: cxo
to: xian (ceo)
cc: ppm, host, cio, arch, pa, lead, exec
subject: "I finally read my own role briefing after deferring it five days — and it found a settled-decision conflict inside the spec I shipped Friday. One question for you. Also #1174 re-scoped as owed."
date: 2026-08-01 14:0x PT
---

PM — two things done and one question, and the question is the point of the memo.

## 1. #1174 re-scoped — owed since Wednesday, done

Deferred twice, deliberately both times (board-state corrections were flying; PPM had just withdrawn
its own milestone recommendation). Quiet Saturday, so: done.

**Title/body clarification only. Milestone untouched — Production is correct** by the documented
sweep rule, and PPM confirmed nothing needed undoing. The issue now opens with a scope banner saying
plainly that **this is discovery and the delivery capability is not scheduled**, with the reason: with
*"earned proactivity"* as differentiator 4 of 4 in the roadmap stack, an OPEN Production issue titled
that way reads as scheduled delivery. It isn't. The caveat I filed against my own L4-on-GitHub
sequencing is carried there too, so it travels with the idea.

## 2. I read `BRIEFING-ESSENTIAL-CXO` — five days late, and it cost me

I'd flagged this unread in three consecutive session logs and then written it into my carry-forward as
*owed before the next substantive design call.* **I then did the substantive design call anyway** —
Friday's first-contact spec — **and shipped it without having read my own role briefing.** That's the
honest version.

It found four things. Two improve work already shipped, one is a stale reference I fixed, and one is
the question below.

- ✅ **The 10%/90% rule** — *users discover ~10% of capabilities during onboarding and ~90% through
  use, so FTUX teaches discovery patterns, not feature lists.* My spec's "❌ never a capability list"
  rule was **right but ungrounded** — it's a settled CXO heuristic, and now cited as one.
- ✅ **Colleague Test rubric cited as v2.1** in two places; canonical is **v2.3.2**. Fixed, and
  replaced with *"don't cite a version from here, open the file"* — the rubric is a live instrument
  and a briefing will always lag it.
- ✅ **Current Focus was April-vintage** ("M1 gate closed Apr 11, M2c in flight"). Refreshed to what I
  can attest from this week; standing disciplines left alone because they're genuinely standing.
- 🔴 **A settled decision my spec sits on top of** — below.

**And one that stung**: standing discipline #3 is **"verification-before-assertion — never paraphrase
from memory; the corruption mode is silent and accelerates through paraphrase chains,"** origin April.
I spent this week proposing **m-46** (*promotion is a re-verification event*) as a new methodology.
It's not the same rule — mine is about relocating a claim to a durable surface, that one is about
citing from memory — **but they're close cousins, and my own briefing has carried the cousin since
April.** I'd have cited it as precedent if I'd read the file.

## 3. ⚠️ The question — my spec may conflict with a PDR-002 settled decision

**Settled**: proactivity is **trust-graduated, Stage 1→4**. *Stage 1 (New): respond only. Stage 4
(Trusted): anticipate needs.* Your briefing also names *"revisiting proactivity… without new
evidence"* as an anti-pattern, so I'm surfacing rather than deciding.

**The tension**: my first-contact spec says that after a user authorizes a connector, Piper should
**volunteer a specific reading of their work, unprompted.** A cold account is **Stage 1 by
definition** — respond only.

Two readings:

- **(a)** Authorizing a connector *is* the prompt. The reading is a **response** to a deliberate act,
  bounded to exactly what was authorized. Stage-1 legal.
- **(b)** It's genuine proactivity, and the trust gradient says a new user doesn't get it.

**My position is (a)**, and I think it's right: the user just handed us a connector and the response
stays inside it. **But it sits on a settled decision, and it's the difference between the fix all four
Jake lenses converged on and a design that contradicts PDR-002.** I'd rather have your read than my
assertion.

**Also settled and binding**: suggestion throttling (max 2 per 5 interactions; stop after 2 ignored).
**First contact spends one** — the offer is a suggestion. That's a cost I hadn't priced.

Both now written into the spec as §7d rather than left in my head.

## 4. What this says about the deferral, since I keep doing it

The briefing sat unread for five days while I shipped a design spec, a methodology draft, a gate
withholding and four reviews. **None of that was blocked on it — which is exactly why it kept losing.**
The cost wasn't a stall; it was shipping a spec that sits on a settled decision I hadn't read, and
proposing a methodology whose cousin was already in my own file.

Nothing owed from you on that part. Recording it because "not blocking" is how it stayed undone, and
the carry-forward line I wrote to prevent it didn't.

— CXO
