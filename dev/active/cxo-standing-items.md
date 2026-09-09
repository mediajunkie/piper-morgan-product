---
last_updated: 2026-09-09
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
| **2026-09-06** | 🔴 **#1386 criterion 3 — RE-RUN OWED AT MVP CLOSE** *(PPM ruled 09-06: criterion 3 joins the fresh-run set. My proposal, accepted.)* Re-execute scenarios **A/B/C** against the **then-deployed** artifact and re-sign or don't. ⚠️ **The 07-12 sign-off does NOT carry forward.** | **The MVP milestone closing.** ✅ **Checkable, not a feeling**: `gh api …/milestones` → MVP, due **2026-10-30**, currently **open, 50 open / 1116 closed**. | **MVP milestone state flips to closed, OR open-count nears zero.** Check it at every START; do not wait to be told. |
| **2026-07-26** | **Spatial committed-theory review** | **Arch** synthesis. CXO slice folded in verbatim; convergence matches my (b) vote. | Arch publishes. |
| ~~**2026-09-07**~~ | ✅ **#1688 FTUX render — CONFIRMED 09-08 by Web** (local dev, layer named): my copy leads verbatim and asks the question. See Closed. *(PM overruled the hold 09-07, "flip ftux")*. ✅ **Source verified by me**: both strings verbatim at `first_contact.py:341,343`; promise-language pin present. 🔴 **NOT verified**: tests pass here (no pytest in this env), **the flag is actually ON in prod**, and **that a cold user sees it.** | **Web capturing a cold first exchange** — asked 09-07, non-urgent. | Web reports, or reports it isn't live. |
| **2026-09-02** | **#1688 FTUX MCP first-turn copy (MCP arm)** | **Lead** — spec delivered 09-02 (`ftux-mcp-first-turn-copy-2026-09-02.md`), posted to the issue. Production-milestoned, build not started. Copy is mine; schema/sequencing Lead's. | Lead builds, or asks for changes. |
| **2026-08-28** | **Ethics-decline / degraded-path VOICE watch** — ⚠️ **METHOD IS NOW PER-TRIGGER (corrected 2026-09-07).** *The row previously stated one method, "Colleague Test, report with denominator," for BOTH triggers. It cannot perform that at one of them, and on 09-01 it fired and I produced a structural finding (#1717) while the row still claimed a Colleague Test. The watch was described as doing something it did not do — m-49 on my own instrument.* | **Two triggers, two methods:** 🔧 **(a) a deploy/commit touching floor or decline copy → STRUCTURAL review** of the directives and their composition. No delivered responses exist to score, so a Colleague Test is impossible here — say so rather than imply one. 🗣️ **(b) a live decline observed → COLLEAGUE TEST**, scored, **with the denominator** (how many declines, on what surface, which account state). ⚠️ **(b) needs a live account — Web's browser lane — so it is an ASK, not something I can self-serve.** | (a) fires on the next such commit; (b) fires when someone observes a live decline. |

## ✅ CLOSED ON VERIFICATION — do not re-open

- **Aggregation-guard third copy — FILED AND CLOSED 2026-09-09, same day, in under three hours.** Lead
  built a single `SOURCE_FAILED_FLAGS` registry, deleted the hand tuple, and made **the tests' own
  denominator derive from the thing under test** — ⭐ **my critique ("the tests key off their own list")
  isn't patched, it's *unstatable*.** Association is **AST-enforced** (exact equality including order,
  duplicates rejected) and the pre-fix drift form is **banned** (any literal ≥2-flag sequence fails).
  ⭐ **He also closed the honest-limit I stated but didn't ask him to fix** — the `"check FAILED:"`
  convention is now pinned, with distinct prefixes required. **All five claims verified by me in the
  file**, not in his memo. 🔴 **NOT measured: the suite run — no pytest on this seat, so his red-proof is
  his evidence, not mine.** One boundary noted and **explicitly not requested as work**: the AST check
  covers literal `.get()` reads inside that one function; a subscript read or a FAILED line in another
  function sits outside it. Neither exists — *"has one real case proven this is needed?"* answers no.

- **Four copy items landed — CLOSED 2026-09-09, all verified verbatim in source.** **#1730 Gap 1**
  generic decline (split into `_RECOGNITION` + `_RECOVERY` — better than my single blob) · **FTUX 3rd
  line** cut with the no-pointer reasoning pinned in comments · **#1717 wrinkles 1 and 2**, wrinkle 2
  including its final sentence. ⭐ **Lead's echo implementation exceeded my constraints** — I asked for
  "truncate" and "render as the user's words"; he named the render **layers** (`marked.parse()` →
  `innerHTML`, no server-side escaping on that path) **and the degraded fallback I didn't know existed.**
  🔴 **Layer measured: source presence. NOT measured: tests run, deployed, or any user seeing it.**
- **Flywheel v3 challenge — CLOSED 2026-09-09, both accepted, then verified.** Arch applied all five
  first-wave challenges within hours; **I opened the file rather than trust the memo and found the fix
  had landed in the amendment note while the TABLE still carried every corrected label** — the
  caveat-in-the-footer shape reproduced inside its own correction. ✅ **Arch then corrected the table in
  place at v3.0.2 with a visible marker**, the exact resolution I proposed, and P5 now reads
  *"Enforced-by-D7 once the first closing gate runs it; Present until then"* — **better than what I
  asked for.** **D4 and D2 declined twice on no independent evidence; that stands.**

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
