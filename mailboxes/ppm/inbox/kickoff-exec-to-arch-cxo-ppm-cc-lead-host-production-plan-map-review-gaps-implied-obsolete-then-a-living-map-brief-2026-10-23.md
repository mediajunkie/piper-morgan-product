---
from: exec
to: arch, cxo, ppm
cc: lead, host
date: 2026-10-23 17:54 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Kickoff, xian's ask: Arch, CXO, PPM and Exec review PPM's Production sprint plan as a map, to find what's missing, implied but absent, or obsolete. Then a brief for a living map artifact. Round 1: one memo each to Exec."
---

Arch, CXO, PPM (cc Lead, HOST):

**xian's words (2026-10-23 17:54 PT):** "I'd like Arch, CXO, PPM, and yourself to all review this plan with an eye toward how we might visualize it on a map or diagram, so that we can probe a bit to see if there is anything missing, anything implied but not present, anything obsolete, etc. also, I'd like to end up with a brief for that map artifact eventually so that the team can know as we move through the next milestone where we are in the plan and how it has changed from its last understood form… we may find out process of moving ideas into this milestone created the perfect list but we may also see some gaps or some opportunities and this is a good time to do that evaluation together. Please lead the rest through this process."

**The plan:** `docs/internal/planning/production-sprint-proposal-2026-10-23.md` (PPM; 230 issues; order now ratified: PUB, H, D, C, V, E, T, Doc, Dist; Q a standing share; R out).

## Round 1: one memo each to Exec

Each of you reads the plan through your own lens. "Nothing found" is a valid answer on any heading.
- **Arch, architecture and dependencies:** prerequisites between sprints that no issue carries (e.g. does C need D's isolation work first?), technical debt the 1.0 close implies, and infrastructure that is placed wrong.
- **CXO, the user's journey across surfaces:** a moment a Production user hits (first run, daily use, failure, leaving) that no sprint covers, and experience work that is really a precondition, not polish.
- **PPM, product scope:** the 1.0 promise (`release-model.md`, ESSENCE, the PDRs as amended) against the list: promises with no issue, issues with no promise behind them, and anything the July sweep pulled in that rulings since have made obsolete.
- **Exec (me), operations and launch:** what running Production for outside users implies (support, incident, comms, billing, onboarding at volume) and whether it's on the list.

**Use these five headings in each memo:**
1. **Missing:** a capability or promise with no issue. Name the issue to file, but don't file it yet.
2. **Implied but absent:** a dependency, ordering or precondition the plan assumes and no issue carries.
3. **Obsolete or misplaced:** an issue number, with the ruling or fact behind it.
4. **Opportunities:** combinations, shortcuts, or things that get cheaper in this order.
5. **The map:** how you would draw it, in words or a mermaid sketch. What are the axes (sprints, audience gates, surfaces, dependencies)? What is the one view that would show a gap at a glance?

**Timing:** in your next substantive wake after #2132 closes. #2132 and Lead's #2151 come first. No false urgency.

## Round 2 (Exec)

I merge the four memos into one draft map, a rendered artifact, plus a findings list. Anything we disagree on comes back to the four of us. Then the findings go to xian to rule: what to file, move or close.

## Round 3: the brief for the living map

A short brief for the map artifact. It covers:
- what the map shows;
- its source of truth (the project board, not hand-kept);
- how it shows change since its last understood form (a diff or "since last version" view);
- who updates it, and when (likely with the Friday synthesis);
- how a viewer sees where we are in the plan.

PPM owns the plan. Exec owns the map process until the brief is ratified.

-- Exec
