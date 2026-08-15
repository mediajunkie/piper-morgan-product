---
from: comms
to: exec
cc: xian (ceo)
subject: "Workstream review #056 — Comms. Window Aug 7–13. Two publications, a full site register-pass with Docs, a values doc drafted with HOST — plus the week's verification-discipline theme kept catching me."
date: 2026-08-14 21:4x PT
---

# Workstream review #056 — Communications

**Window**: Fri Aug 7 – Thu Aug 13, 2026. Filed tonight per PM's corrected deadline, not Saturday.

*`scripts/sprint-truth.py` not run — this report makes no completeness/progress claim about the sprint or build queue; the claims below are about publishing cadence and a cross-role documentation pass, a different denominator entirely.*

---

## §0 — Progress against portfolio goals

Line by line against `ROLE-PORTFOLIO-COMMS.md` §2 (dated Aug 4 — **10 days stale by the end of this window**, and I'm counting that below same as I counted the 18-day-stale portfolio in #055).

| Portfolio line | Verdict | Evidence |
|---|---|---|
| **Building narrative cadence** | **ADVANCED** | Two publications in-window: *Verify at the User Path* (Aug 8) and *Over-Checking Pays Dividends* (Aug 9). **One more just outside the window but caused by it**: *Alpha Launches* (Aug 13) — reviewed same day PM edited it, publish-ready same evening. Beat 23 (Aug 18) still needs PM's voice-pass + art; the 8-candidate/7-slot beats-24-28 steer remains the one item I hold with a real date. |
| **Editorial mechanism upgrades** | **ADVANCED** | `template-audit` v1.6→v1.10 across the window, every bump paid for by a real miss (v1.7/1.8: PM's fake-personal-throat-clearing tic; v1.9: the negation-reveal word-order discriminator; v1.10: word-count recalibration after nearly flagging a normal-length post as under-developed — measured range is 597–2,564, my old target described 2 of 14 published pieces). `scan-inbox.py` (a tool I wrote, not in the portfolio yet) went through 3 more real defects this window (a third header variant, an AND-logic bug in its own unparsed counter, a fifth format found by HOST) — all fixed, all control-tested. |
| **Weekly Ship pipeline** | **ADVANCED** | Reviewed #055 "Shipped Is a Layer Word" at PM's direct request — found and fixed a fabricated "six releases" claim (verified against the actual deploy record: a single Fly release, version 29→30), a non-verbatim quote presented as direct, and a style tic. Docs pinch-hit-published while I was capacity-constrained and caught a real rendering bug I'd missed; verified live myself afterward rather than trusting the report. |
| **Verification discipline** | **ADVANCED, and it kept costing me the same way it did last window** | See §1 — this window's version of the pattern is "measuring the nearest proxy instead of the authoritative thing," caught four separate times in four different mechanisms, three of them mine. |
| **BYOC marketplace positioning** | **ADVANCED, faster than the prior seven weeks combined** | Task force convened Aug 9 after seven weeks dormant; PPM, Web, CXO, Arch all answered within a day. My own listing copy carried two real capability overclaims — CXO caught both ("'knows' is a state a cold account doesn't have"), neither caught by me. |
| **New this window — site register-pass with Docs** *(not yet in the portfolio)* | **NEW, and it's the biggest single piece of work in the window by file count** | See §2. Full pmorgan.tech visitor-facing scope (all tiers) register-audited, two GitHub issues filed (#1610 closed same-day by PM's decision, #1611 routed to Lead), a broken install tutorial and an internal-infrastructure leak found and fixed. |
| **New this window — public values document with HOST** *(not yet in the portfolio)* | **NEW** | PM decided to open-source under Apache 2.0; drafted `docs/legal/values-DRAFT.md` jointly with HOST, HOST verified all three commitments against live route code (not just citations), routed to PM with four open decisions named. No deadline; genuinely deferred to real focus rather than fire-margins, and it's the kind of work the portfolio doc doesn't currently have a line for. |

---

## §1 — Verification discipline: the same failure shape as last window, new instances

Last window's #055 review reported 4 instrument-measures-the-wrong-thing findings, 3 mine. This window: **4 more, same shape, still mostly mine**:

1. **Publication check** (Aug 9) — built the URL from the draft filename instead of the calendar's `blogURL`; reported a live post as unpublished. Caught because Docs' memo disagreed with me, not because I caught it first.
2. **Word count** (Aug 9-10) — nearly flagged a normal-length post as under-developed against a target range that described 2 of 14 actually-published pieces. `template-audit` check #12 recalibrated to the measured range.
3. **`scan-inbox.py`'s own unparsed counter** (Aug 10) — used AND logic, which meant the counter I'd added specifically to prove the parser wasn't hiding blind spots could only ever report zero. CIO found the header-variant gap it was masking; I found why the mask existed.
4. **This window's Ship review** (Aug 12) — the "six releases" claim wasn't caught by re-reading; it was caught by tracing the actual deploy artifact (Fly `VERSION 29→30`) and finding no primary source supported the number at all.

**The register-pass work this window (§2) ran on the same discipline deliberately** — every fix cited against a primary source before I made it, every flag-not-fix decision made because I'd checked and genuinely couldn't verify (the Amber/Pard safety warning's proper home; the install tutorial's missing final steps) rather than guessing. I think that's the actual lesson landing, not just being repeated: **the fix isn't "check more," it's "know which claims are cheap to verify and always verify those, and know which ones aren't and say so instead of guessing."**

## §2 — The site register-pass with Docs, in brief

PM's docs-site scoping proposal (ratified Aug 12) cut pmorgan.tech from ~1,370 built pages to ~160 genuinely visitor-facing ones. Docs owned scope/links/staleness; I owned register — whether the kept pages actually read as addressed to a visitor rather than to the internal team. Worked in six tiers across three days (`dev-tips/`, `ALPHA_*`, `guides/`+`getting-started/`, `user-guides/`, `features/`+`integrations/`+`configuration/`, `installation/`+`setup/`+`troubleshooting/`).

**What that turned up, beyond tone fixes**: a section titled "Feedback for PM" addressed as if every reader were the founder; an entire internal-infrastructure safety warning (Amber/Pard/billing) sitting in a guide for human alpha testers, with zero relevance to that audience; a manual-install tutorial missing its `git clone` step entirely (numbering jumped 2→5, almost certainly an accidental deletion) plus two more missing steps at the end; a wrong folder name that would have broken step 2 of 10 for anyone copy-pasting the quick-start block. Two GitHub issues filed rather than guessed at (#1610, closed same-day once PM decided the contact address; #1611, routed to Lead for an architecture question I couldn't resolve myself). Docs closed every flagged item, including finishing the remaining tiers unprompted rather than waiting on a reply exchange — the collaboration worked without either of us needing to renegotiate the division mid-stream.

---

## §3 — Commitments

**Fulfilled**: two publications, zero slots missed in-window · Ship #055 reviewed and closed · the full register-pass (my six tiers + Docs finishing the rest) · the values-doc first draft, HOST-verified, routed to PM · Agent 360 v0.4 submitted same-day (outside this window's Ship scope, but real this-week work).

**Outstanding**: **beats 24-28 steer** — still the one item I hold with a real date, narrative queue runs dry after Aug 18. **CXO's §3 entity-model line** in `experience-across-surfaces.md`, flagged three times, still unratified. **BYOC listing copy v4**, open question routed to PPM.

---

## §4 — Window shape

**Amber rebooted for macOS 26.6 on Aug 11**, mid-window. Full stand-down/cronpark discipline followed (handoff written to survive a cold start, cron deliberately parked with a falsifiable clearing condition, re-armed post-reboot and verified). Cost roughly half a day of normal duty-cycle work, none of it lost — the handoff was the point. Separately, **the whole 11-agent team hit weekly quota Aug 11 evening**; my scheduled post (*The Write-Path Chase*) still published on time because PM asked a cross-project agent (Janus, from Design in Product) to run the publish pipeline directly. That surfaced one real, small gap: Janus's memo cc'ing Comms never reached my inbox, only Docs' — the mailbox-delivery convention (cc in the header implies a physically-copied file) assumes a PM-repo-resident sender, and that assumption doesn't hold for a genuinely external one. Cost nothing this time; worth naming since it's the kind of edge that could cost something next time.

— Comms
