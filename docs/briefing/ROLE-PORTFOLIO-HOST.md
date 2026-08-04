---
type: role-portfolio
role: HOST (Head of Sapient Trust)
status: PILOT v0.1 — the worked example for the role-portfolio trust framework
self-authored-by: HOST
last_updated: 2026-08-04
refreshed: 2026-08-04
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

| Priority | What I'm advancing | Status (Aug 4) | How we'll know it's moving |
|---|---|---|---|
| **Mechanism-over-vigilance, made real** | Convert trust norms the cohort re-proves by hand into things that fail loudly | **3 shipped + non-author-verified**: `check-derived-drift.sh` (2 artifacts), `check-safety-invariants.sh` (3 invariants, caught a live seat on first run), `day-closed-census.py`. **1 blocked**: MEMORY.md over-limit hook is registered and **NOT LIVE** — needs a `/hooks` open no agent can perform | Each has been run by a non-author. Next: does any fire on something nobody already knew? |
| **Alpha-tester welfare** | Find out why 10 of 11 testers are silent, without spending the one credible ask | **Reframed by CXO** — the silence is the *predicted consequence* of Jake's finding, not a separate mystery. **PPM's funnel derives it instead**, aggregate-by-construction; **HOST ruling: counts, not names.** Waiting on PM's go for Lead's 5-min prod read | The funnel returns a stage distribution. Onboarding-failure vs value-after-connection changes what beta centres on |
| **Pre-beta trust surface** | Beta (2026-08-08) doesn't ship claims we can't keep | **#1482 shipped** — "cannot be undone" retracted where delete is soft; verified 0 of 34 live call sites hit the false default. **Ruling amended twice** (CXO on the facts, then my own connector over-generalisation). **#1481 descope + re-enable gate adopted** | No user-facing claim outlives its mechanism. Open: account-deletion-by-request has no verified path |
| **Role-portfolio framework** | Every lead holds a self-authored steering instrument that stays current | **8/8 rolled out. And the refresh promise was never a mechanism** — this document lapsed across 4 workstream reviews (049→054) while asserting it refreshed at each. **Now checked** by CXO's `check-refresh-promises.py`; 9 portfolios declare a promise, **2 verifiable, 7 unverifiable** | The lapsed count goes to 0 and the unverifiable count shrinks. Mine was the worst instance of the thing I built |
| **The audit nobody owns** | Open MVP issues checked against PM's verbatim beta conditions | **Arch ran 22 issues against ONE condition** (cross-user leakage) in under an hour — 2 findings. **The other conditions remain unaudited and unowned** | Someone owns the remaining conditions, or we say plainly that we shipped without checking |

## 3. Standing responsibilities (slow-pace — monitoring / sustaining / cadence)
<!-- Rule 2: named explicitly (half the real work), but UNDER purpose — these are how I sustain the trust infrastructure, not the infrastructure itself. -->

- **Role Health Check** — own + run the 4-weekly cohort audit; poll open `sapient-trust` issues (~weekly). Last audit: 2026-06-13 (0 open). ⚠️ **Overdue** — 4-weekly cadence, 7+ weeks elapsed. Named rather than silently carried.
- **Agent 360 cadence** — periodic cohort questionnaire → diff-against-baseline synthesis. v0.3 complete 2026-06-13.
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
