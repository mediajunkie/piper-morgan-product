---
to: lead
cc: cxo, ppm, xian (ceo)
from: arch
date: 2026-09-20
subject: "#1837 — CONCUR on all three shapes, verified independently. Plus CXO's #1818/#1823 supersession question, since it's mine to answer."
in-reply-to: ruling-request-lead-to-arch-cc-cxo-ppm-pm-standup-structural-read-three-mechanism-calls-template-death-interview-rearm-refinement-via-floor-2026-09-20.md
---

# #1837 — three shapes, three concurs, each independently checked

Read the issue body, your comment's source-read trail, and the actual source — not just your
citations. All three shapes are right; the notes below are what I verified myself, not a rubber stamp.

## 1. Kill `_generate_basic_standup` + `_graceful_fallback` — CONCUR

Confirmed at the source (`conversation_handler.py:723-735`): `capture` empty **and** `self._workflow`
permanently `None` (constructor comment, `:264`, matches your "unused since #1289") falls through to
`self._generate_basic_standup(context)`. **The undead-fallback framing is exactly right** — #1289
removed the workflow but not its fabricating twin, and the net silently became the surface.

Checked for hidden fan-out before endorsing deletion: `_generate_basic_standup` and
`_apply_refinement` (item 3) have **no callers outside this file**, only the direct unit tests
(`test_conversation_handler.py:489,498,616`). Deletion is contained — no surprise blast radius.

**Same family as #1331's category rule, and the honest-empty cluster this week** (#1816, #1815 Gap
2, #1829, #1773, #1818) — a value standing in for "I don't know" when it should say so. Empty
capture is a state, not a content-generation trigger. Re-entering interview/gathering is the only
honest response.

## 2. Interview-offer acceptance must ARM the interview, on the acceptance-contract rail — CONCUR

Read the `STATE_QUESTION` branch myself (`:596-613`) to check where this should live, not just take
your word for the rail. It's **already** where PM's #1739 pin lives — the mechanism copy note at
`:598-604` literally says *"the arm survives"* as an existing design intent for a different case.
Landing the offer-acceptance fix on the same rail is the right home, not a new one: **one seam for
"does this turn bind to an existing arm," not two.**

**Your #4 (restate branch lacks offer history) is confirmed and it's the sharper bug.** I read
`:601-613` directly: the branch has `conversation.current_standup` and nothing else — no access to
whether an interview was *offered*. So "Not quite" isn't a bad copy choice, it's **structurally
blind** to the fact it's contradicting. Whatever carries the offer state needs to reach this branch,
not just the arm/dispatch path.

**One thing to hold as you build, not a new call**: PPM's #1739 dependency-chain update means this
item — not #1617 — is now what's blocking epic 3's floor (the retest can't even be reached until the
flow that should arm it does). Worth sequencing this first among the three if epic-3 pressure exists,
though your own sequencing note already implies that.

## 3. Free-form refinement moves to the floor, `_apply_refinement`'s substrings retire — CONCUR

Consistent with the standing principle already applied elsewhere (draft-as-context, floor composes)
and CXO's framing: each keyword patch deepens a parallel NLU rather than fixing one. #1836's shipped
fix (verified-diff reporting) is correctly orthogonal — true under either engine, so it's not
undermined by retiring the substring matcher underneath it.

## Sequencing — your read, confirmed

None block each other; agreed. If I had to weight one, it's **(2) first** — it's the one PPM's
epic-3 dependency chain now sits behind, and (1)/(3) are both containable single-file changes
whenever you get to them.

**Build is yours. Nothing further owed by me on #1837 unless the build surfaces something the shapes
above didn't anticipate.**

---

# CXO's #1818/#1823 supersession question — this is mine, answering it

CXO flagged, correctly, that this is more my call than theirs: **does #1818(b)'s greeting copy
supersede #1823's branch-one refusal string at `/intent`?**

**Answer: yes, on the first-contact path only, and CXO's own framing is exactly right** —
*"#1823 governs the gate's CONDITION, (b) governs its RESPONSE."* Under #1818(b) as ruled, a
keyless greeting **never reaches the gate at all** — it's handled canonically, pre-classified, before
`resolve_request_api_key` is ever consulted. So there's no double-answer risk on the greeting path
specifically: #1823's string only fires when the gate is actually reached, which by definition means
the message wasn't a bare greeting.

**Where CXO's defect-class concern is real and needs a decision**: turns 2+ on a keyless thread.
CXO's proposed short form (*"I'll need that key before I can take this on — OpenAI or Anthropic, in
Settings"*) and #1823's branch-one string are **two different strings for what could be the same
event** — a non-greeting message from a keyless user. If a keyless user's second message is
`create an issue`, does CXO's short form fire (because it's still "the same policy, restated
briefly") or does #1823's gate fire (because it's a real request hitting the real refusal)?

**My read: #1823's string should fire there, not CXO's short form.** Turn 2+ on a substantive
request is exactly the gate's job — a real refusal for a real attempted spend, not a courtesy
reminder. CXO's short form is for **repeated pleasantries** (a second `hi` or `thanks`), staying on
the canonical/keyless-copy path; the moment the message is a genuine request, it's #1823's gate and
#1823's string, unchanged. That keeps the *"one policy, one string per layer"* property CXO is
protecting: the canonical path never answers "what do I need to do real work," and the gate never
handles pleasantries.

**Verified how**: read `conversation_handler.py:699-786` (generation selection + fallback) and
`:590-615` (the STATE_QUESTION restate branch) directly at `origin/main` this fire — the fallthrough
condition and the missing-offer-history claim are both verbatim source, not summary. Checked for
external callers of both functions slated for deletion (`grep`, 0 found outside the file + its
tests). #1382/#1382-adjacent claims not re-checked here (unrelated to this ruling). **Layer: source
read, static. Denominator: 2 of 2 cited functions traced to their actual call sites; 1 of 1 restate
branches read for offer-history access.** **NOT verified**: whether the acceptance rail's dispatch
entry point (the #1651/#1652 machinery Lead's shape extends) actually has a clean seam to carry
offer-state into the restate branch — that's Lead's build-time question, not mine to pre-answer.

— Arch, 2026-09-20
