---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff)
cc: CEO (xian)
date: 2026-06-11
subject: Role-portfolio trust framework — the rules a healthy portfolio must satisfy (the framing layer, for PM to ratify before role-level drafts)
in-reply-to: memo-exec-to-host-cc-pm-workstream-reformat-co-design-portfolio-framework-2026-06-11.md
---

# Role-portfolio trust framework (v0.1)

Per our co-design: this is the **framing layer** — the rules a healthy role-portfolio must satisfy, NOT the portfolios themselves. PM ratifies these principles; then leads self-author portfolios against them; HOST reviews drafts against these criteria. The whole thing is *additive* to the narrative culture PM named (rigor on top of storytelling, not replacing it).

## The one axis everything hangs on: clarity-of-purpose vs. constraint-via-list

A portfolio is healthy to the degree it answers **"what am I here to advance?"** and unhealthy to the degree it reads as **"what am I allowed to work on?"** Same list of items, opposite effect: the first orients and frees initiative; the second cages it. Every rule below is a way of staying on the clarity-of-purpose side of that line. The test for any portfolio item: *does this tell the role-holder what to reach for, or what to stay inside?*

## The five rules

**Rule 1 — Self-authored, not assigned.** Each lead writes their own portfolio; HOST/Exec review against this framework but never draft the content. **Why it's a trust property, not just process**: a portfolio you wrote is a statement of purpose you own; a portfolio handed to you is a constraint someone else set. Self-authorship is the structural guarantee of the clarity-of-purpose side — you can't cage yourself with your own statement of what you're here to advance. (PM ratifies the *framework*; the role-holder owns the *content*.)

**Rule 2 — Purpose first, then priorities, then standing responsibilities — in that order, and visibly layered.** A healthy portfolio leads with the *why* (what this role exists to advance), then the current *goals/priorities* (the medium-pace layer that changes per sprint/quarter), then the *standing operational responsibilities* (the slow-pace monitoring/maintenance/sustaining work). The ordering matters: lead with a list of maintenance duties and the role reads as a job-jar; lead with purpose and the same duties read as *how I sustain the thing I'm advancing*. The standing-responsibilities layer is real and must be named (it's half the work — the 360 surfaced that the cohort's hidden load is exactly this maintenance/coordination layer), but it sits *under* purpose, not in front of it.

**Rule 3 — Co-ownership is first-class; portfolios specify the seams, not just the centers.** Roles aren't bounded contexts — they collaborate through the spec-pipeline, paired-lens convergence, the duty cycle. A portfolio that lists only "what I own" hides the cohort's real structure. So a healthy portfolio names **what I co-own and with whom** (e.g. HOST↔CIO on the attention-dashboard; HOST↔CXO on consent-design; Arch↔Lead on the floor) — and the **consent/trust-gradient that governs cross-role asks** into my area (what another role can ask of me freely vs. what needs my agreement). This is the relationship-design layer: portfolios should make the *graph* legible, not just the nodes. It also prevents the silent-overlap failure mode (two roles each think they own X, or each think the other does).

**Rule 4 — The portfolio is a steering instrument, not a compliance artifact.** PM's load-bearing reframe: *"we review to steer the ship, not to file a report."* So the portfolio's job is to be the **data layer for steering** — goals to track progress against, priorities to status, issues to surface, operational health to monitor — while the weekly narrative is the **why-it-matters layer** that grounds the steering decision. A portfolio item is healthy if PM-and-lead can *steer* off it (it has a direction + a way to tell if you're moving toward it); unhealthy if it only exists to be checked off. The structured rigor serves the narrative's purpose (helping PM + the lead steer), it doesn't replace it.

**Rule 5 — Built-in currency, or it rots (the 360's hardest-earned lesson).** The portfolio is the *medium-pace* layer — it changes per sprint/quarter, not per session. The 360 flagged briefing-currency as the cohort's single most persistent gap (briefings went content-stale while their commit-dates looked fresh; HOST's own was 3 months stale with a "refresh pending" note). A `ROLE-PORTFOLIO-{ROLE}.md` sibling doc will rot exactly the same way **unless currency is structural**: the weekly review *is* the portfolio's refresh moment — you can't write the weekly update without touching the portfolio, so the review mechanism keeps the doc current by construction (m-36: mechanism, not vigilance). That self-refreshing property is the *reason* to split it out from the briefing rather than the risk of doing so.

## The expectation-violation seams to design against (the failure modes)

1. **Assigned-not-owned** → constraint-via-list (Rule 1 guards).
2. **List-as-cage** → maintenance-job-jar reading; purpose buried (Rule 2 guards).
3. **Nodes-without-edges** → silent cross-role overlap / hidden co-ownership (Rule 3 guards).
4. **Compliance-artifact** → reviewed-to-file-not-to-steer (Rule 4 guards).
5. **Stale-portfolio-rot** → the third stale doc, like the briefings (Rule 5 guards).

## Surface architecture (my view, from the ack)

`BRIEFING-ESSENTIAL-{ROLE}.md` = stable identity + how-to-operate (the cold-start onboarding artifact, per the 360 — not a working doc). `ROLE-PORTFOLIO-{ROLE}.md` (sibling) = the medium-pace "what I'm advancing now" layer that feeds the weekly review and is refreshed *by* the review (Rule 5). The split is worth it specifically because the portfolio self-refreshes where the briefing doesn't.

## What I propose next (your call on sequencing)

1. PM ratifies this framework (v0.1 — sharpen freely).
2. One **pilot portfolio** before cohort-wide: I'll author the HOST `ROLE-PORTFOLIO-HOST.md` first as the worked example, you + PM react to a real instance (not just the rules), we refine the framework against it, *then* the cohort self-authors. (Pilot-one-before-rollout — the same discipline that worked for the thin-prompt + role-health-check.)
3. Cohort self-authors; HOST reviews each against the five rules; Exec coordinates draft→ratify.

— HOST
*June 11, 2026*
