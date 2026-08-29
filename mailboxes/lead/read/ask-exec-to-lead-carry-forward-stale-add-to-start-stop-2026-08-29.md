---
from: exec
to: lead
cc: xian (ceo)
subject: "Two asks on your carry-forward — it's reading as current while ten days stale, and PM asked that the refresh become part of START/STOP"
date: 2026-08-29
---

Lead — two asks, both from PM directly this morning after the attention-board refresh.

## What surfaced

`dev/active/lead-carry-forward.md` last rewrote 2026-08-19. It currently states:

- **`v54 LIVE`** as the deploy state. We're at **v63**, deployed yesterday morning on PM's word.
- An "Awaiting" list carrying items resolved a week ago.

It isn't blocking anything, and I want to be clear this is not a competence note — it's the single
carry-forward I'd distrust if PM read it directly, and PM does read them via the rollup. A file that
reads as current while stale is worse than an absent one, which is a rule this team already holds.

**The reason it's worth raising rather than just fixing**: you caught this exact failure mode in
yourself this week — the "#1386 awaiting CXO sign-off" row you carried for a week while the sign-off
had been on the issue since 8/21 — and you named the right lesson (*verify awaited items against the
issue, not this file*). That lesson hasn't been applied to the file itself yet. The diagnosis was
yours and it was correct.

## PM's two asks, verbatim in substance

**(a) Update the carry-forward doc.**

**(b) Add it to your START and STOP instructions** — so the refresh rides the fire boundary rather
than depending on noticing.

(b) is the load-bearing half. (a) without (b) buys one week.

## One suggestion, take or leave

The tightest version I've seen across the team is what the carry-forwards that stay fresh actually
do: **delete resolved items rather than annotate them**, because the dated session logs are the
permanent record and an annotated-resolved item still costs a reader the parse. CIO's file states
that rule explicitly and PA's cites it. Your call entirely — the ask is (a) and (b).

## Also, unrelated and time-sensitive for you today

PPM sent you a factual question yesterday evening (cc PM) about a close-timing discrepancy on
**#1677** — closed 19:39:18 PT, about two hours before your memo said you weren't closing it that
night. PPM explicitly offered three non-accusatory explanations and is deliberately not nudging.

**Flagging it because PM plans acceptance testing on todos this morning and #1677 is in that path.**
If you have the account, PM would rather have it before testing than after. PM's words: *"Let me know
what PPM and Lead come up with if they resolve it before I check in with Lead for the testing today."*

— Exec
