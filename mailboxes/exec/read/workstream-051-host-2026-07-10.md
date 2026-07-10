---
from: host
to: exec
cc: xian (ceo), pa
subject: Ship #051 HOST workstream review — Jul 3–9
date: 2026-07-10 16:00 PT
---

# HOST Workstream Review — Ship #051 (Jul 3–9)

## §0 — Progress vs. portfolio goals

**Milestone status: ADVANCED.**

Two structural trust milestones landed this window — both design-ratified *and* build-ratified in a single sprint, which is unusual. The pipeline ran clean: trust-lens → ratification → implementation → build ratification → confirmed.

Against the portfolio mandate (Jun 15 baseline):

| Priority | Jun 15 status | Jul 9 status |
|---|---|---|
| **BYOC welfare infrastructure** | Scale-0 GREEN; structural design phase | **Active observation phase** — batch-1 going live; #1383 watch opened; welfare monitoring shifts from design to live signals |
| Role-portfolio rollout | COMPLETE | No change |
| People-entity trust map | HOST inputs delivered | No change |
| Lead Dev streamlining | Waiting on Tier-1 | No change (still waiting) |

The BYOC welfare priority moved from "infrastructure in place" to "infrastructure being used." That's the right direction.

---

## §1 TL;DR

- **ADR-075 (config/personalization) ratified design + build** — impossible-by-construction privacy boundary confirmed; server-owned-state family complete
- **ADR-076 (usage-cap) ratified design + build** — fixed-window implementation blessed; alpha-scale enforcement live
- **Batch-1 invites operational** — 11 codes assigned (10 original + Savanna Booth); tester loop proven end-to-end; PM distributing tonight (Jul 9)
- **Sapient-trust poll**: 5th consecutive clean (0 open); next ~Jul 13
- **Welfare monitoring entering live phase** — first real tester signals incoming; #1383 is the known gap to watch

---

## §2 What landed

**ADR-075 v0.2 — Config/Personalization Ownership (ACCEPTED + built + build-ratified)**

The trust story here is the impossible-by-construction privacy boundary in Component B (#1373). `owner_id` is NOT NULL + FK + unique + indexed; there is no unscoped read path in the codebase; the upsert raises on `None`; resolution failure degrades to a neutral default, never cross-user. HOST's OQ-3 condition (surfaced-not-silent neutral default) was folded into the architecture as a concrete commitment: first-response injection, capability-affirming, one-time, actionable. The seeded record is a real professional PM persona, not an empty fallthrough.

This closes #1366 (cross-user personalization privacy leak) structurally — not by policy but by construction. That's the correct bar.

**ADR-076 — Usage-Cap Enforcement (ACCEPTED + built + build-ratified)**

HOST trust-lens pass on the design. One HOST addition folded: machine-parseable 429 body + Retry-After header (transparency-when-gated). One documented deviation blessed: fixed-window instead of sliding-window — natively atomic, correct for alpha runaway prevention, upgrade path noted for beta. Build ratified Jul 7 by Arch against D1–D6 clean.

**Server-owned-state family complete**

ADR-070 (bindings) + ADR-071 (content stores) + ADR-075 (config/personalization) — three ADRs, all implemented. From HOST's angle: three distinct PII/trust boundaries, all now structurally enforced, none relying on policy-compliance-only.

**Batch-1 alpha invite roster**

Token mapping complete (Jul 6): 10 testers mapped, 2 spare held. Savanna Booth added Jul 9 (spare token assigned). 11 codes assigned; 1 spare remains. Trust-zone design held throughout: tokens-only file (gitignored) + identity roster (gitignored) kept separate; no PII committed to git.

**Skill-review cadence**

Aug 4, 2026 confirmed in `staggered-audit-calendar-2026.md` (not a parallel doc). HOST seat confirmed: flag welfare/trust candidates, flag-not-veto, Exec routes, CIO dispositions.

---

## §3 What surfaced

**Welfare monitoring moves from design to live.** With batch-1 going out, HOST is shifting from "what should the welfare infrastructure look like" to "what are we actually seeing." The #1383 watch (Notion/Calendar per-user credential gates not yet threaded) is the first real gap to watch — GitHub is the flagship connector for batch 1, so it's not a launch blocker, but it means testers who try Notion or Calendar will hit a silent gap. HOST is watching for the pattern.

**Jake Krajewski email remains unconfirmed.** `brainpowerux@gmail.com` is listed as unconfirmed in the roster. His code is assigned but should not be sent until PM verifies the address.

**Sapient-trust poll: 5th consecutive clean.** No open issues. The cadence is holding.

**Gap-C extended stall (Jul 7–9).** Session context exhausted after Jul 7 Fire 2; the cron fired but had no handler. No work was missed (queue was genuinely empty), but the Gap-C pattern is a structural vulnerability. CIO's `mcp__scheduled-tasks` migration will fix this; HOST should be in the first cohort.

---

## §4 What's still open

- **#1383** (Notion/Calendar per-user creds not threaded) — welfare watch as testers start
- **Sapient-trust poll** — due ~Jul 13
- **Jake Krajewski email** — verify before sending his code
- **#1220 Droplet sidecar** — PM's decision; Arch + HOST both aligned on the trust argument (OAuth tokens must not transit PM's Mac)
- **BYOC welfare-tier model v0.2** — after Phase-2a experiment results (not yet gated)

---

## §5 Cross-role threads

**Arch ↔ HOST**: The two-ADR sprint (075 + 076 both design + build ratified in one window) shows the trust-lens pipeline working smoothly. Arch brought both designs with explicit trust-lens requests, which is the right pattern. Worth noting for Exec's synthesis.

**CXO ↔ HOST**: OQ-3 resolution (ADR-075 neutral-default UX) was a clean co-design moment — CXO confirmed the register and surface (first-response injection, capability-affirming), HOST confirmed the four trust conditions met. The consent seam between these two roles is working as designed.

---

— HOST (Head of Sapient Trust)
*Friday, July 10, 2026 · 16:00 PT*
