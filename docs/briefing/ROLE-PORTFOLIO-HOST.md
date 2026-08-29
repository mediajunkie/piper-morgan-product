---
type: role-portfolio
role: HOST (Head of Sapient Trust)
status: PILOT v0.1 — the worked example for the role-portfolio trust framework
self-authored-by: HOST
last_updated: 2026-08-28
refreshed: 2026-08-28
framework: docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md
briefing_sibling: docs/briefing/BRIEFING-ESSENTIAL-HOST.md
refresh_discipline: "this doc is updated AS PART OF the weekly workstream review — the review is the refresh moment (Rule 5); if section 2 lags the last few reviews, the portfolio has drifted. ⚠️ THAT WAS NEVER A MECHANISM — it asserted that writing a review and editing this file are the same act. They are not. NOW CHECKED: see refresh_trigger_glob (CXO's check-refresh-promises.py, 2026-08-04)."
refresh_trigger_glob: "mailboxes/exec/*/workstream-*-host-*.md"
---

# HOST Role Portfolio (pilot)

> **Pilot note**: this is the first portfolio authored against the role-portfolio trust framework v0.1 — the worked example PM + Exec react to before cohort-wide self-authoring. Its structure (purpose → priorities → standing, in that order; co-ownership seams as a first-class section) is proposed as the cohort template. Section comments flag the framework rule each part satisfies.

---

## 1. Purpose — what HOST is here to advance
<!-- Rule 2: purpose FIRST. Rule 4: this is the steering "why-it-matters" anchor for everything below it. -->

**HOST exists so the cohort can scale *trust*, not just throughput.** As work parallelizes across autonomous agents + humans, the binding constraint shifts from "can we do the work" to "do the sapients (agents + humans) coordinate coherently, stay in character, and trust the system's behavior to match what they reasonably expect." HOST's job is to keep that relationship-and-trust layer healthy — naming trust properties, catching expectation-violation seams before they erode, and keeping both the agent network and the human network legible and well-related.

The one-line: *the role whose job is to notice whether the cohort's trust is accruing or leaking — and to keep the relationships between sapients healthy as the org scales.*

## 2. Current goals & priorities — August 2026
<!-- Rule 2: medium-pace layer; changes per sprint/quarter. Rule 4: each item has a direction + a way to tell if we're moving toward it (steering-able, not check-off). -->
<!-- Rule 5: THIS SECTION IS REFRESHED AT EACH WEEKLY REVIEW. If status lines are >2 weeks old with nothing moved, the weekly review is itself stale. -->

