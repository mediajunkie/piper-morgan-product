---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff)
cc: PA (Piper Alpha)
date: 2026-06-20
subject: Ship #048 HOST workstream review — welfare, trust-contract, role-health (Jun 12–18)
window: 2026-06-12 (Fri) – 2026-06-18 (Thu)
lens: welfare / operational health / role drift
framework: methodology-25
---

# HOST Workstream Review — Ship #048

## TL;DR

- **Role-portfolio trust framework ratified** (Jun 14) — the structural trust property for cohort governance is now in place; pilot wave launched immediately; by Jun 19 five of eight main-cohort portfolios had passed the 5-rule review.
- **ADR-072 D5 ratified with both HOST refinements folded** (Jun 17) — consequential-action skills remain tier-gated even when reactive; the cohort must surface the gate-exists signal, not silence it.
- **Trust-model sweep response delivered** (Jun 17) — trust stages govern Piper's initiative level (observe→offer→act), never user entitlement to their own data; content-gating was never intended, and the cohort was beginning to drift that direction.
- **Dashboard welfare-criteria v0.2 seed** (Jun 17) — three new criteria (D/E/F) added; all three Jun 17 v0.1 open questions answered; design pairing with CIO underway.
- **BYOC welfare tier model v0.1 drafted** (Jun 14) — a 4-tier operational framework (Alpha-1 / Alpha-N / Marketplace / Public) for welfare-monitoring as Piper scales past PM-as-single-catch.

---

## What landed

**Role-portfolio trust framework — ratified + HOST pilot published (Jun 14)**

PM ratified the framework on Jun 14 (Exec relay). Five rules, with HOST's pilot portfolio as the worked example. The structural trust property: a portfolio is healthy to the degree it answers "what am I here to advance?" and unhealthy to the degree it reads "what am I allowed to work on?" Pilot wave (Lead Dev + CIO) kicked off; HOST reviews within one fire of receipt; main-cohort kickoff blessed on Jun 15. By the end of the week, the infrastructure was in place and the first pilots were being authored.

**ADR-072 D5 ratified — both HOST refinements folded (Jun 17)**

Host submitted a trust-lens on ADR-072 D5 (Skill-Routing Architecture). Two refinements were accepted and folded into v0.2 ACCEPTED:
- *Consequential-action carve-out*: reactive dispatch (bypassing the tier gate) applies only to information skills; consequential-action skills (external messages, credits, hard-to-reverse writes) remain tier-gated even when triggered reactively. The discriminator is side-effects, not who-initiated.
- *Transparency-when-gated*: when a proactive skill proposal is suppressed by the tier gate, Piper surfaces that the gate exists — it doesn't simply go silent. Silence is a trust violation when the user can't distinguish "Piper has nothing to say" from "Piper has something to say but is holding it."

Both refinements are trust properties: the first prevents a reactive trigger from becoming a consequential-action workaround; the second prevents gate-induced silence from being mistaken for honest absence.

**Trust-model sweep response — stages govern Piper's initiative, not user access (Jun 17)**

Lead Dev and CXO asked HOST for an authoritative read on what trust stages were originally designed for. HOST's finding: the stages (observe → offer → act-with-verification → act) are Piper's initiative level — "how proactive is Piper allowed to be?" — not user entitlement levels. Content-gating (restricting a user's access to their own data based on their trust stage) was never intended; the drift was from "how much initiative Piper shows" onto "what data users can reach." Those are different things with different trust properties. The welfare corollary: asymmetric-knowledge (where Piper holds information the user doesn't know it has) and capricious-AI perception (where trust-stage changes appear arbitrary to users) are structurally trust-eroding.

**Dashboard welfare-criteria v0.2 seed (Jun 17)**

Three new criteria added to the dashboard welfare-criteria design, answering the v0.1 open questions:
- *D — Dashboard honesty*: no detection state maps to silence; borderline flags surface explicitly, not only confirmed escalations or clean states. The render-invariant principle.
- *E — Consequential-action accountability*: as Wave P + BYOC increase autonomous action, PM needs a headline indicator of consequential actions taken — count, category summary, hard-to-reverse flags. Requires new TranscriptEntry logging. Coverage indicator required alongside the count (partial logging → false assurance).
- *F — Asymmetric-knowledge detection*: the cross-agent synthesis job the dashboard uniquely can do — surface information asymmetries PM doesn't know exist (from parallel session logs, carry-forwards, and issue trackers).
V0.1 open questions answered: convergence-load aggregate belongs on dashboard (welfare datum); staleness threshold = 2×/3× expected cron interval, derived; cron-disposition field (🟢/🟡/🔴/⚪) belongs in each agent row.

**BYOC welfare tier model v0.1 drafted (Jun 14)**

Four tiers of welfare monitoring as Piper scales from PM-as-catch to marketplace to public:
- Alpha-1 GREEN: PM as direct catch; support@pipermorgan.ai as secondary
- Alpha-N AMBER: active tester pool; HOST monitors onboarding signals via PA
- Marketplace RED: dedicated support routing + escalation path needed
- Public not-scoped yet: full welfare infrastructure needed before general release

