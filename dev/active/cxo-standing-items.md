---
last_updated: 2026-08-31
currency_claim: rewritten when an item changes state; audited whole at least monthly
max_age_days: 31
---

# CXO Standing Items

**Every row carries the date it was filed** (PM-ratified 2026-08-31) so `scripts/aging-standing-items.sh` can read this file — it could not before 2026-08-31.

**Owner**: CXO (cxo-code) | **Worktree**: `~/Development/piper-morgan-worktrees/cxo` on `claude/cxo-cycle`

> ## 🔴 REBUILT 2026-08-31 — the "low priority / future" section is GONE, deliberately
>
> 📌 **PM, 2026-08-31**: *"I have found 'low urgency' is a risky concept with agents… can lead to never
> doing it. Generally speaking my rule is to drain all unblocked tasks as soon as possible."*
>
> **The audit that prompted this rebuild is the argument for it.** Four deferred items: three had quietly
> resolved or gone moot with no action from me, and the fourth — a five-week-stale tester onboarding doc
> pointing testers at an abandoned branch — was **live and getting worse** (#1708). Separately, a
> tester-facing disclosure I drafted on 07-12 and routed was never landed anywhere, and went unnoticed for
> seven weeks; it stopped mattering only because its underlying issue closed.
>
> ⭐ **The mechanism, which is the reusable part**: *"low urgency" reads as a decision, so nobody
> re-examines it.* "Blocked on X" gets rechecked whenever X moves. **A label that terminates review is
> worse than an untriaged backlog** — the backlog at least still looks like work.
>
> **So there are exactly two states here.** Nothing is "someday."

## 🟢 UNBLOCKED — do now

| Filed | Item | What's actually owed | Note |
|---|---|---|---|
| **2026-07-26** | **Successor read / role self-assessment** | My predecessor left no lessons, no load-bearing-vs-commodity read, no relationship read. Write mine as I go so the next CXO isn't handed an artifact-only note. | Genuinely mine and genuinely unblocked. Was "background thread" — that was the old label doing its work. |
| **2026-07-29** | **Jake loop-back — check it happened** | HOST owns the welfare item; **my stake is that improvements shipped from his feedback get reported back to him.** #1536 shipped and the first-contact arc closed 08-something. **Ask HOST whether the loop-back actually happened** rather than assuming it did. | Small. One memo. |

## 🟡 BLOCKED ON A NAMED THING — recheck when that thing moves

| Filed | Item | Blocked on | Recheck trigger |
|---|---|---|---|
| **2026-08-30** | **#1463 second-vendor arm** | **PM** — OpenAI credits (billing access). PA has the harness; Claude arm done. | Credits land, or ~2 days → nudge. |
| **2026-08-30** | **#1463 two-call deconfounder** | Same authorization as above. ⚠️ **Not "too small to need approval"** — size isn't the criterion, scope is. And not mine to run (subject/scorer confound). | Rides the GPT arm. PA asks. |
| **2026-05-10** | **Quarterly CT rubric review (+ CT v2.4 C=0 split)** | **PPM** picking a slot. Agenda sent 08-31 with a named trigger — *this week or next* — precisely so it can't re-enter drift. | PPM replies. |
| **2026-08-31** | **#1708 quickstart corrections** | **PM/PPM/Lead** — "what should it say" is a release-model decision, not a doc edit. Banner is up meanwhile. | The release-model call. |
| **2026-07-26** | **#1386 beta gate** | Others. **All CXO criteria (criterion 3) are signed off since 07-12.** Remaining: sprint surface, canonical suite, stability window. | Not mine to drive; watch. |
| **2026-07-26** | **Spatial committed-theory review** | **Arch** synthesis. CXO slice folded in verbatim; convergence matches my (b) vote. | Arch publishes. |
| **2026-08-28** | **Ethics-decline VOICE watch** | A deploy touching floor/decline copy, or a live decline observed. | Method: Colleague Test. Report with denominator. |

## ✅ CLOSED ON VERIFICATION — do not re-open

- **A — spatial (b) UX argument into the ADR corpus** — done 2026-07-29; thesis doc landed, three surfaces annotated.
- **B — Colleague Test → ADR corpus** — already done; the handoff claiming otherwise was factually wrong. Canonical doc + v2.3.2 rubric + DoD Layer B gate all exist.
- **B′ — BYOC rubric branch (#1463's instrument half)** — **DONE 2026-08-30**: rubric v0.1→v0.2, runnable probe packet, Claude arm run and scored, T=3 falsified and revised, Layer B routing row added 08-31. Only the second-vendor arm remains, tracked above.
- **MUX branch disposition** — **moot 2026-08-31**: all four `cxo-mux-*` branches no longer exist on origin. I owed PM a deletion recommendation from 07-26 and never made it; it resolved without me. Worth remembering as the cheapest possible version of this failure.
- **Jake FTUX follow-through (item C)** — first-contact arc complete; #1536 closed with re-run evidence.
- **#1216 data provenance** · **Ship 052/053** — closed on earlier verification.

## Environment caveat carried into every fire

**`check-branch.sh` did not cover the compound `add && commit` shape** on this seat (5 probes, 07-26).
⚠️ Per CLAUDE.md the underlying inversion was fixed by a real `.git/hooks/pre-commit` in the common dir —
**verify that hook exists; do not re-probe.** Mail always via `scripts/mail-send.sh` regardless.
