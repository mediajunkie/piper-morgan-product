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
| **2026-09-02** | **PDR-006:35 gate count stale + residual** | **PA** — PDR-006's author. Exact replacement wording sent 09-02; ⚠️ **decrement alone would lose the residual** (T axis can't issue a pass). | PA edits or declines. |
| **2026-09-01** | **#1463 class-discriminator test (2 calls)** *(⚠️ #1463 itself CLOSED 09-01 22:49 — the test survives it; the instrument's T axis is still `PENDING-PROBE`)* — item 3's payload carrying BOTH a class-A caveat (cached read) and a class-B caveat (`coverage: partial`), one question. Holds → staleness survives, completeness vanishes, same reply. Both vanish → I'm wrong again. | **PM** — needs its own authorization; deliberately not folded into the run already approved. **Not asking yet**, flagged as cheap and available. | PM's word. |
| ~~**2026-07-30**~~ | ✅ **#1463 both arms — DONE 09-01** (PA, 30 trials, 2 vendors; credential resolved). See Closed. | 🔴 **BLOCKED, cause FOUND 08-31 ~16:0x.** Key prefix is **`sk-proj-`** (PA verified) = project-scoped; PM's org has **two** projects and the top-up landed in the funded one ("Intern", $9.22) while the key belongs elsewhere. **A project-scoped key cannot see org-level or sibling-project balance.** PM is minting a fresh key from inside the funded project; PA stores via `KeychainService` and verifies live. ⚠️ *I marked this UNBLOCKED at ~13:2x on PM's report of a top-up; PA tested the credential live twice, an hour apart, and it still fails. Authorizations are fine — the credential is not.* **Diagnostic put to PM**: check the billing page directly, which distinguishes propagation delay from a top-up posted to a different org/project. | A live API call succeeds. PA runs both immediately then. |
 Ownership answer. |
| ~~**2026-05-10**~~ | ~~**Quarterly CT rubric review**~~ — ✅ superseded by the two rows above | ~~**PPM marking the dispositions.** *(Moved 08-31 12:xx: PPM picked Thursday 09-03 — **their** trigger, not PM's — and I sent the four dispositions the same fire rather than sitting on them until Wednesday.)* `docs/internal/testing/rubric-review-2026-q3-dispositions.md` | PPM marks agree/disagree/needs-live. |
| **2026-07-26** | **#1386 beta gate** | Others. **All CXO criteria (criterion 3) are signed off since 07-12.** Remaining: sprint surface, canonical suite, stability window. | Not mine to drive; watch. |
| **2026-07-26** | **Spatial committed-theory review** | **Arch** synthesis. CXO slice folded in verbatim; convergence matches my (b) vote. | Arch publishes. |
| **2026-09-01** | **#1717 — two voice directives** *(scope changed: my litany prediction was FALSIFIED; these are the two wrinkles Lead's run actually found)* | **Lead** — drafted copy sent 09-01 for the scope-leak and unverified-reassurance directives. MVP, explicitly not urgent. | Lead lands them on whatever touches the floor next. |
| **2026-08-28** | **Ethics-decline / degraded-path VOICE watch** | ✅ **FIRED 09-01** on `000ca9421` (#1645) and produced #1717. Re-arms on the next deploy touching floor/decline copy, or a live decline observed. | Method: Colleague Test. Report with denominator. |

## ✅ CLOSED ON VERIFICATION — do not re-open

- **A — spatial (b) UX argument into the ADR corpus** — done 2026-07-29; thesis doc landed, three surfaces annotated.
- **B — Colleague Test → ADR corpus** — already done; the handoff claiming otherwise was factually wrong. Canonical doc + v2.3.2 rubric + DoD Layer B gate all exist.
- **B′ — BYOC rubric branch (#1463's instrument half)** — **DONE 2026-08-30**: rubric v0.1→v0.2, runnable probe packet, Claude arm run and scored, T=3 falsified and revised, Layer B routing row added 08-31. Only the second-vendor arm remains, tracked above.
- **MUX branch disposition** — **moot 2026-08-31**: all four `cxo-mux-*` branches no longer exist on origin. I owed PM a deletion recommendation from 07-26 and never made it; it resolved without me. Worth remembering as the cheapest possible version of this failure.
- **Jake FTUX follow-through (item C)** — first-contact arc complete; #1536 closed with re-run evidence.
- **#1216 data provenance** · **Ship 052/053** — closed on earlier verification.
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
