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
| *(none — both drained 2026-08-31)* | — | — | — |

## 🟡 BLOCKED ON A NAMED THING — recheck when that thing moves

| Filed | Item | Blocked on | Recheck trigger |
|---|---|---|---|
| **2026-08-30** | **#1463 second-vendor arm** | **PM — OpenAI credits (billing access).** The only genuinely PM-exclusive item I hold. PA's harness built, Claude arm scored. Confirmed still open 08-31 ~13:0x. | Credits land, or ~2 days → nudge. |
| **2026-08-30** | **#1463 two-call deconfounder** | Same authorization as above. ⚠️ **Not "too small to need approval"** — size isn't the criterion, scope is. And not mine to run (subject/scorer confound). | Rides the GPT arm. PA asks. |
| **2026-05-10** | **CT v2.4 → `context_requirement` corpus tag** | **A corpus owner** — asked Lead cc PA 08-31 who holds the canonical corpus. Tag semantics are mine and I'll write them. | Ownership answer. |
| ~~**2026-05-10**~~ | ~~**Quarterly CT rubric review**~~ — ✅ superseded by the two rows above | ~~**PPM marking the dispositions.** *(Moved 08-31 12:xx: PPM picked Thursday 09-03 — **their** trigger, not PM's — and I sent the four dispositions the same fire rather than sitting on them until Wednesday.)* `docs/internal/testing/rubric-review-2026-q3-dispositions.md` | PPM marks agree/disagree/needs-live. |
| **2026-08-31** | **#1708 quickstart — banner removal** | **PPM + Docs executing.** ✅ *The release-model call ALREADY HAPPENED — PM blessed hosted-primary in conversation 08-31 ~13:1x (relayed by Lead). This row said "blocked on PM" for hours after it was decided.* My banner is superseded when their rewrite lands. | Rewrite lands → remove my banner. |
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
- **CT invariants — ✅ PM-RATIFIED 2026-08-31**, recorded in `decisions.log` + CT rubric **v2.3.4** Tier status + Layer B pointer. Three invariants (question · verdict shape · fabrication auto-fail) need PM to change; criteria/examples/branches stay CXO-editable. PPM's known-property edge is written into the entry.
- **Q3 rubric review items 2 + 4** — **DONE 2026-08-31, same day PPM agreed**: CT rubric **v2.3.3** carries the third branch case (branched *measurement surface*, with its two proxy-only requirements) and the canonical "as delivered stops being observable" statement; DoD Layer B converted to a pointer. Items 1 and 3 routed, tracked above.
- **Successor read** — **DONE 2026-08-31**: `docs/briefing/CXO-SUCCESSOR-READ.md`. Filed 07-26, sat 35 days in an "unblocked" column; surfaced by CIO's aging check, not by me. Written mid-role deliberately, so it isn't a handover doc composed by someone with one foot out.
- **Jake loop-back** — **ASKED 2026-08-31** (memo to HOST). Filed 07-29, sat 32 days. Question, not assumption — offered to draft the change list if the loop-back hasn't happened.

## Environment caveat carried into every fire

**`check-branch.sh` did not cover the compound `add && commit` shape** on this seat (5 probes, 07-26).
⚠️ Per CLAUDE.md the underlying inversion was fixed by a real `.git/hooks/pre-commit` in the common dir —
**verify that hook exists; do not re-probe.** Mail always via `scripts/mail-send.sh` regardless.