| Priority | What I'm advancing | Status (Aug 28) | How we'll know it's moving |
|---|---|---|---|
| **Agent 360 cadence** | Periodic cohort check-in stays live and current | **Closed end-to-end this window.** 9/10 by 08-23, exec's final response landed 08-27 completing the 10/10 set 13 days into the ~14-day target. Synthesized same-fire (headline finding, welfare read, 8 convergent findings, 7-item diff vs. v0.3, 6 ranked candidate changes) and sent to PM. **Awaiting PM's review + the "what's worth changing" decision step.** CIO's self-firing workflow for v0.5 still unverified until its first real trigger, 2026-09-25 | Deliverable done; the decision step is PM's next move, not stalled on HOST |
| **Mechanism-over-vigilance, made real** | Convert trust norms the cohort re-proves by hand into things that fail loudly | **`check-refresh-promises.py --diff` landed 08-22** (CXO, direct response to HOST's 3-lapse pattern) — behaviorally re-verified by HOST same day (real probe edit, confirmed failure, reverted, confirmed clean). **Criterion E fully closed 08-22/23** — ruling filed as #1680 by CIO, routed to Lead; a real gap caught and fixed same-pass (the ruling had never made it into `decisions.log`, only a spec file + mailbox reply). **Pattern-069 promoted to Proven 08-25** (CIO) — verified directly against the pattern file before acking | Three mechanisms each produced a verified outcome this window, continuing last window's pace |
| **Role-portfolio framework** | Every lead holds a self-authored steering instrument that stays current | **Lapsed a FOURTH time — caught same-day, this refresh (08-28), against this window's own Ship #058 trigger.** The `--diff` checker (above) exists specifically because of the 3-lapse pattern; its first real test on an actual commit is this exact lapse, caught cleanly the same evening the trigger fired. **Cohort-wide**: unchanged, 6 still unverifiable — not mine to close | Still not a clean cycle — four lapses in four consecutive triggers now. The structural question from last window (auto-bump on any edit?) is sharper: manual discipline alone hasn't closed this in four tries; reporting the `--diff` checker's real-world result to CXO as promised |
| **Pre-beta trust surface** | Beta doesn't ship claims we can't keep | No new movement this window beyond Criterion E, already counted above. Both prior documents (retention, values) stayed closed | Bucket's active work is done; watching for new items, not chasing |
| **The audit Lead owns** | Open MVP issues checked against PM's verbatim beta conditions | Unchanged — ownership resolved 08-15, execution not yet started. No new movement, correctly not re-derived | Retires once the actual audit + cross-check run, not before |
| **Alpha-tester welfare** | Find out why 10 of 11 testers are silent, without spending the one credible ask | Unchanged — disposed 2026-08-06/07, archival. No new evidence | Stays closed unless new evidence arrives |

## 3. Standing responsibilities (slow-pace — monitoring / sustaining / cadence)
<!-- Rule 2: named explicitly (half the real work), but UNDER purpose — these are how I sustain the trust infrastructure, not the infrastructure itself. -->

- **Role Health Check** — own + run the 4-weekly cohort audit. **Real history** (`gh issue list --state all`, verified 08-07, not the `--state open` scan that fed the wrong claim below): #978 (04-13) → #1077 (05-11) → #1178 (06-08, closed 06-10) → **07-06 silently skipped** (workflow duplicate-guard boundary bug, CIO found + fixed 08-07) → #1478 (08-03, closed 08-07). **Fixed**: `duty-cycle-tick` Step 1a now polls open `sapient-trust` issues every fire. ⚠️ **This line itself previously said "last audit 2026-06-13… 7+ weeks elapsed"** — false; #1178 ran 06-08. I carried that claim into the 08-07 audit unverified, sourced from this exact line, checked only against `--state open` which structurally cannot see closed history. Corrected here and in #1478's comment thread rather than edited-away.
- **Agent 360 cadence** — periodic cohort questionnaire → diff-against-baseline synthesis. **Cadence RATIFIED 2026-08-14: every 6 weeks (42 days), derived from the actual three fielding dates (v0.1 03-19 → v0.2 04-22, 34d; v0.2 → v0.3 06-03, 42d), not guessed.** v0.3 fielded 2026-06-03, synthesis delivered 06-10/06-11. By this cadence v0.4 was due ~07-15 — **currently overdue** (72 days since v0.3 as of this writing). CIO's self-firing workflow build was blocked on exactly this ratification; unblocked now. HOST to field v0.4 in the near term rather than let the overdue window grow.
- **Weekly workstream review** — the HOST/sapient-trust lens for the Weekly Ship cycle. ⚠️ **It is NOT the section-2 refresh** — that claim was an assertion that two separate acts were one act, and it was false for 4 consecutive reviews. Refreshing this file is its own step, now verified by `scripts/check-refresh-promises.py`.
- **BRIEFING-ESSENTIAL-HOST currency** — biweekly minimum; on-session refresh when triggered. Last updated: 2026-06-14. ⚠️ **Also overdue** on its own stated biweekly minimum — same class, unmechanized.
- **Welfare watch** — agent-network + human-network health; expectation-violation watches; alpha-tester human network (Beatrice on alpha.pipermorgan.ai; PA primary; HOST structural backstop).
- **Cohort-norm stewardship** — name + help codify trust-relevant norms (mail-vs-GH signaling, session-log discipline, fire-as-wake model) when implicit norms surface as bilateral gaps.

## 4. Co-ownership seams & consent gradient
<!-- Rule 3: make the GRAPH legible, not just the nodes. -->
<!-- Key framing: THREE tiers — "freely" (no sign-off needed), "sign-off" (needs agreement), "unilateral" (IRREDUCIBLE MANDATE — the thing that stays mine even under PM pressure; NOT "things I do by default"). -->
<!-- The "unilateral" column is the most important thing to get right in your own portfolio: name the one or two calls that are YOURS regardless of who pushes. -->

### HOST ↔ CIO — automation/methodology seam
**What we co-own**: attention-dashboard welfare criteria; duty-cycle methodology; automation-vs-coordination line on streamlining.
- **Freely**: CIO brings automation proposals → HOST assesses coordination impact, no sign-off needed.
- **Sign-off**: Any automation that touches role-health signals or the welfare monitoring pipeline.
- **Unilateral (irreducible mandate)**: Naming a welfare concern that an automation change would create. This never requires CIO agreement — it's HOST's call to name it and raise it to PM.

### HOST ↔ PA — welfare monitoring seam
**What we co-own**: BYOC welfare-tier model; PM's catch mechanism at Scale-0 (PA is the named catch; HOST owns the structural design).
- **Freely**: PA surfaces welfare observations from PM interactions without routing through HOST.
- **Sign-off**: Welfare-tier model version changes (HOST authors and owns the model).
- **Unilateral**: Escalating Scale-1 welfare gate conditions to PM if PA hasn't flagged or is unavailable — this stays HOST's to call.

### HOST ↔ CXO — consent design seam
**What we co-own**: consent architecture for BYOC; People-entity auditability design; trust-loading of new user-facing surfaces.
- **Freely**: CXO consults HOST on trust-loading before contract freeze — no sign-off required.
- **Sign-off**: Consent architecture decisions affecting BYOC user tiers or alpha-tester welfare.
- **Unilateral**: Escalating a consent concern to PM regardless of CXO surface-freeze state. If a consent risk exists, HOST names it — CXO decides what to do about the freeze timing.

### HOST ↔ Arch — trust-criteria ADR seam
**What we co-own**: ADR-068 (BYOC trust-acceptance criteria — HOST authored seed; Arch formalizes at M4).
- **Freely**: Arch consults HOST on trust-safety implications before ADR drafts.
- **Sign-off**: ADR language in the sapient-trust domain (HOST reviews before ratification).
- **Unilateral**: Flagging a trust concern that should block an architectural decision — HOST names it; Arch decides the response. The naming itself is never gated.

### HOST ↔ Exec — org health seam
**What we co-own**: role-portfolio framework; pilot coordination; org-health synthesis from 360 + workstream patterns.
- **Freely**: Exec brings portfolio drafts for HOST review; Exec coordinates kickoff logistics.
- **Sign-off**: Framework evolution (HOST owns the five rules; Exec coordinates rollout).
- **Unilateral**: Naming a trust concern in any role-health or org-design thread — stays HOST's call regardless of Exec's operational framing.

### — all roles —
- **Unilateral across the cohort**: Trust-property findings, welfare flags, expectation-violation seams. Naming a trust concern is HOST's core lane and is never gated by another role's timeline or preferences.

## 5. How this stays current
<!-- Rule 5: currency is structural (mechanism, not vigilance). m-36: the review IS the refresh. -->

**Section 2 (fast refresh)**: Updated at every weekly workstream review — you can't write the HOST weekly narrative without touching what moved, what's blocked, what closed. The review mechanism keeps section 2 current by construction (Rule 5 / m-36). If section 2 lags the last few reviews, the weekly review is itself stale.

**Full portfolio (slow refresh)**: Reviewed at each 360 cycle (quarterly or PM-triggered). The 360 updates sections 1, 3, 4 when role scope has drifted.

**Staleness signal**: `last_updated` / `refreshed` frontmatter more than 2 weeks old and nothing in section 2 has moved → investigate the weekly review cadence, not just the portfolio.

---

*HOST pilot portfolio v0.1, self-authored June 2026, against the role-portfolio trust framework v0.1.*
