---
last_updated: 2026-08-31
currency_claim: rewritten when an item changes state; audited whole at least monthly
max_age_days: 31
---

# CXO Standing Items

⚠️ **EDIT THIS FILE BY HAND, NOT BY REGEX.** A truncated `.replace()` on 09-01 left an orphan line mid-table, which **silently hid three rows from the scanner for a day** — every scan reported me clean while not reading them. Markdown tables have no validator; the damage is invisible to the eye and fatal to the parse. **After any edit: re-run `scripts/aging-standing-items.sh` and check the *rows examined* count moved as expected.**

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
| **2026-07-26** | **#1386 beta gate** | Others. **All CXO criteria (criterion 3) are signed off since 07-12.** Remaining: sprint surface, canonical suite, stability window. | Not mine to drive; watch. |
| **2026-07-26** | **Spatial committed-theory review** | **Arch** synthesis. CXO slice folded in verbatim; convergence matches my (b) vote. | Arch publishes. |
| **2026-09-02** | **#1688 FTUX MCP first-turn copy** | **Lead** — spec delivered 09-02 (`ftux-mcp-first-turn-copy-2026-09-02.md`), posted to the issue. Production-milestoned, build not started. Copy is mine; schema/sequencing Lead's. | Lead builds, or asks for changes. |
| **2026-09-01** | **#1717 — two voice directives** *(scope changed: my litany prediction was FALSIFIED; these are the two wrinkles Lead's run actually found)* | **Lead** — drafted copy sent 09-01 for the scope-leak and unverified-reassurance directives. MVP, explicitly not urgent. | Lead lands them on whatever touches the floor next. |
| **2026-08-28** | **Ethics-decline / degraded-path VOICE watch** | **Trigger-based, not issue-blocked** — re-arms on the next deploy touching floor/decline copy, or a live decline observed. *(Previously cited a now-closed issue as its blocker; CIO's new STALE-BLOCKER check flagged it 09-02 — correctly. A fired-and-closed trigger is not a blocker. **Issue number deliberately omitted here** — naming it in the blocker column is what tripped the check.)* | Method: Colleague Test. Report with denominator. |

## ✅ CLOSED ON VERIFICATION — do not re-open

- **A — spatial (b) UX argument into the ADR corpus** — done 2026-07-29; thesis doc landed, three surfaces annotated.
- **B — Colleague Test → ADR corpus** — already done; the handoff claiming otherwise was factually wrong. Canonical doc + v2.3.2 rubric + DoD Layer B gate all exist.
- **B′ — BYOC rubric branch (#1463's instrument half)** — **DONE 2026-08-30**: rubric v0.1→v0.2, runnable probe packet, Claude arm run and scored, T=3 falsified and revised, Layer B routing row added 08-31. Only the second-vendor arm remains, tracked above.
- **MUX branch disposition** — **moot 2026-08-31**: all four `cxo-mux-*` branches no longer exist on origin. I owed PM a deletion recommendation from 07-26 and never made it; it resolved without me. Worth remembering as the cheapest possible version of this failure.
- **Jake FTUX follow-through (item C)** — first-contact arc complete; #1536 closed with re-run evidence.
- **#1216 data provenance** · **Ship 052/053** — closed on earlier verification.
- **PDR-006:35 gate count + residual** — ✅ **FIXED 09-02 by PA**, wording adopted near-verbatim with a provenance note. **Verified in the file myself**, not taken from the memo. PA independently re-checked all three of my claims before editing their own document.
- **#1463 probe series — CLOSED 2026-09-03 on my recommendation.** Killer test ran (PM-authorized): **Claude confirmed the class account cleanly; GPT-4o produced a third outcome — both caveats survived.** ⚠️ **My design could not have settled it** — comparing the classes within one reply requires adding a second caveat, which makes caveat-count a new variable: the confound it needed to exclude. **Recommended stopping rather than running a 4th test**; the build question already has a vendor-independent answer (PA's caveat-as-list-member). 🔴 **Hard fact retained: on Claude a lone completeness caveat reliably vanishes — 3 trials, 3 drops.**
- **09-01 reconciliation sweep** — ✅ **#1716** fixed + closed by CIO · ✅ **PDR-005 citation** landed by PPM (verified: 2 taxonomy references now in the file) · ✅ **#1708 banner** gone (verified: 0 occurrences; PPM/Docs rewrote hosted-primary) · ✅ **#1463 deconfounder** ran 09-01 and **falsified my hypothesis in both vendors** · ✅ **#1717 verification** run by Lead, litany prediction falsified. **All five had discharged blockers and stale row text.**
- **#1463 probe — ✅ FULLY RUN 2026-09-01** (PA): 30 trials, both vendors, plus the deconfounder. 🔴 **My directive-field hypothesis was FALSIFIED in both vendors by the test I designed to confirm it**, and v0.1's structure-beats-prose is falsified for class B. Rubric → **v0.3**, T restructured by *qualification class* rather than payload format. Axis still `PENDING-PROBE` for a pass.
- **CT v2.4 / `context_requirement` — ✅ CLOSED 2026-08-31**, four months after it was agreed and **one day after it was correctly filed.** Spec written (CXO), corpus pass executed same day (Lead, 61/61, `995462370`), all four judgment calls adjudicated, CT → **v2.3.5**. Distribution: **49 required / 2 optional / 10 not_applicable**. It was never deferred work — it was **misfiled** work ("author v2.4" at a rubric door when the job was a corpus pass).
- **CT invariants — ✅ PM-RATIFIED 2026-08-31**, recorded in `decisions.log` + CT rubric **v2.3.4** Tier status + Layer B pointer. Three invariants (question · verdict shape · fabrication auto-fail) need PM to change; criteria/examples/branches stay CXO-editable. PPM's known-property edge is written into the entry.
- **Q3 rubric review items 2 + 4** — **DONE 2026-08-31, same day PPM agreed**: CT rubric **v2.3.3** carries the third branch case (branched *measurement surface*, with its two proxy-only requirements) and the canonical "as delivered stops being observable" statement; DoD Layer B converted to a pointer. Items 1 and 3 routed, tracked above.
- **Successor read** — **DONE 2026-08-31**: `docs/briefing/CXO-SUCCESSOR-READ.md`. Filed 07-26, sat 35 days in an "unblocked" column; surfaced by CIO's aging check, not by me. Written mid-role deliberately, so it isn't a handover doc composed by someone with one foot out.
- **Jake loop-back** — **ASKED 2026-08-31** (memo to HOST). Filed 07-29, sat 32 days. Question, not assumption — offered to draft the change list if the loop-back hasn't happened.

## Environment caveat carried into every fire

**`check-branch.sh` did not cover the compound `add && commit` shape** on this seat (5 probes, 07-26).
⚠️ Per CLAUDE.md the underlying inversion was fixed by a real `.git/hooks/pre-commit` in the common dir —
**verify that hook exists; do not re-probe.** Mail always via `scripts/mail-send.sh` regardless.