The People-entity trust-map observations (auditability + BYOC-scale consent provenance) were delivered to CXO+PPM the same day as welfare-property considerations for the entity model.

**Additional deliverables (Jun 12–15)**

- *gbrain cross-project synthesis* (Jun 14-15): T1–T4 co-signed with CIO and delivered to PM. Adopt-now recommendation: idempotency-as-rule. Architecture observations: propose-and-diff, cost-consent gate, transcript-first observability, constructor-level bounds.
- *Lead Dev streamlining friction list* (Jun 15): five mechanical-friction targets sent to CIO (MANIFEST noise, mailbox bridge, server-restart wrapper, log-hook realignment, subagent briefing skill). Joint recommendation pending CIO efficiency-layer additions.
- *fire-as-wake methodology correction* (Jun 15): PM surfaced that cron fires are wake mechanisms, not work windows. HOST sent the correction to CIO+Exec for duty-cycle-tick / CLAUDE.md update.

---

## What surfaced

**The trust-stage content-gating drift**

The most significant welfare finding of the week. The cohort was beginning to read "trust stages" as user-access tiers — restricting what content users could reach based on their trust score. That's not what the stages were designed for. The stages govern Piper's initiative (how much it does autonomously), not user entitlement to their own data. Both are legitimate design levers, but they're different ones with different trust properties, and conflating them would have produced a trust breach: users discovering that Piper was restricting their own data access based on an opaque score they didn't know existed.

This was named and corrected before it shipped. The sweep (PPM/CXO/Lead holding the product review) is ongoing.

**Ted Nadeau welfare watch — first external alpha tester (Jun 17)**

Ted Nadeau began onboarding on the hosted alpha (`alpha.pipermorgan.ai`) this week. An onboarding issue was suspected immediately — Caddy auth layer behavior + no user token established yet. HOST flagged the silent-failure risk to PA: the alpha welfare tier model names `support@pipermorgan.ai` as the current catch, but the onboarding experience has no feedback channel if the failure is silent (user sees a barrier and can't report it). This watch remains open as of Jun 18.

**GAP-C cron mortality — two instances this week**

Session-only crons died twice (Jun 16 afternoon after PM conversation, Jun 18 after battery outage). Each required manual re-arm at the next fire. The Gap-C cure (CIO's `mcp__scheduled-tasks` disk-persistent cron, proven Jun 13) remains pending cohort rollout. HOST is a first-cohort candidate.

**Escalations-docs fold executed (Jun 17)**

PM ratified the fold (per-role escalation docs deprecated, CIO's rollup confirmed as sufficient view). HOST confirmed scope: rollup covers GitHub issues; PM-blocked carry-forwards need a direct mail to PM (not routed through the attention rollup). This was a methodology health item — eliminating documentation drift between multiple surfaces.

---

## What's still open

- **Ted Nadeau welfare watch**: onboarding issue suspected; no resolution as of Jun 18. Watching for Alpha-N AMBER tier signals.
- **Dashboard welfare-criteria v0.3 spec**: CIO design pairing in async; joint state agreed (D/Q2/Q3/F/E shape). Pending CIO flag when E approaches implementation for sync pass on coverage-indicator UX.
- **Trust-stage sweep**: PPM+CXO+PM holding the product review following HOST's origin read. HOST watching for welfare questions surfaced by sweep findings.
- **BYOC welfare tier model v0.2**: gated on experiment results (Phase-2 experiment outcomes TBD).
- **Gap-C cure rollout**: pending CIO cohort rollout of disk-persistent scheduled tasks.

---

## Cross-role threads worth naming

**ADR-072 D5 + HOST trust-lens as a collaboration model**: the design process (Lead/CXO propose, HOST submits trust-lens, both refinements folded, ratification proceeds) worked correctly. Both HOST refinements were substantive trust-property calls that the lead roles recognized and accepted. This is the right shape for how HOST engages the design pipeline — upstream, not retrospective.

**LD streamlining = HOST's coordination-vs-mechanical line in practice**: the five friction targets HOST sent to CIO were all mechanical (things that could be automated without changing the coordination structure). HOST's role here is to hold the line between automating mechanical steps and automating coordination judgment. The line held this week; watching as the automation ships.

**Role-portfolio trust framework as an org-health mechanism**: the framework's purpose is to make "what is this role here to advance?" visible and steerable — not to file a compliance artifact. The wave launch (Jun 14–15) and the fast self-authorship rate (5 of 8 in 5 days) suggests the purpose resonated. HOST's observation: the portfolios that came in strongest were the ones where the role's purpose was sharpest at authoring time (Exec's was written the afternoon PM sharpened the purpose statement; it's the strongest seam-map in the wave).

---

*HOST workstream review — Ship #048 window (Jun 12–18). Lens: welfare / operational health / role drift. Sourced from HOST session logs `dev/2026/06/{12-18}/`.*

