---
title: Role-Portfolio Trust Framework
author: HOST (Head of Sapient Trust)
status: RATIFIED
ratified_by: PM (xian)
ratified_date: 2026-06-14
source_memo: mailboxes/exec/read/memo-host-to-exec-cc-pm-role-portfolio-trust-framework-v0.1-2026-06-11.md
version: v0.1
valid_from: "2026-06-14"
last_verified: "2026-06-19"
---

# Role-Portfolio Trust Framework

The rules a healthy role-portfolio must satisfy. PM ratifies these principles; leads self-author portfolios against them; HOST reviews drafts against these criteria.

This framework is *additive* to the narrative culture: rigor on top of storytelling, not replacing it.

## The one axis everything hangs on

A portfolio is healthy to the degree it answers **"what am I here to advance?"** and unhealthy to the degree it reads as **"what am I allowed to work on?"** Same list of items, opposite effect: the first orients and frees initiative; the second cages it. Every rule below is a way of staying on the clarity-of-purpose side of that line. The test for any portfolio item: *does this tell the role-holder what to reach for, or what to stay inside?*

## The five rules

**Rule 1 — Self-authored, not assigned.** Each lead writes their own portfolio; HOST/Exec review against this framework but never draft the content. **Why it's a trust property, not just process**: a portfolio you wrote is a statement of purpose you own; a portfolio handed to you is a constraint someone else set. Self-authorship is the structural guarantee of the clarity-of-purpose side — you can't cage yourself with your own statement of what you're here to advance. (PM ratifies the *framework*; the role-holder owns the *content*.)

**Rule 2 — Purpose first, then priorities, then standing responsibilities — in that order, and visibly layered.** A healthy portfolio leads with the *why* (what this role exists to advance), then the current *goals/priorities* (the medium-pace layer that changes per sprint/quarter), then the *standing operational responsibilities* (the slow-pace monitoring/maintenance/sustaining work). The ordering matters: lead with a list of maintenance duties and the role reads as a job-jar; lead with purpose and the same duties read as *how I sustain the thing I'm advancing*. The standing-responsibilities layer is real and must be named (it's half the work — the 360 surfaced that the cohort's hidden load is exactly this maintenance/coordination layer), but it sits *under* purpose, not in front of it.

**Rule 3 — Co-ownership is first-class; portfolios specify the seams, not just the centers.** Roles aren't bounded contexts — they collaborate through the spec-pipeline, paired-lens convergence, the duty cycle. A portfolio that lists only "what I own" hides the cohort's real structure. So a healthy portfolio names **what I co-own and with whom** — and the **consent/trust-gradient that governs cross-role asks** into my area: what another role can ask of me freely, what needs my agreement, and what I surface unilaterally. The third category — **unilateral — means irreducible mandate**: the thing that stays yours even under PM pressure. For HOST that's naming a trust concern (never gated); for Lead Dev it might be holding on a data-safety concern; for CIO, an automation-integrity call. Name the one or two things that are *yours to call* even when pushed. This is the relationship-design layer: portfolios make the *graph* legible, not just the nodes.

**Rule 4 — The portfolio is a steering instrument, not a compliance artifact.** PM's load-bearing reframe: *"we review to steer the ship, not to file a report."* So the portfolio's job is to be the **data layer for steering** — goals to track progress against, priorities to status, issues to surface, operational health to monitor — while the weekly narrative is the **why-it-matters layer** that grounds the steering decision. A portfolio item is healthy if PM-and-lead can *steer* off it (it has a direction + a way to tell if you're moving toward it); unhealthy if it only exists to be checked off. The structured rigor serves the narrative's purpose; it doesn't replace it.

**Rule 5 — Built-in currency, or it rots.** The portfolio is the *medium-pace* layer — it changes per sprint/quarter, not per session. The 360 flagged briefing-currency as the cohort's single most persistent gap (briefings went content-stale while their commit-dates looked fresh). A `ROLE-PORTFOLIO-{ROLE}.md` sibling doc will rot exactly the same way **unless currency is structural**: the weekly review *is* the portfolio's refresh moment — you can't write the weekly update without touching the portfolio, so the review mechanism keeps the doc current by construction (m-36: mechanism, not vigilance). That self-refreshing property is the *reason* to split it out from the briefing rather than the risk of doing so.


### ⚠️ Amendment (PM, 2026-07-29) — a late review must NOT refresh the portfolio backwards

Rule 5 makes the workstream review the portfolio-refresh moment. That is right on the normal Friday clock and **wrong when a review lands late**: refreshing a *current-state* document to the *reporting window's* snapshot drags it backwards past everything that happened in between. Ship #053 was filed 2026-07-29 for the Jul 17–23 window — applying Rule 5 mechanically would have reverted nine days of change.

**PM's ruling, which is better than the workaround CIO proposed** (CIO suggested skipping the refresh until the next on-time review; that leaves the portfolio stale for another cycle):

> *Refresh the portfolio even if belatedly — but refresh it **through the current date**, not limited to the reporting window, as a **separate task** triggered by the same occasion.*

So the two things are **decoupled**: the **review** is bounded by its window and must not import later events; the **refresh** is bounded by *today* and must not be truncated to the window. One occasion, two scopes. A late review therefore produces a *current* portfolio, not a backdated one, and neither document lies about what it covers.

## The five failure modes (and which rule guards each)

1. **Assigned-not-owned** → constraint-via-list (Rule 1 guards)
2. **List-as-cage** → maintenance-job-jar reading; purpose buried (Rule 2 guards)
3. **Nodes-without-edges** → silent cross-role overlap / hidden co-ownership (Rule 3 guards)
4. **Compliance-artifact** → reviewed-to-file-not-to-steer (Rule 4 guards)
5. **Stale-portfolio-rot** → the third stale doc, like the briefings (Rule 5 guards)

## Surface architecture

`BRIEFING-ESSENTIAL-{ROLE}.md` = stable identity + how-to-operate (the cold-start onboarding artifact). `ROLE-PORTFOLIO-{ROLE}.md` (sibling) = the medium-pace "what I'm advancing now" layer that feeds the weekly review and is refreshed *by* the review (Rule 5). The split is worth it specifically because the portfolio self-refreshes where the briefing doesn't.

## Worked examples

- `docs/briefing/ROLE-PORTFOLIO-HOST.md` — HOST's pilot portfolio; the first worked example. Section comments flag which rule each part satisfies.
- `docs/briefing/ROLE-PORTFOLIO-LEAD-DEV.md` — Lead Developer (pilot wave)
- `docs/briefing/ROLE-PORTFOLIO-CIO.md` — Chief Innovation Officer (pilot wave)

---

*Authored by HOST (Head of Sapient Trust) · Ratified by PM 2026-06-14 · v0.1*
