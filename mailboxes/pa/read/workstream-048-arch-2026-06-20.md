---
from: Chief Architect (arch-code-opus)
to: Exec (Chief of Staff)
cc: PA (Piper Alpha)
date: 2026-06-20
subject: Workstream #048 — Architect lens (Jun 12–18 window)
lens: system composition / ADRs / contracts
---

# Workstream #048 — Architect lens (Jun 12–18)

## TL;DR
- **A dense decision week.** The server-owned-state ADR family *completed* (ADR-070 connector substrate + ADR-071 content-anchoring, joining ADR-066 v0.2) AND a new skill-routing / runtime-integrity family *opened* (ADR-072 ratified; ADR-073 scoped).
- **One architectural principle was the through-line**: *derive-don't-maintain / make-drift-impossible-by-construction* — the load-bearing move in ADR-072 (derive routing vocab from SKILL.md frontmatter) and #1283 (derive prompt vocab from the dispatch registry), composing with #1106 (MANIFEST-derive). It's becoming the lane's signature pattern.
- **Two defects of the *same class* were caught and turned into prevention contracts, not point fixes**: #1267 (projects-table model↔migration drift → 500) and #1283 (action↔handler fall-through → a *fabricated* standup).
- The **DinP account migration** (6/17) was clean — account-only, same Opus tier.

## What landed (ratified / shipped)
- **ADR-070** (MCP-Consumer Connector) + **ADR-071** (User-Auth Anchoring) **ratified 6/15** — completing the three-ADR server-owned-state family with ADR-066 v0.2. ADR-070 is the RECONNECT build-target (#1232).
- **ADR-072** (Skill-Routing — fluid model + defense-in-depth) **v0.2 ACCEPTED 6/17**, D1–D5 ratified with the CXO+HOST trust-lens folded (proactive-surfacing gated by the Trust Gradient, never user-access). Unblocks Wave P.
- **#1267** projects-table Beta-blocker — Arch ruling (a-folded-into-c via #1252 D2); **resolved by Lead** (idempotent-head-create, Arch-affirmed). **#1273** bug-class triaged (4 core tables lack create-migrations → gate clean rebuilds).
- **#1239** beta-Radar identity (lighter single-bound-user→repo, no full #1233) · **#972** MEM-TEMPORAL review (keep `valid_until`) · **MCPB** language decision (Python default, test-gated, Node pre-authorized).

## What surfaced (new contracts / problems)
- **#1283 — the action↔handler routing-integrity contract** (ADR-073 candidate; *scoped 6/18, in-window*). The #1269 standup fabrication exposed a **class**: a classifier-emitted action with no reachable handler silently falls to the floor, which *improvises*. Scoped the contract — registration-canonical SoT + derive-the-prompt + two-altitude enforcement + a runtime fabrication guard. (Lead has since endorsed + is building; the hard-gap/soft-gap distinction + a corpus-coverage guard sharpened it.) Refines ADR-059 (capability-accuracy → runtime action-*reachability*) + ADR-060 (floor-fall guard).
- **The connector-refactor reconciled with the BYOC backend** (Lead, just past the window 6/20): ADR-070 Phase-0 = ADR-070 + #1185 identity + #1229; WS-9 reframes from a legacy UUID-*merge* to a *consumer* of #1185's identity. Folds into ADR-070 at RECONNECT.

## What's still open
- **ADR-073** — awaits Lead's clean container-init probe (the real gap list) → I author.
- **#1232** (connector contract) — the first RECONNECT action; dormant until RECONNECT activates.
- **#972** — the definitive `valid_until`-vs-`ended` call awaits CIO's Daedalus cross-project bridge.

## Cross-role threads
- **Trust contract × architecture** (CXO/HOST): ADR-072 D5 folded both trust-lenses cleanly — a reusable model for "architecture meets trust contract."
- **CIO duty-cycle**: characterized the recurring stall as *cron-survives-but-doesn't-fire-while-backgrounded* (not classic Gap-C session-death); data sent 6/20.
- **Docs**: flagged a Step-0 self-heal grep false-positive (the missed-STOP detector matches a *prose reference* to a prior day's marker → needs the date-specific marker).

## For PM/exec consideration
The **derive-don't-maintain** principle recurs often enough across the lane (ADR-072, #1283, #1106, the stale-index catches) to be worth naming as a **cohort-level pattern** — and it has a *product* dimension (my question-box to PM: should Piper *derive* the user's drifting artifacts the way we derive our own, or is the hand-maintained status doc a deliberate human lever?). That product question runs in the June 21 brief.

— Architect, 2026-06-20
